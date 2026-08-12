frontend/
│
├── src/
│   │
│   ├── api/
│   │   ├── client.ts
│   │   ├── rag.ts
│   │   ├── documents.ts
│   │   └── conversations.ts
│   │
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── StreamingMessage.tsx
│   │   │
│   │   ├── sources/
│   │   │   ├── SourcePanel.tsx
│   │   │   ├── SourceCard.tsx
│   │   │   └── SourceDetails.tsx
│   │   │
│   │   ├── documents/
│   │   │   ├── UploadZone.tsx
│   │   │   ├── UploadProgress.tsx
│   │   │   └── UploadResult.tsx
│   │   │
│   │   ├── conversations/
│   │   │   ├── ConversationSidebar.tsx
│   │   │   └── ConversationItem.tsx
│   │   │
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Modal.tsx
│   │       ├── Drawer.tsx
│   │       └── Spinner.tsx
│   │
│   ├── hooks/
│   │   ├── useChat.ts
│   │   ├── useStreaming.ts
│   │   ├── useUpload.ts
│   │   └── useConversations.ts
│   │
│   ├── types/
│   │   ├── chat.ts
│   │   ├── rag.ts
│   │   ├── document.ts
│   │   └── source.ts
│   │
│   ├── pages/
│   │   └── ChatPage.tsx
│   │
│   ├── layouts/
│   │   └── AppLayout.tsx
│   │
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── errors.ts
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
└── package.json