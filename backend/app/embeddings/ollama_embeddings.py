import httpx
from app.core.config import settings
from app.embeddings.base import EmbeddingProvider
from app.schemas.embedding import (
    EmbeddingRequest,
    EmbeddingResponse,
    OllamaEmbeddingResponse,
)


class OllamaEmbeddingProvider(EmbeddingProvider):

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        response = await self.client.post(
            f"{settings.OLLAMA_BASE_URL}/api/embed",
            json={
                "model": settings.EMBEDDING_MODEL,
                "input": request.text,
            },
        )

        response.raise_for_status()

        data = OllamaEmbeddingResponse.model_validate(
            response.json()
        )

        embedding = data.embeddings[0]
        
        if len(embedding) != settings.EMBEDDING_DIMENSION:
            raise ValueError(
                "Unexpected embedding dimension. "
                f"Expected {settings.EMBEDDING_DIMENSION}, "
                f"got {len(embedding)}."
            )

        return EmbeddingResponse(
            embedding=embedding,
        )