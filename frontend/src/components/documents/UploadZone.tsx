import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, AlertCircle } from 'lucide-react';
import { Spinner } from '../ui/Spinner';

interface UploadZoneProps {
  onUpload: (file: File) => Promise<void>;
  isUploading: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onUpload, isUploading }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    try {
      await onUpload(file);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Document indexing failed');
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFileChange(file);
  };

  return (
    <div className="space-y-3">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !isUploading && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all duration-200 ${
          isDragOver
            ? 'border-blue-500 bg-blue-50/60'
            : 'border-slate-300 hover:border-slate-400 bg-slate-50/50 hover:bg-slate-50'
        } ${isUploading ? 'pointer-events-none opacity-60' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt,.md,.doc,.docx"
          className="hidden"
          onChange={(e) => handleFileChange(e.target.files?.[0])}
        />

        <div className="flex flex-col items-center gap-2">
          {isUploading ? (
            <div className="p-3 bg-blue-100 rounded-full text-blue-600">
              <Spinner size="lg" />
            </div>
          ) : (
            <div className="p-3 bg-blue-50 text-blue-600 rounded-2xl shadow-subtle">
              <UploadCloud className="w-6 h-6" />
            </div>
          )}

          <div>
            <h4 className="text-sm font-semibold text-slate-800">
              {isUploading ? 'Parsing & Indexing Document...' : 'Upload Document to Knowledge Base'}
            </h4>
            <p className="text-xs text-slate-500 mt-1">
              Drag and drop PDF, TXT, or Markdown file, or click to browse
            </p>
          </div>

          <div className="flex items-center gap-2 text-[11px] text-slate-400 mt-1">
            <FileText className="w-3.5 h-3.5" />
            <span>Automatic Chunking & Vector Store Indexing</span>
          </div>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 text-xs text-rose-600 bg-rose-50 border border-rose-200 p-3 rounded-xl">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
