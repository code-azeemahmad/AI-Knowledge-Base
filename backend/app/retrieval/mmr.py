# backend\app\retrieval\mmr.py
import math

from app.schemas.search import SearchResult


class MMRSelector:
    """
    Maximum Marginal Relevance (MMR) diversity filter.

    Selects k results that balance relevance to the query
    and diversity between selected documents.

    Formula:
        MMR = λ * Sim(query, doc) - (1 - λ) * max Sim(doc, selected)
    """

    def __init__(
        self,
        lambda_param: float = 0.7,
    ):
        self.lambda_param = lambda_param

    def select(
        self,
        query_vector: list[float],
        candidates: list[SearchResult],
        k: int = 5,
    ) -> list[SearchResult]:

        selected: list[SearchResult] = []
        remaining = candidates.copy()

        while remaining and len(selected) < k:

            best = None
            best_score = float("-inf")

            for candidate in remaining:

                relevance = candidate.score

                diversity = self._diversity_score(
                    candidate,
                    selected,
                )

                mmr_score = (
                    self.lambda_param * relevance
                    - (1 - self.lambda_param) * diversity
                )

                if mmr_score > best_score:
                    best_score = mmr_score
                    best = candidate

            if best is None:
                break

            selected.append(best)
            remaining.remove(best)

        return selected

    def _diversity_score(
        self,
        candidate: SearchResult,
        selected: list[SearchResult],
    ) -> float:
        """
        Returns the maximum cosine similarity between the candidate
        and any already-selected document.

        If no documents are selected yet, returns 0.0 (no penalty).
        If the candidate has no vector, returns 0.0 (no penalty).
        """
        if not selected or candidate.vector is None:
            return 0.0

        return max(
            self._cosine_similarity(candidate.vector, doc.vector)
            for doc in selected
            if doc.vector is not None
        ) if any(doc.vector is not None for doc in selected) else 0.0

    @staticmethod
    def _cosine_similarity(
        a: list[float],
        b: list[float],
    ) -> float:
        """
        Cosine similarity between two vectors.
        Returns a value in [-1, 1]; returns 0.0 for zero vectors.
        """
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        return dot / (norm_a * norm_b)