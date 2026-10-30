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

export const otpEmailHtml = (otp: string) => `<p style="font-size:20px">Your code: <b>${otp}</b></p>`
