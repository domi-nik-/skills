# Authentication (BetterAuth)

Contents:
1. Server instance
2. Catch-all handler
3. Server middleware (event.context.user)
4. Client composable
5. Email + OTP
6. Custom user columns

## 1. Server instance — `server/utils/auth.ts`

BetterAuth owns its own tables via the Drizzle adapter. Minimal setup:

```ts
import { betterAuth } from 'better-auth'
import { drizzleAdapter } from 'better-auth/adapters/drizzle'
import { emailOTP } from 'better-auth/plugins'
import { db } from '../db'
import * as schema from '../db/schema'
import { sendEmail, otpEmailHtml } from './email'

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: 'pg', schema }),
  emailAndPassword: { enabled: true, requireEmailVerification: false },
  emailVerification: { sendOnSignUp: true, autoSignInAfterVerification: true },
  plugins: [
    emailOTP({
      async sendVerificationOTP({ email, otp }) {
        await sendEmail({ to: email, subject: 'Your login code', html: otpEmailHtml(otp) })
      },
    }),
  ],
  secret:  process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
})
```

## 2. Catch-all handler — `server/api/auth/[...all].ts`

```ts
import { auth } from '../../utils/auth'
export default defineEventHandler((event) => auth.handler(toWebRequest(event)))
```

This is why `netlify.toml` needs the `/api/auth/*` redirect — all auth traffic flows through this one route.

## 3. Server middleware — `server/middleware/auth.ts`

Populate `event.context.user` on every request so routes can read it. Skip the BetterAuth catch-all itself to avoid a circular call.

```ts
export default defineEventHandler(async (event) => {
  const path = getRequestURL(event).pathname
  if (path.startsWith('/api/auth/')) return   // handler owns these
  const session = await auth.api.getSession({ headers: event.headers })
  event.context.session = session?.session ?? null
  event.context.user    = session?.user ?? null
})
```

`getSession()` can be slow; a short per-cookie cache (a few seconds) is a worthwhile optimization on pages that fire several API calls per render. Keep the TTL small so logout/login feels instant.

The middleware **populates** context but does **not** gate access. Every protected route checks for itself:
```ts
const user = event.context.user
if (!user) throw createError({ statusCode: 401, message: 'Sign in required' })
```

## 4. Client composable — `app/composables/useAuth.ts`

Wrap the client in a builder function so the return type keeps any plugin types (e.g. `emailOTPClient`). A direct `ReturnType<typeof createAuthClient>` annotation strips plugin methods.

```ts
import { createAuthClient } from 'better-auth/vue'
import { emailOTPClient } from 'better-auth/client/plugins'

function buildAuthClient() {
  return createAuthClient({
    baseURL: typeof window !== 'undefined' ? window.location.origin
      : (process.env.NUXT_PUBLIC_APP_URL ?? 'http://localhost:3000'),
    plugins: [emailOTPClient()],   // mirror every server plugin here
  })
}
let _client: ReturnType<typeof buildAuthClient> | null = null
function getClient() { return (_client ??= buildAuthClient()) }
```

Rule of thumb: **whatever plugins you enable server-side, register the matching client plugin** — otherwise the methods exist at runtime but aren't typed, and TS errors look mysterious.

## 5. Email + OTP

The email-OTP plugin calls your `sendVerificationOTP` for login codes; email verification on signup uses the same `sendEmail`. Keep all sending in `server/utils/email.ts` (see email.md) so there's one place that talks to Resend.

## 6. Custom user columns

`getSession()` returns only BetterAuth core fields (id, email, name). Extra columns you added to `user` (locale, role, location, ...) aren't included. For SSR page renders that need them (e.g. route middleware deciding redirects), load them with one extra query in the server middleware and merge into `event.context.user`. API routes that need a column should select it themselves rather than relying on the merged context.
