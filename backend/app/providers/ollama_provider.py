# app/providers/ollama_provider.py

from __future__ import annotations

import json
from collections.abc import AsyncGenerator

import httpx
from app.core.config import settings
from app.domain.chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    TokenUsage,
)
from app.domain.stream import (
    StreamEvent,
    StreamEventType,
)
from app.exceptions.llm import (
    LLMAuthenticationError,
    LLMConnectionError,
    LLMProviderError,
    LLMRateLimitError,
    LLMResponseError,
    LLMTimeoutError,
)
from app.providers.base import LLMProvider
from app.providers.ollama_models import (
    OllamaChatRequest,
    OllamaChatResponse,
    OllamaMessage,
    OllamaOptions,
)
from pydantic import ValidationError


class OllamaProvider(LLMProvider):
    """
    Concrete implementation of the LLMProvider interface for Ollama.
    """

    _CHAT_ENDPOINT = "/api/chat"

    def __init__(
        self,
        client: httpx.AsyncClient,
    ) -> None:
        self._client = client

        self._timeout = httpx.Timeout(
            connect=5.0,
            read=settings.request_timeout,
            write=5.0,
            pool=5.0,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate_response(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Generate a complete response from Ollama.
        """

        payload = self._build_payload(request)

        response = await self._send_request(payload)

        return self._to_domain_response(response)

    async def stream_response(
        self,
        request: ChatRequest,
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Stream a response from Ollama.
        """

        payload = self._build_payload(
            request,
            stream=True,
        )

        async for chunk in self._send_stream_request(payload):

            # Final metadata chunk
            if chunk.done:

                yield StreamEvent(
                    type=StreamEventType.DONE,
                    usage=self._build_token_usage(chunk),
                    finish_reason=chunk.done_reason,
                )

                return

            event = self._to_stream_event(chunk)

            if event is not None:
                yield event

    # ------------------------------------------------------------------
    # Payload
    # ------------------------------------------------------------------

    def _build_payload(
        self,
        request: ChatRequest,
        *,
        stream: bool = False,
    ) -> OllamaChatRequest:
        """
        Build an Ollama request payload from the domain request.
        """

        return OllamaChatRequest(
            model=settings.ollama_model,
            stream=stream,
            messages=[
                self._to_ollama_message(message)
                for message in request.messages
            ],
            options=OllamaOptions(
                temperature=request.temperature,
                num_predict=request.max_tokens,
            ),
        )
        

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    async def _send_request(
        self,
        payload: OllamaChatRequest,
    ) -> OllamaChatResponse:
        """
        Send a non-streaming request to Ollama.
        """

        try:

            response = await self._client.post(
                url=f"{settings.ollama_base_url}{self._CHAT_ENDPOINT}",
                json=payload.model_dump(),
                timeout=self._timeout,
            )

            response.raise_for_status()

            return OllamaChatResponse.model_validate(
                response.json()
            )

        except httpx.ConnectError as exc:
            raise LLMConnectionError(
                "Unable to connect to Ollama."
            ) from exc

        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(
                "Request to Ollama timed out."
            ) from exc

        except httpx.HTTPStatusError as exc:
            self._raise_http_error(exc)

        except ValidationError as exc:
            raise LLMResponseError(
                "Invalid response received from Ollama."
            ) from exc

        except json.JSONDecodeError as exc:
            raise LLMResponseError(
                "Invalid JSON received from Ollama."
            ) from exc

    async def _send_stream_request(
        self,
        payload: OllamaChatRequest,
    ) -> AsyncGenerator[OllamaChatResponse, None]:
        """
        Send a streaming request to Ollama and yield validated chunks.
        """

        try:

            async with self._client.stream(
                method="POST",
                url=f"{settings.ollama_base_url}{self._CHAT_ENDPOINT}",
                json=payload.model_dump(),
                timeout=self._timeout,
            ) as response:

                response.raise_for_status()

                async for line in response.aiter_lines():

                    if not line:
                        continue

                    yield self._validate_stream_chunk(
                        line
                    )

        except httpx.ConnectError as exc:
            raise LLMConnectionError(
                "Unable to connect to Ollama."
            ) from exc

        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(
                "Request to Ollama timed out."
            ) from exc

        except httpx.HTTPStatusError as exc:
            self._raise_http_error(exc)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_stream_chunk(
        line: str,
    ) -> OllamaChatResponse:
        """
        Validate a streamed JSON chunk from Ollama.
        """

        try:

            return OllamaChatResponse.model_validate(
                json.loads(line)
            )

        except json.JSONDecodeError as exc:
            raise LLMResponseError(
                "Invalid JSON received from Ollama stream."
            ) from exc

        except ValidationError as exc:
            raise LLMResponseError(
                "Invalid streaming response received from Ollama."
            ) from exc

    # ------------------------------------------------------------------
    # Error Handling
    # ------------------------------------------------------------------

    @staticmethod
    def _raise_http_error(
        exc: httpx.HTTPStatusError,
    ) -> None:
        """
        Convert HTTP errors into domain-specific exceptions.
        """

        status = exc.response.status_code

        if status == 401:
            raise LLMAuthenticationError(
                "Authentication failed."
            ) from exc

        if status == 429:
            raise LLMRateLimitError(
                "Rate limit exceeded."
            ) from exc

        raise LLMProviderError(
            f"Ollama returned HTTP {status}."
        ) from exc
        
        
    # ------------------------------------------------------------------
    # Domain Conversion
    # ------------------------------------------------------------------

    def _to_domain_response(
        self,
        response: OllamaChatResponse,
    ) -> ChatResponse:
        """
        Convert an Ollama response into the application's
        provider-agnostic ChatResponse.
        """

        return ChatResponse(
            content=response.message.content,
            usage=self._build_token_usage(response),
            finish_reason=response.done_reason,
        )

    @staticmethod
    def _to_stream_event(
        chunk: OllamaChatResponse,
    ) -> StreamEvent | None:
        """
        Convert a streamed Ollama chunk into a StreamEvent.
        """

        if chunk.message is None:
            return None

        if not chunk.message.content:
            return None

        return StreamEvent(
            type=StreamEventType.TEXT,
            content=chunk.message.content,
        )

    # ------------------------------------------------------------------
    # Shared Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_token_usage(
        response: OllamaChatResponse,
    ) -> TokenUsage | None:
        """
        Build domain token usage from an Ollama response.

        Works for both normal responses and the final
        streaming metadata chunk.
        """

        if (
            response.prompt_eval_count is None
            or response.eval_count is None
        ):
            return None

        return TokenUsage(
            prompt_tokens=response.prompt_eval_count,
            completion_tokens=response.eval_count,
            total_tokens=(
                response.prompt_eval_count
                + response.eval_count
            ),
        )

    @staticmethod
    def _to_ollama_message(
        message: ChatMessage,
    ) -> OllamaMessage:
        """
        Convert a domain ChatMessage into an OllamaMessage.
        """

        return OllamaMessage(
            role=message.role.value,
            content=message.content,
        )