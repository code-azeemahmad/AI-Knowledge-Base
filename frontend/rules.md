# Manual RAG Frontend — Implementation Rules

## 1. Core Principles & Constraints

1. **Backend First**: Never modify working backend code or endpoints merely to make frontend development easier. Always conform to the existing FastAPI API contracts.
2. **No Fake Endpoints**: Never invent or fake API endpoints that do not exist in the backend.
3. **No Hardcoded URLs**: Never hardcode `http://localhost:8000` inside component files. Always use `import.meta.env.VITE_API_BASE_URL` or relative paths via Vite proxy.
4. **Decoupled API Logic**: Never make `fetch` calls directly inside UI components. All HTTP and SSE network logic must live inside `src/api/` and `src/services/`.
5. **Strict TypeScript Typing**: Use strict TypeScript interfaces for all backend requests, responses, SSE stream events, and UI props. No `any` types unless explicitly required for dynamic payloads.

---

## 2. Streaming & Interactivity Rules

6. **Non-Blocking Streaming**: Streaming updates must append text incrementally without freezing or blocking the user interface.
7. **Cancelable Generation**: The UI must provide a visible "Stop" button during active text generation. Clicking Stop must invoke `AbortController.abort()` and preserve the partial response.
8. **Disabled Duplicates**: Disable the submission button and `Enter` submit key while a response is streaming or pending.
9. **Conversation Persistence**: Maintain conversation history (`conversation_id` and messages) locally in state and sync with `localStorage` so refreshing the page does not lose chat history.

---

## 3. Visual & UI Rules

10. **Source Attribution**: Render retrieved sources separately underneath the AI answer. Display source filename, chunk index, text snippet, and exact relevance score (`Relevance score: 0.70`). Do not convert relevance scores into fake confidence percentages.
11. **Developer Debug View**: Place low-level technical information (evaluation metrics, full vector payload, raw JSON) inside a collapsible/toggleable "Developer Details" panel. Keep the main view focused on answer + sources.
12. **Light Mode Primary**: Follow the clean Google-app-inspired light mode visual design system defined in `design.md`.
13. **Markdown Rendering**: Render AI responses safely using `react-markdown` with syntax highlighting or clear code formatting.

---

## 4. Code Structure & Conventions

14. **Small Reusable Components**: Keep components small, focused, and reusable (`<Button />`, `<Card />`, `<Modal />`, `<Badge />`).
15. **Custom Hooks for State**: Encapsulate chat state, document upload state, and conversation state inside custom hooks (`useChat`, `useDocuments`, `useConversation`).
16. **Friendly Error Handling**: Catch network and SSE errors gracefully. Show friendly error banners (e.g., "Cannot connect to RAG server. Please ensure the backend is running.") instead of raw stack traces.
17. **Responsive Design**: Ensure full responsiveness across desktop, tablet, and mobile (collapsible sidebar / mobile navigation drawer).
