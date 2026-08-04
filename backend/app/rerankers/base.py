# backend\app\rerankers\base.py
from abc import ABC, abstractmethod

from app.schemas.search import SearchResult


class Reranker(ABC):

    @abstractmethod
    async def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int,
    ) -> list[SearchResult]:
        """
        Return the most relevant search results.
        """
        ...