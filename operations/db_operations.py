from sqlalchemy.orm import Session
from fastapi import Depends
from models.base import get_db, SessionLocal

# This will be used as a dependency
def get_db_session():
    """
    Get database session function that can be used by operations layer.
    This abstracts the database session creation from the models layer.
    """
    return next(get_db())

def create_session():
    """Alternative method to create a new database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 