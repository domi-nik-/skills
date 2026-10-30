---
type: llm
focus: trace
weight: 1
---

server/api/auth/[...all].ts passes the request to auth.handler (e.g. via toWebRequest(event)).
