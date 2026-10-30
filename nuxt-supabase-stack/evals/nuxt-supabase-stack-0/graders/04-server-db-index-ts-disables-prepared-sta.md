---
type: llm
focus: trace
weight: 1
---

server/db/index.ts disables prepared statements (prepare: false) when DATABASE_URL points at a Supabase pooler host.
