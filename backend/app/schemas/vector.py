# backend\app\schemas\vector.
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class VectorPoint(BaseModel):
    """
    Represents a point to be stored in Qdrant.
    """

    id: UUID = Field(default_factory=uuid4)
    vector: list[float]
    payload: dict[str, Any] = Field(default_factory=dict)