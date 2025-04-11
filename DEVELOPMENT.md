# Development Guide

This document contains detailed technical information for developers working on this project. For general information, project overview, and getting started instructions, please refer to the [README.md](./README.md).

## Table of Contents

1. [Authentication](#authentication)
2. [Database Migrations](#database-migrations)
3. [Advanced Testing](#advanced-testing)
4. [Code Style and Conventions](#code-style-and-conventions)
5. [Security Best Practices](#security-best-practices)
6. [Performance Optimization](#performance-optimization)
7. [Cloud Deployment](#cloud-deployment)
8. [Advanced Development Topics](#advanced-development-topics)

## Authentication

The current implementation uses a simplified authentication system:

- Passwords are hashed using SHA-256 (insecure, for demonstration only)
- The login endpoint returns a dummy token

For production, implement JWT authentication:

1. Add JWT dependencies:

   ```bash
   pip install python-jose[cryptography] passlib[bcrypt]
   ```

2. Update the auth service to use secure password hashing:

   ```python
   from passlib.context import CryptContext
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

   def verify_password(plain_password, hashed_password):
       return pwd_context.verify(plain_password, hashed_password)

   def get_password_hash(password):
       return pwd_context.hash(password)
   ```

3. Generate and validate JWT tokens:

   ```python
   from jose import jwt
   from datetime import datetime, timedelta

   def create_access_token(data, expires_delta):
       to_encode = data.copy()
       expire = datetime.utcnow() + expires_delta
       to_encode.update({"exp": expire})
       return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   ```

4. Add token validation dependency:

   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import OAuth2PasswordBearer

   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

   def get_current_user(token: str = Depends(oauth2_scheme)):
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           username = payload.get("sub")
           if username is None:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
       except JWTError:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

       return username
   ```

## Database Migrations

For production use, implement database migrations using Alembic:

1. Install Alembic:

   ```bash
   pip install alembic
   ```

2. Initialize Alembic:

   ```bash
   alembic init alembic
   ```

3. Configure Alembic to use your SQLAlchemy models:

   Edit `alembic/env.py` to point to your models:

   ```python
   # Import your models
   from models.user_model import User
   from lib.database import Base

   # Set metadata object
   target_metadata = Base.metadata
   ```

4. Create migrations for schema changes:

   ```bash
   alembic revision --autogenerate -m "description"
   ```

5. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## Advanced Testing

### Mocking External Dependencies

Use pytest's monkeypatch fixture to mock external services:

```python
def test_email_service(monkeypatch):
    # Mock the SMTP connection
    class MockSMTP:
        def __init__(self, server, port):
            pass

        def starttls(self):
            pass

        def login(self, username, password):
            pass

        def send_message(self, msg):
            pass

        def quit(self):
            pass

    # Apply the mock
    monkeypatch.setattr("smtplib.SMTP", MockSMTP)

    # Test the service
    email_service = get_email_service()
    result = email_service.send_email(["test@example.com"], "Test", "Content")
    assert result is True
```

### Testing with Fixtures

Create reusable fixtures for database entities:

```python
@pytest.fixture
def test_user(test_db):
    """Create a test user in the database"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "hashed_password": "hashed_password"
    }
    user = User(**user_data)
    db = next(get_db_session())
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
```

## Code Style and Conventions

### Type Hints

Always use type hints for function parameters and return values:

```python
def get_user_by_id(user_id: int) -> Optional[User]:
    ...
```

### Error Handling

Follow these error handling patterns:

1. Use specific exceptions:

```python
if not user:
    raise UserNotFoundError(f"User with ID {user_id} not found")
```

2. Convert exceptions at layer boundaries:

```python
try:
    return self.repository.get_user(user_id)
except SQLAlchemyError as e:
    logger.error(f"Database error: {str(e)}")
    raise HTTPException(status_code=500, detail="Database error occurred")
```

### Logging

Use the Python logging module consistently:

```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    try:
        # Operation
        logger.info("Operation completed successfully")
    except Exception as e:
        logger.error(f"Error during operation: {str(e)}")
        raise
```

## Security Best Practices

### Input Validation

Beyond Pydantic's validation, implement additional validation:

```python
def validate_username(username: str) -> bool:
    """Check if username meets security requirements"""
    if len(username) < 3:
        return False
    if not username.isalnum():
        return False
    return True
```

### Rate Limiting

Implement rate limiting for public endpoints:

```python
from fastapi import Depends, HTTPException, Request
from datetime import datetime, timedelta

# Simple in-memory rate limiting
request_history = {}

def rate_limit(request: Request, max_requests: int = 5, window_seconds: int = 60):
    client_ip = request.client.host
    now = datetime.now()

    # Clean up old records
    if client_ip in request_history:
        request_history[client_ip] = [
            timestamp for timestamp in request_history[client_ip]
            if now - timestamp < timedelta(seconds=window_seconds)
        ]
    else:
        request_history[client_ip] = []

    # Check limit
    if len(request_history[client_ip]) >= max_requests:
        raise HTTPException(status_code=429, detail="Too many requests")

    # Record request
    request_history[client_ip].append(now)
    return True
```

### Security Headers

Add security headers to your FastAPI application:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trusted-site.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.yoursite.com"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

## Performance Optimization

### Database Query Optimization

Use SQLAlchemy efficiently:

1. Select only needed columns:

```python
db.query(User.id, User.username).filter(User.active == True).all()
```

2. Use joins efficiently:

```python
db.query(User).options(
    joinedload(User.posts)
).filter(User.id == user_id).first()
```

3. Indexing key columns:

```python
username = Column(String, unique=True, index=True)
email = Column(String, unique=True, index=True)
```

### Caching Strategies

Use Redis for caching with appropriate invalidation strategies:

```python
def get_user_with_cache(user_id: int, redis_client):
    # Try cache first
    cache_key = f"user:{user_id}"
    cached_user = redis_client.get(cache_key)

    if cached_user:
        return json.loads(cached_user)

    # Get from database if not in cache
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # Cache for 5 minutes
        user_data = user.to_dict()
        redis_client.set(cache_key, json.dumps(user_data), expiry=300)
        return user_data

    return None
```

### Async IO

Use FastAPI's async support for I/O-bound operations:

```python
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    # Use async database clients or make external API calls
    return await async_get_user(user_id)
```

## Cloud Deployment

### AWS Deployment

To deploy on AWS ECS:

1. Create an ECR repository:

   ```bash
   aws ecr create-repository --repository-name ai-backend-service
   ```

2. Build and push the Docker image:

   ```bash
   aws ecr get-login-password | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
   docker build -t ai-backend-service .
   docker tag ai-backend-service:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-backend-service:latest
   docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-backend-service:latest
   ```

3. Create an ECS task definition, cluster, and service using the AWS console or CLI

### Google Cloud Run

1. Build the Docker image
2. Tag it for Google Container Registry:

   ```bash
   docker tag ai-backend-service gcr.io/[PROJECT_ID]/ai-backend-service
   ```

3. Push to Container Registry:

   ```bash
   docker push gcr.io/[PROJECT_ID]/ai-backend-service
   ```

4. Deploy to Cloud Run:
   ```bash
   gcloud run deploy ai-backend-service \
     --image gcr.io/[PROJECT_ID]/ai-backend-service \
     --platform managed \
     --allow-unauthenticated
   ```

## Advanced Development Topics

### Background Tasks

Use FastAPI's background tasks for simple operations:

```python
from fastapi import BackgroundTasks

@app.post("/users/")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks
):
    user_id = create_user_in_db(user)

    # Add a background task
    background_tasks.add_task(send_welcome_email, user.email)

    return {"id": user_id}
```

For more complex tasks, integrate with Celery:

```python
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_data(data):
    # Long-running task
    result = expensive_computation(data)
    return result

@app.post("/process/")
async def process_endpoint(data: Dict):
    # Submit task to Celery
    task = process_data.delay(data)
    return {"task_id": task.id}

@app.get("/results/{task_id}")
async def get_results(task_id: str):
    # Check task status
    task = process_data.AsyncResult(task_id)
    if task.ready():
        return {"status": "completed", "result": task.result}
    return {"status": "processing"}
```

### Dependency Injection Patterns

Use FastAPI's dependency system effectively:

1. Scoped dependencies:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = validate_token_and_get_user(db, token)
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

2. Class-based dependencies:

```python
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}
```
