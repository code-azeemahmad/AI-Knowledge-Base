# backend\app\schemas\rag.py
from typing import Any

from app.schemas.search import SearchResult
from pydantic import BaseModel


class RAGResponse(BaseModel):
    answer: str
    sources: list[SearchResult]
    evaluation: dict[str, Any] | None = None


class RAGRequest(BaseModel):
    conversation_id: str
    question: str
    document_id: str | None = None