# backend\app\core\config.py
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --------------------------------------------------
    # Application (Reused from AI Chat Assistant)
    # --------------------------------------------------

    app_name: str = "AI Knowledge Base"
    app_version: str = "1.0.0"
    debug: bool = True

    # --------------------------------------------------
    # Server (Reused from AI Chat Assistant)
    # --------------------------------------------------

    host: str = "127.0.0.1"
    port: int = 8000

    # --------------------------------------------------
    # LLM Provider (Reused from AI Chat Assistant)
    # --------------------------------------------------

    llm_provider: str = "ollama"

    # --------------------------------------------------
    # Ollama (Reused from AI Chat Assistant)
    # --------------------------------------------------

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"

    # --------------------------------------------------
    # Generation (Reused from AI Chat Assistant)
    # --------------------------------------------------

    request_timeout: int = 60
    max_tokens: int = 1024
    temperature: float = 0.7

    # --------------------------------------------------
    # Embeddings (New RAG Configuration)
    # --------------------------------------------------

    EMBEDDING_MODEL: str = "nomic-embed-text"
    EMBEDDING_DIMENSION: int = 768
    query_rewriter: str = "noop"

    # --------------------------------------------------
    # Qdrant (New RAG Configuration)
    # --------------------------------------------------

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    DEFAULT_COLLECTION: str = "documents"
    VECTOR_DISTANCE: str = "cosine"

    # --------------------------------------------------
    # Retrieval (New RAG Configuration)
    # --------------------------------------------------

    TOP_K: int = 5

    # --------------------------------------------------
    # Chunking (New RAG Configuration)
    # --------------------------------------------------

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()