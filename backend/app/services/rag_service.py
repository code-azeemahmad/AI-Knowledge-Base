from collections.abc import AsyncGenerator

from app.core.logging import logging
from app.domain.chat import ChatMessage, ChatRequest, ChatRole
from app.domain.stream import StreamEvent
from app.providers.base import LLMProvider
from app.retrieval.prompt_builder import PromptBuilder
from app.retrieval.retriever import Retriever
from app.schemas.rag import RAGResponse

logger = logging.getLogger(__name__)

class RAGService:

    def __init__(
        self,
        retriever: Retriever,
        llm_provider: LLMProvider,
    ):
        self.retriever = retriever
        self.llm_provider = llm_provider

    async def ask(
        self,
        question: str,
    ) -> RAGResponse:

        # Retrieve relevant context
        results = await self.retriever.retrieve(question)

        if not results:
            logger.info(f"No relevant context found for query: {question}")
            return RAGResponse(
                answer=(
                    "I couldn't find any relevant information "
                    "in the indexed documents."
                ),
                sources=[],
            )


        # Build the RAG prompt
        prompt = PromptBuilder.build(
            question=question,
            context=results,
        )

        # Generate the final answer
        response = await self.llm_provider.generate_response(
            ChatRequest(
                messages=[
                    ChatMessage(
                        role=ChatRole.USER,
                        content=prompt,
                    )
                ]
            )
        )

        return RAGResponse(
            answer=response.content,
            sources=results,
        )


    async def stream_ask(
        self,
        question: str,
    ) -> AsyncGenerator[StreamEvent, None]:

        # Retrieve relevant context
        results = await self.retriever.retrieve(question)

        # Build prompt
        prompt = PromptBuilder.build(
            question=question,
            context=results,
        )

        request = ChatRequest(
            messages=[
                ChatMessage(
                    role=ChatRole.USER,
                    content=prompt,
                )
            ]
        )

        async for event in self.llm_provider.stream_response(request):
            yield event