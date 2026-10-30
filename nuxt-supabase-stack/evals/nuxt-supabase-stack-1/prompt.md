---
tags: [nuxt-supabase-stack]
max_turns: 50
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

My app is already on Nuxt 4 + Supabase + Drizzle + BetterAuth. Add a feature: a `listings` table (id, owner = the user, title, description, price in cents, status open/sold, created_at) and a POST /api/listings endpoint to create one, plus GET /api/listings/[id]. Follow whatever conventions the project already uses for auth checks, validation, and RLS.

Input files: .env.example, .gitignore, app/app.vue, app/assets/css/main.css, app/composables/useAuth.ts, drizzle.config.ts, eslint.config.mjs, i18n/locales/de.json, i18n/locales/en.json, netlify.toml, nuxt.config.ts, package.json, server/api/auth/[...all].ts, server/api/things.post.ts, server/context.d.ts, server/db/index.ts, server/db/schema.ts, server/middleware/auth.ts, server/utils/auth.ts, server/utils/email.ts, server/utils/schemas.ts, tests/unit/schemas.test.ts, tsconfig.json, vitest.config.ts
