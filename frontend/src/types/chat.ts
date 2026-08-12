import { SearchResult } from './search';
import { TokenUsage } from './rag';

export type Role = 'user' | 'assistant';

export interface ChatMessageItem {
  id: string;
  role: Role;
  content: string;
  timestamp: number;
  sources?: SearchResult[];
  evaluation?: Record<string, number> | null;
  usage?: TokenUsage | null;
  isStreaming?: boolean;
}

export interface ConversationSession {
  id: string;
  title: string;
  createdAt: number;
  updatedAt: number;
  messages: ChatMessageItem[];
}
