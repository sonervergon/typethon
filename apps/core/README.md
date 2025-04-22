# Core API Service

A Python backend service using a layered architecture with FastAPI.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Infrastructure Libraries](#infrastructure-libraries)
- [Development Guide](#development-guide)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)

## Overview

This service provides the core API functionality for the monorepo. It follows a clean, layered architecture to promote maintainability and separation of concerns. With this architecture baked in, you can focus on implementing your business logic rather than setting up infrastructure.

## Architecture

This service follows a layered architecture to separate concerns and promote maintainability:

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
|      (ORM models, database schema definitions)          |
+---------------------------------------------------------+
                            ↑
                            |
+---------------------------------------------------------+
|                Infrastructure/Lib Layer                 |
| (Database connections, caching, messaging, file storage)|
+---------------------------------------------------------+
```

Each layer has a specific responsibility:

- **API Layer**: Handles HTTP requests/responses using FastAPI
- **Service Layer**: Contains business logic and orchestrates operations
- **Operations Layer**: Manages data access using the repository pattern
- **Models/Database Layer**: Defines the data model and database schema
- **Infrastructure/Lib Layer**: Provides shared utilities and external service integrations

## Getting Started

### Prerequisites

- Python 3.13+ with uv (https://docs.astral.sh/uv/)
- pnpm (for monorepo management)

### Installation

From the monorepo root:

```bash
pnpm setup-env
```

### Running the Service

From the monorepo root:

```bash
pnpm --filter @typethon/core dev
```

Or from this directory:

```bash
pnpm dev
```

The API will be available at http://localhost:8000

## Infrastructure Libraries

The project includes a `lib` folder that contains common infrastructure components:

### Available Libraries

- **Cache**: Redis client for caching data

  ```python
  from lib import get_redis_client

  # In your service/endpoint
  def my_function(redis = Depends(get_redis_client)):
      redis.set("key", "value", expiry=3600)  # Set with TTL
      return redis.get("key")  # Get value
  ```

- **Database**: Connection management and session utilities

  ```python
  from lib import get_db_session

  # In your repository
  def my_repository_function(db = Depends(get_db_session)):
      result = db.query(MyModel).filter(MyModel.id == 1).first()
      return result
  ```

- **Messaging**: Email service with template support

  ```python
  from lib import get_email_service

  # In your service
  def notify_user(email_service = Depends(get_email_service)):
      email_service.send_email(
          to_email=["user@example.com"],
          subject="Welcome",
          body="Welcome to our service!",
          is_html=False
      )
  ```

- **Storage**: File storage for handling uploads

  ```python
  from lib import get_file_storage
  from fastapi import UploadFile

  # In your endpoint
  def upload_file(file: UploadFile, storage = Depends(get_file_storage)):
      file_path = storage.save_file(file, subdir="profiles")
      return {"file_path": file_path}
  ```

## Development Guide

### Project Structure

```
core/
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
│   └── user_model.py     # User ORM model
├── lib/                  # Infrastructure Libraries
│   ├── cache/            # Caching utilities (Redis)
│   ├── database/         # Database connections and sessions
│   ├── messaging/        # Email and messaging services
│   └── storage/          # File storage utilities
├── tests/                # Test suite
│   └── test_api.py       # API tests
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
├── setup.py              # Package installation
├── Dockerfile            # Container definition
└── .env                  # Environment variables
```

### Adding New Features

When adding a new feature, follow these steps:

1. **Define the data model**: Add/update models in `models/`
2. **Implement data access**: Create/update repositories in `operations/`
3. **Implement business logic**: Add service methods in `services/`
4. **Create API endpoints**: Define schemas and routes in `api/`
5. **Write tests**: Add tests for new functionality

### Database Management

Database connections are managed in `lib/database/connection.py`. Tables are automatically created at startup with:

```python
Base.metadata.create_all(bind=engine)
```

## Testing

Run the test suite with pytest:

```bash
# From monorepo root
pnpm --filter @typethon/core test
```

Tests use an in-memory SQLite database and are isolated from production data.

## API Endpoints

- `GET /api/v1/users/{user_id}` - Get user by ID
- `POST /api/v1/users/` - Create a new user
- `POST /api/v1/login/` - Login and get access token

Explore the full API at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
