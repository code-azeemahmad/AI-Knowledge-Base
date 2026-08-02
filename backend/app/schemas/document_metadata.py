from datetime import datetime

from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    chunks: int
    uploaded_at: datetime