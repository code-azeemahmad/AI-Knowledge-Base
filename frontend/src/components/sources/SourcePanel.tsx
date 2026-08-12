import React, { useState } from 'react';
import { SearchResult } from '../../types/search';
import { SourceCard } from './SourceCard';
import { SourceDetailModal } from './SourceDetailModal';
import { BookOpen, ChevronDown, ChevronUp } from 'lucide-react';

interface SourcePanelProps {
  sources: SearchResult[];
}

export const SourcePanel: React.FC<SourcePanelProps> = ({ sources }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [selectedSource, setSelectedSource] = useState<SearchResult | null>(null);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-100">
      <div className="flex items-center justify-between mb-2">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-700 hover:text-blue-600 transition-colors"
        >
          <BookOpen className="w-3.5 h-3.5 text-blue-600" />
          <span>Retrieved Sources ({sources.length})</span>
          {isExpanded ? (
            <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
          ) : (
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          )}
        </button>
      </div>

      {isExpanded && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
          {sources.map((source, idx) => (
            <SourceCard
              key={source.id || idx}
              source={source}
              index={idx}
              onSelect={(src) => setSelectedSource(src)}
            />
          ))}
        </div>
      )}

      <SourceDetailModal
        source={selectedSource}
        isOpen={Boolean(selectedSource)}
        onClose={() => setSelectedSource(null)}
      />
    </div>
  );
};
