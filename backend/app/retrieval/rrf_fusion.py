# backend\app\retrieval\rrf_fusion.py
from collections import defaultdict

from app.retrieval.fusion import FusionStrategy
from app.schemas.search import SearchResult


class ReciprocalRankFusion(FusionStrategy):
    """
    Reciprocal Rank Fusion (RRF).

    score = Σ 1 / (k + rank)
    """

    def __init__(
        self,
        k: int = 60,
    ):
        self.k = k

    def fuse(
        self,
        result_sets: list[list[SearchResult]],
        limit: int,
    ) -> list[SearchResult]:

        scores: dict[str, float] = defaultdict(float)
        documents: dict[str, SearchResult] = {}

        for results in result_sets:

            for rank, result in enumerate(results, start=1):

                scores[result.id] += 1.0 / (self.k + rank)

                documents[result.id] = result

        ranked = sorted(
            documents.values(),
            key=lambda result: scores[result.id],
            reverse=True,
        )

        return ranked[:limit]