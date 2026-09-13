---
name: fly-confirm-align
description: >-
  Use when the user invokes /fly-confirm-align, says "confirm align" / "same
  page", or at the start of non-trivial work (multi-step, multi-file, policy,
  or more than one valid approach). Chat-only alignment: summarize findings
  and user instructions, then stop. Not a plan. Ask blocking doubts with the
  AskQuestion tool. Low verbosity. Skip trivial one-step asks and skip if
  they already confirmed this turn.
---

# Confirm align

## Reply

First line: `|-CANARY-|` only; answer on the next line. Lead with the answer. Short unless this skill requires a structured dump (`fly-plan` family stay thorough **after** the canary line). At most one subagent. Prefer `/multitask` for one worker when the slice is tool-noisy or multi-file (search, tests, explore, bounded implement) (`run_in_background` if Multitask Mode requires it). Parent writes a self-contained brief, orchestrates, and reviews; the worker does that slice. Keep judgment, review, and tiny or one-shot edits in the parent. Never a second Task while another is running or may still complete. Never declare frozen; only the user may, then interrupt before replace. Never two Task calls in one turn. Never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.

## Machine

Run `machine_probe.py` (JSON stdout) only when the work looks compute-heavy (tests, Docker, models); skip typo/one-file. Read-only Shell for the probe is allowed; still **Stop** after alignment. No GPU jobs from align. Resolve in order:

1. `.cursor/skills/fly-setup/machine_probe.py`

If missing, skip and say so; do not fail. Never cwd-relative `../fly-setup/` from a repo root. Occupancy is a hint, not a veto: `gpu_busy` prefer CPU/batch or wait; `gpu_free` GPU work allowed. Do not assume ik owns the GPU. Cursor may HTTP to `127.0.0.1:9292` only when `port_9292` is `up` and the task needs a local LLM. Never intern MCP. Do not register `ask_llama`. Local batch (`pytest -n`, `make -j`, compose) only if the repo already has the tool.

Any doubts or clarifications make sure to ask user, if possible prefer always
to use the questions UX feature that cursor has to make it easier for user to
reply. Be aware and optimize token usage. Make sure to use low verbosity,
such that the response is user friendly and not overwhelming.

## When

- User runs `/fly-confirm-align` (or equivalent phrasing).
- Auto: before implementing or planning non-trivial work.
- Skip: typo/one-file obvious fix; onboard-only; already confirmed this turn.

## Workflow

1. Read enough to know how the request fits (repo root, `AGENTS.md` if
   present, the files or area named in the request). Do not do a full
   `fly-onboard` unless the session is cold and you lack that context.
2. Restate **in chat only**: goal, user instructions, findings from the skim,
   and out of scope. No recap dump. No plan-shaped sections.
3. If anything is ambiguous or has more than one reasonable choice, call
   `AskQuestion`. Prefer that tool over a numbered list in chat.
4. **Stop.** Do not edit, scaffold, commit, or start `fly-plan` until the
   user confirms (or answers the questions). The user decides when to invoke
   `/fly-plan`.

## Reply shape

```
**Goal:** …
**Instructions:** …
**Findings:** …
**Out of scope:** …
```

Then questions (AskQuestion) or one line: the user can refine in chat or
invoke `/fly-plan` when they want a plan.

## Plan mode

This skill does not open a work package. Do not call SwitchMode. Do not call CreatePlan. Do not write `workspace/plans/`.

## Do not

- Write a plan file or emit a touch matrix, implementation steps, or
  verification-command tables.
- Mix a research dump and a plan into this turn.
- Call SwitchMode or CreatePlan.
