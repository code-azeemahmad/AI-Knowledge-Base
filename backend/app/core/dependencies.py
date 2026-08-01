from contextlib import asynccontextmanager

import httpx
from app.core.config import settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.ollama_embeddings import OllamaEmbeddingProvider
from app.schemas.embedding import EmbeddingRequest
from app.schemas.vector import VectorPoint
from app.vector_store.qdrant_store import QdrantStore
from fastapi import Depends, FastAPI, Request
from qdrant_client import AsyncQdrantClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management.
    """

    qdrant_client = AsyncQdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )

    http_client = httpx.AsyncClient()

    try:
        app.state.qdrant_client = qdrant_client
        app.state.http_client = http_client

        store = QdrantStore(qdrant_client)
        await store.ensure_collection()
        
        provider = OllamaEmbeddingProvider(http_client)

        result = await provider.embed(
            EmbeddingRequest(
                text="FastAPI is an async web framework."
            )
        )

        point = VectorPoint(
            vector=result.embedding,
            payload={
                "text": "FastAPI is an async web framework.",
                "source": "startup-test",
            },
        )

        await store.upsert([point])

        print("Inserted first vector into Qdrant.")
        

        yield

    finally:
        await http_client.aclose()
        await qdrant_client.close()


def get_qdrant_client(request: Request) -> AsyncQdrantClient:
    return request.app.state.qdrant_client


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_vector_store(
    client: AsyncQdrantClient = Depends(get_qdrant_client),  # noqa: B008
) -> QdrantStore:
    return QdrantStore(client)


def get_embedding_provider(
    client: httpx.AsyncClient = Depends(get_http_client),  # noqa: B008
) -> EmbeddingProvider:
    return OllamaEmbeddingProvider(client)


'''
The lifespan() should only:

Create the Qdrant client
Create the shared httpx.AsyncClient
Store both in app.state
Ensure the collection exists
Yield
Clean up resources

From now on, all embedding and vector operations will happen through services and API endpoints—not during application startup.
'''
