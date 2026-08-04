from app.chunking.base import TextChunker


class RecursiveChunker(TextChunker):
    """
    A simple recursive text chunker that tries progressively
    smaller separators to preserve semantic boundaries.
    """

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

        self.separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ]

    def chunk(self, text: str) -> list[str]:
        return self._split(text, self.separators)

    def _split(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:

        if len(text) <= self.chunk_size:
            return [text]

        separator = separators[0]

        if separator == "":
            return [
                text[i:i + self.chunk_size]
                for i in range(
                    0,
                    len(text),
                    self.chunk_size - self.chunk_overlap,
                )
            ]

        pieces = text.split(separator)

        chunks: list[str] = []
        current = ""

        for piece in pieces:
            candidate = (
                piece
                if not current
                else current + separator + piece
            )

            if len(candidate) <= self.chunk_size:
                current = candidate
            else:
                if current:
                    chunks.extend(
                        self._split(current, separators[1:])
                    )
                current = piece

        if current:
            chunks.extend(
                self._split(current, separators[1:])
            )

        return chunks