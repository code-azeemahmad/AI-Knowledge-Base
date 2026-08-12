# Manual RAG Frontend — Design Specification

## 1. Project Goal

Build a minimal, modern frontend for the existing Manual RAG backend.

The frontend should provide a clean interface for:

- Asking questions against the RAG knowledge base
- Viewing streamed LLM responses
- Viewing retrieved sources
- Viewing source metadata
- Uploading documents
- Seeing upload/indexing status
- Maintaining conversation context
- Starting a new conversation

The frontend must feel like a polished Google application rather than a typical developer dashboard.

Design inspiration:

- Google Gemini
- Google Search
- Google Drive
- Google AI Studio

Do NOT copy any existing product exactly.

The design should be minimal, spacious, vibrant, friendly, and highly usable.

---

# 2. Visual Direction

## Overall Style

Use:

- Minimal UI
- Vibrant Google-inspired colors
- Large whitespace
- Rounded corners
- Soft borders
- Subtle shadows
- Clean typography
- Lightweight animations
- Clear visual hierarchy

Avoid:

- Heavy dashboards
- Excessive cards
- Dense tables
- Dark enterprise-admin styling
- Excessive gradients
- Excessive icons
- Unnecessary animations
- Overloaded navigation

The application should feel like an AI workspace.

---

# 3. Color Direction

Use a Google-inspired palette.

Primary colors can include:

- Google Blue
- Google Red
- Google Yellow
- Google Green

Use these colors sparingly.

The main interface should remain mostly neutral/white.

Suggested concept:

- Background: very light neutral
- Primary action: blue
- Success: green
- Warning: yellow/orange
- Error: red
- Accent: subtle multicolor gradient where appropriate

Do not make the entire interface colorful.

Color should guide attention.

---

# 4. Typography

Use a clean modern sans-serif font.

Preferred:

- Inter
- Google Sans
- system sans-serif fallback

Typography hierarchy:

## Page title

Large and confident.

## Section title

Medium weight.

## Body

Comfortable reading size.

## Metadata

Small and muted.

Do not use excessive font weights.

---

# 5. Main Application Layout

Use a simple three-area architecture.

```text
┌──────────────────────────────────────────────────────────┐
│                    Top Navigation                        │
├───────────────┬──────────────────────────┬───────────────┤
│               │                          │               │
│  Conversations│       Chat Area          │   Sources     │
│               │                          │               │
│               │                          │               │
│               │                          │               │
│               │                          │               │
│               │                          │               │
│               │                          │               │
├───────────────┴──────────────────────────┴───────────────┤
│                     Message Input                        │
└──────────────────────────────────────────────────────────┘

on smaller screens
┌───────────────────────────────┐
│          Header               │
├───────────────────────────────┤
│                               │
│          Chat                 │
│                               │
│                               │
├───────────────────────────────┤
│       Message Input           │
└───────────────────────────────┘