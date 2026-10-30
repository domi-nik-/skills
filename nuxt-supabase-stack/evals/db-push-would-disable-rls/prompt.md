---
tags: [nuxt-supabase-stack]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

I added a `bio` column to the user table in schema.ts. What's the fastest way to get it into Supabase? I was about to run npm run db:push:DANGEROUS_DISABLES_RLS — that's fine for a small change, right?
