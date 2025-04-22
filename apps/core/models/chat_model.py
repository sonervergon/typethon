import uuid

from lib.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=True)
    # Anonymous chats don't need a user_id, but we can add it later if needed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    # Relationships
    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )

    # Add index on created_at for sorting chats by date
    __table_args__ = (Index("ix_chats_created_at", created_at.desc()),)


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chat_id = Column(
        UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(Text, nullable=False)
    # is_from_ai: True if message is from AI, False if from user
    is_from_ai = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    chat = relationship("Chat", back_populates="messages")

    # Add indexes for query optimization
    __table_args__ = (
        Index("ix_messages_chat_id", chat_id),
        Index("ix_messages_created_at", created_at),
    )
