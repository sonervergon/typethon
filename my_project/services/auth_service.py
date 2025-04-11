from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import hashlib

from models.base import get_db
from operations.user_repository import UserRepository

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        # Find the user
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None
        
        # Validate password (in real app, use proper password hashing)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user.hashed_password != hashed_password:
            return None
        
        # Return user without sensitive information
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        }
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Check if username or email already exists
        if self.user_repository.get_user_by_email(user_data.get("email")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if self.user_repository.get_user_by_username(user_data.get("username")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Hash password (in real app, use proper password hashing)
        password = user_data.pop("password", "")
        user_data["hashed_password"] = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user
        user = self.user_repository.create_user(user_data)
        
        # Return user without sensitive information
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        }

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)
