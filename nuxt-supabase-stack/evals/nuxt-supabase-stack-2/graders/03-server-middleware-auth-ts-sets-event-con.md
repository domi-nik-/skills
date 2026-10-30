---
type: llm
focus: trace
weight: 1
---

server/middleware/auth.ts sets event.context.user from auth.api.getSession and skips /api/auth/ paths.
