from abc import ABC, abstractmethod

from app.core.collections import CollectionConfig
from app.schemas.search import SearchResult
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
        self, collection: CollectionConfig, query_vector: list[float], limit: int = 5
    ) -> list[SearchResult]: ...

    @abstractmethod
    async def delete(self, collection: CollectionConfig, point_id: str) -> None: ...
