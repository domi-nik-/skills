import { createAuthClient } from 'better-auth/vue'
import { emailOTPClient } from 'better-auth/client/plugins'

function buildAuthClient() {
  return createAuthClient({
    baseURL: typeof window !== 'undefined' ? window.location.origin
      : (process.env.NUXT_PUBLIC_APP_URL ?? 'http://localhost:3000'),
    plugins: [emailOTPClient()],
  })
}
let _client: ReturnType<typeof buildAuthClient> | null = null
function getClient() { return (_client ??= buildAuthClient()) }

export function useAuth() {
  // Exercises the plugin types: emailOtp exists only if the client plugin is typed.
  const signInWithOtp = (email: string) => getClient().emailOtp.sendVerificationOtp({ email, type: 'sign-in' })
  const session = getClient().useSession()
  return { signInWithOtp, session }
}
