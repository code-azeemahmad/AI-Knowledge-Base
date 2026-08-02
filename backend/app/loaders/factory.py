from pathlib import Path

from app.loaders.base import DocumentLoader
from app.loaders.pdf_loader import PDFLoader


class LoaderFactory:
    """
    Returns the appropriate document loader
    based on the uploaded file extension.
    """

    _loaders: dict[str, type[DocumentLoader]] = {  # noqa: RUF012
        ".pdf": PDFLoader,
    }

    @classmethod
    def get_loader(
        cls,
        filename: str,
    ) -> DocumentLoader:

        extension = Path(filename).suffix.lower()

        loader_class = cls._loaders.get(extension)

        if loader_class is None:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return loader_class()