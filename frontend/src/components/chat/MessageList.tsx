import React, { useRef, useEffect } from 'react';
import { ChatMessageItem } from '../../types/chat';
import { MessageBubble } from './MessageBubble';
import { StreamingMessage } from './StreamingMessage';
import { EmptyState } from './EmptyState';

interface MessageListProps {
  messages: ChatMessageItem[];
  streamingContent: string;
  isStreaming: boolean;
  onStopStreaming: () => void;
  onSelectPrompt: (prompt: string) => void;
  conversationId: string;
  isDebugMode: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  streamingContent,
  isStreaming,
  onStopStreaming,
  onSelectPrompt,
  conversationId,
  isDebugMode,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingContent, isStreaming]);

  if (messages.length === 0 && !isStreaming) {
    return <EmptyState onSelectPrompt={onSelectPrompt} />;
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 max-w-4xl mx-auto w-full">
      {messages.map((msg) => (
        <MessageBubble
          key={msg.id}
          message={msg}
          conversationId={conversationId}
          isDebugMode={isDebugMode}
        />
      ))}

      {isStreaming && (
        <StreamingMessage
          content={streamingContent}
          onStop={onStopStreaming}
        />
      )}

      <div ref={bottomRef} />
    </div>
  );
};
