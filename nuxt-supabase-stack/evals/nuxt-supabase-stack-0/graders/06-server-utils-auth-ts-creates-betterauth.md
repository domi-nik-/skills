---
type: llm
focus: trace
weight: 1
---

server/utils/auth.ts creates BetterAuth with drizzleAdapter(..., { provider: 'pg' }) and enables emailAndPassword.
