import type { auth } from './utils/auth'
type Session = typeof auth.$Infer.Session
declare module 'h3' {
  interface H3EventContext {
    user: Session['user'] | null
    session: Session['session'] | null
  }
}
export {}
