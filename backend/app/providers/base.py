# backend/app/providers/base.py
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from app.domain.chat import ChatRequest, ChatResponse
from app.domain.stream import StreamEvent


class LLMProvider(ABC):

    @abstractmethod
    async def generate_response(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Generate a response from the language model.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def stream_response(
        self,
        request: ChatRequest,
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Stream the model response incrementally.

        Yields:
            StreamEvent:
                A provider-independent stream event.

        Notes:
            - Implementations should yield TEXT events as chunks
              become available.
            - A final DONE event should be yielded when generation
              completes successfully.
            - Provider-specific protocols (SSE, HTTP chunks, etc.)
              must be translated into StreamEvent objects before
              being yielded.
        """
        raise NotImplementedError