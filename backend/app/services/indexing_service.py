# backend/app/services/indexing_service.py

import os
import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from app.chunking.recursive_chunker import RecursiveChunker
from app.core.collections import DOCUMENTS_COLLECTION
from app.embeddings.base import EmbeddingProvider
from app.loaders.factory import LoaderFactory
from app.retrieval.bm25_index import BM25Index, IndexedChunk
from app.schemas.document_chunk import DocumentChunk
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.embedding import EmbeddingRequest
from app.schemas.indexing import IndexingResponse
from app.schemas.vector import VectorPoint
from app.services.document_registry import DocumentRegistry
from app.vector_store.base import VectorStore
from fastapi import UploadFile


class IndexingService:
    """
    Handles the complete document indexing pipeline.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
        registry: DocumentRegistry,
        bm25_index: BM25Index,
    ):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store
        self.registry = registry
        self.chunker = RecursiveChunker()
        self.bm25_index = bm25_index

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
            indexed_chunks: list[IndexedChunk] = []

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

                point_id = str(uuid4())

                points.append(
                    VectorPoint(
                        id=point_id,
                        vector=embedding.embedding,
                        payload=payload.model_dump(),
                    )
                )

                indexed_chunks.append(
                    IndexedChunk(
                        id=point_id,
                        text=chunk,
                        payload=payload.model_dump(),
                    )
                )

            # Store dense vectors
            await self.vector_store.upsert(
                DOCUMENTS_COLLECTION,
                points,
            )

            # Store sparse BM25 index
            self.bm25_index.add_documents(
                indexed_chunks,
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