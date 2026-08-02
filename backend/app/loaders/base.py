from abc import ABC, abstractmethod


class DocumentLoader(ABC):
    """
    Base interface for all document loaders.
    """

    @abstractmethod
    async def load(self, file_path: str) -> str:
        """
        Extract plain text from a document.
        """
        ...