from pydantic import BaseModel


class CreateDocumentRequest(BaseModel):
    text: str
    source: str


class CreateDocumentResponse(BaseModel):
    message: str
    

class DeleteDocumentResponse(BaseModel):
    message: str