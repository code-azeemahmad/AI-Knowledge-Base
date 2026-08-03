# app/mappers/mapper.py
from __future__ import annotations

from app.domain.chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
)
from app.schemas.chat import (
    ChatRequestSchema,
    ChatResponseSchema,
    TokenUsageSchema,
)


class ChatMapper:
    """
    Maps between API schemas and domain models.

    Responsibilities:
    - Schema -> Domain
    - Domain -> Schema

    This class must not contain business logic.
    """

    @staticmethod
    def to_domain(request: ChatRequestSchema) -> ChatRequest:
        """
        Convert an API request schema into a domain request.
        """

        messages = [
            ChatMessage(
                role=message.role,
                content=message.content,
            )
            for message in request.messages
        ]

        return ChatRequest(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

    @staticmethod
    def to_schema(response: ChatResponse) -> ChatResponseSchema:
        """
        Convert a domain response into an API response schema.
        """

        usage = None

        if response.usage is not None:
            usage = TokenUsageSchema(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

        return ChatResponseSchema(
            content=response.content,
            usage=usage,
            finish_reason=response.finish_reason,
        )