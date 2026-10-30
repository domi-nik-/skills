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
