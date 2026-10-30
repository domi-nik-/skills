# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Cursor, …) working in this repo.

## What this repo is

A collection of Agent Skills. Each top-level folder with a `SKILL.md` is one skill; the repo is also a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`, one plugin per skill). The README explains the layout and how users install skills.

## Language

- **English:** code, identifiers, script output, comments, commit messages, README files, ADRs and all other developer documentation (including `docs/`).
- **Skill content** (`SKILL.md`, `references/`, eval prompts) is written in the language of the skill's audience: `webshop-analyse` is German, the other skills are English. Skills answer end users in the user's language.
- Talk to Dominik (the maintainer) in German.

See [ADR 0001](docs/adr/0001-project-language.md).

## Working rules

- **Pull requests only.** Branch per change (`feat/<skill>`, `fix/<skill>`, `test/<topic>`, `docs/<topic>`); never commit to `main` directly.
- **Validate before pushing:** `uv run scripts/validate_skills.py` (or `python3 scripts/validate_skills.py` with PyYAML). CI runs the same check plus every `<skill>/tests` folder.
- **New skill:** folder name = `name:` in `SKILL.md`; add it to the README table (with an install line) and to `marketplace.json`, plus `README.md`, `LICENSE` and `CHANGELOG.md` in the folder. The validator enforces the first three.
- **Changelog:** every user-visible change to a skill gets a line under `## [Unreleased]` in that skill's `CHANGELOG.md`.
- **Evals** live in `<skill>/evals/<case>/` (skill-creator / `claude plugin eval` layout). Running them is billed; ask before you do.
- **Never commit test workspaces** (`*-workspace/`, review pages, `evals/results/`): they can contain analyses of real third-party sites. They are git-ignored; keep it that way.
- **Releases** are tags `<skill>-v<version>`; see `RELEASING.md`.

## Project docs

- `docs/todos.md`: open tasks and open questions.
- `docs/entscheidungen.md`: decisions with date and commit.
- `docs/adr/`: architecture decisions that shape the repo.
