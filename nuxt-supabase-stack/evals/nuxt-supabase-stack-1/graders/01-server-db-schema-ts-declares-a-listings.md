---
type: llm
focus: trace
weight: 1
---

server/db/schema.ts declares a listings table with an integer price-in-cents column, a status limited to open/sold (enum or check), an owner column referencing user.id, and a timezone-aware created_at.
