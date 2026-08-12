import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Sparkles, Square } from 'lucide-react';

interface StreamingMessageProps {
  content: string;
  onStop: () => void;
}

export const StreamingMessage: React.FC<StreamingMessageProps> = ({ content, onStop }) => {
  return (
    <div className="flex items-start gap-3.5 mb-8">
      {/* Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5 animate-pulse">
        <Sparkles className="w-4 h-4" />
      </div>

      {/* Answer Container */}
      <div className="flex-1 min-w-0 max-w-3xl">
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-800">Knowledge Assistant</span>
            <div className="flex items-center gap-1 text-blue-600 text-xs">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse-dot-1" />
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse-dot-2" />
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse-dot-3" />
              <span className="text-[11px] font-medium text-slate-500 ml-1">Thinking & Generating...</span>
            </div>
          </div>

          <button
            onClick={onStop}
            className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-rose-600 bg-rose-50 border border-rose-200 hover:bg-rose-100 rounded-lg transition-colors"
            title="Stop generating"
          >
            <Square className="w-3 h-3 fill-current" />
            <span>Stop</span>
          </button>
        </div>

        <div className="prose prose-slate max-w-none text-sm leading-relaxed text-slate-800 bg-white border border-slate-200 p-4 rounded-2xl shadow-subtle min-h-[60px]">
          {content ? (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {content}
            </ReactMarkdown>
          ) : (
            <p className="text-xs text-slate-400 italic">Formulating grounded answer from retrieved context...</p>
          )}
        </div>
      </div>
    </div>
  );
};
