import { useState, useRef, useCallback } from 'react';
import { ChatMessageItem } from '../types/chat';
import { SearchResult } from '../types/search';
import { askQuestion, streamQuestion } from '../api/rag';
import { StreamEvent } from '../types/rag';

interface UseChatProps {
  conversationId: string;
  initialMessages?: ChatMessageItem[];
  onMessagesChange: (sessionId: string, messages: ChatMessageItem[]) => void;
}

export function useChat({
  conversationId,
  initialMessages = [],
  onMessagesChange,
}: UseChatProps) {
  const [messages, setMessages] = useState<ChatMessageItem[]>(initialMessages);
  const [streamingContent, setStreamingContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);

  const stopStreaming = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  }, []);

  const sendMessage = async (question: string, useStreaming: boolean = true) => {
    if (!question.trim()) return;

    setError(null);
    const userMsgId = `msg_u_${Date.now()}`;
    const userMsg: ChatMessageItem = {
      id: userMsgId,
      role: 'user',
      content: question,
      timestamp: Date.now(),
    };

    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    onMessagesChange(conversationId, newMessages);

    if (useStreaming) {
      setIsStreaming(true);
      setStreamingContent('');
      abortControllerRef.current = new AbortController();

      let currentText = '';
      let receivedSources: SearchResult[] = [];
      let receivedEval: Record<string, number> | null = null;

      try {
        await streamQuestion(
          {
            conversation_id: conversationId,
            question,
          },
          (event: StreamEvent) => {
            if (event.type === 'text' && event.content) {
              currentText += event.content;
              setStreamingContent(currentText);
            } else if (event.type === 'sources' && event.sources) {
              receivedSources = event.sources;
            }
          },
          abortControllerRef.current.signal
        );

        const assistantMsg: ChatMessageItem = {
          id: `msg_a_${Date.now()}`,
          role: 'assistant',
          content: currentText || 'Completed response.',
          timestamp: Date.now(),
          sources: receivedSources,
          evaluation: receivedEval,
        };

        const finalMessages = [...newMessages, assistantMsg];
        setMessages(finalMessages);
        onMessagesChange(conversationId, finalMessages);
      } catch (err: unknown) {
        if (err instanceof Error && err.name === 'AbortError') {
          // Aborted by user — save partial text
          if (currentText.trim()) {
            const partialMsg: ChatMessageItem = {
              id: `msg_a_aborted_${Date.now()}`,
              role: 'assistant',
              content: currentText + ' *(Generation stopped by user)*',
              timestamp: Date.now(),
            };
            const finalMessages = [...newMessages, partialMsg];
            setMessages(finalMessages);
            onMessagesChange(conversationId, finalMessages);
          }
        } else {
          const errText = err instanceof Error ? err.message : 'Connection to RAG server failed.';
          setError(errText);
        }
      } finally {
        setIsStreaming(false);
        setStreamingContent('');
        abortControllerRef.current = null;
      }
    } else {
      // Standard non-streaming POST /rag/ask
      setIsPending(true);
      try {
        const response = await askQuestion({
          conversation_id: conversationId,
          question,
        });

        const assistantMsg: ChatMessageItem = {
          id: `msg_a_${Date.now()}`,
          role: 'assistant',
          content: response.answer,
          timestamp: Date.now(),
          sources: response.sources || [],
          evaluation: response.evaluation || null,
        };

        const finalMessages = [...newMessages, assistantMsg];
        setMessages(finalMessages);
        onMessagesChange(conversationId, finalMessages);
      } catch (err: unknown) {
        const errText = err instanceof Error ? err.message : 'Failed to retrieve response from server.';
        setError(errText);
      } finally {
        setIsPending(false);
      }
    }
  };

  return {
    messages,
    setMessages,
    streamingContent,
    isStreaming,
    isPending,
    error,
    sendMessage,
    stopStreaming,
  };
}
