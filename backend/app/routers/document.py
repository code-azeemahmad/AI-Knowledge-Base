from app.core.dependencies import get_document_service
from app.schemas.document import (
    CreateDocumentRequest,
    CreateDocumentResponse,
    DeleteDocumentResponse,
)
from app.schemas.upload import UploadResponse
from app.services.document_service import DocumentService
from fastapi import APIRouter, Depends, File, UploadFile

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


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),  # noqa: B008
    service: DocumentService = Depends(get_document_service),  # noqa: B008
) -> UploadResponse:
    return await service.upload_document(file)