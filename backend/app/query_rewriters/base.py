# backend\app\query_rewriters\base.py
from abc import ABC, abstractmethod

from app.domain.chat import ChatMessage


class QueryRewriter(ABC):

    @abstractmethod
    async def rewrite(
        self,
        question: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Rewrite a user question into a standalone query
        suitable for semantic retrieval.
        """
        ...