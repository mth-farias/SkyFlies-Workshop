---
name: fly-onboard
description: >-
  Orient in any repo at the start of a session: resolve repo root, read whatever
  of AGENTS.md/CLAUDE.md/README.md exists, check recent git history and working
  tree state, and look for (without assuming) a session/journal/handoff
  convention to read the latest entry from. Produces a short alignment summary -
  never implements. Use when the user starts a new chat cold in a repo, asks to
  "get oriented", "onboard", "catch me up", or "read the handoff", or when you
  need to build context before non-trivial work in an unfamiliar repo.
---

# Onboarding routine

## Reply

First line: `|-CANARY-|` only; answer on the next line. Lead with the answer. Short unless this skill requires a structured dump (`fly-plan` family stay thorough **after** the canary line). At most one subagent. Prefer `/multitask` for one worker when the slice is tool-noisy or multi-file (search, tests, explore, bounded implement) (`run_in_background` if Multitask Mode requires it). Parent writes a self-contained brief, orchestrates, and reviews; the worker does that slice. Keep judgment, review, and tiny or one-shot edits in the parent. Never a second Task while another is running or may still complete. Never declare frozen; only the user may, then interrupt before replace. Never two Task calls in one turn. Never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.

## Machine

Run `machine_probe.py` (JSON stdout) when this skill starts. Resolve in order:

1. `.cursor/skills/fly-setup/machine_probe.py`

If missing, skip and say so; do not fail. Never cwd-relative `../fly-setup/` from a repo root. Occupancy is a hint, not a veto: `gpu_busy` prefer CPU/batch or wait; `gpu_free` GPU work allowed. Do not assume ik owns the GPU. Cursor may HTTP to `127.0.0.1:9292` only when `port_9292` is `up` and the task needs a local LLM. Never intern MCP. Do not register `ask_llama`. Local batch (`pytest -n`, `make -j`, compose) only if the repo already has the tool.

Universal, repo-agnostic session-start orientation. Works in any repo by
detecting its conventions rather than assuming a fixed layout.

## When to use

- First message in a new chat in a repo (especially cold context).
- User asks to "get oriented", "onboard", "catch up", or "read the handoff".

## Workflow

Copy this checklist into your response and check items off as you go:

```
Onboarding progress:
- [ ] 1. Resolve repo root
- [ ] 2. Read behavioral/context docs
- [ ] 3. Check repo state (git log, git status)
- [ ] 4. Find the session/journal/handoff convention (workspace or repo-specific)
- [ ] 5. Reply using the format below
```

### 1. Resolve the repo root

Find the actual project root (look for `.git`, a workspace file,
`pyproject.toml`/`package.json`/etc.). In a multi-root workspace, don't assume
the first folder — confirm which root the user's request is about.

### 2. Read whatever behavioral/context docs exist

Check for, and read what's present (don't error on absence, just note it):

1. `AGENTS.md` (primary Cursor contract)
2. `CLAUDE.md` (if present — still read it)
3. `README.md`

### 3. Check repo state

- `git log --oneline -20` (or similar) for recent history and themes.
- `git status` for uncommitted work — call this out explicitly, it's easy to miss.

### 4. Look for a session/journal/handoff convention — don't assume one

**Prefer `.cursor/workspace/`** when present:

- A `sessionStart` hook may already have injected a **capped** head of
  `handoff.md`. Still read the **full** `.cursor/workspace/handoffs/handoff.md`.
- Skim `.cursor/workspace/context/` (`decisions.md`, `glossary.md`).
- If `.cursor/workspace/journals/JOURNAL.md` exists, read recent entries
  relevant to the task (it is often gitignored).
- Note any active plans in `.cursor/workspace/plans/`.

If `.cursor/workspace/` is missing, fall back (do not create `.cursor/`):

- `.claude/workspace/` (handoffs, context, journals, plans)
- A dated or numbered session-folder pattern (e.g. `*/sessions/<NN>-*/`,
  `docs/journal/`)
- A single handoff file (`HANDOFF.md`, `docs/handoff.md`,
  `.agents/context/handoff.md`, etc.)
- A CHANGELOG or progress doc

If found, read the most recent entry (by name/date sort, not just directory
order). If nothing matches either way, **say so explicitly** rather than
silently skipping — this tells the user whether the repo has this convention
at all, and that `fly-setup` can verify the expected workshop tree.

### 5. Reply format (keep it short)

| Block | Content |
|-------|---------|
| **Repo** | One sentence: what it is, tracked vs local conventions if notable. |
| **History** | 2–4 bullets — themes from git log / session sweep, not a file list. |
| **Now** | 2–5 bullets — current state, constraints, open questions from the latest handoff/journal entry (if any). |
| **Risks** | What could go wrong from skipping this onboarding (wrong root, uncommitted work, stale assumptions). |
| **Next** | Ask what this chat should do, or offer to continue from the last handoff if the user gave no task. |

Example:

```
|-CANARY-|

**Repo:** A Python CLI — tracked surface in git, operator-local knowledge under `.cursor/workspace/` (gitignored journals).
**History:** Ported session skills from a sibling vault; plan family is next.
**Now:** `fly-plan` is in place; no uncommitted changes.
**Risks:** None significant — repo root is unambiguous.
**Next:** What should this chat pick up?
```

## Plan mode

This skill does not open a work package. Do not call SwitchMode. Do not call CreatePlan. Do not write `workspace/plans/`.

## Do not

- Implement pipeline/feature work unless the user explicitly asks — this skill only orients.
- Invent a session/journal convention that doesn't already exist in the repo.
- Skip stating uncommitted changes in `git status`.
- Create `.cursor/` from this skill — `fly-setup` verifies the existing workshop tree.
