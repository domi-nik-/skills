export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  css: ['assets/css/main.css'],

  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/i18n',
    '@nuxtjs/color-mode',
    '@nuxt/eslint',
  ],

  nitro: {
    preset: process.env.NITRO_PRESET ?? 'node-server',
  },

  i18n: {
    locales: [
      { code: 'en', name: 'English', file: 'en.json' },
      { code: 'de', name: 'Deutsch', file: 'de.json' },
    ],
    defaultLocale: 'en',
    langDir: 'locales/',
    strategy: 'no_prefix',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_locale',
      redirectOn: 'root',
    },
  },

  runtimeConfig: {
    // Server-only secrets
    betterAuthSecret:   process.env.BETTER_AUTH_SECRET,
    supabaseServiceKey: process.env.SUPABASE_SERVICE_KEY,
    databaseUrl:        process.env.DATABASE_URL,
    resendApiKey:       process.env.RESEND_API_KEY,
    public: {
      // Browser-safe values only
      supabaseUrl:     process.env.SUPABASE_URL,
      supabaseAnonKey: process.env.SUPABASE_ANON_KEY,
      appUrl:          process.env.NUXT_PUBLIC_APP_URL ?? 'http://localhost:3000',
    },
  },

  typescript: {
    strict: true,
  },
})
