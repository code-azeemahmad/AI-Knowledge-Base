# backend\app\retrieval\prompt_builder.py
from app.domain.chat import ChatRole
from app.schemas.search import SearchResult


class PromptBuilder:
    """
    Builds grounded prompts for Retrieval-Augmented Generation.
    """

    @staticmethod
    def build(
        history,
        question: str,
        context: list[SearchResult],
    ) -> str:

        history_text = ""

        if history:
            history_lines = []

            for message in history:
                role = (
                    "User"
                    if message.role == ChatRole.USER
                    else "Assistant"
                )

                history_lines.append(
                    f"{role}: {message.content}"
                )

            history_text = (
                "Conversation History\n"
                "--------------------\n"
                f"{chr(10).join(history_lines)}\n\n"
            )

        context_text = "\n\n".join(
            result.payload["text"]
            for result in context
        )

        return f"""You are a helpful AI assistant.

Answer ONLY using the retrieved context.

If the answer cannot be found in the retrieved context, reply:

"I don't have enough information in the provided documents."

Do not make up facts.

{history_text}Retrieved Context
-----------------
{context_text}

Current Question
----------------
{question}

Answer:
"""