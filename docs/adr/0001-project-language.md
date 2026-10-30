# ADR 0001: Project language

- Status: accepted
- Date: 2026-10-30

## Context

The maintainer works in German, the skills are published on GitHub for a wider audience, and one skill (`webshop-analyse`) is built for German-speaking customers, with German legal and market content.

## Decision

- Code, comments, script output, commit messages and developer documentation are in English.
- A skill's own content (`SKILL.md`, `references/`, eval prompts) follows its audience: German for `webshop-analyse`, English for the others. Skills answer users in the user's language.
- Conversations with the maintainer are in German.

## Consequences

Contributors and agents can read every tool and doc without German, while the German skill keeps its domain terms (Impressum, Widerrufsbelehrung, …) unchanged. `AGENTS.md` carries these rules for all AI tools.
