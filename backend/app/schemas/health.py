from pydantic import BaseModel


class ServiceStatus(BaseModel):
    qdrant: str
    embedding_provider: str


class HealthResponse(BaseModel):
    status: str
    services: ServiceStatus