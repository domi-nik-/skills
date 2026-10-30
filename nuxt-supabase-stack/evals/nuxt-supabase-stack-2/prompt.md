---
tags: [nuxt-supabase-stack]
max_turns: 50
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Set up login for my Nuxt app using BetterAuth — I want email+password and also a passwordless email one-time-code option. It needs to actually send the codes via Resend. Wire up both the server side and a client composable I can call from my login page.

Input files: .env.example, .gitignore, app/app.vue, app/assets/css/main.css, app/pages/index.vue, drizzle.config.ts, eslint.config.mjs, i18n/locales/de.json, i18n/locales/en.json, netlify.toml, nuxt.config.ts, package.json, server/db/index.ts, server/db/schema.ts, server/utils/email.ts, server/utils/schemas.ts, tests/unit/schemas.test.ts, tsconfig.json, vitest.config.ts
