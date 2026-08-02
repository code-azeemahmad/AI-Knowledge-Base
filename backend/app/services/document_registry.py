from app.schemas.document_metadata import DocumentMetadata


class DocumentRegistry:

    def __init__(self):
        self._documents: dict[str, DocumentMetadata] = {}

    def add(
        self,
        metadata: DocumentMetadata,
    ) -> None:
        self._documents[metadata.document_id] = metadata

    def list(self) -> list[DocumentMetadata]:
        return list(self._documents.values())

    def get(
        self,
        document_id: str,
    ) -> DocumentMetadata | None:
        return self._documents.get(document_id)

    def delete(
        self,
        document_id: str,
    ) -> None:
        self._documents.pop(document_id, None)