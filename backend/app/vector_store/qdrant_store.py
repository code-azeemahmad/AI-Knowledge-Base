# backend\app\vector_store\qdrant_store.py
from app.core.config import settings  # noqa: I001
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams
from app.vector_store.utils import get_distance

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