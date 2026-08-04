# backend\app\query_rewriters\noop_query_rewriter.py
from app.domain.chat import ChatMessage
from app.query_rewriters.base import QueryRewriter


class NoOpQueryRewriter(QueryRewriter):

    async def rewrite(
        self,
        question: str,
        history: list[ChatMessage],
    ) -> str:
        if not history:
            return question
        """
        Return the original question unchanged.
        """
        return question