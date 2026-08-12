# backend\app\evaluations\retrieval_evaluator.py
from app.evaluations.models import (
    EvaluationReport,
    EvaluationResult,
    EvaluationSample,
)
from app.schemas.search import SearchResult


def _get_result_ids(result: SearchResult) -> set[str]:
    """
    Returns candidate IDs for matching against relevant_chunk_ids.
    Matches both point UUID (str(result.id)) and payload-based format
    ("<filename>:<chunk_index>") if available.
    """
    ids = {str(result.id)}
    filename = result.payload.get("filename")
    chunk_index = result.payload.get("chunk_index")
    if filename is not None and chunk_index is not None:
        ids.add(f"{filename}:{chunk_index}")
    return ids


class RetrievalEvaluator:

    @staticmethod
    def recall_at_k(
        results: list[SearchResult],
        sample: EvaluationSample,
        k: int = 5,
    ) -> float:
        top_results = results[:k]
        relevant_ids = {str(cid) for cid in sample.relevant_chunk_ids}
        if not relevant_ids:
            return 0.0

        retrieved_ids = set()
        for res in top_results:
            retrieved_ids.update(_get_result_ids(res))

        retrieved_relevant = retrieved_ids & relevant_ids
        return len(retrieved_relevant) / len(relevant_ids)

    @staticmethod
    def precision_at_k(
        results: list[SearchResult],
        sample: EvaluationSample,
        k: int = 5,
    ) -> float:
        top_results = results[:k]
        if not top_results:
            return 0.0

        relevant_ids = {str(cid) for cid in sample.relevant_chunk_ids}

        relevant_count = sum(
            1
            for res in top_results
            if bool(_get_result_ids(res) & relevant_ids)
        )
        return relevant_count / len(top_results)

    @staticmethod
    def hit_rate_at_k(
        results: list[SearchResult],
        sample: EvaluationSample,
        k: int = 5,
    ) -> float:
        relevant_ids = {str(cid) for cid in sample.relevant_chunk_ids}
        for res in results[:k]:
            if _get_result_ids(res) & relevant_ids:
                return 1.0
        return 0.0

    @staticmethod
    def reciprocal_rank(
        results: list[SearchResult],
        sample: EvaluationSample,
    ) -> float:
        relevant_ids = {str(cid) for cid in sample.relevant_chunk_ids}
        for index, res in enumerate(results, start=1):
            if _get_result_ids(res) & relevant_ids:
                return 1.0 / index
        return 0.0

    @classmethod
    def evaluate(
        cls,
        results: list[SearchResult],
        sample: EvaluationSample,
        k: int = 5,
    ) -> dict[str, float]:
        return {
            "recall_at_k": cls.recall_at_k(results, sample, k),
            "precision_at_k": cls.precision_at_k(results, sample, k),
            "hit_rate_at_k": cls.hit_rate_at_k(results, sample, k),
            "reciprocal_rank": cls.reciprocal_rank(results, sample),
        }

    @classmethod
    def evaluate_dataset(
        cls,
        results_per_sample: list[tuple[list[SearchResult], EvaluationSample]],
        k: int = 5,
    ) -> EvaluationReport:
        report = EvaluationReport()
        for results, sample in results_per_sample:
            metrics = cls.evaluate(results, sample, k)
            report.results.append(
                EvaluationResult(
                    question=sample.question,
                    recall_at_k=metrics["recall_at_k"],
                    precision_at_k=metrics["precision_at_k"],
                    hit_rate_at_k=metrics["hit_rate_at_k"],
                    reciprocal_rank=metrics["reciprocal_rank"],
                )
            )
        return report