# backend\app\retrieval\hybrid.py
from app.retrieval.base import BaseRetriever
from app.retrieval.fusion import FusionStrategy
from app.schemas.search import SearchResult


class HybridRetriever(BaseRetriever):
    """
    Combines dense and sparse retrieval using a fusion strategy.
    """

    def __init__(
        self,
        dense: BaseRetriever,
        sparse: BaseRetriever,
        fusion: FusionStrategy,
    ):
        self.dense = dense
        self.sparse = sparse
        self.fusion = fusion

    async def retrieve(
        self,
        question: str,
        limit: int | None = None,
        document_id: str | None = None,
    ) -> list[SearchResult]:

        dense_results = await self.dense.retrieve(
            question=question,
            limit=limit,
            document_id=document_id,
        )

        sparse_results = await self.sparse.retrieve(
            question=question,
            limit=limit,
            document_id=document_id,
        )

        results = self.fusion.fuse(
            result_sets=[
                dense_results,
                sparse_results,
            ],
            limit=limit or 5,
        )

        return results