import React from 'react';
import { Menu, Database, Bug, Activity } from 'lucide-react';
import { Badge } from './ui/Badge';
import { Toggle } from './ui/Toggle';
import { Button } from './ui/Button';

interface HeaderProps {
  onToggleMobileSidebar: () => void;
  onOpenUploadModal: () => void;
  healthStatus: 'online' | 'offline' | 'checking';
  isDebugMode: boolean;
  onToggleDebugMode: (checked: boolean) => void;
  documentCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  onToggleMobileSidebar,
  onOpenUploadModal,
  healthStatus,
  isDebugMode,
  onToggleDebugMode,
  documentCount,
}) => {
  return (
    <header className="h-14 bg-white border-b border-slate-200 px-4 flex items-center justify-between shrink-0 z-20 shadow-subtle">
      {/* Left: Mobile Menu & App Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleMobileSidebar}
          className="md:hidden p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-colors"
          aria-label="Open navigation menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2">
          <h1 className="text-sm sm:text-base font-bold text-slate-900 tracking-tight">
            AI Knowledge Base
          </h1>
          <span className="hidden sm:inline-block text-xs text-slate-400 font-medium border-l border-slate-200 pl-2">
            Manual RAG Architecture
          </span>
        </div>
      </div>

      {/* Right: Health Badge, Document Upload Button, Debug Mode Toggle */}
      <div className="flex items-center gap-3">
        {/* Backend Status Indicator */}
        <div className="hidden sm:flex items-center gap-1.5">
          {healthStatus === 'online' && (
            <Badge variant="success" size="sm">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              RAG Server Online
            </Badge>
          )}
          {healthStatus === 'offline' && (
            <Badge variant="danger" size="sm">
              <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
              Backend Offline
            </Badge>
          )}
          {healthStatus === 'checking' && (
            <Badge variant="neutral" size="sm">
              <Activity className="w-3 h-3 animate-spin text-slate-400" />
              Connecting...
            </Badge>
          )}
        </div>

        {/* Upload Shortcut */}
        <Button
          variant="outline"
          size="sm"
          onClick={onOpenUploadModal}
          leftIcon={<Database className="w-3.5 h-3.5 text-blue-600" />}
          className="text-xs"
        >
          <span>Docs</span>
          <span className="ml-1 px-1.5 py-0.2 bg-slate-100 rounded-md font-mono text-[10px]">
            {documentCount}
          </span>
        </Button>

        {/* Debug Toggle */}
        <div className="flex items-center gap-1.5 pl-2 border-l border-slate-200">
          <Bug className={`w-3.5 h-3.5 ${isDebugMode ? 'text-blue-600' : 'text-slate-400'}`} />
          <Toggle checked={isDebugMode} onChange={onToggleDebugMode} label="Debug" />
        </div>
      </div>
    </header>
  );
};
