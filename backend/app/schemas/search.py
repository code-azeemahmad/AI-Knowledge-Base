# backend\app\schemas\search.py
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SearchFilter(BaseModel):
    document_id: str | None = None

class SearchRequest(BaseModel):
    query: str
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    id: UUID
    score: float
    payload: dict[str, Any]
    vector: list[float] | None = Field(default=None, exclude=True)


class SearchResponse(BaseModel):
    results: list[SearchResult]

