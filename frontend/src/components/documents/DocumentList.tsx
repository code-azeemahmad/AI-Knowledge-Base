import React from 'react';
import { IndexedDocumentMeta } from '../../types/document';
import { FileText, Layers, Trash2 } from 'lucide-react';
import { Badge } from '../ui/Badge';

interface DocumentListProps {
  documents: IndexedDocumentMeta[];
  onDelete?: (documentId: string) => void;
}

export const DocumentList: React.FC<DocumentListProps> = ({ documents, onDelete }) => {
  if (!documents || documents.length === 0) {
    return (
      <div className="p-4 text-center border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
        <p className="text-xs text-slate-500">No documents indexed yet.</p>
        <p className="text-[11px] text-slate-400 mt-0.5">Upload a document to enable grounded RAG search.</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {documents.map((doc) => (
        <div
          key={doc.document_id}
          className="group flex items-center justify-between p-2.5 bg-white border border-slate-200 rounded-xl hover:border-blue-200 transition-all text-xs"
        >
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="p-1.5 rounded-lg bg-blue-50 text-blue-600 shrink-0">
              <FileText className="w-4 h-4" />
            </div>
            <div className="min-w-0">
              <h5 className="font-semibold text-slate-800 truncate" title={doc.filename}>
                {doc.filename}
              </h5>
              <div className="flex items-center gap-2 text-[11px] text-slate-500 mt-0.5">
                <span className="flex items-center gap-1">
                  <Layers className="w-3 h-3 text-slate-400" />
                  {doc.chunks_indexed} {doc.chunks_indexed === 1 ? 'chunk' : 'chunks'}
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <Badge variant="blue" size="sm">
              Indexed
            </Badge>
            {onDelete && (
              <button
                onClick={() => onDelete(doc.document_id)}
                className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-all"
                title="Remove document reference"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
