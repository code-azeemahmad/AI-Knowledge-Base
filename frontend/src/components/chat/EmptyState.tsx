import React from 'react';
import { Sparkles, MessageSquare, BookOpen, Search } from 'lucide-react';

interface EmptyStateProps {
  onSelectPrompt: (prompt: string) => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onSelectPrompt }) => {
  const examplePrompts = [
    {
      icon: <BookOpen className="w-4 h-4 text-blue-600" />,
      title: "What is RAG?",
      prompt: "What is Retrieval-Augmented Generation?",
    },
    {
      icon: <Search className="w-4 h-4 text-emerald-600" />,
      title: "Core Pipeline Modules",
      prompt: "What are the core components of a RAG pipeline?",
    },
    {
      icon: <MessageSquare className="w-4 h-4 text-amber-600" />,
      title: "Vector Search Mechanics",
      prompt: "How does vector search work in RAG?",
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] max-w-2xl mx-auto px-4 py-8 text-center">
      {/* Icon Badge */}
      <div className="w-14 h-14 rounded-3xl bg-gradient-to-tr from-blue-600 to-indigo-500 text-white flex items-center justify-center shadow-lg shadow-blue-500/20 mb-5">
        <Sparkles className="w-7 h-7" />
      </div>

      {/* Greeting */}
      <h2 className="text-2xl font-bold text-slate-900 tracking-tight mb-2">
        Ask your Knowledge Base
      </h2>
      <p className="text-sm text-slate-500 max-w-md leading-relaxed mb-8">
        Search indexed documents with hybrid vector retrieval, BM25 keyword matching, and reranked context.
      </p>

      {/* Example Suggestion Chips */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-xl">
        {examplePrompts.map((item, idx) => (
          <button
            key={idx}
            onClick={() => onSelectPrompt(item.prompt)}
            className="group flex flex-col items-start p-4 bg-white border border-slate-200 hover:border-blue-300 rounded-2xl shadow-subtle hover:shadow-md text-left transition-all duration-200"
          >
            <div className="p-2 rounded-xl bg-slate-50 group-hover:bg-blue-50 transition-colors mb-3">
              {item.icon}
            </div>
            <h4 className="text-xs font-semibold text-slate-800 group-hover:text-blue-600 transition-colors mb-1">
              {item.title}
            </h4>
            <p className="text-[11px] text-slate-500 line-clamp-2 leading-relaxed">
              "{item.prompt}"
            </p>
          </button>
        ))}
      </div>
    </div>
  );
};
