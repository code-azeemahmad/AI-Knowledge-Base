import { useState, useEffect } from 'react';
import { ConversationSession, ChatMessageItem } from '../types/chat';
import { loadStoredConversations, saveStoredConversations } from '../services/storage';

export function useConversations() {
  const [conversations, setConversations] = useState<ConversationSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string>('');

  useEffect(() => {
    const loaded = loadStoredConversations();
    setConversations(loaded);
    if (loaded.length > 0) {
      setActiveSessionId(loaded[0].id);
    } else {
      createNewConversation();
    }
  }, []);

  const createNewConversation = (): string => {
    const newId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
    const newSession: ConversationSession = {
      id: newId,
      title: 'New Conversation',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      messages: [],
    };

    setConversations((prev) => {
      const updated = [newSession, ...prev];
      saveStoredConversations(updated);
      return updated;
    });
    setActiveSessionId(newId);
    return newId;
  };

  const updateSessionMessages = (sessionId: string, messages: ChatMessageItem[]) => {
    setConversations((prev) => {
      const updated = prev.map((sess) => {
        if (sess.id !== sessionId) return sess;

        // Auto-generate title from first user message
        let title = sess.title;
        if (title === 'New Conversation' && messages.length > 0) {
          const firstUserMsg = messages.find((m) => m.role === 'user');
          if (firstUserMsg) {
            title = firstUserMsg.content.slice(0, 32) + (firstUserMsg.content.length > 32 ? '...' : '');
          }
        }

        return {
          ...sess,
          title,
          messages,
          updatedAt: Date.now(),
        };
      });

      saveStoredConversations(updated);
      return updated;
    });
  };

  const deleteConversation = (sessionId: string, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    setConversations((prev) => {
      const updated = prev.filter((s) => s.id !== sessionId);
      saveStoredConversations(updated);

      if (sessionId === activeSessionId) {
        if (updated.length > 0) {
          setActiveSessionId(updated[0].id);
        } else {
          // Immediately create fresh empty session
          const freshId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
          const freshSession: ConversationSession = {
            id: freshId,
            title: 'New Conversation',
            createdAt: Date.now(),
            updatedAt: Date.now(),
            messages: [],
          };
          saveStoredConversations([freshSession]);
          setActiveSessionId(freshId);
          return [freshSession];
        }
      }
      return updated;
    });
  };

  const activeSession = conversations.find((s) => s.id === activeSessionId);

  return {
    conversations,
    activeSessionId,
    activeSession,
    setActiveSessionId,
    createNewConversation,
    updateSessionMessages,
    deleteConversation,
  };
}
