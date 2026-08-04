# backend\app\services\conversation_service.py
from app.conversations.base import ConversationStore
from app.domain.chat import ChatMessage


class ConversationService:
    """
    Business logic for conversation history.
    """

    def __init__(
        self,
        store: ConversationStore,
    ):
        self.store = store

    async def get_messages(
        self,
        conversation_id: str,
    ) -> list[ChatMessage]:
        return await self.store.get_messages(
            conversation_id,
        )

    async def append_message(
        self,
        conversation_id: str,
        message: ChatMessage,
    ) -> None:
        await self.store.append_message(
            conversation_id,
            message,
        )

    async def clear(
        self,
        conversation_id: str,
    ) -> None:
        await self.store.clear(
            conversation_id,
        )