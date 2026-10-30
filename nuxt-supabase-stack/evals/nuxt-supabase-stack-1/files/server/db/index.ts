import postgres from 'postgres'
import { drizzle } from 'drizzle-orm/postgres-js'
import { sql } from 'drizzle-orm'
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

export const db = new Proxy({} as ReturnType<typeof drizzle<typeof schema>>, {
  get(_, prop) { return getDb()[prop as keyof ReturnType<typeof drizzle<typeof schema>>] },
})
export { schema }

export async function withUserContext<T>(userId: string, cb: (tx: typeof db) => Promise<T>): Promise<T> {
  return getDb().transaction(async (tx) => {
    await tx.execute(sql`SELECT set_config('app.current_user_id', ${userId}, true)`)
    return cb(tx as unknown as typeof db)
  })
}
