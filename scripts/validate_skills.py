#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Validate the skills in this repo.

Usage:
  validate_skills.py [SKILL ...]          validate the given skills (default: all)
  validate_skills.py --field KEY SKILL    print one front-matter field (for release notes)

Checks per skill:
  - folder has a SKILL.md that starts with YAML front matter
  - front matter parses and has `name` and `description` (both strings)
  - `name` matches the folder name, folder does not end in `-workspace`
  - `description` is at most 1024 characters
  - the skill is listed in the root README table
  - relative links in the skill's Markdown files point to existing files
  - bundled Python scripts parse
  - eval case folders under evals/ follow the format `claude plugin eval` and
    skill-creator read (prompt.md, case.yaml, graders/, optional files/)
and once for the repo: .claude-plugin/marketplace.json lists exactly the skills
that exist, each as its own plugin pointing at its folder.

Exits non-zero with GitHub Actions `::error::` lines if any check fails.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MAX_DESCRIPTION = 1024
# [text](target); links inside code blocks and inline code are ignored
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
CASE_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
RESERVED_CASE_NAMES = {"results", "mocks", "node_modules", "files", "true", "false", "null"}
PROMPT_KEYS = {"tags", "max_turns", "timeout_seconds", "allowed_tools"}


def error(path, msg):
    rel = path.relative_to(ROOT) if path.is_absolute() else path
    print(f"::error file={rel}::{msg}")


def front_matter(md):
    """Return the parsed YAML front matter of a Markdown file, or raise ValueError."""
    text = md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("must begin with YAML front matter ('---')")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        raise ValueError("front matter is not closed with '---'") from None
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as e:
        raise ValueError(f"front matter is not valid YAML: {e}") from None
    if not isinstance(data, dict):
        raise ValueError("front matter must be a YAML mapping")
    return data


def skill_dirs():
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def check_links(md):
    ok = True
    text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", md.read_text(encoding="utf-8")))
    for target in LINK_RE.findall(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
            continue  # external URL, mailto: or in-page anchor
        path = target.split("#", 1)[0]
        if path and not (md.parent / path).exists():
            error(md, f"broken relative link '{target}'")
            ok = False
    return ok


def check_eval_cases(skill):
    """Each folder under evals/ is one test case in the `claude plugin eval` layout.
    A malformed case fails to load there, so catch it here."""
    ok = True
    evals = skill / "evals"
    if not evals.is_dir():
        return True
    for case in sorted(p for p in evals.iterdir() if p.is_dir()):
        def bad(path, msg):
            nonlocal ok
            error(path, msg)
            ok = False

        if not CASE_NAME_RE.match(case.name) or case.name in RESERVED_CASE_NAMES:
            bad(case, f"invalid case name '{case.name}' (lowercase, digits, hyphens; not reserved)")
        prompt = case / "prompt.md"
        if not prompt.exists():
            bad(case, "case has no prompt.md")
        else:
            try:
                unknown = set(front_matter(prompt)) - PROMPT_KEYS
                if unknown:
                    bad(prompt, f"unknown settings {sorted(unknown)} (allowed: {sorted(PROMPT_KEYS)})")
            except ValueError as e:
                bad(prompt, str(e))
        spec_path = case / "case.yaml"
        try:
            spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
            if not isinstance(spec, dict):
                raise ValueError("case.yaml must be a YAML mapping")
        except (OSError, ValueError, yaml.YAMLError) as e:
            bad(spec_path, f"cannot read case.yaml: {e}")
            spec = {}
        if spec and spec.get("schema_version") != "1.1":
            bad(spec_path, "schema_version must be the quoted string \"1.1\"")
        if spec and spec.get("name") != case.name:
            bad(spec_path, f"name '{spec.get('name')}' does not match folder '{case.name}'")
        graders = sorted((case / "graders").glob("*.md"))
        if not graders:
            bad(case, "case has no graders (a case without one fails to load)")
        for g in graders:
            try:
                if "type" not in front_matter(g):
                    bad(g, "grader front matter has no 'type'")
            except ValueError as e:
                bad(g, str(e))
        script = (spec.get("context") or {}).get("scaffold_script") if spec else None
        if (case / "files").is_dir() and not script:
            bad(spec_path, "case has files/ but no context.scaffold_script to place them")
        if script and not (case / script).exists():
            bad(spec_path, f"scaffold_script '{script}' does not exist")
    return ok


def validate(skill, readme_text):
    ok = True
    skill_md = skill / "SKILL.md"
    if not skill.is_dir():
        error(skill, f"no skill folder named '{skill.name}' at the repo root")
        return False
    if not skill_md.exists():
        error(skill_md, "SKILL.md is missing")
        return False
    if skill.name.endswith("-workspace"):
        error(skill, "skill folders must not end in '-workspace' (reserved for eval workspaces)")
        ok = False

    try:
        fm = front_matter(skill_md)
    except ValueError as e:
        error(skill_md, str(e))
        return False

    name, desc = fm.get("name"), fm.get("description")
    if not isinstance(name, str) or not name.strip():
        error(skill_md, "front matter has no 'name' field")
        ok = False
    elif name != skill.name:
        error(skill_md, f"name '{name}' does not match folder '{skill.name}'")
        ok = False
    if not isinstance(desc, str) or not desc.strip():
        error(skill_md, "front matter has no 'description' field")
        ok = False
    elif len(desc) > MAX_DESCRIPTION:
        error(skill_md, f"description is {len(desc)} characters (max {MAX_DESCRIPTION})")
        ok = False

    if f"](./{skill.name})" not in readme_text:
        error(ROOT / "README.md", f"skill '{skill.name}' is not listed in the README table")
        ok = False

    for md in sorted(skill.rglob("*.md")):
        ok &= check_links(md)

    ok &= check_eval_cases(skill)

    for script in sorted(skill.rglob("*.py")):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except SyntaxError as e:
            error(script, f"does not compile: {e.msg} (line {e.lineno})")
            ok = False

    if ok:
        print(f"ok  {skill.name}")
    return ok


def check_marketplace(skills):
    """Every skill must be its own plugin in marketplace.json, and vice versa."""
    path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        plugins = json.loads(path.read_text(encoding="utf-8"))["plugins"]
    except (OSError, ValueError, KeyError) as e:
        error(path, f"cannot read plugins: {e}")
        return False
    ok = True
    listed = set()
    for p in plugins:
        name = p.get("name")
        listed.add(name)
        if p.get("skills") != [f"./{name}"]:
            error(path, f"plugin '{name}' must have \"skills\": [\"./{name}\"]")
            ok = False
        if not (ROOT / str(name) / "SKILL.md").exists():
            error(path, f"plugin '{name}' has no skill folder")
            ok = False
    for name in sorted({s.name for s in skills} - listed):
        error(path, f"skill '{name}' is missing from marketplace.json")
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser(description="Validate skills in this repo.")
    ap.add_argument("skills", nargs="*", help="skill folder names (default: all)")
    ap.add_argument("--field", help="print this front-matter field of the single given skill and exit")
    a = ap.parse_args()

    if a.field:
        if len(a.skills) != 1:
            ap.error("--field needs exactly one skill")
        value = front_matter(ROOT / a.skills[0] / "SKILL.md").get(a.field, "")
        print(" ".join(str(value).split()))
        return 0

    skills = [ROOT / s for s in a.skills] if a.skills else skill_dirs()
    if not skills:
        print("::error::no skills found")
        return 1
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    ok = True
    for skill in skills:
        ok &= validate(skill, readme_text)
    ok &= check_links(ROOT / "README.md")
    if not a.skills:
        ok &= check_marketplace(skills)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
