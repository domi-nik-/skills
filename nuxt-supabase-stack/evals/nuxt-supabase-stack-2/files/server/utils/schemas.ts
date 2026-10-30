import { z } from 'zod'

export const CreateThingSchema = z.object({
  title: z.string().min(1).max(200),
  priceCents: z.number().int().nonnegative(),
  free: z.boolean().default(false),
  idempotencyKey: z.string().uuid().optional(),
}).refine(v => v.free || v.priceCents > 0, { message: 'Price required unless free', path: ['priceCents'] })
