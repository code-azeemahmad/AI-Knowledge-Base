from app.core.collections import PRODUCTS_COLLECTION
from app.embeddings.base import EmbeddingProvider
from app.schemas.embedding import EmbeddingRequest
from app.schemas.product import (
    CreateProductRequest,
    CreateProductResponse,
    DeleteProductResponse,
)
from app.schemas.vector import VectorPoint
from app.vector_store.base import VectorStore


class ProductService:
    """
    Handles product ingestion into the vector database.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def create_product(
        self,
        request: CreateProductRequest,
    ) -> CreateProductResponse:
        """
        Convert a product into an embedding and store it.
        """

        searchable_text = f"""
        Name: {request.name}
        Description: {request.description}
        Category: {request.category}
        """

        embedding = await self.embedding_provider.embed(
            EmbeddingRequest(
                text=searchable_text.strip(),
            )
        )

        point = VectorPoint(
            vector=embedding.embedding,
            payload={
                "name": request.name,
                "description": request.description,
                "category": request.category,
            },
        )

        await self.vector_store.upsert(
            collection=PRODUCTS_COLLECTION,
            points=[point],
        )

        return CreateProductResponse(
            message="Product stored successfully."
        )

    async def delete_product(
        self,
        product_id: str,
    ) -> DeleteProductResponse:

        await self.vector_store.delete(
            collection=PRODUCTS_COLLECTION,
            point_id=product_id,
        )

        return DeleteProductResponse(
            message="Product deleted successfully."
        )