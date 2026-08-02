from app.core.dependencies import get_retriever
from app.retrieval.retriever import Retriever
from app.schemas.search import SearchResult
from fastapi import APIRouter, Depends, Query

router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.get(
    "",
    response_model=list[SearchResult],
)
async def retrieve(
    question: str = Query(...),
    limit: int = Query(default=5, ge=1, le=20),
    retriever: Retriever = Depends(get_retriever),  # noqa: B008
) -> list[SearchResult]:
    return await retriever.retrieve(
        question=question,
        limit=limit,
    )