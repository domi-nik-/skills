# Changelog

All notable changes to this skill. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow the release tags `nuxt-supabase-stack-v<version>`.

## [Unreleased]

### Security

- `happy-dom` in the template raised to `^21.0.4` (versions up to 21.0.3 allow code execution on the host through an unsanitized import alias, an incomplete fix for CVE-2026-33943).

### Fixed

- A fresh `npm install` of the template no longer crashes on Node 22 / npm 10 (`vite-tsconfig-paths`, whose `tsconfck` dependency is unmaintained, was removed).

### Changed

- All template dependencies updated to a set tested together on Node 22, 24 and 26 (Nuxt 4.6, better-auth 1.7, zod 4, vitest 5, postgres 4). TypeScript stays on 6.x, because TypeScript 7 breaks `vue-tsc` and `typescript-eslint`.
- Netlify and CI templates use Node 24; `package.json` declares Nuxt's supported Node range in `engines`.

### Added

- Templates `tsconfig.json`, `vitest.config.ts` and `eslint.config.mjs`, which SKILL.md already referred to.
- Node.js version guidance in `references/project-setup.md`.

## [1.0.0] - 2026-06-01

- First release.
