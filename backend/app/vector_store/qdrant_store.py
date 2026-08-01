# backend\app\vector_store\qdrant_store.py
from app.core.config import settings  # noqa: I001
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams
from app.vector_store.utils import get_distance

from qdrant_client.models import PointStruct
from app.schemas.vector import VectorPoint

from app.schemas.search import SearchResult

class QdrantStore:

    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def collection_exists(
        self,
        collection_name: str = settings.DEFAULT_COLLECTION,
    ) -> bool:
        """
        Check whether a collection already exists.
        """
        return await self.client.collection_exists(
            collection_name=collection_name,
        )

    async def create_collection(
        self,
        collection_name: str = settings.DEFAULT_COLLECTION,
    ) -> None:
        """
        Create a new Qdrant collection.
        """

        await self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=settings.EMBEDDING_DIMENSION,
                distance=get_distance(settings.VECTOR_DISTANCE),
            ),
        )

        print(f"Created collection: {collection_name}")
        

    async def ensure_collection(
        self,
        collection_name: str = settings.DEFAULT_COLLECTION,
    ) -> None:
        """
        Ensure that the collection exists.
        """

        exists = await self.collection_exists(collection_name)

        if exists:
            print(f"Collection '{collection_name}' already exists.")
            return

        await self.create_collection(collection_name)
        

    async def upsert(
        self,
        points: list[VectorPoint],
        collection_name: str = settings.DEFAULT_COLLECTION,
    ) -> None:
        """
        Insert or update points in Qdrant.
        """

        qdrant_points = [
            PointStruct(
                id=str(point.id),
                vector=point.vector,
                payload=point.payload,
            )
            for point in points
        ]

        await self.client.upsert(
            collection_name=collection_name,
            points=qdrant_points,
        )
        
        
    async def search(
        self,
        query_vector: list[float],
        limit: int = 5,
        collection_name: str = settings.DEFAULT_COLLECTION,
    ) -> list[SearchResult]:
        """
        Perform semantic similarity search.
        """

        results = await self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        return [
            SearchResult(
                id=point.id,
                score=point.score,
                payload=point.payload or {},
            )
            for point in results.points
        ]