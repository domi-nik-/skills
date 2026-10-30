---
type: llm
focus: trace
weight: 1
---

app/composables/useAuth.ts registers emailOTPClient() in createAuthClient and does not annotate the client as ReturnType<typeof createAuthClient>.
