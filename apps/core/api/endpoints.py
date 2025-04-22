from typing import List
from uuid import UUID

from api.schemas import (
    ChatCreate,
    ChatDetailResponse,
    ChatRequest,
    ChatResponse,
    ChatUpdate,
    HelloResponse,
    LoginRequest,
    MessageCreate,
    MessageResponse,
    StreamingMessageCreate,
    Token,
    UserCreate,
    UserResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from services.ai_service import AIService, get_ai_service
from services.auth_service import AuthService, get_auth_service
from services.chat_service import ChatService, get_chat_service
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Create a new user"""
    return auth_service.register_user(user_data.model_dump())


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Get user by ID"""
    return user_service.get_user_profile(user_id)


@router.post("/login/", response_model=Token)
def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
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


@router.get("/hello", response_model=HelloResponse)
def hello() -> HelloResponse:
    return HelloResponse(message="Hello, World!")


# Chat endpoints
@router.get("/chats/", response_model=List[ChatResponse])
def get_chats(
    skip: int = 0,
    limit: int = 20,
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get all chats"""
    return chat_service.get_chats(skip=skip, limit=limit)


@router.post(
    "/chats/", response_model=ChatDetailResponse, status_code=status.HTTP_201_CREATED
)
def create_chat(
    chat_data: ChatCreate, chat_service: ChatService = Depends(get_chat_service)
):
    """Create a new chat"""
    return chat_service.create_chat(chat_data.model_dump())


@router.get("/chats/{chat_id}", response_model=ChatDetailResponse)
def get_chat(chat_id: UUID, chat_service: ChatService = Depends(get_chat_service)):
    """Get chat by ID with messages"""
    return chat_service.get_chat(chat_id)


@router.put("/chats/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: UUID,
    chat_data: ChatUpdate,
    chat_service: ChatService = Depends(get_chat_service),
):
    """Update chat title"""
    return chat_service.update_chat(chat_id, chat_data.model_dump())


@router.delete("/chats/{chat_id}", status_code=status.HTTP_200_OK)
def delete_chat(chat_id: UUID, chat_service: ChatService = Depends(get_chat_service)):
    """Delete a chat"""
    return chat_service.delete_chat(chat_id)


# Message endpoints
@router.post(
    "/messages/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED
)
def create_message(
    message_data: MessageCreate, chat_service: ChatService = Depends(get_chat_service)
):
    """Create a new message"""
    return chat_service.create_message(message_data.model_dump())


@router.get("/chats/{chat_id}/messages/", response_model=List[MessageResponse])
def get_chat_messages(
    chat_id: UUID,
    skip: int = 0,
    limit: int = 50,
    chat_service: ChatService = Depends(get_chat_service),
):
    """Get all messages for a chat"""
    return chat_service.get_chat_messages(chat_id, skip=skip, limit=limit)


# Streaming Chat endpoints
@router.post("/chat")
async def stream_chat(
    request: ChatRequest,
    protocol: str = Query("data"),
    ai_service: AIService = Depends(get_ai_service),
):
    """
    Stream a chat interaction using Vercel AI protocol
    This endpoint is designed to be compatible with the Vercel AI SDK
    """
    # Return an error if there are no messages or the last message is not from the user
    if not request.messages or request.messages[-1].role != "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from the user",
        )

    # Extract messages in dict format for processing
    client_messages = [msg.model_dump() for msg in request.messages]

    # For demonstration purposes, use chat ID 1
    # In a real app, you would maintain the chat ID in a session or create a new chat
    chat_id = request.chat_id

    # Create a streaming response using the AI service
    response = StreamingResponse(
        ai_service.process_chat_stream(client_messages, chat_id, protocol)
    )

    # Add the Vercel AI protocol header
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


@router.post("/stream-message")
async def stream_message(
    message_data: StreamingMessageCreate,
    ai_service: AIService = Depends(get_ai_service),
):
    """Send a message and get a streaming AI response"""

    # Create a streaming response
    response = StreamingResponse(
        ai_service.stream_ai_response(
            message_content=message_data.content,
            chat_id=message_data.chat_id,
            protocol=message_data.protocol,
        )
    )

    # Add Vercel AI protocol header
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response
