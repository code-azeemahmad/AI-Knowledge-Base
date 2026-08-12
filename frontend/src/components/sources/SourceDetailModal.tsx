import React from 'react';
import { SearchResult } from '../../types/search';
import { Modal } from '../ui/Modal';
import { Badge } from '../ui/Badge';

interface SourceDetailModalProps {
  source: SearchResult | null;
  isOpen: boolean;
  onClose: () => void;
}

export const SourceDetailModal: React.FC<SourceDetailModalProps> = ({
  source,
  isOpen,
  onClose,
}) => {
  if (!source) return null;

  const filename = String(source.payload.filename || source.payload.source || 'Document');
  const chunkIndex = source.payload.chunk_index !== undefined ? source.payload.chunk_index : 'N/A';

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Source Chunk Details — ${filename}`} maxWidth="lg">
      <div className="space-y-4">
        {/* Metadata Bar */}
        <div className="flex flex-wrap items-center gap-2 pb-3 border-b border-slate-100">
          <Badge variant="blue">Filename: {filename}</Badge>
          <Badge variant="neutral">Chunk: {chunkIndex}</Badge>
          <Badge variant="success">Relevance Score: {typeof source.score === 'number' ? source.score.toFixed(4) : 'N/A'}</Badge>
          {source.id && <Badge variant="neutral">ID: {String(source.id).slice(0, 8)}...</Badge>}
        </div>

        {/* Full Text Snippet */}
        <div>
          <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
            Extracted Chunk Text
          </h4>
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs font-mono text-slate-800 whitespace-pre-wrap max-h-80 overflow-y-auto leading-relaxed">
            {source.payload.text}
          </div>
        </div>

        {/* Full Payload Metadata */}
        <div>
          <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
            Payload Metadata
          </h4>
          <pre className="bg-slate-900 text-slate-100 rounded-xl p-3 text-[11px] font-mono overflow-x-auto">
            {JSON.stringify(source.payload, null, 2)}
          </pre>
        </div>
      </div>
    </Modal>
  );
};
