from app.schemas.search import SearchResult
from pydantic import BaseModel


class RAGResponse(BaseModel):
    answer: str
    sources: list[SearchResult]


class RAGRequest(BaseModel):
    question: str