# Decisions

Newest first. Decisions that shape the architecture also get an ADR in `docs/adr/`.

| Date | Decision | Why | Commit |
|---|---|---|---|
| 2026-10-30 | Unit tests for bundled scripts live in `<skill>/tests/` (stdlib `unittest`), run in CI and are left out of release packages. | Tests guard the scripts without shipping dev files to users. | d68cec0 |
| 2026-10-30 | Webshop evals run against the public Sylius community demo (`v2.demo.sylius.com`). | No eval analyses a real company; the demo is meant to be explored. | 73d9ad7 |
| 2026-10-30 | Evals use the case-folder layout (`prompt.md`, `case.yaml`, `graders/`), not `evals.json`; the validator checks the format. | Same files work in skill-creator and `claude plugin eval`; one assertion per file. | 73d9ad7, 18f9351 |
| 2026-10-30 | Nuxt template stays on TypeScript 6.x. | TypeScript 7 breaks `vue-tsc` and `typescript-eslint` (via `@nuxt/eslint`, `@nuxtjs/i18n`). | e20ba19 |
| 2026-10-30 | Nuxt template targets Node 24 (Netlify, CI), `engines` mirrors Nuxt's range. | Nuxt recommends the active LTS (26), but `nodejs26.x` is only a preview on AWS Lambda, which runs Netlify Functions; Node 22 leaves Lambda in April 2027. | e20ba19 |
| 2026-10-30 | The repo is a Claude Code plugin marketplace with one plugin per skill. | Users install only the skills they need with `/plugin install`. | a93acff |
| 2026-10-30 | One validator script (`scripts/validate_skills.py`) for CI and releases; front matter is parsed as YAML. | Catches broken skills on every PR, and folded descriptions (`>-`) no longer break release notes. | e7b6e44 |
| 2026-06-01 | Releases are git tags `<skill>-v<version>`; the tag is the version, `SKILL.md` is not modified. | Each skill is versioned on its own. | 322bedf |
