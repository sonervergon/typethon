"""
Common libraries and utilities for the application.
"""

# Import and expose key components for easier access
from lib.cache import RedisClient, get_redis_client
from lib.database import Base, create_session, engine, get_db_session
from lib.messaging import EmailService, get_email_service
from lib.storage import FileStorage, get_file_storage

__all__ = [
    # Cache
    "RedisClient",
    "get_redis_client",
    # Database
    "engine",
    "Base",
    "get_db_session",
    "create_session",
    # Messaging
    "EmailService",
    "get_email_service",
    # Storage
    "FileStorage",
    "get_file_storage",
]
