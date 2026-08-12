import React from 'react';
import { ConversationSession } from '../../types/chat';
import { MessageSquare, Trash2 } from 'lucide-react';

interface ConversationItemProps {
  session: ConversationSession;
  isActive: boolean;
  onSelect: (session: ConversationSession) => void;
  onDelete: (id: string, e: React.MouseEvent) => void;
}

export const ConversationItem: React.FC<ConversationItemProps> = ({
  session,
  isActive,
  onSelect,
  onDelete,
}) => {
  return (
    <div
      onClick={() => onSelect(session)}
      className={`group flex items-center justify-between px-3 py-2 rounded-xl text-xs cursor-pointer transition-all duration-150 ${
        isActive
          ? 'bg-blue-50 text-blue-700 font-medium shadow-subtle'
          : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
      }`}
    >
      <div className="flex items-center gap-2.5 min-w-0">
        <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />
        <span className="truncate">{session.title || 'Untitled Conversation'}</span>
      </div>

      <button
        onClick={(e) => onDelete(session.id, e)}
        className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-md transition-all"
        title="Delete conversation"
      >
        <Trash2 className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
