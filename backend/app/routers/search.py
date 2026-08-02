from fastapi import APIRouter, Depends

from app.core.dependencies import get_search_service
from app.schemas.search import (
    SearchRequest,
    SearchResponse,
)
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/api/v1/search",
    tags=["Search"],
)


@router.post(
    "",
    response_model=SearchResponse,
)
async def semantic_search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),  # noqa: B008
) -> SearchResponse:
    return await service.search(request)
