# app/domain/stream.py
from enum import Enum

from app.domain.chat import TokenUsage
from pydantic import BaseModel


class StreamEventType(str, Enum):
    TEXT = "text"
    DONE = "done"


class StreamEvent(BaseModel):
    type: StreamEventType
    content: str = ""
    usage: TokenUsage | None = None
    finish_reason: str | None = None