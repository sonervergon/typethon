from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import Depends
from lib.database import create_session
from models.chat_model import Chat, Message
from sqlalchemy import desc
from sqlalchemy.orm import Session


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    # Chat operations
    def get_chat(self, chat_id: UUID) -> Optional[Chat]:
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def get_chats(self, skip: int = 0, limit: int = 20) -> List[Chat]:
        return (
            self.db.query(Chat)
            .order_by(desc(Chat.updated_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_chat(self, chat_data: Dict[str, Any]) -> Chat:
        chat = Chat(**chat_data)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def update_chat(self, chat_id: UUID, chat_data: Dict[str, Any]) -> Optional[Chat]:
        chat = self.get_chat(chat_id)
        if chat:
            for key, value in chat_data.items():
                setattr(chat, key, value)
            self.db.commit()
            self.db.refresh(chat)
        return chat

    def delete_chat(self, chat_id: UUID) -> bool:
        chat = self.get_chat(chat_id)
        if chat:
            self.db.delete(chat)
            self.db.commit()
            return True
        return False

    # Message operations
    def get_message(self, message_id: UUID) -> Optional[Message]:
        return self.db.query(Message).filter(Message.id == message_id).first()

    def get_messages_by_chat(
        self, chat_id: UUID, skip: int = 0, limit: int = 50
    ) -> List[Message]:
        return (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_message(self, message_data: Dict[str, Any]) -> Message:
        message = Message(**message_data)
        self.db.add(message)

        # Update the chat's updated_at timestamp
        chat = self.get_chat(message_data["chat_id"])
        if chat:
            # The updated_at will be automatically updated due to onupdate
            self.db.merge(chat)

        self.db.commit()
        self.db.refresh(message)
        return message

    def delete_message(self, message_id: UUID) -> bool:
        message = self.get_message(message_id)
        if message:
            self.db.delete(message)
            self.db.commit()
            return True
        return False


def get_chat_repository(
    db: Session = Depends(create_session),
) -> ChatRepository:
    return ChatRepository(db)
