from app.schemas.search import SearchResult


class PromptBuilder:
    """
    Builds grounded prompts for Retrieval-Augmented Generation.
    """

    @staticmethod
    def build(
        question: str,
        context: list[SearchResult],
    ) -> str:

        context_text = "\n\n".join(result.payload["text"] for result in context)

        return f"""You are a helpful AI assistant.
Answer the user's question using ONLY the provided context.
If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."
Do not make up facts.
Context:
{context_text}
Question:
{question}
Answer:
"""


# Why This Prompt? It contains four important instructions:
# 1. Role
# 2. Grounding
# 3. Fallback
# 4. Context + Question
