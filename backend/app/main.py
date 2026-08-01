# backend\app\main.py
from app.core.dependencies import lifespan
from app.routers.search import router as search_router
from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Base",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(search_router)