# AI Knowledge Base RAG Frontend — Design System Specification

## 1. Vision & Core Principles

The AI Knowledge Base frontend is a clean, modern, Google-app-inspired AI workspace. It prioritizes clarity, whitespace, vibrant subtle accents, and responsive readability over visual clutter or dark-mode developer dashboards.

### Principles:
- **Content & Conversation First**: The user question, AI response, and verified sources are the primary visual focus.
- **Subtle Elegance**: Use soft shadows, clean borders (`1px solid #E5E7EB`), light gray backgrounds (`#F9FAFB`), and generous padding.
- **Vibrant Accent Colors**: Inspired by modern Google productivity tools (Gemini, Drive, Search, AI Studio), using curated primary blues (`#1A73E8` / `#2563EB`), success greens (`#16A34A`), and warning ambers (`#D97706`).
- **Restrained Motion**: Micro-animations (150ms–200ms ease-out) for dropdowns, drawers, and streaming text; no distracting canvas or heavy hero animations.
- **Light Mode First**: Clean white/light surfaces tailored for high legibility during long research sessions.

---

## 2. Design Tokens

### 2.1 Color System
```css
:root {
  /* Surfaces */
  --bg-app: #f8fafc;
  --bg-surface: #ffffff;
  --bg-subtle: #f1f5f9;
  --bg-hover: #e2e8f0;
  
  /* Text */
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-inverse: #ffffff;
  
  /* Brand & Accents */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-500: #2563eb;
  --primary-600: #1d4ed8;
  --primary-700: #1e40af;
  
  /* Functional Colors */
  --success: #16a34a;
  --success-bg: #f0fdf4;
  --warning: #d97706;
  --warning-bg: #fffbeb;
  --danger: #dc2626;
  --danger-bg: #fef2f2;
  
  /* Borders & Shadows */
  --border-light: #e2e8f0;
  --border-focus: #3b82f6;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}
```

### 2.2 Typography
- **Font Family**: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif.
- **Headings**:
  - H1: `1.5rem` (`24px`), Weight: 600, Line-height: `1.3`
  - H2: `1.25rem` (`20px`), Weight: 600, Line-height: `1.35`
  - H3: `1rem` (`16px`), Weight: 600, Line-height: `1.4`
- **Body**:
  - Regular: `0.9375rem` (`15px`), Weight: 400, Line-height: `1.6`
  - Small: `0.8125rem` (`13px`), Weight: 400, Line-height: `1.5`
  - Micro/Badge: `0.75rem` (`12px`), Weight: 500, Line-height: `1.4`

### 2.3 Spacing & Radius
- **Spacing Scale**: 4px, 8px, 12px, 16px, 24px, 32px, 48px.
- **Border Radius**:
  - Small (Badges, buttons): `6px` / `8px`
  - Medium (Cards, inputs): `12px`
  - Large (Bubbles, Modals): `16px`
  - Pill (Pill buttons, Search bar): `9999px`

---

## 3. Component Specs

### 3.1 Header & Sidebar
- **Header**: Height `56px`, white surface with subtle bottom border. Displays app title, backend status badge (Green online / Red offline), and mobile menu button.
- **Sidebar**: Width `260px` desktop. Holds "New Chat" pill button, list of recent conversations, and indexed document list badge.

### 3.2 Chat Experience
- **User Bubble**: Right-aligned or subtle background, soft primary tint (`#EFF6FF`), dark text (`#1E3A8A`), radius `16px`.
- **AI Answer Container**: Left-aligned, transparent/white background with clean Markdown rendering (headers, lists, inline code blocks).
- **Chat Input Bar**: Rounded pill-style container (`border-radius: 24px`) with shadow-md, textarea expanding up to 120px, submit button (vibrant blue circle with arrow icon), and Stop button when generation is streaming.

### 3.3 Source Attribution Cards
- Positioned directly under AI responses.
- Header: "Retrieved Sources (N)" with expand/collapse toggle.
- Source Card:
  - Filename tag + Chunk index (e.g., `rag_sample_5pages.pdf • Chunk 0`).
  - Relevance metric: `Relevance score: 0.70` (formatted as decimal, not fake percentage).
  - Text preview snippet with line-clamp.
  - "View Chunk" modal/drawer toggle for full context inspect.

### 3.4 Document Upload UI
- Clean Drag-and-Drop zone with subtle dashed border (`#CBD5E1`).
- Icon + "Click or drag PDF/txt file to index".
- Upload status: Progress spinner -> Success badge with document ID and chunk count (`6 chunks indexed`).

### 3.5 Developer / Debug View
- Collapsible "RAG Pipeline Details" panel at bottom of answer.
- Displays Query Rewriting result, Hybrid Retrieval hit count, MMR filtering status, and optional Evaluation metrics (`recall_at_k`, `mrr`) when available.

---

## 4. States & Accessibility

- **Empty State**: Friendly greeting ("Ask your knowledge base"), 3 quick clickable example questions.
- **Loading / Streaming**: Animated inline pulse dots (`● ● ●`) while waiting for first token; smooth text append during SSE stream.
- **Error State**: Non-intrusive alert toast or banner with human-readable guidance (e.g., "Cannot connect to RAG server. Ensure backend is running on port 8000").
- **Accessibility**: Full keyboard navigation (`Tab`, `Enter`, `Escape`), focus ring (`2px solid #2563EB`), ARIA live regions for streaming content.
