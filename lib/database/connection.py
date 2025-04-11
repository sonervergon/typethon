from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from core.config import DATABASE_URL

# Create SQLAlchemy engine
# Add connect_args for SQLite compatibility
connect_args = {}
if DATABASE_URL.startswith('sqlite'):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency function to get DB session
    Usage: db: Session = Depends(get_db_session)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_session() -> Session:
    """Create and return a new session"""
    return SessionLocal() 