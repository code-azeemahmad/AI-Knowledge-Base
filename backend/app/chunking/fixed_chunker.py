from app.chunking.base import TextChunker


class FixedChunker(TextChunker):

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        text: str,
    ) -> list[str]:

        chunks: list[str] = []

        start = 0

        step = self.chunk_size - self.chunk_overlap

        while start < len(text):

            end = start + self.chunk_size

            chunks.append(
                text[start:end]
            )

            start += step

        return chunks