from app.loaders.base import DocumentLoader


class DocxLoader(DocumentLoader):
    """
    Extracts plain text from Microsoft Word (.docx) documents.
    """

    async def load(
        self,
        file_path: str,
    ) -> str:
        try:
            import docx

            doc = docx.Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)
        except ImportError:
            # Fallback if python-docx is not installed
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
