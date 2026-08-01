# backend\app\embedding\base.py
from abc import ABC, abstractmethod

from app.schemas.embedding import (
    EmbeddingRequest,
    EmbeddingResponse,
)


class EmbeddingProvider(ABC):

    @abstractmethod
    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate an embedding for the given text.
        """
        ...
