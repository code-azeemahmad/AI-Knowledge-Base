import { request } from './client';
import { HealthResponse } from '../types/health';

export async function getHealthStatus(): Promise<HealthResponse> {
  return request<HealthResponse>('/health', {
    method: 'GET',
  });
}
