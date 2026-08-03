from app.core.collections import DOCUMENTS_COLLECTION, PRODUCTS_COLLECTION
from app.embeddings.base import EmbeddingProvider
from app.schemas.embedding import EmbeddingRequest
from app.schemas.search import (
    SearchRequest,
    SearchResponse,
)
from app.vector_store.base import VectorStore


class SearchService:

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        embedding = await self.embedding_provider.embed(
            EmbeddingRequest(
                text=request.query,
            )
        )

        document_results = await self.vector_store.search(
            collection=DOCUMENTS_COLLECTION,
            query_vector=embedding.embedding,
            limit=request.limit,
        )

        product_results = await self.vector_store.search(
            collection=PRODUCTS_COLLECTION,
            query_vector=embedding.embedding,
            limit=request.limit,
        )

        results = document_results + product_results

        results.sort(key=lambda x: x.score, reverse=True)

        results = results[: request.limit]

        return SearchResponse(
            results=results,
        )