from app.core.collections import DOCUMENTS_COLLECTION
from app.embeddings.base import EmbeddingProvider
from app.schemas.embedding import EmbeddingRequest
from app.schemas.search import SearchResult
from app.vector_store.qdrant_store import QdrantStore


class Retriever:
    """
    Retrieves the most relevant document chunks
    for a user question.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: QdrantStore,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def retrieve(
        self,
        question: str,
        limit: int = 5,
    ) -> list[SearchResult]:

        embedding = await self.embedding_provider.embed(
            EmbeddingRequest(
                text=question,
            )
        )

        return await self.vector_store.search(
            collection=DOCUMENTS_COLLECTION,
            query_vector=embedding.embedding,
            limit=limit,
        )