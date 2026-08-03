# app/exceptions/llm.py

from __future__ import annotations


class LLMError(Exception):
    """
    Base exception for all LLM provider errors.
    """


class LLMConnectionError(LLMError):
    """
    Raised when the provider cannot be reached.
    """


class LLMTimeoutError(LLMError):
    """
    Raised when a request to the provider times out.
    """


class LLMAuthenticationError(LLMError):
    """
    Raised when authentication with the provider fails.
    """


class LLMRateLimitError(LLMError):
    """
    Raised when the provider rejects the request due to rate limits.
    """


class LLMResponseError(LLMError):
    """
    Raised when the provider returns an unexpected or malformed response.
    """


class LLMProviderError(LLMError):
    """
    Raised for any other provider-side error.
    """
    
    
class UnsupportedProviderError(LLMError):
    """Raised when an unknown LLM provider is configured."""
    