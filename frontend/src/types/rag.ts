import { SearchResult } from './search';

export interface RAGRequest {
  conversation_id: string;
  question: string;
  document_id?: string | null;
}

export interface RAGResponse {
  answer: string;
  sources: SearchResult[];
  evaluation?: Record<string, number> | null;
}

export type StreamEventType = 'text' | 'sources' | 'done';

export interface TokenUsage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface StreamEvent {
  type: StreamEventType;
  content: string;
  sources?: SearchResult[] | null;
  usage?: TokenUsage | null;
  finish_reason?: string | null;
}
