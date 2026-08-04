from app.core.dependencies import get_rag_service
from app.schemas.rag import RAGRequest, RAGResponse
from app.serializers.sse import (
    sse_event_generator,
)
from app.services.rag_service import RAGService
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/ask",
    response_model=RAGResponse,
)
async def ask(
    request: RAGRequest,
    service: RAGService = Depends(get_rag_service),  # noqa: B008
) -> RAGResponse:

    return await service.ask(question=request.question, document_id=request.document_id)


@router.post("/stream")
async def stream(
    request: RAGRequest,
    service: RAGService = Depends(get_rag_service),  # noqa: B008
):

    generator = service.stream_ask(
        question=request.question,
        document_id=request.document_id,
    )

    return StreamingResponse(
        sse_event_generator(generator),
        media_type="text/event-stream",
    )