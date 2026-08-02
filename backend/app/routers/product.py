from app.core.dependencies import get_product_service
from app.schemas.product import (
    CreateProductRequest,
    CreateProductResponse,
    DeleteProductResponse,
)
from app.services.product_service import ProductService
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=CreateProductResponse,
    status_code=201,
)
async def create_product(
    request: CreateProductRequest,
    service: ProductService = Depends(get_product_service),  # noqa: B008
) -> CreateProductResponse:
    return await service.create_product(request)


@router.delete(
    "/{product_id}",
    response_model=DeleteProductResponse,
)
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),  # noqa: B008
) -> DeleteProductResponse:
    return await service.delete_product(product_id)