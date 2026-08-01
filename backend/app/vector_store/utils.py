# backend\app\vector_store\utils.py
from qdrant_client.models import Distance

_DISTANCE_MAP = {
    "cosine": Distance.COSINE,
    "dot": Distance.DOT,
    "euclidean": Distance.EUCLID,
}


def get_distance(distance: str) -> Distance:
    """
    Convert a string from configuration into a Qdrant Distance enum.
    """
    try:
        return _DISTANCE_MAP[distance.lower()]
    except KeyError as exc:
        supported = ", ".join(_DISTANCE_MAP.keys())
        raise ValueError(
            f"Unsupported VECTOR_DISTANCE '{distance}'. "
            f"Supported values: {supported}."
        ) from exc