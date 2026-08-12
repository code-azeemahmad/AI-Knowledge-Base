import React from 'react';
import { Modal } from '../ui/Modal';
import { UploadZone } from './UploadZone';
import { DocumentList } from './DocumentList';
import { IndexedDocumentMeta } from '../../types/document';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUpload: (file: File) => Promise<void>;
  isUploading: boolean;
  documents: IndexedDocumentMeta[];
  onDeleteDocument: (documentId: string) => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({
  isOpen,
  onClose,
  onUpload,
  isUploading,
  documents,
  onDeleteDocument,
}) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Knowledge Base Documents" maxWidth="lg">
      <div className="space-y-6">
        <div>
          <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
            Index New Document
          </h4>
          <UploadZone onUpload={onUpload} isUploading={isUploading} />
        </div>

        <div>
          <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
            Indexed Documents ({documents.length})
          </h4>
          <DocumentList documents={documents} onDelete={onDeleteDocument} />
        </div>
      </div>
    </Modal>
  );
};
