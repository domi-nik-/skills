export default defineEventHandler(async (event) => {
  const path = getRequestURL(event).pathname
  if (path.startsWith('/api/auth/')) return
  const session = await auth.api.getSession({ headers: event.headers })
  event.context.session = session?.session ?? null
  event.context.user    = session?.user ?? null
})
