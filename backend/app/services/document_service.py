from app.embeddings.base import EmbeddingProvider
from app.schemas.document import (
    CreateDocumentRequest,
    CreateDocumentResponse,
    DeleteDocumentResponse,
)
from app.schemas.embedding import EmbeddingRequest
from app.schemas.vector import VectorPoint
from app.vector_store.qdrant_store import QdrantStore


class DocumentService:
    """
    Handles document ingestion into the vector database.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: QdrantStore,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def create_document(
        self,
        request: CreateDocumentRequest,
    ) -> CreateDocumentResponse:
        """
        Generate an embedding and store it in Qdrant.
        """

        embedding = await self.embedding_provider.embed(
            EmbeddingRequest(
                text=request.text,
            )
        )

        point = VectorPoint(
            vector=embedding.embedding,
            payload={
                "text": request.text,
                "source": request.source,
            },
        )

        await self.vector_store.upsert([point])

        return CreateDocumentResponse(
            message="Document stored successfully."
        )
        

    async def delete_document(
        self,
        document_id: str,
    ) -> DeleteDocumentResponse:

        await self.vector_store.delete(document_id)

        return DeleteDocumentResponse(
            message="Document deleted successfully."
        )