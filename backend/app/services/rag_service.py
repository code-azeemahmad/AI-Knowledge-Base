# backend\app\services\rag_service.py
from collections.abc import AsyncGenerator

from app.core.logging import logging
from app.domain.chat import ChatMessage, ChatRequest, ChatRole
from app.domain.stream import StreamEvent, StreamEventType
from app.evaluations.dataset import EVALUATION_DATASET
from app.evaluations.retrieval_evaluator import RetrievalEvaluator
from app.providers.base import LLMProvider
from app.query_rewriters.base import QueryRewriter
from app.rerankers.base import Reranker
from app.retrieval.base import BaseRetriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.prompt_builder import PromptBuilder
from app.schemas.rag import RAGRequest, RAGResponse
from app.services.conversation_service import ConversationService

logger = logging.getLogger(__name__)


class RAGService:

    def __init__(
        self,
        retriever: BaseRetriever,
        llm_provider: LLMProvider,
        reranker: Reranker,
        conversation_service: ConversationService,
        query_rewriter: QueryRewriter,
    ):
        self.retriever = retriever
        self.llm_provider = llm_provider
        self.reranker = reranker
        self.conversation_service = conversation_service
        self.query_rewriter = query_rewriter

    async def ask(
        self,
        request: RAGRequest,
    ) -> RAGResponse:

        # Load conversation history
        history = await self.conversation_service.get_messages(
            request.conversation_id,
        )

        # Save user message
        await self.conversation_service.append_message(
            request.conversation_id,
            ChatMessage(
                role=ChatRole.USER,
                content=request.question,
            ),
        )

        # Retrieve relevant chunks
        rewritten_question = await self.query_rewriter.rewrite(
            question=request.question,
            history=history,
        )

        results = await self.retriever.retrieve(
            question=rewritten_question,
            document_id=request.document_id,
        )

        # Re-rank chunks
        results = await self.reranker.rerank(
            query=rewritten_question,
            results=results,
            top_k=5,
        )

        if not results:
            logger.info(
                f"No relevant context found for query: {request.question}"
            )

            return RAGResponse(
                answer=(
                    "I couldn't find any relevant information "
                    "in the indexed documents."
                ),
                sources=[],
            )

        # Build prompt
        prompt = PromptBuilder.build(
            history=history,
            context=results,
            question=request.question,
        )

        # Generate response
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

        # Save assistant message
        await self.conversation_service.append_message(
            request.conversation_id,
            ChatMessage(
                role=ChatRole.ASSISTANT,
                content=response.content,
            ),
        )

        # --- Inline RAG evaluation ---
        evaluation_metrics: dict | None = None
        try:
            user_q = request.question.strip().lower()
            rewritten_q = rewritten_question.strip().lower()
            
            matched_sample = next(
                (
                    s for s in EVALUATION_DATASET
                    if s.question.strip().lower() == user_q
                    or s.question.strip().lower() == rewritten_q
                    or s.question.lower() in user_q
                    or user_q in s.question.lower()
                    or s.question.lower() in rewritten_q
                    or rewritten_q in s.question.lower()
                ),
                None,
            )
            if matched_sample:
                eval_result = RetrievalEvaluator.evaluate(
                    results=results,
                    sample=matched_sample,
                    k=5,
                )
                evaluation_metrics = (
                    eval_result if isinstance(eval_result, dict) else eval_result.to_dict()
                )
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"RAG evaluation failed: {exc}")

        return RAGResponse(
            answer=response.content,
            sources=results,
            evaluation=evaluation_metrics,
        )

    async def stream_ask(
        self,
        request: RAGRequest,
    ) -> AsyncGenerator[StreamEvent, None]:

        # Load conversation history
        history = await self.conversation_service.get_messages(
            request.conversation_id,
        )

        # Save user message
        await self.conversation_service.append_message(
            request.conversation_id,
            ChatMessage(
                role=ChatRole.USER,
                content=request.question,
            ),
        )

        # Retrieve relevant chunks
        rewritten_question = await self.query_rewriter.rewrite(
            question=request.question,
            history=history,
        )

        results = await self.retriever.retrieve(
            question=rewritten_question,
            document_id=request.document_id,
        )

        # Re-rank retrieved chunks
        results = await self.reranker.rerank(
            query=rewritten_question,
            results=results,
            top_k=5,
        )

        if not results:
            logger.info(
                f"No relevant context found for query: {request.question}"
            )

            yield StreamEvent(
                type=StreamEventType.TEXT,
                content=(
                    "I couldn't find any relevant information "
                    "in the indexed documents."
                ),
            )
            return

        # Emit sources event to stream subscribers
        yield StreamEvent(
            type=StreamEventType.SOURCES,
            sources=[r.model_dump() for r in results],
        )

        # Build prompt
        prompt = PromptBuilder.build(
            history=history,
            context=results,
            question=request.question,
        )

        chat_request = ChatRequest(
            messages=[
                ChatMessage(
                    role=ChatRole.USER,
                    content=prompt,
                )
            ]
        )

        parts: list[str] = []

        # Stream response
        async for event in self.llm_provider.stream_response(chat_request):

            if event.type == "text":
                parts.append(event.content)

            yield event

        # Save assistant message
        await self.conversation_service.append_message(
            request.conversation_id,
            ChatMessage(
                role=ChatRole.ASSISTANT,
                content="".join(parts),
            ),
        )