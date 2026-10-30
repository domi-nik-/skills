import { pgTable, text, boolean, timestamp, integer, uniqueIndex, index } from 'drizzle-orm/pg-core'

const timestamptz = (n: string) => timestamp(n, { withTimezone: true, mode: 'date' })

// BetterAuth core tables
export const user = pgTable('user', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  emailVerified: boolean('email_verified').notNull().default(false),
  image: text('image'),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
  updatedAt: timestamptz('updated_at').notNull().defaultNow(),
})
export const session = pgTable('session', {
  id: text('id').primaryKey(),
  expiresAt: timestamptz('expires_at').notNull(),
  token: text('token').notNull().unique(),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
  updatedAt: timestamptz('updated_at').notNull().defaultNow(),
  ipAddress: text('ip_address'),
  userAgent: text('user_agent'),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
})
export const account = pgTable('account', {
  id: text('id').primaryKey(),
  accountId: text('account_id').notNull(),
  providerId: text('provider_id').notNull(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  accessToken: text('access_token'),
  refreshToken: text('refresh_token'),
  idToken: text('id_token'),
  accessTokenExpiresAt: timestamptz('access_token_expires_at'),
  refreshTokenExpiresAt: timestamptz('refresh_token_expires_at'),
  scope: text('scope'),
  password: text('password'),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
  updatedAt: timestamptz('updated_at').notNull().defaultNow(),
})
export const verification = pgTable('verification', {
  id: text('id').primaryKey(),
  identifier: text('identifier').notNull(),
  value: text('value').notNull(),
  expiresAt: timestamptz('expires_at').notNull(),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
  updatedAt: timestamptz('updated_at').notNull().defaultNow(),
})

// Domain table
export const thing = pgTable('thing', {
  id: integer('id').primaryKey().generatedAlwaysAsIdentity(),
  ownerId: text('owner_id').notNull().references(() => user.id),
  title: text('title').notNull(),
  priceCents: integer('price_cents').notNull(),
  idempotencyKey: text('idempotency_key'),
  createdAt: timestamptz('created_at').notNull().defaultNow(),
}, t => [
  index('thing_owner_idx').on(t.ownerId),
  uniqueIndex('thing_idem_idx').on(t.ownerId, t.idempotencyKey),
])
