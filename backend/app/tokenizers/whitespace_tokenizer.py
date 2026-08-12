# backend\app\tokenizers\whitespace_tokenizer.py
import re

from app.tokenizers.base import Tokenizer


class WhitespaceTokenizer(Tokenizer):
    """
    A simple tokenizer for BM25.

    - Lowercases text
    - Removes most punctuation
    - Splits on whitespace
    """

    _pattern = re.compile(r"[^\w\s]")

    def tokenize(
        self,
        text: str,
    ) -> list[str]:

        normalized = self._pattern.sub(
            " ",
            text.lower(),
        )

        return normalized.split()