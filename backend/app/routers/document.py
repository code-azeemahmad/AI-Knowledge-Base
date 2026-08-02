from app.core.dependencies import get_document_service
from app.schemas.document import (
    CreateDocumentRequest,
    CreateDocumentResponse,
    DeleteDocumentResponse,
)
from app.services.document_service import DocumentService
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=CreateDocumentResponse,
    status_code=201,
)
async def create_document(
    request: CreateDocumentRequest,
    service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> CreateDocumentResponse:
    return await service.create_document(request)


@router.delete(
    "/{document_id}",
    response_model=DeleteDocumentResponse,
)
async def delete_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> DeleteDocumentResponse:
    return await service.delete_document(document_id)
