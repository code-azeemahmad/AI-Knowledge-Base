import fitz
from app.loaders.base import DocumentLoader


class PDFLoader(DocumentLoader):
    """
    Extracts plain text from PDF documents.
    """

    async def load(
        self,
        file_path: str,
    ) -> str:
        document = fitz.open(file_path)

        try:
            pages: list[str] = []

            for page in document:
                pages.append(page.get_text())

            return "\n".join(pages)

        finally:
            document.close()