import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Square, Zap } from 'lucide-react';

interface MessageInputProps {
  onSendMessage: (question: string, useStreaming: boolean) => void;
  onStop: () => void;
  isStreaming: boolean;
  isPending: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  onStop,
  isStreaming,
  isPending,
}) => {
  const [input, setInput] = useState('');
  const [useStreaming, setUseStreaming] = useState(true);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 140)}px`;
    }
  }, [input]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isStreaming || isPending) return;

    onSendMessage(trimmed, useStreaming);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative max-w-3xl mx-auto w-full px-4 mb-4">
      <div className="relative flex flex-col bg-white border border-slate-300 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 rounded-3xl shadow-floating transition-all p-2">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your indexed documents..."
          rows={1}
          disabled={isStreaming || isPending}
          className="w-full px-3 py-2 text-sm text-slate-800 placeholder-slate-400 bg-transparent resize-none focus:outline-none max-h-36 disabled:opacity-60"
        />

        <div className="flex items-center justify-between pt-1 px-2 border-t border-slate-100/80">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setUseStreaming(!useStreaming)}
              className={`inline-flex items-center gap-1 text-xs px-2 py-1 rounded-lg border transition-colors ${
                useStreaming
                  ? 'bg-blue-50 text-blue-700 border-blue-200 font-medium'
                  : 'bg-slate-50 text-slate-500 border-slate-200'
              }`}
              title="Toggle real-time SSE streaming responses"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>{useStreaming ? 'Streaming On' : 'Standard POST'}</span>
            </button>
          </div>

          <div className="flex items-center gap-2">
            {isStreaming ? (
              <button
                type="button"
                onClick={onStop}
                className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-rose-600 hover:bg-rose-700 text-white transition-colors shadow-sm"
                title="Stop generation"
              >
                <Square className="w-3.5 h-3.5 fill-current" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={!input.trim() || isPending}
                className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-sm"
                title="Send message"
              >
                <ArrowUp className="w-4 h-4 stroke-[2.5]" />
              </button>
            )}
          </div>
        </div>
      </div>
      <p className="text-[11px] text-center text-slate-400 mt-1.5 font-sans">
        AI Knowledge Base uses ground context retrieval. Answers are generated from indexed sources.
      </p>
    </form>
  );
};
