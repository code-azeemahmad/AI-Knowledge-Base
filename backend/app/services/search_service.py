from app.core.collections import DOCUMENTS_COLLECTION, PRODUCTS_COLLECTION
from app.embeddings.base import EmbeddingProvider
from app.schemas.embedding import EmbeddingRequest
from app.schemas.search import (
    SearchRequest,
    SearchResponse,
)
from app.vector_store.qdrant_store import QdrantStore


class SearchService:

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: QdrantStore,
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

        results = await self.vector_store.search(
            collection=DOCUMENTS_COLLECTION,
            query_vector=embedding.embedding,
            limit=request.limit,
        )
        
        results = await self.vector_store.search(
            collection=PRODUCTS_COLLECTION,
            query_vector=embedding.embedding,
            limit=request.limit,
        )

        return SearchResponse(
            results=results,
        )