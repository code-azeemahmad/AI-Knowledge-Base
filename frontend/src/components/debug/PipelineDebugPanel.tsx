import React, { useState } from 'react';
import { Terminal, ChevronDown, ChevronUp, Cpu, BarChart2 } from 'lucide-react';
import { Badge } from '../ui/Badge';

interface PipelineDebugPanelProps {
  evaluation?: Record<string, number> | null;
  conversationId: string;
}

export const PipelineDebugPanel: React.FC<PipelineDebugPanelProps> = ({
  evaluation,
  conversationId,
}) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="mt-3 text-xs border border-slate-200 rounded-xl bg-slate-50/80 overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-3.5 py-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100/60 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Terminal className="w-3.5 h-3.5 text-blue-600" />
          <span className="font-medium">RAG Pipeline Debug Details</span>
          {evaluation && (
            <Badge variant="blue" size="sm">
              Eval Active
            </Badge>
          )}
        </div>
        {isOpen ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </button>

      {isOpen && (
        <div className="p-3.5 border-t border-slate-200 space-y-3 bg-white">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1">
              <span className="text-[11px] text-slate-500 font-medium">Session Conversation ID</span>
              <p className="font-mono text-slate-800 bg-slate-100 px-2 py-1 rounded-md text-[11px] truncate">
                {conversationId}
              </p>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] text-slate-500 font-medium">Retrieval Strategy</span>
              <p className="font-mono text-slate-800 bg-slate-100 px-2 py-1 rounded-md text-[11px]">
                Hybrid (Dense + BM25) → MMR (λ=0.7) → CrossEncoder Rerank
              </p>
            </div>
          </div>

          {evaluation && (
            <div className="space-y-1.5 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-1.5 text-slate-700 font-semibold">
                <BarChart2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>RAG Retrieval Evaluation Metrics</span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {Object.entries(evaluation).map(([metric, val]) => (
                  <div key={metric} className="bg-emerald-50/60 border border-emerald-100 p-2 rounded-lg text-center">
                    <span className="block text-[10px] text-emerald-700 font-medium uppercase tracking-wider">
                      {metric.replace(/_/g, ' ')}
                    </span>
                    <span className="text-xs font-bold text-emerald-900 font-mono">
                      {typeof val === 'number' ? val.toFixed(4) : String(val)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center gap-2 text-[11px] text-slate-500 pt-1">
            <Cpu className="w-3 h-3 text-slate-400" />
            <span>Executed via Backend FastAPI `/rag/ask` or `/rag/stream`</span>
          </div>
        </div>
      )}
    </div>
  );
};
