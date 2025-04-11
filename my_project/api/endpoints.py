from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from api.schemas import UserCreate, UserResponse, UserUpdate, LoginRequest, Token
from services.user_service import UserService, get_user_service
from services.auth_service import AuthService, get_auth_service

router = APIRouter()

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Create a new user"""
    return auth_service.register_user(user_data.model_dump())

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID"""
    return user_service.get_user_profile(user_id)

@router.post("/login/", response_model=Token)
def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login and get access token"""
    user = auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In a real app, generate JWT token here
    access_token = f"dummy_token_for_{user['username']}"
    
    return {"access_token": access_token, "token_type": "bearer"}
