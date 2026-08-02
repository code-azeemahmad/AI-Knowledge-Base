# backend\app\core\config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # Embeddings / Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    
    EMBEDDING_DIMENSION: int
    DEFAULT_COLLECTION: str
    VECTOR_DISTANCE: str
    
    # Pydantic v2 Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignores any extra unknown keys in .env instead of throwing an error
    )


settings = Settings()
