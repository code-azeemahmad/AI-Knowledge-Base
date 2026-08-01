# backend\app\schemas\embedding.py
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: list[float]
    

class OllamaEmbeddingResponse(BaseModel):
    model: str
    embeddings: list[list[float]]