# Releasing a skill

Each skill in this repo is released independently by pushing a git tag. The tag
is the **source of truth** for the version — `SKILL.md` is never modified by the
release process.

## Tag format

```
<skill-name>-v<version>
```

- `<skill-name>` must exactly match a skill folder at the repo root **and** the
  `name:` field in that skill's `SKILL.md`.
- `<version>` is semantic versioning: `MAJOR.MINOR.PATCH`, optionally with a
  pre-release suffix (e.g. `-rc.1`).

Examples:

| Tag | Result |
|---|---|
| `nuxt-supabase-stack-v1.0.0` | Stable release of `nuxt-supabase-stack` |
| `nuxt-supabase-stack-v1.1.0-rc.1` | Pre-release (flagged as such on GitHub) |

## How to cut a release

```bash
git tag nuxt-supabase-stack-v1.0.0
git push origin nuxt-supabase-stack-v1.0.0
```

Pushing the tag triggers `.github/workflows/release-skill.yml`, which:

1. Parses the skill name and version from the tag.
2. Validates the skill with `scripts/validate_skills.py` — folder exists,
   `SKILL.md` front matter parses as YAML, `name:` matches the folder,
   `description:` is present and at most 1024 characters, and relative links
   resolve. The release fails fast if any check fails, so a broken skill is
   never published. The same checks run on every pull request
   (`.github/workflows/validate.yml`), so problems usually surface earlier.
3. Packages the skill folder (excluding `evals/`, `tests/`, `.git`, `.DS_Store`) as both
   `<skill>-v<version>.zip` and `<skill>-v<version>.skill`.
4. Creates a GitHub Release for the tag with both files attached and notes
   pulled from the skill's description.

## Installing a released skill

Download `<skill>-v<version>.skill` from the release and open it in
Claude/Cowork, or unzip the `.zip` into your skills directory.
