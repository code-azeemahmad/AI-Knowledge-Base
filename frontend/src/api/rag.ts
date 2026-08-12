import { request } from './client';
import { RAGRequest, RAGResponse, StreamEvent } from '../types/rag';
import { parseSSEReadableStream } from '../services/sse';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function askQuestion(payload: RAGRequest): Promise<RAGResponse> {
  return request<RAGResponse>('/rag/ask', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function streamQuestion(
  payload: RAGRequest,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal
): Promise<void> {
  const url = `${API_BASE_URL}/rag/stream`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
    signal,
  });

  if (!response.ok) {
    let errorText = '';
    try {
      errorText = await response.text();
    } catch {
      errorText = response.statusText;
    }
    throw new Error(`Streaming failed (${response.status}): ${errorText}`);
  }

  if (!response.body) {
    throw new Error('Response body is missing or unreadable stream.');
  }

  await parseSSEReadableStream(response.body, onEvent, signal);
}
