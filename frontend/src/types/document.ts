export interface IndexingResponse {
  document_id: string;
  filename: string;
  chunks_indexed: number;
}

export interface CreateDocumentRequest {
  text: string;
  source: string;
}

export interface CreateDocumentResponse {
  message: string;
}

export interface DeleteDocumentResponse {
  message: string;
}

export interface IndexedDocumentMeta {
  document_id: string;
  filename: string;
  chunks_indexed: number;
  uploaded_at: string;
}
