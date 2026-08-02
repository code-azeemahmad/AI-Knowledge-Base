# backend\app\main.py
from app.core.dependencies import lifespan
from app.routers.document import router as document_router
from app.routers.health import router as health_router
from app.routers.product import router as product_router
from app.routers.search import router as search_router
from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Base",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(search_router)   
app.include_router(document_router)
app.include_router(product_router)
app.include_router(health_router)   


@app.get("/", tags=["Root"])
async def root():
    return {
        "title": app.title,
        "version": app.version,
        "status": "running",
    }