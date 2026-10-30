# Todos and open questions

## Todos

- [ ] Run the evals for the first time (billed; start with `nuxt-supabase-stack/evals/db-push-would-disable-rls`) and fix assertions that do not discriminate.
- [ ] Release `nuxt-supabase-stack-v1.1.0`: v1.0.0 ships a vulnerable `happy-dom` and fails `npm install` on Node 22.
- [ ] First releases of `bambu-3mf-figurine-edit` and `webshop-analyse`.
- [ ] Nuxt template: move from `@nuxtjs/tailwindcss` (Tailwind 3, stale since 6.14.0) to Tailwind 4 with `@tailwindcss/vite`; update SKILL.md and references.
- [ ] Nuxt template: switch to Node 26 once AWS Lambda's `nodejs26.x` is generally available (planned November 2026).
- [ ] Nuxt template: TypeScript 7 once `vue-tsc` and `typescript-eslint` support it.
- [ ] Pin GitHub Actions to commit SHAs.
- [ ] `bambu3mf.py`: readability (one statement per line, `with open(...)`).
- [ ] GitHub settings: enable "Automatically delete head branches"; delete the stale `fix/ci-validation` branch.

## Open questions

- Should the release notes link the skill's CHANGELOG section only, or also list the evals/tests status?
- `bambu3mf.py`: after Bambu Studio updates, new per-filament keys without the `filament_` prefix must be added to `FILAMENT_KEYS`. Worth a check against a fresh Bambu Studio project from time to time.
