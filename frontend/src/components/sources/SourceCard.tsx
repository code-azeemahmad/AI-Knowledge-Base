import React from 'react';
import { SearchResult } from '../../types/search';
import { FileText, ChevronRight } from 'lucide-react';
import { Badge } from '../ui/Badge';

interface SourceCardProps {
  source: SearchResult;
  index: number;
  onSelect: (source: SearchResult) => void;
}

export const SourceCard: React.FC<SourceCardProps> = ({ source, index, onSelect }) => {
  const filename = String(source.payload.filename || source.payload.source || 'Document Chunk');
  const chunkIndex = source.payload.chunk_index !== undefined ? source.payload.chunk_index : index;
  const scoreFormatted = typeof source.score === 'number' ? source.score.toFixed(2) : 'N/A';

  return (
    <div
      onClick={() => onSelect(source)}
      className="group relative bg-white rounded-xl border border-slate-200 p-3 hover:border-blue-300 hover:shadow-subtle cursor-pointer transition-all duration-150 flex flex-col justify-between gap-2"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <div className="p-1.5 rounded-lg bg-blue-50 text-blue-600 shrink-0">
            <FileText className="w-4 h-4" />
          </div>
          <div className="min-w-0">
            <h4 className="text-xs font-semibold text-slate-800 truncate group-hover:text-blue-600 transition-colors">
              {filename}
            </h4>
            <p className="text-[11px] text-slate-500 font-mono">Chunk {chunkIndex}</p>
          </div>
        </div>

        <Badge variant="blue" size="sm">
          Relevance: {scoreFormatted}
        </Badge>
      </div>

      <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed font-sans bg-slate-50 p-2 rounded-lg border border-slate-100">
        "{source.payload.text}"
      </p>

      <div className="flex items-center justify-end text-[11px] font-medium text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity">
        <span>View details</span>
        <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
      </div>
    </div>
  );
};
