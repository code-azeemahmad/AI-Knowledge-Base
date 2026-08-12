from app.loaders.base import DocumentLoader


class TextLoader(DocumentLoader):
    """
    Extracts plain text from text-based files (.txt, .md, .json, .csv, .log).
    """

    async def load(
        self,
        file_path: str,
    ) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
