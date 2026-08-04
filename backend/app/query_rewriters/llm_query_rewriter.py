# backend\app\query_rewriters\llm_query_rewriter.py
from textwrap import dedent

from app.domain.chat import (
    ChatMessage,
    ChatRequest,
    ChatRole,
)
from app.providers.base import LLMProvider
from app.query_rewriters.base import QueryRewriter


class LLMQueryRewriter(QueryRewriter):

    def __init__(
        self,
        llm_provider: LLMProvider,
    ):
        self.llm_provider = llm_provider

    async def rewrite(
        self,
        question: str,
        history: list[ChatMessage],
    ) -> str:    

        history_text = "\n".join(
            f"{message.role.value}: {message.content}"
            for message in history
        )

        prompt = dedent(
            f"""
        You rewrite follow-up questions into standalone search queries.

        Conversation:

        {history_text}

        Latest Question:

        {question}

        You are rewriting the latest user question for semantic search.

        Rules:
        - Resolve pronouns such as "it", "they", "that", and "this" using the conversation history.
        - Preserve the user's intent.
        - Do not answer the question.
        - Do not add explanations.
        - Return exactly one standalone search query.

        Do not explain anything.
        """
        ).strip()

        request = ChatRequest(
            messages=[
                ChatMessage(
                    role=ChatRole.USER,
                    content=prompt,
                )
            ]
        )

        response = await self.llm_provider.generate_response(
            request
        )

        return response.content.strip()