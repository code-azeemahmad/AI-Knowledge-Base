from fastapi import APIRouter, Depends

from app.core.dependencies import get_health_service
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
)
async def health(
    service: HealthService = Depends(get_health_service),  # noqa: B008
) -> HealthResponse:
    return await service.check()