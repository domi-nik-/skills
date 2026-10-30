import { db, schema } from '../db'
import { eq } from 'drizzle-orm'
import { CreateThingSchema } from '../utils/schemas'

export default defineEventHandler(async (event) => {
  const user = event.context.user
  if (!user) throw createError({ statusCode: 401, message: 'Sign in required' })

  const { free: _free, ...body } = await readValidatedBody(event, CreateThingSchema.parse)

  const [thing] = await db.insert(schema.thing)
    .values({ ownerId: user.id, ...body })
    .onConflictDoNothing({ target: [schema.thing.ownerId, schema.thing.idempotencyKey] })
    .returning()
  if (!thing) throw createError({ statusCode: 409, message: 'Already created' })

  await db.transaction(async (tx) => {
    const [row] = await tx.select().from(schema.thing).where(eq(schema.thing.id, thing.id)).for('update').limit(1)
    return row
  })
  return thing
})
