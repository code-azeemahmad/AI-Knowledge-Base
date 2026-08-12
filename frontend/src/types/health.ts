export interface HealthResponse {
  status: string;
  qdrant?: string;
  timestamp?: string;
  [key: string]: unknown;
}
