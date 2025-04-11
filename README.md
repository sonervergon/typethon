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

### Python Version Management (Optional)

If you need to install or manage multiple Python versions, we recommend using pyenv:

```bash
# Install pyenv (macOS)
brew install pyenv

# Install Python 3.9
pyenv install 3.9.18

# Set as your active Python version
pyenv global 3.9.18

# Verify the installation
python --version
```

For more detailed instructions, see the DEVELOPMENT.md file.

### Development Setup

For development, you can install the package in development mode:

```bash
pip install -e .
```

### Testing

Run the test suite with pytest:

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run a specific test file
python -m pytest tests/test_api.py

# Run a specific test function
python -m pytest tests/test_api.py::test_create_user
```

The project uses pytest with an in-memory SQLite database for testing. Tests are isolated and don't affect any production data.

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
