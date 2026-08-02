from qdrant_client import AsyncQdrantClient

from app.schemas.health import (
    HealthResponse,
    ServiceStatus,
)


class HealthService:

    def __init__(
        self,
        qdrant_client: AsyncQdrantClient,
    ):
        self.qdrant_client = qdrant_client

    async def check(self) -> HealthResponse:
        """
        Verify application dependencies.
        """

        try:
            await self.qdrant_client.get_collections()
            qdrant_status = "up"
        except Exception:  # noqa: BLE001
            qdrant_status = "down"

        # We'll replace this placeholder in Phase 13 with an actual
        # embedding provider health check.
        embedding_status = "up"

        overall = "healthy" if qdrant_status == "up" else "unhealthy"

        return HealthResponse(
            status=overall,
            services=ServiceStatus(
                qdrant=qdrant_status,
                embedding_provider=embedding_status,
            ),
        )
