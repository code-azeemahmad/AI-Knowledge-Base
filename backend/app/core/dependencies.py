# backend\app\core\dependencies.py
import httpx
from app.conversations.memory_store import InMemoryConversationStore
from app.core.config import settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.ollama_embeddings import OllamaEmbeddingProvider
from app.exceptions import UnsupportedProviderError
from app.providers.base import LLMProvider
from app.providers.ollama_provider import OllamaProvider
from app.query_rewriters.base import QueryRewriter
from app.query_rewriters.llm_query_rewriter import LLMQueryRewriter
from app.query_rewriters.noop_query_rewriter import NoOpQueryRewriter
from app.rerankers.base import Reranker
from app.retrieval.base import BaseRetriever
from app.retrieval.bm25_index import BM25Index
from app.retrieval.dense import DenseRetriever
from app.retrieval.fusion import FusionStrategy
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.mmr import MMRSelector
from app.retrieval.rrf_fusion import ReciprocalRankFusion
from app.retrieval.sparse import SparseRetriever
from app.services.conversation_service import ConversationService, ConversationStore
from app.services.document_registry import DocumentRegistry
from app.services.document_service import DocumentService
from app.services.health_service import HealthService
from app.services.indexing_service import IndexingService
from app.services.product_service import ProductService
from app.services.rag_service import RAGService
from app.services.search_service import SearchService
from app.tokenizers.base import Tokenizer
from app.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from app.vector_store.base import VectorStore
from app.vector_store.qdrant_store import QdrantStore
from fastapi import Depends, Request
# pyrefly: ignore [missing-import]
from qdrant_client import AsyncQdrantClient

_document_registry = DocumentRegistry()
conversation_store = InMemoryConversationStore()
_tokenizer = WhitespaceTokenizer()
bm25_index = BM25Index(
    tokenizer=_tokenizer,
)


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

def get_document_registry() -> DocumentRegistry:
    return _document_registry


def get_fusion_strategy() -> FusionStrategy:
    return ReciprocalRankFusion()


def get_tokenizer() -> Tokenizer:
    return _tokenizer


def get_bm25_index() -> BM25Index:
    return bm25_index


def get_dense_retriever(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: VectorStore = Depends(get_vector_store),  # noqa: B008
) -> BaseRetriever:
    return DenseRetriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )


def get_sparse_retriever(
    bm25_index: BM25Index = Depends(get_bm25_index),  # noqa: B008
) -> BaseRetriever:
    return SparseRetriever(
        bm25_index=bm25_index,
    )


def get_mmr_selector() -> MMRSelector:
    return MMRSelector(lambda_param=0.7)


def get_hybrid_retriever(
    dense: BaseRetriever = Depends(get_dense_retriever),  # noqa: B008
    sparse: BaseRetriever = Depends(get_sparse_retriever),  # noqa: B008
    fusion: FusionStrategy = Depends(get_fusion_strategy),  # noqa: B008
    mmr: MMRSelector = Depends(get_mmr_selector),  # noqa: B008
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
) -> BaseRetriever:
    return HybridRetriever(
        dense=dense,
        sparse=sparse,
        fusion=fusion,
        mmr=mmr,
        embedding_provider=embedding_provider,
    )


def get_indexing_service(
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),  # noqa: B008
    vector_store: VectorStore = Depends(get_vector_store),  # noqa: B008
    registry: DocumentRegistry = Depends(get_document_registry),  # noqa: B008
    bm25_index: BM25Index = Depends(get_bm25_index),  # noqa: B008
) -> IndexingService:
    return IndexingService(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
        registry=registry,  # ← Pass registry instance here
        bm25_index=bm25_index
    )


def get_reranker(
        request: Request
) -> Reranker:
    return request.app.state.reranker

def get_conversation_store() -> ConversationStore:
    return conversation_store


def get_conversation_service(
    store: ConversationStore = Depends(get_conversation_store),  # noqa: B008
) -> ConversationService:
    return ConversationService(store)

def get_query_rewriter(
    llm_provider: LLMProvider = Depends(get_llm_provider),  # noqa: B008
) -> QueryRewriter:

    provider = settings.query_rewriter.lower()

    if provider == "llm":
        return LLMQueryRewriter(llm_provider)

    return NoOpQueryRewriter()

def get_rag_service(
    retriever: BaseRetriever = Depends(get_hybrid_retriever),  # noqa: B008
    llm_provider: LLMProvider = Depends(get_llm_provider),  # noqa: B008
    reranker: Reranker = Depends(get_reranker),  # noqa: B008
    conversation_service: ConversationService = Depends(get_conversation_service),  # noqa: B008
    query_rewriter: QueryRewriter = Depends(get_query_rewriter),  # noqa: B008
) -> RAGService:
    return RAGService(
        retriever=retriever,
        llm_provider=llm_provider,
        reranker=reranker,
        conversation_service=conversation_service,
        query_rewriter=query_rewriter,
    )

