# backend\app\retrievers\base.py
from abc import ABC, abstractmethod

from app.schemas.search import SearchResult


class BaseRetriever(ABC):
    """
    Abstract interface for all retrieval strategies.
    """

    @abstractmethod
    async def retrieve(
        self,
        question: str,
        limit: int | None = None,
        document_id: str | None = None,
    ) -> list[SearchResult]:
        """
        Retrieve relevant document chunks.
        """
        ...