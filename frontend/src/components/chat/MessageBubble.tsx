import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChatMessageItem } from '../../types/chat';
import { SourcePanel } from '../sources/SourcePanel';
import { PipelineDebugPanel } from '../debug/PipelineDebugPanel';
import { User, Sparkles, Copy, Check } from 'lucide-react';

interface MessageBubbleProps {
  message: ChatMessageItem;
  conversationId: string;
  isDebugMode: boolean;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  conversationId,
  isDebugMode,
}) => {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isUser) {
    return (
      <div className="flex items-start justify-end gap-3 mb-6">
        <div className="max-w-[85%] sm:max-w-[75%] bg-blue-50/80 border border-blue-100/80 text-blue-950 px-4 py-3 rounded-3xl rounded-tr-sm shadow-subtle text-sm leading-relaxed font-sans">
          {message.content}
        </div>
        <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0 text-xs font-semibold shadow-sm">
          <User className="w-4 h-4" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3.5 mb-8 group">
      {/* AI Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5">
        <Sparkles className="w-4 h-4" />
      </div>

      {/* Answer Container */}
      <div className="flex-1 min-w-0 max-w-3xl">
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <span className="text-xs font-semibold text-slate-800">Knowledge Assistant</span>
          <button
            onClick={handleCopy}
            className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-all flex items-center gap-1 text-[11px]"
            title="Copy answer"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>

        <div className="prose prose-slate max-w-none text-sm leading-relaxed text-slate-800 bg-white border border-slate-200/80 p-4 rounded-2xl shadow-subtle">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Source Attribution */}
        {message.sources && message.sources.length > 0 && (
          <SourcePanel sources={message.sources} />
        )}

        {/* Pipeline Debug Details */}
        {isDebugMode && (
          <PipelineDebugPanel
            evaluation={message.evaluation}
            conversationId={conversationId}
          />
        )}
      </div>
    </div>
  );
};
