from abc import ABC, abstractmethod


class TextChunker(ABC):
    """
    Base interface for text chunking strategies.
    """

    @abstractmethod
    def chunk(
        self,
        text: str,
    ) -> list[str]:
        ...