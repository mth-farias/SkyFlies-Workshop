# handoff

Living session snapshot. Update in place at session end (`fly-handoff`).

| Field | Value |
|-------|--------|
| **Date** | 2026-09-13 |
| **HEAD** | `8ca56ef` on `master` — https://github.com/mth-farias/SkyFlies-Workshop |
| **Active focus** | Step 1 repo bootstrap |
| **Next session** | Stay on `workshop/01-repo-bootstrap` |

## TL;DR

1. This repo is **SkyFlies-Workshop**, the student tree. Do not edit a
   sibling SkyFlies instructor repo.
2. Students work from `workshop/`. Step 1 creates `.venv` (gitignored) and
   tracks `fly-*` skills, rules, and hooks.
3. Public GitHub: https://github.com/mth-farias/SkyFlies-Workshop
4. Generated/local stay gitignored: `.venv/`, `data/**` except
   `data/README.md`, Cursor journals/artifacts/archive/plan bodies.

## What not to touch

- Do not pip into the host interpreter; use repo `.venv`
- Do not copy skills into `~/.cursor/skills`
- Do not gitignore all of `.cursor/` (skills/rules/hooks are tracked)
- Commit only when asked

## Starter prompt (copy-paste)

```
Read AGENTS.md, then .cursor/workspace/handoffs/handoff.md, then
.cursor/workspace/context/. Skills: fly-onboard, fly-confirm-align,
fly-plan, fly-plan-improve, fly-review-plan, fly-handoff, fly-setup.
Reply contract: first line |-CANARY-| only; answer on next line.
Confirm align before large diffs. Commit only when asked.
This repo is SkyFlies-Workshop. Write only here.
Python: workshop/01-repo-bootstrap runners create .venv.
```
