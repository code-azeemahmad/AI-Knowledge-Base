# backend\app\vector_store\base.py
from abc import ABC, abstractmethod

from app.schemas.vector import VectorPoint


class VectorStore(ABC):

    @abstractmethod
    async def collection_exists(self, collection_name: str) -> bool:
        """Return True if the collection exists."""
        ...

    @abstractmethod
    async def create_collection(self) -> None:
        ...

    @abstractmethod
    async def ensure_collection(self) -> None:
        ...

    @abstractmethod
    async def upsert(
        self,
        points: list[VectorPoint],
    ) -> None:
        ...

    @abstractmethod
    async def search(self):
        ...

    @abstractmethod
    async def delete(self):
        ...