import { ConversationSession } from '../types/chat';
import { IndexedDocumentMeta } from '../types/document';

const CONVERSATIONS_KEY = 'manual_rag_conversations_v1';
const DOCUMENTS_KEY = 'manual_rag_documents_v1';

export function loadStoredConversations(): ConversationSession[] {
  try {
    const data = localStorage.getItem(CONVERSATIONS_KEY);
    return data ? JSON.parse(data) : [];
  } catch (err) {
    console.error('Failed to load conversations from localStorage:', err);
    return [];
  }
}

export function saveStoredConversations(conversations: ConversationSession[]): void {
  try {
    localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(conversations));
  } catch (err) {
    console.error('Failed to save conversations to localStorage:', err);
  }
}

export function loadStoredDocuments(): IndexedDocumentMeta[] {
  try {
    const data = localStorage.getItem(DOCUMENTS_KEY);
    return data ? JSON.parse(data) : [];
  } catch (err) {
    console.error('Failed to load documents from localStorage:', err);
    return [];
  }
}

export function saveStoredDocuments(documents: IndexedDocumentMeta[]): void {
  try {
    localStorage.setItem(DOCUMENTS_KEY, JSON.stringify(documents));
  } catch (err) {
    console.error('Failed to save documents to localStorage:', err);
  }
}
