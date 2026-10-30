import { defineConfig } from 'vitest/config'

// Unit tests on pure logic (validation, money math, helpers); no DB, no Nuxt runtime.
export default defineConfig({
  test: {
    environment: 'node',
    include: ['tests/**/*.test.ts'],
  },
})
