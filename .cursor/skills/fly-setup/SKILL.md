---
name: fly-setup
description: >-
  Verify this SkyFlies-Workshop Cursor tree: AGENTS.md, workshop/01-repo-bootstrap,
  tracked .cursor/skills fly-* skills, and that .gitignore does not ignore all of
  .cursor/. Does not scaffold a third generic repo. Use after clone, when checking
  workshop setup, or when the user asks whether Cursor conventions are in place.
disable-model-invocation: true
---

# fly-setup

## Reply

First line: `|-CANARY-|` only; answer on the next line. Lead with the answer. Short unless this skill requires a structured dump (`fly-plan` family stay thorough **after** the canary line). At most one subagent. Prefer `/multitask` for one worker when the slice is tool-noisy or multi-file (search, tests, explore, bounded implement) (`run_in_background` if Multitask Mode requires it). Parent writes a self-contained brief, orchestrates, and reviews; the worker does that slice. Keep judgment, review, and tiny or one-shot edits in the parent. Never a second Task while another is running or may still complete. Never declare frozen; only the user may, then interrupt before replace. Never two Task calls in one turn. Never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.

## Machine

Run `machine_probe.py` (JSON stdout) when this skill starts. Resolve in order:

1. `.cursor/skills/fly-setup/machine_probe.py`

If missing, skip and say so; do not fail. Never cwd-relative `../fly-setup/` from a repo root. Occupancy is a hint, not a veto: `gpu_busy` prefer CPU/batch or wait; `gpu_free` GPU work allowed. Do not assume ik owns the GPU. Cursor may HTTP to `127.0.0.1:9292` only when `port_9292` is `up` and the task needs a local LLM. Never intern MCP. Do not register `ask_llama`. Local batch (`pytest -n`, `make -j`, compose) only if the repo already has the tool.

Verifier for **this** SkyFlies-Workshop tree. The other `fly-*` skills assume
the layout below. Do not scaffold a third generic repo. Do not gitignore all
of `.cursor/`. Skills and rules stay tracked; only session noise under
`.cursor/workspace/` is ignored.

## When to use

- After clone, or when checking that workshop Cursor conventions are present.
- User asks whether setup is complete or why skills/hooks are missing.

## What it verifies

```
AGENTS.md
workshop/01-repo-bootstrap/
.cursor/skills/fly-onboard/
.cursor/skills/fly-confirm-align/
.cursor/skills/fly-plan/
.cursor/skills/fly-plan-improve/
.cursor/skills/fly-review-plan/
.cursor/skills/fly-handoff/
.cursor/skills/fly-setup/
.gitignore   (must NOT ignore all of .cursor/)
```

Expected `fly-*` skill ids (folders + `name:` in each `SKILL.md`):
`fly-onboard`, `fly-confirm-align`, `fly-plan`, `fly-plan-improve`,
`fly-review-plan`, `fly-handoff`, `fly-setup`.

`.gitignore` should ignore session noise (journals, artifacts, archive,
plans content) while keeping `.cursor/skills/`, `.cursor/rules/`, and
hooks tracked. A line that ignores the entire `.cursor/` tree is a **fail**.

## Workflow

Copy this checklist into your response and check items off as you go:

```
Setup progress:
- [ ] 1. Resolve this workshop repo root
- [ ] 2. Check AGENTS.md
- [ ] 3. Check workshop/01-repo-bootstrap
- [ ] 4. Check tracked .cursor/skills fly-*
- [ ] 5. Check .gitignore does not ignore all of .cursor/
- [ ] 6. Report pass/fail per check
```

**Step 1 — Resolve the repo root.** Confirm this is SkyFlies-Workshop (write
root). Do not treat a sibling instructor tree as the target.

**Step 2 — `AGENTS.md`.** Present at repo root. Note if missing; do not invent
a generic contract.

**Step 3 — `workshop/01-repo-bootstrap`.** Directory (or lesson path) exists.
If missing, report it; do not add extra folders under `workshop/`.

**Step 4 — Tracked `fly-*` skills.** Each expected folder exists under
`.cursor/skills/` with `SKILL.md` whose frontmatter `name:` matches the
folder. Report missing ids. Do not copy skills from the home skills tree.

**Step 5 — Gitignore.** Read `.gitignore`. **Fail** if it ignores all of
`.cursor/` (a full-tree `.cursor/` or `.cursor` ignore). **Pass** if only
workspace session paths are ignored and skills/rules/hooks remain eligible
to track. Do not add a full-tree `.cursor/` ignore. Do not run
`git rm -r --cached .cursor`.

**Step 6 — Report** each check as pass/fail. Do not scaffold missing trees
into a third repo. Do not write `~/.cursor/skills`.

## Plan mode

This skill does not open a work package. Do not call SwitchMode. Do not call CreatePlan. Do not write `workspace/plans/`.

## Do not

- Scaffold a third generic repo or a generic `.cursor/` from templates.
- Gitignore all of `.cursor/`.
- Overwrite an existing `AGENTS.md`.
- Delete or rewrite an existing `CLAUDE.md`.
- Write `~/.cursor/skills` or copy instructor home skills into this repo.
- Create `JOURNAL.md` from this skill.
- Add extra lesson folders under `workshop/`.

## See also

- `fly-confirm-align` is chat-only alignment; the user starts `/fly-plan`.
- `fly-onboard` reads `.cursor/workspace/handoffs/handoff.md` and `context/`.
- `fly-plan` uses Cursor CreatePlan + `workspace/plans/` (Suggested model banner).
- `fly-plan-improve` edits the plan document before execute.
- `fly-review-plan` audits landed work after execute.
- `fly-handoff` updates `handoff.md` in place, appends `journals/JOURNAL.md`,
  archives completed plans, wipes `artifacts/`.
- Prefer `/multitask` for one worker on noisy or multi-file slices; never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.
