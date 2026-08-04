from abc import ABC, abstractmethod

from app.domain.chat import ChatMessage


class ConversationStore(ABC):

    @abstractmethod
    async def get_messages(
        self,
        conversation_id: str,
    ) -> list[ChatMessage]:
        ...

    @abstractmethod
    async def append_message(
        self,
        conversation_id: str,
        message: ChatMessage,
    ) -> None:
        ...

    @abstractmethod
    async def clear(
        self,
        conversation_id: str,
    ) -> None:
        ...