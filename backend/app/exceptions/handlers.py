# app/exceptions/handlers.py
from __future__ import annotations

from app.exceptions import (
    LLMAuthenticationError,
    LLMConnectionError,
    LLMError,
    LLMProviderError,
    LLMRateLimitError,
    LLMTimeoutError,
    UnsupportedProviderError,
)
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

# Map each custom exception class to its HTTP status code
EXCEPTION_STATUS_MAP = {
    UnsupportedProviderError: status.HTTP_400_BAD_REQUEST,
    LLMAuthenticationError: status.HTTP_401_UNAUTHORIZED,
    LLMRateLimitError: status.HTTP_429_TOO_MANY_REQUESTS,
    LLMProviderError: status.HTTP_502_BAD_GATEWAY,
    LLMConnectionError: status.HTTP_503_SERVICE_UNAVAILABLE,
    LLMTimeoutError: status.HTTP_504_GATEWAY_TIMEOUT,
}


async def llm_exception_handler(request: Request, exc: LLMError) -> JSONResponse:
    """Unified handler for all LLM-related exceptions."""
    status_code = EXCEPTION_STATUS_MAP.get(
        type(exc), 
        status.HTTP_500_INTERNAL_SERVER_ERROR  # Fallback safety
    )
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc),
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers with FastAPI."""
    app.add_exception_handler(LLMError, llm_exception_handler)