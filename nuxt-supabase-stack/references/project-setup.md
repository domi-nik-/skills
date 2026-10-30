# Project setup & configuration

Contents:
1. Directory layout (Nuxt 4)
2. Config files explained
3. Environment variables
4. Netlify deployment
5. Dev workflow & scripts
6. Node.js version

## 1. Directory layout (Nuxt 4)

Nuxt 4 moves app code under `app/`. The server lives at the repo root under `server/`.

```
project/
├── app/
│   ├── assets/css/main.css      # Tailwind layers + design tokens
│   ├── components/
│   ├── composables/             # useApiError, useAuth, ...
│   ├── layouts/
│   ├── middleware/              # route middleware (auth.ts, admin.ts)
│   ├── pages/                   # file-based routes
│   └── types/                   # shared TS types
├── server/
│   ├── api/                     # Nitro API routes (file = endpoint)
│   │   └── auth/[...all].ts     # BetterAuth catch-all
│   ├── db/
│   │   ├── index.ts             # Drizzle client
│   │   └── schema.ts            # all tables in one file
│   ├── middleware/auth.ts       # sets event.context.user
│   └── utils/                   # auth.ts, email.ts, schemas.ts, ...
├── i18n/locales/                # de.json, en.json, ...
├── supabase/migrations/         # SQL migration files
├── tests/unit/                  # vitest
├── nuxt.config.ts
├── drizzle.config.ts
├── vitest.config.ts
├── eslint.config.mjs
├── netlify.toml
└── .env                         # never committed
```

## 2. Config files explained

**nuxt.config.ts** — register modules (`@nuxtjs/tailwindcss`, `@nuxtjs/i18n`, `@nuxtjs/color-mode`, `@nuxt/eslint`), set the Nitro preset, and expose runtime config. Keep server-only secrets at the top level of `runtimeConfig` and only browser-safe values under `runtimeConfig.public`. Set `typescript: { strict: true }`. See `assets/nuxt.config.ts`.

**tsconfig.json** — see `assets/tsconfig.json`. Thin; it only references the four generated `.nuxt/tsconfig.*.json` files. `npm run postinstall` (`nuxt prepare`) generates them, so run `npm install` before `npm run typecheck`. Consider enabling `noUncheckedIndexedAccess` for real null-safety on array/record access — it catches a class of runtime bugs, at the cost of more explicit guards.

**drizzle.config.ts** — points `schema` at `server/db/schema.ts`, `out` at `supabase/migrations`, dialect `postgresql`, url from `DATABASE_URL`. See `assets/drizzle.config.ts`.

**vitest.config.ts** — `environment: 'node'`, `include: ['tests/**/*.test.ts']` (see `assets/vitest.config.ts`). Keep unit tests on pure logic (validation, money math, pure helpers); they run without a DB.

**eslint.config.mjs** — flat config that wraps the one `@nuxt/eslint` generates into `.nuxt/` (see `assets/eslint.config.mjs`), so `npm run lint` needs `nuxt prepare` to have run.

**netlify.toml** — `command = "npm run build"`, `publish = "dist"`, Node 24, esbuild bundler, and a redirect so `/api/auth/*` reaches the server function. See `assets/netlify.toml`.

## 3. Environment variables

Keep a committed `.env.example` documenting every variable; never commit `.env`. Core set:

```
DATABASE_URL=                 # Supabase Postgres connection string (pooler)
SUPABASE_URL=
SUPABASE_ANON_KEY=            # browser-safe
SUPABASE_SERVICE_KEY=         # server-only, bypasses RLS — never expose
BETTER_AUTH_SECRET=           # openssl rand -hex 32
BETTER_AUTH_URL=              # e.g. http://localhost:3000
NUXT_PUBLIC_APP_URL=          # base URL for redirects / email links
RESEND_API_KEY=
NITRO_PRESET=node-server      # optional override
```

`DATABASE_URL` should use the Supabase **pooler** host. The Drizzle client disables prepared statements when it detects a pooler host (see database-and-rls.md) — both must agree or you get protocol errors.

## 4. Netlify deployment

The Nitro `node-server` preset turns `server/` routes into a Netlify function. Two things people trip on:

- The `/api/auth/*` redirect in `netlify.toml` must exist, or BetterAuth's catch-all 404s in production.
- Avoid Nitro ISR route rules unless `@netlify/functions` is in dependencies — ISR handlers import it at runtime and 500 on the first request otherwise. Prefer `prerender: true` for truly static pages and plain SSR for the rest.

Set all env vars in the Netlify dashboard — never in the repo.

## 5. Dev workflow & scripts

```
npm run dev        # localhost:3000
npm run typecheck  # nuxt typecheck (vue-tsc)
npm run test       # vitest watch
npm run test:ci    # vitest run (one-shot, for CI)
npm run lint       # eslint .
npm run db:generate  # generate SQL migration from schema.ts
npm run db:studio    # Drizzle Studio (read-only browsing)
```

Note the deliberately scary name `db:push:DANGEROUS_DISABLES_RLS` — see database-and-rls.md for why `drizzle-kit push` is unsafe against a database that uses RLS.

## 6. Node.js version

Nuxt needs Node `^22.22.3 || ^24.15.0 || >=26.0.0` (the `engines` range in `assets/package.json` mirrors it) and recommends an even-numbered, active LTS release. The templates pin **Node 24** for Netlify and CI because Netlify Functions run on AWS Lambda, which supports `nodejs24.x` until April 2028; Node 22 leaves Lambda support in April 2027. Move to Node 26 once Lambda's `nodejs26.x` runtime is generally available (planned for November 2026; it is in preview until then).

Use the same major version locally (e.g. `nvm use 24`) so the lockfile is produced by the same npm generation that CI and Netlify use.

Known build warning: with Nuxt 4.6 and `@nuxtjs/tailwindcss` 6.14 the build prints `The PostCSS plugin tailwindcss/nesting could not be loaded`. It is harmless; the CSS is generated normally.
