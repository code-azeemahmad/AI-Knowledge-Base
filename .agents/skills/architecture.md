# Manual RAG Frontend — Architecture

## 1. Objective

Build the frontend for the existing Manual RAG backend.

The backend already implements a complete manually engineered RAG pipeline.

The frontend must consume the existing APIs.

Do NOT redesign or rewrite the backend.

Do NOT duplicate RAG logic inside the frontend.

The frontend is responsible for:

- UI
- User interaction
- API communication
- Streaming rendering
- Conversation state
- Source visualization
- Upload interaction
- Error/loading states

---

# 2. Existing Manual RAG Architecture

The backend pipeline is:

```text
Documents
   │
   ▼
Extraction
   │
   ▼
Chunking
   │
   ▼
Embeddings
   │
   ▼
Qdrant
   │
   ▼
Dense Retrieval
   │
   ├──── BM25 / Sparse Retrieval
   │
   └──── Hybrid Search
            │
            ▼
       Query Rewriting
            │
            ▼
           MMR
            │
            ▼
        Reranking
            │
            ▼
      Context Building
            │
            ▼
           LLM
            │
            ▼
        Streaming
            │
            ▼
       Conversation
          Memory
            │
            ▼
        RAG Answer
            │
            ▼
       RAG Evaluation