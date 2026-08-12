# Manual RAG Frontend — Architecture Specification

## 1. Overview & Objectives

The frontend is a modular, feature-oriented React + TypeScript application built using Vite. It connects directly to the FastAPI backend, implementing real-time SSE (Server-Sent Events) streaming, document upload/indexing, conversation persistence, and source attribution visualization.

---

## 2. Directory Structure

```text
frontend/
├── public/
├── src/
│   ├── api/                  # Backend API clients & endpoint definitions
│   │   ├── client.ts         # Base fetch wrapper with base URL & error handling
│   │   ├── rag.ts            # RAG endpoints (/rag/ask, /rag/stream)
│   │   ├── documents.ts      # Document endpoints (/api/v1/documents, /index)
│   │   └── health.ts         # Health check endpoint (/health)
│   │
│   ├── components/           # Reusable UI components
│   │   ├── ui/               # Primitive UI controls (Button, Input, Card, Modal, Spinner, Badge)
│   │   ├── chat/             # MessageBubble, MessageInput, StreamingMessage, EmptyState
│   │   ├── sources/          # SourcePanel, SourceCard, SourceDetailModal
│   │   ├── documents/        # UploadZone, DocumentList, UploadModal
│   │   ├── conversation/     # Sidebar, ConversationItem
│   │   └── debug/            # PipelineDebugPanel, EvaluationMetricsCard
│   │
│   ├── features/             # Feature modules & custom hooks
│   │   ├── chat/             # useChat state & streaming logic
│   │   ├── documents/        # useDocuments indexing & document state
│   │   └── conversation/     # useConversation history management
│   │
│   ├── services/             # Low-level services (Streaming SSE reader, LocalStorage)
│   │   ├── sse.ts            # ReadableStream SSE parser
│   │   └── storage.ts        # Client-side persistence for conversations & docs
│   │
│   ├── types/                # Strict TypeScript contracts matching FastAPI backend
│   │   ├── api.ts            # Shared API response wrappers & error types
│   │   ├── rag.ts            # RAGRequest, RAGResponse, StreamEvent
│   │   ├── search.ts         # SearchResult, SearchFilter
│   │   ├── document.ts       # IndexingResponse, CreateDocumentResponse
│   │   └── health.ts         # HealthResponse
│   │
│   ├── pages/                # App pages (Main Workspace page)
│   │   └── WorkspacePage.tsx
│   │
│   ├── App.tsx               # Main entry component with Layout
│   ├── main.tsx              # React DOM mounting
│   └── index.css             # Tailwind CSS & global design tokens
│
├── package.json
├── tsconfig.json
├── vite.config.ts
├── design.md
├── architecture.md
└── rules.md
```

---

## 3. Data Flow & State Management

### 3.1 Streaming SSE Data Flow
```text
User Submits Question
        │
        ▼
useChat.sendMessage()
        │
        ├──── Generate/Reuse conversation_id
        ├──── Append User Message to local state
        ├──── Create AbortController
        │
        ▼
api/rag.ts -> streamAsk() (fetch POST /rag/stream)
        │
        ▼
services/sse.ts -> parseSSEReadableStream()
        │
        ├──── Emits StreamEvent { type: "text", content: "..." }
        │       └──── Incrementally updates assistant message buffer
        │
        └──── Emits StreamEvent { type: "done", content: "..." }
                └──── Finalizes message, updates sources & token usage
```

### 3.2 Document Upload & Indexing Data Flow
```text
User Drops File in UploadZone
        │
        ▼
api/documents.ts -> indexDocument(file)
        │
        ▼
POST /api/v1/documents/index (multipart/form-data)
        │
        ▼
Receives IndexingResponse { document_id, filename, chunks_indexed }
        │
        ▼
Updates DocumentList state & persists to LocalStorage
```

---

## 4. API Contract Alignment

All types in `src/types/` strictly mirror the FastAPI Pydantic models:

- **`RAGRequest`**: `{ conversation_id: string, question: string, document_id?: string | null }`
- **`RAGResponse`**: `{ answer: string, sources: SearchResult[], evaluation?: Record<string, any> | null }`
- **`SearchResult`**: `{ id: string, score: number, payload: { document_id?: string, filename?: string, chunk_index?: number, text: string, [key: string]: any } }`
- **`StreamEvent`**: `{ type: 'text' | 'done', content: string, usage?: TokenUsage | null, finish_reason?: string | null }`
- **`IndexingResponse`**: `{ document_id: string, filename: string, chunks_indexed: number }`

---

## 5. Streaming & Abort Handling

- Uses `fetch` with `ReadableStream` reader in `src/services/sse.ts`.
- Exposes `stopGeneration()` from `useChat` hook, which triggers `abortController.abort()`.
- Aborting stops the SSE stream immediately, keeps all text received up to that instant, and releases UI lock.

---

## 6. Environment & Configuration

- `VITE_API_BASE_URL`: Base backend URL (defaults to `http://localhost:8000`).
- Configured in `src/api/client.ts` and Vite proxy in `vite.config.ts`.
