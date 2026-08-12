# backend\app\retrieval\hybrid.py
from app.embeddings.base import EmbeddingProvider
from app.retrieval.base import BaseRetriever
from app.retrieval.fusion import FusionStrategy
from app.retrieval.mmr import MMRSelector
from app.schemas.embedding import EmbeddingRequest
from app.schemas.search import SearchResult


class HybridRetriever(BaseRetriever):
    """
    Combines dense and sparse retrieval using a fusion strategy,
    then applies MMR diversity filtering before returning results.
    """

    def __init__(
        self,
        dense: BaseRetriever,
        sparse: BaseRetriever,
        fusion: FusionStrategy,
        mmr: MMRSelector,
        embedding_provider: EmbeddingProvider,
    ):
        self.dense = dense
        self.sparse = sparse
        self.fusion = fusion
        self.mmr = mmr
        self.embedding_provider = embedding_provider

    async def retrieve(
        self,
        question: str,
        limit: int | None = None,
        document_id: str | None = None,
    ) -> list[SearchResult]:

        top_k = limit or 5

        dense_results = await self.dense.retrieve(
            question=question,
            limit=top_k,
            document_id=document_id,
        )

        sparse_results = await self.sparse.retrieve(
            question=question,
            limit=top_k,
            document_id=document_id,
        )

        # Fuse dense + sparse with Reciprocal Rank Fusion
        # Fetch more candidates than needed so MMR has room to diversify
        fused = self.fusion.fuse(
            result_sets=[
                dense_results,
                sparse_results,
            ],
            limit=top_k * 3,
        )

        # Embed the query once so MMR can compute cosine diversity
        query_embedding = await self.embedding_provider.embed(
            EmbeddingRequest(text=question)
        )

        # Apply MMR to select diverse top-k from the fused pool
        results = self.mmr.select(
            query_vector=query_embedding.embedding,
            candidates=fused,
            k=top_k,
        )

        return results