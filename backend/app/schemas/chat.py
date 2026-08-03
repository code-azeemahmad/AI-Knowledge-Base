# app/schemas/chat.py
from enum import Enum

from app.core.config import settings
from pydantic import BaseModel, Field


class ChatRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessageSchema(BaseModel):
    role: ChatRole
    content: str = Field(..., min_length=1)


class ChatRequestSchema(BaseModel):
    messages: list[ChatMessageSchema]

    temperature: float = Field(
        default=settings.temperature
    )

    max_tokens: int = Field(
        default=settings.max_tokens
    )


class TokenUsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponseSchema(BaseModel):
    content: str

    usage: TokenUsageSchema | None = None

    finish_reason: str | None = None
    
    
'''
Why duplicate these models?
Today they look identical.
Six lessons later they won't.

The domain stays stable while the API evolves.
'''