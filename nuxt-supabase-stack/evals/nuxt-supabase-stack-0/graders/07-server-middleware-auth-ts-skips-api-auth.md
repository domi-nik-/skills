---
type: llm
focus: trace
weight: 1
---

server/middleware/auth.ts skips /api/auth/ paths and sets event.context.user without rejecting unauthenticated requests.
