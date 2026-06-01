# API routes, validation, errors & transactions

Contents:
1. Anatomy of an API route
2. Zod validation
3. Error handling (server + client)
4. Transactions & locking
5. Rate limiting

## 1. Anatomy of an API route

Nitro maps `server/api/foo/bar.post.ts` to `POST /api/foo/bar`. A route reads like this:

```ts
import { db, schema } from '../../db'
import { eq } from 'drizzle-orm'
import { CreateThingSchema } from '../../utils/schemas'

export default defineEventHandler(async (event) => {
  const user = event.context.user
  if (!user) throw createError({ statusCode: 401, message: 'Sign in required' })

  const body = await readValidatedBody(event, CreateThingSchema.parse)

  const [thing] = await db.insert(schema.thing)
    .values({ ownerId: user.id, ...body })
    .returning()
  if (!thing) throw createError({ statusCode: 500, message: 'Could not create item' })

  return thing
})
```

Note the guard on the destructured insert result — under `noUncheckedIndexedAccess`, `[thing]` is `T | undefined`, and asserting it makes both the type and the runtime honest.

## 2. Zod validation

Keep schemas in `server/utils/schemas.ts` and import them into both routes and tests so there's a single source of truth. Couple related constraints with `.refine()` (e.g. "amount required when type isn't free") instead of validating it ad hoc in the route. Validate server-side always; client validation is only UX.

## 3. Error handling

**Server:** throw `createError({ statusCode, message })` with a short, human message. Put stack traces and IDs in logs, never in `message`. A good error answers three things: what happened, why, and what the user can do.

**Client:** map errors through one composable, `useApiError()`, so every flow shows localized, friendly text instead of raw `e.data.message`. Prefer matching on a server-provided error `code` over substring-matching the prose — message wording changes break substring maps silently.

```ts
// app/composables/useApiError.ts (shape)
export function useApiError() {
  const { t } = useI18n()
  function apiError(e: unknown): string {
    const code = (e as any)?.data?.code
    if (code && messages[code]) return t(messages[code])
    return t('errors.generic')
  }
  return { apiError }
}
```

## 4. Transactions & locking

Any operation that writes more than one row, or reads-then-writes a contended row, belongs in a transaction. For read-modify-write races (a counter, a balance, "only one winner"), lock the row with `.for('update')` and recompute inside the lock:

```ts
await db.transaction(async (tx) => {
  const [row] = await tx.select().from(schema.account)
    .where(eq(schema.account.id, id)).for('update').limit(1)
  // ... check + mutate using row, all inside the lock
})
```

For idempotency (webhooks redelivered, double-clicks), prefer `insert(...).onConflictDoNothing({ target: [...] }).returning()` backed by a unique index declared in `schema.ts`. Check-then-insert is not atomic and races under concurrency.

## 5. Rate limiting

A small fixed-window limiter keyed by `action:actor` is enough for abuse-prone endpoints (OTP, payouts, signups). Note the caveat: an in-process Map only limits per warm serverless instance — for real distributed limits use a shared store (e.g. Upstash Redis). Document which guarantee you actually have so nobody assumes more than is true.
