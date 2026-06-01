# Database, Drizzle & Row Level Security

Contents:
1. The Drizzle client (pooler-safe singleton)
2. Schema patterns
3. Migration workflow
4. Row Level Security — the rules
5. `withUserContext` — exposing the current user to policies

## 1. The Drizzle client

`server/db/index.ts` is a lazily-initialized singleton. The key detail: when the connection string points at a Supabase pooler, prepared statements must be disabled, or you hit "prepared statement already exists" errors under the transaction pooler.

```ts
import postgres from 'postgres'
import { drizzle } from 'drizzle-orm/postgres-js'
import * as schema from './schema'

let _client: ReturnType<typeof postgres> | undefined
let _db: ReturnType<typeof drizzle<typeof schema>> | undefined

function getDb() {
  if (!_db) {
    const url = process.env.DATABASE_URL
    if (!url) throw new Error('DATABASE_URL is not set')
    const isPooler = url.includes('pooler.supabase.com')
    _client = postgres(url, { max: 10, idle_timeout: 20, connect_timeout: 10, prepare: !isPooler })
    _db = drizzle(_client, { schema, logger: process.env.NODE_ENV === 'development' })
  }
  return _db
}

// Proxy so `import { db }` works while staying lazy (env may not be ready at import time)
export const db = new Proxy({} as ReturnType<typeof drizzle<typeof schema>>, {
  get(_, prop) { return getDb()[prop as keyof ReturnType<typeof drizzle<typeof schema>>] },
})
export { schema }
```

## 2. Schema patterns

All tables live in one `server/db/schema.ts`. Start from the BetterAuth core tables (`user`, `session`, `account`, `verification`) — BetterAuth's Drizzle adapter reads them — then extend `user` with app columns and add your domain tables.

Conventions that prevent later pain:
- Use `timestamptz` (timestamp with timezone) consistently. A small helper keeps it terse: `const timestamptz = (n: string) => timestamp(n, { withTimezone: true, mode: 'date' })`.
- **Declare every index in the schema, including unique/idempotency indexes.** If a unique index exists only in a migration, `drizzle-kit` treats it as drift and will drop it on the next push/generate cycle — silently removing a guarantee your code relies on.
- Money in integer cents, never floats.
- Append-only audit/ledger tables: never update or delete rows; model corrections as new rows.

## 3. Migration workflow

```
npm run db:generate   # writes SQL into supabase/migrations/
# review the generated SQL (see RLS warning below), then apply via
# the Supabase SQL editor or the Supabase MCP apply_migration
```

Review every generated file before applying. Strip any `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` or `DROP POLICY` statements Drizzle emits — those are the drift-correction it should never perform.

## 4. Row Level Security — the rules

RLS is the backstop that keeps tenants/users from reading each other's rows even if an API route forgets a check. Treat it as load-bearing security, not decoration.

- Enable RLS on **every** table in a raw-SQL migration the moment the table exists:
  ```sql
  ALTER TABLE public."your_table" ENABLE ROW LEVEL SECURITY;
  ```
- **Never let Drizzle manage RLS.** `drizzle-kit push` / `migrate` don't understand policies, so they interpret RLS as drift and emit `DISABLE ROW LEVEL SECURITY` — turning protection off across the board. That's why the push script is named `db:push:DANGEROUS_DISABLES_RLS` as a tripwire. Manage RLS only through raw SQL you control.
- Tables accessed exclusively through server routes with the service-role key (which bypasses RLS) can have RLS enabled with no policies — the service key still works, and nothing else can touch them.

## 5. `withUserContext` — exposing the current user to policies

When you want RLS policies to reference the acting user, wrap the query in a transaction that sets a Postgres GUC the policy can read:

```ts
export async function withUserContext<T>(userId: string, cb: (tx: typeof db) => Promise<T>): Promise<T> {
  return getDb().transaction(async (tx) => {
    await tx.execute(sql`SELECT set_config('app.current_user_id', ${userId}, true)`)
    return cb(tx as unknown as typeof db)
  })
}
```

Policies then compare against `current_setting('app.current_user_id', true)`. Use this for user-facing mutations; reserve the raw `db` + service key for trusted server-only paths (webhooks, admin, cron).
