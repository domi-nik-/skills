---
name: nuxt-supabase-stack
description: >-
  Scaffold and build full-stack web apps on the Nuxt 4 + Vue 3 (SSR) + Supabase/Postgres (Drizzle ORM) + BetterAuth + Netlify + Resend + Tailwind + i18n stack. Use this whenever the user wants to start a new Nuxt app, bootstrap a web project on Supabase, set up Drizzle with Postgres, wire BetterAuth (email + OTP), deploy a Nuxt app to Netlify, add transactional email via Resend, or add features (API routes, auth, RLS, migrations, email) to a project already built on this stack. Trigger even when the user names only part of the stack (e.g. "new Nuxt app with auth", "Supabase + Drizzle project", "Nuxt on Netlify") — this skill carries the battle-tested wiring and conventions so the pieces fit together correctly instead of being reinvented each time.
---

# Nuxt 4 + Supabase + Netlify + Resend Stack

This skill captures a production-proven full-stack setup and the conventions that keep it secure, type-safe, and maintainable. It serves two jobs:

1. **Scaffold** a new project with the pieces correctly wired together.
2. **Guide** feature work in an existing project on this stack so new code matches established patterns.

Figure out which job applies from the request, then act. A request like "start a new Nuxt app with Supabase auth and email" is scaffolding. "Add a `/api/orders` endpoint" or "add a payments table" in an existing repo is feature work — read the relevant reference and follow the house style.

## The stack at a glance

| Layer | Choice | Why |
|---|---|---|
| Framework | Nuxt 4 (Vue 3, SSR) | File-based routing for pages **and** server API (Nitro) |
| DB | PostgreSQL via Supabase | Managed Postgres + RLS + connection pooler |
| ORM | Drizzle | Type-safe queries, migrations generated from one schema file |
| Auth | BetterAuth (email + email-OTP) | Session-based, owns its own tables, Drizzle adapter |
| Email | Resend | Transactional email, simple HTTP API |
| Styling | Tailwind CSS | Utility-first |
| i18n | @nuxtjs/i18n | Multi-locale without URL prefixes |
| Deploy | Netlify (Nitro `node-server` preset) | Server routes become functions |
| Validation | Zod | One schema reused by API routes and tests |
| Tests | Vitest | Fast unit tests on pure logic |

Pin the working dependency set from `assets/package.json` rather than letting `npm install <latest>` pull majors that drift apart. The combination in that file is known to work together.

## Scaffolding a new project

Work through these in order. Each step has a copy-ready template in `assets/` — read it, then adapt names to the user's project. Don't dump all files blindly; explain what each piece does as you place it, because the user will maintain it.

1. **Project skeleton & config** — `package.json`, `nuxt.config.ts`, `tsconfig.json`, `drizzle.config.ts`, `vitest.config.ts`, `netlify.toml`, `.env.example`, `.gitignore`. Templates in `assets/`. See `references/project-setup.md` for what each config does and the gotchas (Nuxt 4 `app/` dir, Netlify auth redirect, the dangerous `db:push` script naming).
2. **Database layer** — `server/db/index.ts` (Drizzle client with the Supabase-pooler `prepare:false` guard) and `server/db/schema.ts` (start from the BetterAuth core tables). See `references/database-and-rls.md`.
3. **Auth** — `server/utils/auth.ts` (BetterAuth instance), `server/api/auth/[...all].ts` (catch-all handler), `server/middleware/auth.ts` (attaches `event.context.user`). See `references/auth.md`.
4. **Email** — `server/utils/email.ts` (Resend `sendEmail` + HTML template helpers). See `references/email.md`.
5. **RLS** — enable Row Level Security on every table in a raw-SQL migration. This is load-bearing for security; see `references/database-and-rls.md` for why Drizzle must never manage RLS.
6. **Conventions** — drop in `app/composables/useApiError.ts` and adopt the API-route + error-handling patterns from `references/api-and-errors.md` so the first feature sets the tone for the rest.

After scaffolding, verify before declaring done: `npm install`, `npm run typecheck`, and `npm run build` should all pass. If the user has Supabase credentials ready, generate the first migration with `npm run db:generate` and apply it. If not, leave a clear note on what they need to fill into `.env`.

## Building features on this stack

When adding to an existing project, match what's already there. The non-negotiable conventions:

- **Every server route checks auth explicitly.** `const user = event.context.user; if (!user) throw createError({ statusCode: 401, ... })`. The middleware populates the context but does not gate routes.
- **Validate input with Zod**, server-side, before touching the DB. Keep schemas in `server/utils/schemas.ts` and reuse them in tests. Client validation is UX only.
- **Errors:** server throws `createError({ statusCode, message })` with short, user-friendly messages; the frontend maps them via `useApiError()`. Technical detail goes to logs, never the UI.
- **Money / multi-step mutations** run inside `db.transaction(...)` and lock contended rows with `.for('update')`. See `references/api-and-errors.md`.
- **New tables** get RLS enabled in a raw-SQL migration the moment they're created, and any unique/idempotency index must be declared in `schema.ts` (not only in the migration) so `drizzle-kit` doesn't drop it.

Read the matching reference file before writing code — they carry the exact patterns and the reasoning behind them.

## Reference files

Load these as needed; each opens with a short table of contents.

- `references/project-setup.md` — config files explained, Nuxt 4 layout, Netlify deploy, env vars, dev workflow.
- `references/database-and-rls.md` — Drizzle client, schema patterns, migration workflow, and the RLS rules (why `db:push` is dangerous, how `withUserContext` exposes the current user to policies).
- `references/auth.md` — BetterAuth setup, email + OTP, the server middleware, the client composable, and how custom user columns get loaded.
- `references/email.md` — Resend wiring, template helpers, and event-notification opt-out pattern.
- `references/api-and-errors.md` — API-route anatomy, Zod validation, the `useApiError` mapping, transactions, rate limiting.

## Quality gates worth setting up early

These pay for themselves fast and are cheap to add at scaffold time:

- `npm run typecheck` (`nuxt typecheck`, needs `vue-tsc`) — Nuxt's generated types catch most integration mistakes.
- A CI workflow running `npm ci → typecheck → test` on pull requests. A starter is in `assets/ci.yml`.
- ESLint via `@nuxt/eslint` with a flat config. Roll it out non-blocking first if the codebase predates it, then make it blocking once clean.

Explain the "why" when you set these up: the stack has many moving parts that only connect at the type level, so a typecheck gate is the cheapest way to keep them honest.
