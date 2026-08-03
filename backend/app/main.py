# backend\app\main.py
import app.core.logging
from app.core.config import settings
from app.core.lifespan import lifespan
from app.routers.document import router as document_router
from app.routers.health import router as health_router
from app.routers.product import router as product_router
from app.routers.rag import router as rag_router
from app.routers.retrieval import router as retrieval_router
from app.routers.search import router as search_router
from fastapi import FastAPI

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(search_router)
app.include_router(rag_router)
app.include_router(document_router)
app.include_router(product_router)
app.include_router(health_router)   
app.include_router(retrieval_router)   


@app.get("/", tags=["Root"])
async def root():
    return {
        "title": app.title,
        "version": app.version,
        "status": "running",
    }