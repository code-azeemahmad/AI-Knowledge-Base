# backend\app\core\dependencies.py
from contextlib import asynccontextmanager

from app.core.config import settings
from app.vector_store.qdrant_store import QdrantStore
from fastapi import Depends, FastAPI, Request
from qdrant_client import AsyncQdrantClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manages the application lifecycle. QdrantStore manages Qdrant.
    """
    client = AsyncQdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )

    app.state.qdrant_client = client
    store = QdrantStore(client)
    
    await store.ensure_collection()
    
    yield

    await client.close()


def get_qdrant_client(request: Request) -> AsyncQdrantClient:
    return request.app.state.qdrant_client


def get_vector_store(
    client: AsyncQdrantClient = Depends(get_qdrant_client),  # noqa: B008
) -> QdrantStore:
    return QdrantStore(client)

