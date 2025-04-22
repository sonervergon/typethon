from typing import Any, Dict, List
from uuid import UUID

from fastapi import Depends, HTTPException, status
from operations.chat_repository import ChatRepository, get_chat_repository


class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    # Chat operations
    def get_chats(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        chats = self.chat_repository.get_chats(skip=skip, limit=limit)
        return [
            {
                "id": chat.id,
                "title": chat.title
                if chat.title is not None
                else f"Chat {chat.id}",  # Default title if none is provided
                "created_at": chat.created_at,
                "updated_at": chat.updated_at,
            }
            for chat in chats
        ]

    def get_chat(self, chat_id: UUID) -> Dict[str, Any]:
        chat = self.chat_repository.get_chat(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )

        # Get messages for this chat
        messages = self.chat_repository.get_messages_by_chat(chat_id)

        return {
            "id": chat.id,
            "title": chat.title if chat.title is not None else f"Chat {chat.id}",
            "created_at": chat.created_at,
            "updated_at": chat.updated_at,
            "messages": [
                {
                    "id": message.id,
                    "content": message.content,
                    "is_from_ai": bool(message.is_from_ai),
                    "created_at": message.created_at,
                    "chat_id": message.chat_id,
                }
                for message in messages
            ],
        }

    def create_chat(self, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        # Create new chat
        chat = self.chat_repository.create_chat(chat_data)

        return {
            "id": chat.id,
            "title": chat.title if chat.title is not None else f"Chat {chat.id}",
            "created_at": chat.created_at,
            "updated_at": chat.updated_at,
            "messages": [],
        }

    def update_chat(self, chat_id: UUID, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        # Check if chat exists
        chat = self.chat_repository.get_chat(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )

        # Update chat
        updated_chat = self.chat_repository.update_chat(chat_id, chat_data)
        if not updated_chat:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update chat",
            )

        return {
            "id": updated_chat.id,
            "title": updated_chat.title
            if updated_chat.title is not None
            else f"Chat {updated_chat.id}",
            "created_at": updated_chat.created_at,
            "updated_at": updated_chat.updated_at,
        }

    def delete_chat(self, chat_id: UUID) -> Dict[str, Any]:
        # Check if chat exists
        chat = self.chat_repository.get_chat(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )

        # Delete chat
        self.chat_repository.delete_chat(chat_id)

        return {"success": True, "message": "Chat deleted successfully"}

    # Message operations
    def create_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        # Check if chat exists
        chat_id = message_data.get("chat_id")
        if not chat_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chat ID is required",
            )

        chat = self.chat_repository.get_chat(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )

        # Create message
        message = self.chat_repository.create_message(message_data)

        return {
            "id": message.id,
            "content": message.content,
            "is_from_ai": bool(message.is_from_ai),
            "created_at": message.created_at,
            "chat_id": message.chat_id,
        }

    def get_chat_messages(
        self, chat_id: UUID, skip: int = 0, limit: int = 50
    ) -> List[Dict[str, Any]]:
        # Check if chat exists
        chat = self.chat_repository.get_chat(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )

        # Get messages
        messages = self.chat_repository.get_messages_by_chat(
            chat_id, skip=skip, limit=limit
        )

        return [
            {
                "id": message.id,
                "content": message.content,
                "is_from_ai": bool(message.is_from_ai),
                "created_at": message.created_at,
                "chat_id": message.chat_id,
            }
            for message in messages
        ]


def get_chat_service(
    chat_repository: ChatRepository = Depends(get_chat_repository),
) -> ChatService:
    return ChatService(chat_repository)
