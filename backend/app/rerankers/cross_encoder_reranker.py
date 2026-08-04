# backend\app\rerankers\cross_encoder_reranker.py
from app.rerankers.base import Reranker
from app.schemas.search import SearchResult
from sentence_transformers import CrossEncoder


class CrossEncoderReranker(Reranker):

    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

    async def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:

        if not results:
            return []

        pairs = [
            (
                query,
                result.payload["text"],
            )
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(scores, results),
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            result
            for _, result in ranked[:top_k]
        ]