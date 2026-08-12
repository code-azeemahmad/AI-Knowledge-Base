export interface SearchResultPayload {
  document_id?: string;
  filename?: string;
  chunk_index?: number;
  text: string;
  [key: string]: unknown;
}

export interface SearchResult {
  id: string;
  score: number;
  payload: SearchResultPayload;
}

export interface SearchFilter {
  document_id?: string | null;
}

export interface SearchRequest {
  query: string;
  limit?: number;
}

export interface SearchResponse {
  results: SearchResult[];
}
