# backend/app/domain/chat.py
from enum import StrEnum

from app.core.config import settings
from pydantic import BaseModel, ConfigDict, Field


class ChatRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    model_config = ConfigDict(frozen=True)
    role: ChatRole
    content: str = Field(
        min_length=1,
    )
    
class TokenUsage(BaseModel):
    model_config = ConfigDict(frozen=True)
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    
class ChatResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    content: str
    usage: TokenUsage | None = None
    finish_reason: str | None = None
    
    
class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    temperature: float = Field(
        default=settings.temperature,
        ge=0.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=settings.max_tokens,
        gt=0,
    )
