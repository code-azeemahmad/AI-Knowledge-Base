import { request } from './client';
import { IndexingResponse, CreateDocumentRequest, CreateDocumentResponse, DeleteDocumentResponse } from '../types/document';

export async function indexDocumentFile(file: File): Promise<IndexingResponse> {
  const formData = new FormData();
  formData.append('file', file);

  return request<IndexingResponse>('/api/v1/documents/index', {
    method: 'POST',
    body: formData,
  });
}

export async function createRawDocument(payload: CreateDocumentRequest): Promise<CreateDocumentResponse> {
  return request<CreateDocumentResponse>('/api/v1/documents', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function deleteDocument(documentId: string): Promise<DeleteDocumentResponse> {
  return request<DeleteDocumentResponse>(`/api/v1/documents/${documentId}`, {
    method: 'DELETE',
  });
}
