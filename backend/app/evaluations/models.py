# backend\app\evaluations\models.py
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class EvaluationSample:
    """
    One labelled test case for RAG evaluation.

    relevant_chunk_ids: UUIDs of the Qdrant point IDs that are
    considered ground-truth relevant for this question.
    """
    question: str
    relevant_chunk_ids: list[str]
    expected_answer: str


@dataclass
class EvaluationResult:
    """Metrics for a single evaluated question."""
    question: str
    recall_at_k: float
    precision_at_k: float
    hit_rate_at_k: float
    reciprocal_rank: float

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "recall_at_k": round(self.recall_at_k, 4),
            "precision_at_k": round(self.precision_at_k, 4),
            "hit_rate_at_k": round(self.hit_rate_at_k, 4),
            "reciprocal_rank": round(self.reciprocal_rank, 4),
        }


@dataclass
class EvaluationReport:
    """
    Aggregated evaluation metrics across a full dataset.
    MRR = mean of per-sample reciprocal_rank.
    """
    results: list[EvaluationResult] = field(default_factory=list)

    @property
    def mean_recall(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.recall_at_k for r in self.results) / len(self.results)

    @property
    def mean_precision(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.precision_at_k for r in self.results) / len(self.results)

    @property
    def hit_rate(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.hit_rate_at_k for r in self.results) / len(self.results)

    @property
    def mrr(self) -> float:
        """Mean Reciprocal Rank across all evaluation samples."""
        if not self.results:
            return 0.0
        return sum(r.reciprocal_rank for r in self.results) / len(self.results)

    def to_dict(self) -> dict:
        return {
            "samples": len(self.results),
            "mean_recall_at_k": round(self.mean_recall, 4),
            "mean_precision_at_k": round(self.mean_precision, 4),
            "hit_rate_at_k": round(self.hit_rate, 4),
            "mrr": round(self.mrr, 4),
            "per_question": [r.to_dict() for r in self.results],
        }
