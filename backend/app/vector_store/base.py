from abc import ABC, abstractmethod

from app.core.collections import CollectionConfig
from app.schemas.search import SearchFilter, SearchResult
from app.schemas.vector import VectorPoint


class VectorStore(ABC):

    @abstractmethod
    async def create_collection(self, collection: CollectionConfig) -> None: ...

    @abstractmethod
    async def ensure_collection(self, collection: CollectionConfig) -> None: ...

    @abstractmethod
    async def upsert(self, collection: CollectionConfig, points: list[VectorPoint]) -> None: ...

    @abstractmethod
    async def search(
        self, collection: CollectionConfig, query_vector: list[float], limit: int = 5, search_filter: SearchFilter | None = None,
    ) -> list[SearchResult]: ...

    @abstractmethod
    async def delete(self, collection: CollectionConfig, document_id: str) -> None: ...
