# Development Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Layer Details](#layer-details)
4. [Development Workflow](#development-workflow)
5. [Database Management](#database-management)
6. [Testing](#testing)
7. [Authentication](#authentication)
8. [API Documentation](#api-documentation)
9. [Deployment](#deployment)
10. [Best Practices](#best-practices)

## Architecture Overview

This project follows a layered architecture to separate concerns and promote maintainability:

```
+---------------------------------------------------------+
|                      API Layer                          |
|      (FastAPI endpoints, request/response schemas)      |
+---------------------------+-----------------------------+
                            |
                            v
+---------------------------------------------------------+
|                    Service Layer                        |
|   (Business logic, validations, access control, etc.)   |
+---------------------------+-----------------------------+
                            |
                            v
+---------------------------------------------------------+
|                   Operations Layer                     |
|      (Repository pattern, database query logic)         |
+---------------------------+-----------------------------+
                            |
                            v
+---------------------------------------------------------+
|                 Models/Database Layer                   |
|      (ORM models, database engine, and schema definitions)|
+---------------------------------------------------------+
```

Each layer has a specific responsibility:

- **API Layer**: Handles HTTP requests/responses using FastAPI
- **Service Layer**: Contains business logic and orchestrates operations
- **Operations Layer**: Manages data access using the repository pattern
- **Models/Database Layer**: Defines the data model and database connectivity

## Project Structure

```
my_project/
├── api/                  # API Layer
│   ├── endpoints.py      # FastAPI route definitions
│   └── schemas.py        # Pydantic request/response models
├── services/             # Service Layer
│   ├── user_service.py   # User-related business logic
│   └── auth_service.py   # Authentication/authorization logic
├── operations/           # Operations Layer
│   ├── user_repository.py # Data access for users
│   └── transaction_repo.py # Transaction management
├── models/               # Models/Database Layer
│   ├── base.py           # Database connection setup
│   └── user_model.py     # User ORM model
├── core/                 # Core functionality
│   └── config.py         # Configuration settings
├── tests/                # Test suite
│   └── test_api.py       # API tests
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
├── setup.py              # Package installation
├── Dockerfile            # Container definition
├── .env                  # Environment variables
└── README.md             # Project overview
```

## Layer Details

### API Layer

The API layer is implemented using FastAPI and defines:

- **Endpoints**: HTTP routes that receive and respond to client requests
- **Request Schemas**: Pydantic models for validating incoming data
- **Response Schemas**: Pydantic models for structuring response data

Example endpoint:

```python
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_user_profile(user_id)
```

This layer should handle only:

- Request routing
- Data validation
- Response formatting
- Dependency injection

### Service Layer

The service layer contains business logic and orchestrates operations:

- **Business Rules**: Application-specific logic
- **Validations**: Complex validations beyond basic type checking
- **Orchestration**: Coordinating multiple operations
- **Error Handling**: Business-level exceptions

Example service method:

```python
def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
    # Business logic: Check if user already exists
    if self.user_repository.get_user_by_email(user_data.get("email")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user = self.user_repository.create_user(user_data)

    # Transform data for response
    return {
        "id": user.id,
        "username": user.username,
        ...
    }
```

### Operations Layer

The operations layer manages data access using repositories:

- **Repositories**: Data access objects for each entity
- **Transactions**: Database transaction management
- **Queries**: Complex query construction

Example repository method:

```python
def get_user_by_email(self, email: str) -> Optional[User]:
    return self.db.query(User).filter(User.email == email).first()
```

### Models/Database Layer

The models layer defines the data structure:

- **ORM Models**: SQLAlchemy models representing database tables
- **Database Connection**: Engine and session management
- **Migrations**: Database schema changes (not implemented yet)

Example model:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    ...
```

## Development Workflow

### Setting Up Development Environment

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies in development mode:
   ```bash
   pip install -e .
   ```
4. Create a `.env` file with appropriate settings (or use the existing one)
5. Run the application:
   ```bash
   python main.py
   ```

### Adding New Features

When adding a new feature, follow these steps:

1. **Define the data model**:

   - Add or update model classes in `models/`
   - Update the database schema

2. **Implement data access**:

   - Create or update repository methods in `operations/`
   - Ensure proper transaction handling

3. **Implement business logic**:

   - Add service methods in `services/`
   - Handle validations and business rules

4. **Create API endpoints**:

   - Define request/response schemas in `api/schemas.py`
   - Add routes in `api/endpoints.py`

5. **Write tests**:
   - Add unit tests for service layer
   - Add integration tests for API endpoints

### Code Style and Conventions

- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Document complex functions with docstrings
- Keep functions small and focused on a single responsibility

## Database Management

The project uses SQLAlchemy as an ORM and currently supports SQLite.

### Connection Management

Database connections are managed in `models/base.py`:

```python
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

The `get_db` function is used as a dependency in FastAPI to provide database sessions.

### Creating Tables

Tables are automatically created at startup:

```python
Base.metadata.create_all(bind=engine)
```

### Migrations

For production use, implement database migrations using Alembic:

1. Install Alembic:

   ```bash
   pip install alembic
   ```

2. Initialize Alembic:

   ```bash
   alembic init alembic
   ```

3. Configure Alembic to use your SQLAlchemy models
4. Create migrations for schema changes:

   ```bash
   alembic revision --autogenerate -m "description"
   ```

5. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## Testing

### Test Setup

Tests use pytest and an in-memory SQLite database:

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

The `test_db` fixture creates and drops tables for each test:

```python
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

### Running Tests

Run tests with pytest:

```bash
pytest
```

### Types of Tests

- **Unit Tests**: Test individual functions/methods in isolation
- **Integration Tests**: Test API endpoints with FastAPI's TestClient
- **Repository Tests**: Test data access operations

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

   def create_access_token(data, expires_delta):
       to_encode = data.copy()
       expire = datetime.utcnow() + expires_delta
       to_encode.update({"exp": expire})
       return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   ```

## API Documentation

FastAPI automatically generates API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

To improve documentation:

- Add descriptions to Pydantic models
- Add docstrings to endpoint functions
- Use response_model to specify responses

Example:

```python
@router.post("/users/",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new user",
             description="Creates a new user with the provided information")
def create_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Create a new user with the following information:

    - **username**: unique username
    - **email**: unique email address
    - **full_name**: optional full name
    - **password**: user's password
    """
    return auth_service.register_user(user_data.model_dump())
```

## Deployment

### Docker Deployment

The project includes a Dockerfile for containerization:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Build and run:

```bash
docker build -t ai-backend-service .
docker run -p 8080:8080 ai-backend-service
```

### Cloud Deployment

For Google Cloud Run deployment:

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

## Best Practices

### Security

- Use HTTPS in production
- Implement proper authentication with JWT tokens
- Use secure password hashing (bcrypt)
- Add rate limiting for login attempts
- Validate and sanitize all user inputs
- Set appropriate CORS policies
- Avoid SQL injection through ORM use
- Keep secrets in environment variables, not in code

### Performance

- Use async endpoints for I/O-bound operations:

  ```python
  @router.get("/users/{user_id}")
  async def get_user_by_id(user_id: int):
      ...
  ```

- Use appropriate database indexes
- Implement caching for frequently accessed data
- Optimize database queries to fetch only needed data
- Use pagination for list endpoints

### Future Enhancements

- Add health check endpoints
- Implement request logging middleware
- Add OpenTelemetry for distributed tracing
- Add a CORS configuration file
- Implement background tasks using Celery or FastAPI background tasks
- Add a GraphQL endpoint using Strawberry
- Implement rate limiting middleware
- Add fine-grained authorization with role-based access control
