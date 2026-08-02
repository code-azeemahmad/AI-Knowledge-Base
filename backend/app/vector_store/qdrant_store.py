# backend\app\vector_store\qdrant_store.py
from app.core.collections import CollectionConfig
from app.schemas.search import SearchResult
from app.schemas.vector import VectorPoint
from app.vector_store.base import VectorStore
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointIdsList, PointStruct, VectorParams


class QdrantStore(VectorStore):

    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def collection_exists(self, collection: CollectionConfig) -> bool:
        return await self.client.collection_exists(collection_name=collection.name)

    async def create_collection(self, collection: CollectionConfig) -> None:
        await self.client.create_collection(
            collection_name=collection.name,
            vectors_config=VectorParams(size=collection.dimension, distance=collection.distance),
        )

    async def ensure_collection(self, collection: CollectionConfig) -> None:
        exists = await self.collection_exists(collection)

        if not exists:
            await self.create_collection(collection)
            print(f"Collection '{collection.name}' created.")
        else:
            print(f"Collection '{collection.name}' already exists.")

    async def upsert(self, collection: CollectionConfig, points: list[VectorPoint]) -> None:

        qdrant_points = [PointStruct(id=str(point.id), vector=point.vector, payload=point.payload) for point in points]

        await self.client.upsert(collection_name=collection.name, points=qdrant_points)

    async def search(
        self, collection: CollectionConfig, query_vector: list[float], limit: int = 5
    ) -> list[SearchResult]:

        results = await self.client.query_points(
            collection_name=collection.name, query=query_vector, limit=limit, with_payload=True
        )

        return [SearchResult(id=point.id, score=point.score, payload=point.payload or {}) for point in results.points]

    async def delete(self, collection: CollectionConfig, point_id: str) -> None:

        await self.client.delete(collection_name=collection.name, points_selector=PointIdsList(points=[point_id]))
