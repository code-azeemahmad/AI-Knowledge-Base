# backend\app\retrieval\config.py
from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalConfig:
    """
    Configuration for retrieval behavior.
    """

    top_k: int
    score_threshold: float

    rerank_top_k: int = 5

    dense_weight: float = 1.0
    sparse_weight: float = 1.0


DEFAULT_RETRIEVAL = RetrievalConfig(
    top_k=5,
    score_threshold=0.50,
)