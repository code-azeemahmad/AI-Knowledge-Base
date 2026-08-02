# backend\app\core\collections.py
from dataclasses import dataclass

from qdrant_client.models import Distance


@dataclass(frozen=True)
class CollectionConfig:
    name: str
    dimension: int
    distance: Distance


DOCUMENTS_COLLECTION = CollectionConfig(
    name="documents",
    dimension=768,
    distance=Distance.COSINE,
)

CHAT_MEMORY_COLLECTION = CollectionConfig(
    name="chat_memory",
    dimension=768,
    distance=Distance.COSINE,
)

PRODUCTS_COLLECTION = CollectionConfig(
    name="products",
    dimension=768,
    distance=Distance.COSINE,
)