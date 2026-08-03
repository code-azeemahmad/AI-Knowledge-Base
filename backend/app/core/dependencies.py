# backend\app\core\dependencies.py
import httpx
from app.core.config import settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.ollama_embeddings import OllamaEmbeddingProvider
from app.exceptions import UnsupportedProviderError
from app.providers.base import LLMProvider
from app.providers.ollama_provider import OllamaProvider
from app.retrieval.retriever import Retriever
from app.services.document_service import DocumentService
from app.services.health_service import HealthService
from app.services.indexing_service import IndexingService
from app.services.product_service import ProductService
from app.services.rag_service import RAGService
from app.services.search_service import SearchService
from app.vector_store.base import VectorStore
from app.vector_store.qdrant_store import QdrantStore
from fastapi import Depends, Request
from qdrant_client import AsyncQdrantClient


def get_qdrant_client(request: Request) -> AsyncQdrantClient:
    return request.app.state.qdrant_client


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_vector_store(client: AsyncQdrantClient = Depends(get_qdrant_client)) -> VectorStore:  # noqa: B008
    return QdrantStore(client)


def get_embedding_provider(client: httpx.AsyncClient = Depends(get_http_client)) -> EmbeddingProvider:  # noqa: B008
    return OllamaEmbeddingProvider(client)

def get_llm_provider(
    client: httpx.AsyncClient = Depends(get_http_client),  # noqa: B008
) -> LLMProvider:
    """
    Return the configured LLM provider.
    """

    provider = settings.llm_provider.lower()

    if provider == "ollama":
        return OllamaProvider(client)

    raise UnsupportedProviderError(provider)


def get_search_service(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: VectorStore = Depends(get_vector_store),  # noqa: B008
) -> SearchService:
    return SearchService(embedding_provider=embedding_provider, vector_store=vector_store)


def get_document_service(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # # noqa: B008
    vector_store: VectorStore = Depends(get_vector_store),  # noqa: B008
) -> DocumentService:
    return DocumentService(embedding_provider=embedding_provider, vector_store=vector_store)


def get_product_service(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: VectorStore = Depends(get_vector_store),  # noqa: B008
) -> ProductService:
    return ProductService(embedding_provider=embedding_provider, vector_store=vector_store)


def get_health_service(client: AsyncQdrantClient = Depends(get_qdrant_client)) -> HealthService:  # noqa: B008
    return HealthService(client)


def get_indexing_service(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: VectorStore = Depends(get_vector_store),  # noqa: B008
) -> IndexingService:
    return IndexingService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )


def get_retriever(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: VectorStore = Depends(get_vector_store),  # noqa: B008
) -> Retriever:
    return Retriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )


def get_rag_service(
    retriever: Retriever = Depends(get_retriever),  # noqa: B008
    llm_provider: LLMProvider = Depends(get_llm_provider),  # noqa: B008
) -> RAGService:
    return RAGService(
        retriever=retriever,
        llm_provider=llm_provider,
    )