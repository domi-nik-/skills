# Skills

A collection of [Agent Skills](https://support.claude.com/en/articles/12512176-what-are-skills) I've built — reusable instruction sets that teach Claude (and other compatible agents) how to do specific tasks the way I want them done.

Each skill is a self-contained folder with a `SKILL.md` plus any reference docs and templates. The `SKILL.md` format is an [open standard](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), so these work in Claude (Desktop, Code, API) and other agents that support it.

## Available skills

| Skill | What it does |
|-------|--------------|
| [**bambu-3mf-figurine-edit**](./bambu-3mf-figurine-edit) | Recolor parts, remove unused filament slots and simplify painted Bambu Studio 3MF projects (e.g. MakerLab figurines), and match colors to real Bambu/Polymaker filaments. |
| [**nuxt-supabase-stack**](./nuxt-supabase-stack) | Scaffold and build full-stack Nuxt 4 (Vue 3, SSR) apps on Supabase/Postgres with Drizzle ORM, BetterAuth, Netlify, and Resend — and keep feature work consistent with the stack's conventions. |
| [**webshop-analyse**](./webshop-analyse) | *(German)* Sourced business, website and SEO analysis of a shop or company URL — market & competitors, SWOT, UX/conversion, technical SEO, passive tech/security check, German legal quick wins, social media, Google Ads, marketplaces & distributors, cost levers and a prioritised action plan. |

_More skills will be added here over time._

## What's a skill?

A skill is just a folder:

```
skill-name/
├── SKILL.md        # YAML frontmatter (name, description) + instructions — required
├── references/     # detail docs Claude reads only when needed (optional)
└── assets/         # templates and files used in output (optional)
```

Claude always sees the short `description`, reads the `SKILL.md` body when the skill becomes relevant, and pulls in the reference files only as needed. That keeps the context lean while still carrying deep know-how.

## How to install a skill

### Claude Desktop / claude.ai

Skills run inside Claude's code-execution environment, so enable that first.

1. **Settings → Capabilities** → turn on **Code execution and file creation**. _(On Team/Enterprise plans an owner enables this — and **Skills** — in Organization settings first.)_
2. Go to **Customize → Skills**.
3. Click **“+”** → **“+ Create skill”** → **“Upload a skill”**.
4. Upload the skill as a **ZIP** of its folder (a `.skill` file is just a renamed ZIP — both work).
5. Toggle it **on**. Claude will use it automatically when your request matches; if not, name it explicitly (e.g. *“use my nuxt-supabase-stack skill to …”*).

> **To get the ZIP from this repo:** open a skill's folder, or download the whole repo (green **Code → Download ZIP**) and zip just the skill subfolder. Some skills also ship a ready-made `.skill` on the [Releases](https://github.com/domi-nik-/skills/releases) page.

Uploaded skills are private to your account. On Team/Enterprise plans you can share them org-wide (an owner must enable sharing).

### Claude Code

This repo is a Claude Code plugin marketplace; every skill is its own plugin, so you install only what you need. In Claude Code (2.1.275 or later):

```
/plugin install bambu-3mf-figurine-edit --marketplace domi-nik-/skills
/plugin install nuxt-supabase-stack --marketplace domi-nik-/skills
/plugin install webshop-analyse --marketplace domi-nik-/skills
```

On older versions, add the marketplace first with `/plugin marketplace add domi-nik-/skills`, then `/plugin install <skill-name>@domi-nik-skills`. `/plugin marketplace update domi-nik-skills` pulls in new versions.

To try a skill without installing, copy its folder into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).

## Working on this repo

This repo is the single source of truth for my skills — I keep a local clone and develop every skill inside it rather than in scattered folders.

```bash
git clone https://github.com/domi-nik-/skills.git
cd skills
git checkout -b feat/<skill-name>
```

**Conventions**

- **One folder per skill** at the repo root. The folder name must match the `name:` in its `SKILL.md` (the release workflow enforces this when a tag is pushed). Folder names must not end in `-workspace` — that suffix is reserved for local eval workspaces and is git-ignored.
- **Marketplace:** every skill has an entry in `.claude-plugin/marketplace.json` (checked by the validator) and an install line in the README.
- **Per skill:** `SKILL.md` (required), `README.md`, `LICENSE`, `CHANGELOG.md`, and optionally `references/`, `assets/`, `evals/`. `evals/` is excluded from release packages.
- **Pull requests only.** Every change goes through a branch (`feat/<skill-name>`, `fix/<skill-name>`, `docs/<topic>`) and a reviewed pull request before it is merged into `main`.
- **Test runs stay local.** Eval workspaces (`<skill-name>-workspace/`) and generated review pages are git-ignored — they can contain analyses of real third-party sites and should never be published. Local `.env` files are ignored as well.
- **Validation** runs on every pull request (`.github/workflows/validate.yml`). Run it locally before pushing with `uv run scripts/validate_skills.py` (or `python3 scripts/validate_skills.py` with PyYAML installed).
- **Project docs:** [`AGENTS.md`](./AGENTS.md) (rules for AI agents and contributors), [`docs/todos.md`](./docs/todos.md), [`docs/entscheidungen.md`](./docs/entscheidungen.md) (decisions) and [`docs/adr/`](./docs/adr).
- **Releases** are cut by tagging `<skill-name>-v<version>`; see [RELEASING.md](./RELEASING.md).

## Security note

Only install skills from sources you trust, and skim a skill's contents before enabling it — pay attention to any bundled scripts, network calls, or third-party package installs. The skills here contain instructions and config templates; check each skill's README for details on what it bundles.

## License

[MIT](./LICENSE) — use, adapt, and share freely. Attribution appreciated.
