# backend\app\conversations\memory_store.py
from collections import defaultdict

from app.conversations.base import ConversationStore
from app.domain.chat import ChatMessage


class InMemoryConversationStore(ConversationStore):

    def __init__(self):
        self._conversations = defaultdict(list)

    async def get_messages(
        self,
        conversation_id: str,
    ) -> list[ChatMessage]:
        return list(self._conversations[conversation_id])

    async def append_message(
        self,
        conversation_id: str,
        message: ChatMessage,
    ) -> None:
        self._conversations[conversation_id].append(message)

    async def clear(
        self,
        conversation_id: str,
    ) -> None:
        self._conversations.pop(conversation_id, None)