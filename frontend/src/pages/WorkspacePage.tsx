import React, { useState, useEffect } from 'react';
import { Header } from '../components/Header';
import { Sidebar } from '../components/conversation/Sidebar';
import { MessageList } from '../components/chat/MessageList';
import { MessageInput } from '../components/chat/MessageInput';
import { UploadModal } from '../components/documents/UploadModal';
import { useConversations } from '../hooks/useConversations';
import { useDocuments } from '../hooks/useDocuments';
import { useHealth } from '../hooks/useHealth';
import { useChat } from '../hooks/useChat';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const WorkspacePage: React.FC = () => {
  const healthStatus = useHealth();
  const { documents, isUploading, uploadDocument, removeDocument } = useDocuments();
  const {
    conversations,
    activeSessionId,
    activeSession,
    setActiveSessionId,
    createNewConversation,
    updateSessionMessages,
    deleteConversation,
  } = useConversations();

  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isDebugMode, setIsDebugMode] = useState(false);

  const {
    messages,
    setMessages,
    streamingContent,
    isStreaming,
    isPending,
    error,
    sendMessage,
    stopStreaming,
  } = useChat({
    conversationId: activeSessionId,
    initialMessages: activeSession?.messages || [],
    onMessagesChange: updateSessionMessages,
  });

  // Sync chat messages state whenever active conversation session changes
  useEffect(() => {
    if (activeSession) {
      setMessages(activeSession.messages);
    } else {
      setMessages([]);
    }
  }, [activeSessionId, activeSession, setMessages]);

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-slate-50 text-slate-900 font-sans">
      {/* Top Header */}
      <Header
        onToggleMobileSidebar={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
        onOpenUploadModal={() => setIsUploadModalOpen(true)}
        healthStatus={healthStatus}
        isDebugMode={isDebugMode}
        onToggleDebugMode={setIsDebugMode}
        documentCount={documents.length}
      />

      {/* Main Container */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          conversations={conversations}
          activeConversationId={activeSessionId}
          onSelectConversation={(s) => setActiveSessionId(s.id)}
          onNewConversation={createNewConversation}
          onDeleteConversation={deleteConversation}
          onOpenUploadModal={() => setIsUploadModalOpen(true)}
          documents={documents}
          isOpenMobile={isMobileSidebarOpen}
          onCloseMobile={() => setIsMobileSidebarOpen(false)}
        />

        {/* Central Chat Viewport */}
        <main className="flex-1 flex flex-col h-full overflow-hidden bg-white relative">
          {/* Server Offline Alert Banner */}
          {healthStatus === 'offline' && (
            <div className="bg-rose-50 border-b border-rose-200 px-4 py-2 flex items-center justify-between text-xs text-rose-800">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>
                  <strong>Backend Unavailable:</strong> Could not connect to FastAPI RAG server. Make sure it is running on <code>http://localhost:8000</code>.
                </span>
              </div>
              <Button variant="ghost" size="sm" onClick={() => window.location.reload()} className="text-rose-700 hover:bg-rose-100">
                <RefreshCw className="w-3 h-3 mr-1" /> Retry
              </Button>
            </div>
          )}

          {/* Error Banner */}
          {error && (
            <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 flex items-center justify-between text-xs text-amber-900">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Messages Stream & Output */}
          <MessageList
            messages={messages}
            streamingContent={streamingContent}
            isStreaming={isStreaming}
            onStopStreaming={stopStreaming}
            onSelectPrompt={(prompt) => sendMessage(prompt, true)}
            conversationId={activeSessionId}
            isDebugMode={isDebugMode}
          />

          {/* Floating Input Dock */}
          <MessageInput
            onSendMessage={(q, stream) => sendMessage(q, stream)}
            onStop={stopStreaming}
            isStreaming={isStreaming}
            isPending={isPending}
          />
        </main>
      </div>

      {/* Upload Modal */}
      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onUpload={uploadDocument}
        isUploading={isUploading}
        documents={documents}
        onDeleteDocument={removeDocument}
      />
    </div>
  );
};
