import os
import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.chunking.fixed_chunker import FixedChunker
from app.core.collections import DOCUMENTS_COLLECTION
from app.embeddings.base import EmbeddingProvider
from app.loaders.factory import LoaderFactory
from app.schemas.document_chunk import DocumentChunk
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.embedding import EmbeddingRequest
from app.schemas.indexing import IndexingResponse
from app.schemas.vector import VectorPoint
from app.vector_store.qdrant_store import QdrantStore
from fastapi import UploadFile


class IndexingService:
    """
    Handles the complete document indexing pipeline.

    Upload
        ↓
    Extract Text
        ↓
    Chunk Text
        ↓
    Generate Embeddings
        ↓
    Store in Qdrant
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: QdrantStore,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store
        self.chunker = FixedChunker()

    async def index_document(
        self,
        file: UploadFile,
    ) -> IndexingResponse:

        document_id = str(uuid4())

        suffix = Path(file.filename).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(await file.read())
            temp_path = temp_file.name

        try:
            loader = LoaderFactory.get_loader(file.filename)

            text = await loader.load(temp_path)

            chunks = self.chunker.chunk(text)

            points: list[VectorPoint] = []

            for index, chunk in enumerate(chunks):

                embedding = await self.embedding_provider.embed(
                    EmbeddingRequest(
                        text=chunk,
                    )
                )

                payload = DocumentChunk(
                    document_id=document_id,
                    filename=file.filename,
                    chunk_index=index,
                    text=chunk,
                )

                points.append(
                    VectorPoint(
                        id=str(uuid4()),
                        vector=embedding.embedding,
                        payload=payload.model_dump(),
                    )
                )

            await self.vector_store.upsert(
                DOCUMENTS_COLLECTION,
                points,
            )

            metadata = DocumentMetadata(
                document_id=document_id,
                filename=file.filename,
                chunks=len(points),
                uploaded_at=datetime.utcnow(),  # noqa: DTZ003
            )

            self.registry.add(metadata)            

            return IndexingResponse(
                document_id=document_id,
                filename=file.filename,
                chunks_indexed=len(points),
            )

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
