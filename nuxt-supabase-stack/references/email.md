# Transactional email (Resend)

Contents:
1. The send helper
2. Template helpers
3. Event notifications & opt-out

## 1. The send helper — `server/utils/email.ts`

One module talks to Resend; everything else calls `sendEmail`. Fail soft on non-critical mail (log, don't crash the request) but surface failures for mail that gates a flow (verification, password reset).

```ts
interface SendEmailOptions { to: string; subject: string; html: string }

export async function sendEmail({ to, subject, html }: SendEmailOptions) {
  const key  = process.env.RESEND_API_KEY
  const from = process.env.RESEND_FROM ?? 'onboarding@resend.dev'
  if (!key) { console.warn('[email] RESEND_API_KEY not set — skipping'); return }
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from, to, subject, html }),
  })
  if (!res.ok) {
    const text = await res.text()
    console.error(`[email] Resend failed: ${res.status} ${text}`)
    throw createError({ statusCode: 502, message: 'Email could not be sent' })
  }
}
```

During local dev without a key, the helper logs instead of sending — keeps the signup flow usable offline.

## 2. Template helpers

Keep HTML in small pure functions next to `sendEmail`, e.g. `otpEmailHtml(otp)`, `verificationEmailHtml(url)`. Pure string builders are trivially unit-testable and keep routes clean. Inline the CSS — email clients ignore `<style>` blocks and external sheets.

## 3. Event notifications & opt-out

For non-essential notifications (someone messaged you, your item sold), route them through a wrapper that (a) checks the recipient's opt-out flag and skips if set, and (b) appends an unsubscribe footer. Keep transactional mail (verification, password reset, receipts) on the direct `sendEmail` path — those must always send and need no opt-out.

```ts
export async function sendEventNotification(opts: { to: string; userId: string; subject: string; html: string }) {
  if (!(await canReceiveNotifications(opts.userId))) return
  await sendEmail({ ...opts, html: opts.html + unsubscribeFooter(opts.userId) })
}
```

Call event notifications fire-and-forget from the route (`.catch(logErr)`) so a mail hiccup never fails the user's actual action.
