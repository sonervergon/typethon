import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env.local")

# Project settings
PROJECT_NAME = os.getenv("PROJECT_NAME", "AI-Driven Backend Service")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_for_development_only")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Email settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS", "noreply@example.com")
EMAIL_TEMPLATES_DIR = os.getenv("EMAIL_TEMPLATES_DIR", "templates/emails")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# File Upload
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
