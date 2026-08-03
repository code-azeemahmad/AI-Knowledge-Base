from app.core.collections import DOCUMENTS_COLLECTION
from app.embeddings.base import EmbeddingProvider
from app.retrieval.retrieval import DEFAULT_RETRIEVAL
from app.schemas.embedding import EmbeddingRequest
from app.schemas.search import SearchResult
from app.vector_store.base import VectorStore


class Retriever:
    """
    Retrieves the most relevant document chunks
    for a user question.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def retrieve(
        self,
        question: str,
        limit: int | None = None,
    ) -> list[SearchResult]:

        search_limit = limit or DEFAULT_RETRIEVAL.top_k

        embedding = await self.embedding_provider.embed(
            EmbeddingRequest(
                text=question,
            )
        )

        results = await self.vector_store.search(
            collection=DOCUMENTS_COLLECTION,
            query_vector=embedding.embedding,
            limit=search_limit,
        )

        results = [
            result
            for result in results
            if result.score >= DEFAULT_RETRIEVAL.score_threshold
        ]

        return results