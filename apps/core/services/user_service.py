from typing import Dict, Any
from fastapi import Depends, HTTPException, status

from operations.user_repository import UserRepository, get_user_repository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        user = self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Business logic: exclude sensitive information
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        }
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
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

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
