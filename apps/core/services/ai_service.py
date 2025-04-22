import asyncio
import json
from typing import Any, AsyncGenerator, Dict, List, cast
from uuid import UUID

from fastapi import Depends

# Import and configure OpenAI
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from operations.chat_repository import ChatRepository, get_chat_repository

from core.config import OPENAI_API_KEY

# Initialize OpenAI client with API key from config
client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class AIService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    async def generate_ai_response(
        self, message_content: str, chat_id: UUID
    ) -> Dict[str, Any]:
        """
        Generate AI response using OpenAI API
        """
        # Get chat history for context
        chat_history = await self.get_chat_history(chat_id)

        # Add the current message to history
        chat_history.append({"role": "user", "content": message_content})

        # Call OpenAI API to get a response
        response = await client.chat.completions.create(
            model="o4-mini",
            messages=cast(List[ChatCompletionMessageParam], chat_history),
        )

        ai_response = response.choices[0].message.content

        # Create and store the AI response message
        message_data = {
            "content": ai_response,
            "is_from_ai": True,
            "chat_id": chat_id,
        }

        ai_message = self.chat_repository.create_message(message_data)

        return {
            "id": ai_message.id,
            "content": ai_message.content,
            "is_from_ai": bool(ai_message.is_from_ai),
            "created_at": ai_message.created_at,
            "chat_id": ai_message.chat_id,
        }

    async def get_chat_history(self, chat_id: UUID) -> List[Dict[str, Any]]:
        """Get the chat history in a format usable for AI context"""
        messages = self.chat_repository.get_messages_by_chat(chat_id)
        result = []

        for msg in messages:
            # Create a new Python dictionary instead of modifying one
            if hasattr(msg, "is_from_ai"):
                source_value = getattr(msg, "is_from_ai")
                if source_value == 1:
                    role = "assistant"
                else:
                    role = "user"
            else:
                role = "user"

            # Create new dict with all values at once
            message_dict = {"role": role, "content": msg.content}

            result.append(message_dict)

        return result

    async def stream_ai_response(
        self, message_content: str, chat_id: UUID, protocol: str = "data"
    ) -> AsyncGenerator[str, None]:
        """
        Stream an AI response according to the Vercel AI protocol
        """
        # Get chat history for context
        chat_history = await self.get_chat_history(chat_id)

        # Add the current message to history
        chat_history.append({"role": "user", "content": message_content})

        # Save the user message to the database
        user_message_data = {
            "content": message_content,
            "is_from_ai": False,
            "chat_id": chat_id,
        }
        self.chat_repository.create_message(user_message_data)

        # Use OpenAI streaming API
        complete_response = ""

        # Create a streaming response from OpenAI
        stream = await client.chat.completions.create(
            model="o4-mini",
            messages=cast(List[ChatCompletionMessageParam], chat_history),
            stream=True,
        )

        if protocol == "text":
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    complete_response += content
                    yield content

        elif protocol == "data":
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    complete_response += content
                    yield f"0:{json.dumps(content)}\n"

            # Send the completion message
            yield f'd:{{"finishReason":"stop","usage":{{"promptTokens":0,"completionTokens":{len(complete_response)}}}}}\n'

        # Save the complete AI response to the database
        ai_message_data = {
            "content": complete_response,
            "is_from_ai": True,
            "chat_id": chat_id,
        }
        self.chat_repository.create_message(ai_message_data)

    async def convert_to_openai_messages(self, client_messages: List[Dict[str, Any]]):
        """
        Convert client messages to OpenAI format
        In a real implementation, you would handle attachments and tool invocations
        """
        openai_messages = []

        for message in client_messages:
            # Basic conversion for text content
            openai_messages.append(
                {
                    "role": message.get("role", "user"),
                    "content": message.get("content", ""),
                }
            )

        return openai_messages

    async def process_chat_stream(
        self,
        client_messages: List[Dict[str, Any]],
        chat_id: UUID,
        protocol: str = "data",
    ) -> AsyncGenerator[str, None]:
        """
        Process a complete chat interaction with streaming response
        This matches the example's pattern for handling chat requests
        """
        # In a real app, you would process the full message history
        # For this dummy implementation, we'll just use the last message from the user
        if client_messages and client_messages[-1]["role"] == "user":
            last_message = client_messages[-1]
            message_content = last_message.get("content", "")

            # Get a streaming response
            async for chunk in self.stream_ai_response(
                message_content, chat_id, protocol
            ):
                yield chunk
        else:
            # No valid messages found
            yield "No valid user messages found"


def get_ai_service(
    chat_repository: ChatRepository = Depends(get_chat_repository),
) -> AIService:
    return AIService(chat_repository)
