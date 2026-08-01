# backend\app\main.py
from app.core.dependencies import lifespan
from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Base",
    version="1.0.0",
    lifespan=lifespan,
)