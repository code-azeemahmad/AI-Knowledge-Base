# backend\app\tokenizers\base.py
from abc import ABC, abstractmethod


class Tokenizer(ABC):
    """
    Converts text into tokens for sparse retrieval.
    """

    @abstractmethod
    def tokenize(
        self,
        text: str,
    ) -> list[str]:
        ...