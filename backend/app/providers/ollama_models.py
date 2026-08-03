# app/providers/ollama_models.py

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

# ---------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------


class OllamaMessage(BaseModel):
    """
    A single chat message in Ollama's format.
    """

    role: str
    content: str


class OllamaOptions(BaseModel):
    """
    Generation options supported by Ollama.
    """

    temperature: float
    num_predict: int


class OllamaChatRequest(BaseModel):
    """
    Request payload sent to POST /api/chat.
    """

    model: str
    messages: list[OllamaMessage]
    stream: bool = False
    options: OllamaOptions

    model_config = ConfigDict(extra="forbid")


# ---------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------


class OllamaResponseMessage(BaseModel):
    """
    Assistant message returned by Ollama.
    """

    role: str
    content: str

    model_config = ConfigDict(extra="ignore")


class OllamaChatResponse(BaseModel):
    """
    Response returned by POST /api/chat.

    Used for both:
    - Non-streaming responses
    - Streaming chunks
    """

    model: str

    created_at: str

    # Optional because the final streaming chunk may not contain a message.
    message: OllamaResponseMessage | None = None

    done: bool

    done_reason: str | None = None

    total_duration: int | None = None

    load_duration: int | None = None

    prompt_eval_count: int | None = None

    prompt_eval_duration: int | None = None

    eval_count: int | None = None

    eval_duration: int | None = None

    model_config = ConfigDict(extra="ignore")