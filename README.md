# Skills

A collection of [Agent Skills](https://support.claude.com/en/articles/12512176-what-are-skills) I've built — reusable instruction sets that teach Claude (and other compatible agents) how to do specific tasks the way I want them done.

Each skill is a self-contained folder with a `SKILL.md` plus any reference docs and templates. The `SKILL.md` format is an [open standard](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), so these work in Claude (Desktop, Code, API) and other agents that support it.

## Available skills

| Skill | What it does |
|-------|--------------|
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

Point Claude Code at a skill folder, or install it from this repo as a plugin/marketplace source. See each skill's own README for specifics.

## Working on this repo

This repo is the single source of truth for my skills — I keep a local clone and develop every skill inside it rather than in scattered folders.

```bash
git clone https://github.com/domi-nik-/skills.git
cd skills
git checkout -b feat/<skill-name>
```

**Conventions**

- **One folder per skill** at the repo root. The folder name must match the `name:` in its `SKILL.md` (the release workflow enforces this when a tag is pushed). Folder names must not end in `-workspace` — that suffix is reserved for local eval workspaces and is git-ignored.
- **Per skill:** `SKILL.md` (required), `README.md`, `LICENSE`, and optionally `references/`, `assets/`, `evals/`. `evals/` is excluded from release packages.
- **Pull requests only.** Every change goes through a branch (`feat/<skill-name>`, `fix/<skill-name>`, `docs/<topic>`) and a reviewed pull request before it is merged into `main`.
- **Test runs stay local.** Eval workspaces (`<skill-name>-workspace/`) and generated review pages are git-ignored — they can contain analyses of real third-party sites and should never be published. Local `.env` files are ignored as well.
- **Releases** are cut by tagging `<skill-name>-v<version>`; see [RELEASING.md](./RELEASING.md).

## Security note

Only install skills from sources you trust, and skim a skill's contents before enabling it — pay attention to any bundled scripts, network calls, or third-party package installs. The skills here contain instructions and config templates; check each skill's README for details on what it bundles.

## License

[MIT](./LICENSE) — use, adapt, and share freely. Attribution appreciated.
