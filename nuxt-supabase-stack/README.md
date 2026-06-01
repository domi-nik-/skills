# nuxt-supabase-stack

A [Claude Agent Skill](https://support.claude.com/en/articles/12512176-what-are-skills) that scaffolds and helps build full-stack web apps on a proven stack:

**Nuxt 4 (Vue 3, SSR) · Supabase/Postgres · Drizzle ORM · BetterAuth · Netlify · Resend · Tailwind · i18n**

It carries the battle-tested wiring and conventions so the pieces fit together correctly instead of being reinvented each time — the connection-pooler gotcha, RLS managed via raw SQL (never Drizzle), the BetterAuth client-plugin typing pattern, Zod-validated API routes, transactions for money-flows, and more.

The skill does two jobs:

1. **Scaffold** a new project with everything wired together (`npm install`-ready).
2. **Guide** feature work in an existing project on this stack so new code matches established patterns.

## What's inside

```
nuxt-supabase-stack/
├── SKILL.md                       # workflow + when-to-use + house conventions
├── references/
│   ├── project-setup.md           # config files, Nuxt 4 layout, Netlify, env, scripts
│   ├── database-and-rls.md        # Drizzle client, schema patterns, RLS rules
│   ├── auth.md                    # BetterAuth (email + OTP), middleware, client composable
│   ├── email.md                   # Resend wiring, templates, opt-out notifications
│   └── api-and-errors.md          # route anatomy, Zod, error mapping, transactions, rate limiting
└── assets/                        # copy-ready templates
    ├── package.json               # pinned, known-good dependency set
    ├── nuxt.config.ts
    ├── drizzle.config.ts
    ├── netlify.toml               # incl. the load-bearing /api/auth/* redirect
    ├── .env.example
    ├── ci.yml                     # GitHub Actions: install → typecheck → test
    └── gitignore
```

## Install & use in Claude Desktop

Skills run inside Claude's code-execution environment, so that has to be on first.

1. **Enable code execution.** Open **Settings → Capabilities** and turn on **Code execution and file creation**. (On Team/Enterprise plans an owner enables this — and **Skills** — under Organization settings first.)
2. **Open your skills.** Go to **Customize → Skills**.
3. **Upload this skill.** Click the **“+”** button → **“+ Create skill”** → **“Upload a skill”**, and select the `nuxt-supabase-stack.skill` file (it's just a ZIP of this folder — a `.zip` works too).
4. **Toggle it on** in your skills list.
5. **Use it.** Just describe what you want — Claude triggers the skill automatically when it fits:
   - *“Start a new Nuxt app with Supabase, Drizzle, BetterAuth login and Resend email.”*
   - *“Add a `listings` table and a POST/GET API following my project's conventions.”*
   - *“Set up passwordless email-OTP login via Resend.”*

   If it doesn't trigger, name it explicitly: *“Use my nuxt-supabase-stack skill to …”*.

Custom skills you upload are **private to your account**. On Team/Enterprise plans you can share them with colleagues or your whole org (an owner must enable sharing first).

> **Building it yourself?** You don't need the packaged file — point Claude Code or the Claude Agent SDK at this folder, or drop it into a plugin/marketplace `marketplace.json`. The `SKILL.md` format is an open standard, so the same folder also works in tools like Codex CLI.

## Repackaging after edits

A `.skill` file is a ZIP of the skill folder. To rebuild it after changes:

```bash
cd nuxt-supabase-stack
zip -r ../nuxt-supabase-stack.skill . -x '.*'
```

(or use Anthropic's `skill-creator` packaging script if you have it).

## A note on conventions

The opinionated bits in this skill exist for concrete reasons, each explained in the reference files — e.g. why prepared statements are disabled against the Supabase pooler, why `drizzle-kit push` is renamed to a scary `db:push:DANGEROUS_DISABLES_RLS` tripwire, and why the BetterAuth client is wrapped in a builder function so plugin types survive. They're general best practices for this stack, not tied to any specific app.

## Security

Only install skills from sources you trust, and skim the contents before enabling — this one contains instructions and config templates only (no executable scripts, no network calls, no third-party package installs beyond the documented stack dependencies).

## License

[MIT](./LICENSE) — do what you like, attribution appreciated.
