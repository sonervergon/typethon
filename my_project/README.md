# AI-Driven Backend Service

A Python backend service using a layered architecture with FastAPI.

## Architecture

This project follows a layered architecture:

- **API Layer:** FastAPI endpoints and Pydantic schemas
- **Service Layer:** Business logic and orchestration
- **Operations Layer:** Data access through repositories
- **Models/Database Layer:** SQLAlchemy ORM models and database connectivity

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

The API will be available at http://localhost:8000

### Development Setup

For development, you can install the package in development mode:

```bash
pip install -e .
```

### Testing

Run tests with pytest:

```bash
pytest
```

## Docker

Build and run the Docker container:

```bash
docker build -t ai-backend-service .
docker run -p 8080:8080 ai-backend-service
```

The API will be available at http://localhost:8080

## API Endpoints

- `GET /api/v1/users/{user_id}` - Get user by ID
- `POST /api/v1/users/` - Create a new user
- `POST /api/v1/login/` - Login and get access token
