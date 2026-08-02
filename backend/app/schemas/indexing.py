from pydantic import BaseModel


class IndexingResponse(BaseModel):
    document_id: str
    filename: str
    chunks_indexed: int
    