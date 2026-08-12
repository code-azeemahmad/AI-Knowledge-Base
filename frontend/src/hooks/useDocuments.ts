import { useState, useEffect } from 'react';
import { IndexedDocumentMeta } from '../types/document';
import { indexDocumentFile, deleteDocument as apiDeleteDocument } from '../api/documents';
import { loadStoredDocuments, saveStoredDocuments } from '../services/storage';

export function useDocuments() {
  const [documents, setDocuments] = useState<IndexedDocumentMeta[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    setDocuments(loadStoredDocuments());
  }, []);

  const uploadDocument = async (file: File) => {
    setIsUploading(true);
    try {
      const res = await indexDocumentFile(file);

      const newMeta: IndexedDocumentMeta = {
        document_id: res.document_id,
        filename: res.filename,
        chunks_indexed: res.chunks_indexed,
        uploaded_at: new Date().toISOString(),
      };

      setDocuments((prev) => {
        // Prevent duplicate filename entries
        const filtered = prev.filter((d) => d.filename !== res.filename);
        const updated = [newMeta, ...filtered];
        saveStoredDocuments(updated);
        return updated;
      });
    } finally {
      setIsUploading(false);
    }
  };

  const removeDocument = async (documentId: string) => {
    try {
      await apiDeleteDocument(documentId);
    } catch (err) {
      console.warn('Backend delete document failed or unneeded:', err);
    }
    setDocuments((prev) => {
      const updated = prev.filter((d) => d.document_id !== documentId);
      saveStoredDocuments(updated);
      return updated;
    });
  };

  return {
    documents,
    isUploading,
    uploadDocument,
    removeDocument,
  };
}
