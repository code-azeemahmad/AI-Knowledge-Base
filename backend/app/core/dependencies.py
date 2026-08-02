from contextlib import asynccontextmanager

import httpx
from app.core.config import settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.ollama_embeddings import OllamaEmbeddingProvider
from app.services.document_service import DocumentService
from app.services.search_service import SearchService
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

def get_search_service(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: QdrantStore = Depends(get_vector_store),  # noqa: B008
) -> SearchService:
    return SearchService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )


def get_document_service(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: QdrantStore = Depends(get_vector_store),  # noqa: B008
) -> DocumentService:
    return DocumentService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )