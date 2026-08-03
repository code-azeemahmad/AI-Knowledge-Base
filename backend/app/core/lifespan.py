from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import httpx
from app.core.collections import ALL_COLLECTIONS
from app.core.config import settings
from app.vector_store.qdrant_store import QdrantStore
from fastapi import FastAPI
from qdrant_client import AsyncQdrantClient

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan.

    Creates shared infrastructure clients on startup and
    gracefully closes them on shutdown.
    """

    logger.info("Starting AI Knowledge Base...")

    timeout = httpx.Timeout(
        connect=5.0,
        read=settings.request_timeout,
        write=5.0,
        pool=5.0,
    )

    try:
        # Shared HTTP client
        app.state.http_client = httpx.AsyncClient(
            timeout=timeout,
        )

        logger.info("Shared AsyncClient initialized.")

        # Shared Qdrant client
        app.state.qdrant_client = AsyncQdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        logger.info("Shared AsyncQdrantClient initialized.")

        # Ensure collections exist
        store = QdrantStore(app.state.qdrant_client)

        for collection in ALL_COLLECTIONS:
            await store.ensure_collection(collection)

        logger.info("Qdrant collections verified.")

        yield

    finally:
        logger.info("Closing shared AsyncClient...")
        await app.state.http_client.aclose()

        logger.info("Closing shared AsyncQdrantClient...")
        await app.state.qdrant_client.close()

        logger.info("AI Knowledge Base stopped.")