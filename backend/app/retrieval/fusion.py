# backend\app\retrieval\fusion.py
from abc import ABC, abstractmethod

from app.schemas.search import SearchResult


class FusionStrategy(ABC):
    """
    Combines results from multiple retrieval strategies.
    """

    @abstractmethod
    def fuse(
        self,
        result_sets: list[list[SearchResult]],
        limit: int,
    ) -> list[SearchResult]:
        ...