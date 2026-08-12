import React from 'react';
import { ConversationSession } from '../../types/chat';
import { IndexedDocumentMeta } from '../../types/document';
import { ConversationItem } from './ConversationItem';
import { Plus, Upload, Database, X, Sparkles } from 'lucide-react';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';

interface SidebarProps {
  conversations: ConversationSession[];
  activeConversationId: string;
  onSelectConversation: (session: ConversationSession) => void;
  onNewConversation: () => void;
  onDeleteConversation: (id: string, e: React.MouseEvent) => void;
  onOpenUploadModal: () => void;
  documents: IndexedDocumentMeta[];
  isOpenMobile: boolean;
  onCloseMobile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  onOpenUploadModal,
  documents,
  isOpenMobile,
  onCloseMobile,
}) => {
  const content = (
    <div className="flex flex-col h-full bg-slate-50/70 border-r border-slate-200 p-4">
      {/* Top Header / Branding */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-blue-600 text-white flex items-center justify-center shadow-sm">
            <Sparkles className="w-4 h-4" />
          </div>
          <span className="font-semibold text-sm text-slate-900">Knowledge Workspace</span>
        </div>

        {isOpenMobile && (
          <button
            onClick={onCloseMobile}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* New Chat Button */}
      <Button
        variant="primary"
        size="md"
        className="w-full justify-start shadow-subtle mb-4"
        leftIcon={<Plus className="w-4 h-4" />}
        onClick={() => {
          onNewConversation();
          if (isOpenMobile) onCloseMobile();
        }}
      >
        New Conversation
      </Button>

      {/* Conversations Section */}
      <div className="flex-1 overflow-y-auto space-y-1 pr-1 mb-4">
        <h4 className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-2 mb-2">
          Recent Chats
        </h4>

        {conversations.length === 0 ? (
          <p className="text-xs text-slate-400 px-2 italic">No conversations yet.</p>
        ) : (
          conversations.map((sess) => (
            <ConversationItem
              key={sess.id}
              session={sess}
              isActive={sess.id === activeConversationId}
              onSelect={(s) => {
                onSelectConversation(s);
                if (isOpenMobile) onCloseMobile();
              }}
              onDelete={onDeleteConversation}
            />
          ))
        )}
      </div>

      {/* Document Knowledge Base Card */}
      <div className="pt-3 border-t border-slate-200 bg-white p-3 rounded-2xl border border-slate-200 shadow-subtle">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-800">
            <Database className="w-3.5 h-3.5 text-blue-600" />
            <span>Indexed Documents</span>
          </div>
          <Badge variant="blue" size="sm">
            {documents.length}
          </Badge>
        </div>

        <p className="text-[11px] text-slate-500 mb-3 leading-snug">
          Upload PDFs or text files to retrieve grounded answers.
        </p>

        <Button
          variant="outline"
          size="sm"
          className="w-full text-xs"
          leftIcon={<Upload className="w-3.5 h-3.5 text-blue-600" />}
          onClick={onOpenUploadModal}
        >
          Manage & Upload
        </Button>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:block w-64 h-full shrink-0">
        {content}
      </aside>

      {/* Mobile Drawer Overlay */}
      {isOpenMobile && (
        <div className="fixed inset-0 z-40 md:hidden flex">
          <div
            className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs"
            onClick={onCloseMobile}
          />
          <div className="relative w-72 max-w-[80vw] h-full z-10">
            {content}
          </div>
        </div>
      )}
    </>
  );
};
