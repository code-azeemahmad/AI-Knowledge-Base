from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    name: str
    description: str
    category: str


class CreateProductResponse(BaseModel):
    message: str


class DeleteProductResponse(BaseModel):
    message: str