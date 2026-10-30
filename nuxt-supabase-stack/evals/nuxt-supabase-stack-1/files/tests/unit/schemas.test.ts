import { describe, it, expect } from 'vitest'
import { CreateThingSchema } from '../../server/utils/schemas'

describe('CreateThingSchema', () => {
  it('accepts a priced item', () => {
    expect(CreateThingSchema.parse({ title: 'Fern', priceCents: 500 })).toMatchObject({ free: false })
  })
  it('rejects a zero price unless free', () => {
    expect(CreateThingSchema.safeParse({ title: 'Fern', priceCents: 0 }).success).toBe(false)
    expect(CreateThingSchema.safeParse({ title: 'Fern', priceCents: 0, free: true }).success).toBe(true)
  })
})
