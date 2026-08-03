from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalConfig:
    """
    Configuration for retrieval behavior.
    """

    top_k: int
    score_threshold: float


DEFAULT_RETRIEVAL = RetrievalConfig(
    top_k=5,
    score_threshold=0.50,
)