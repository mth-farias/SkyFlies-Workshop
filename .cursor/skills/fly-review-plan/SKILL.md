---
name: fly-review-plan
description: >-
  Use after execute, when the user asks to review what landed, or before
  calling the WP done. Audit landed work against the plan (or a better bar)
  for completeness, regressions, and real verification. Optional bounded
  smoke with Read/Grep/Shell on a named repo path. Patch P0/P1 in the repo;
  still no git commit unless the user asked. Not fly-plan-improve (that edits
  the plan document before execute).
disable-model-invocation: true
---

# Plan review (audit landed work)

## Reply

First line: `|-CANARY-|` only; answer on the next line. Lead with the answer. Short unless this skill requires a structured dump (`fly-plan` family stay thorough **after** the canary line). At most one subagent. Prefer `/multitask` for one worker when the slice is tool-noisy or multi-file (search, tests, explore, bounded implement) (`run_in_background` if Multitask Mode requires it). Parent writes a self-contained brief, orchestrates, and reviews; the worker does that slice. Keep judgment, review, and tiny or one-shot edits in the parent. Never a second Task while another is running or may still complete. Never declare frozen; only the user may, then interrupt before replace. Never two Task calls in one turn. Never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.

## Machine

Run `machine_probe.py` (JSON stdout) when this skill starts. Resolve in order:

1. `.cursor/skills/fly-setup/machine_probe.py`

If missing, skip and say so; do not fail. Never cwd-relative `../fly-setup/` from a repo root. Occupancy is a hint, not a veto: `gpu_busy` prefer CPU/batch or wait; `gpu_free` GPU work allowed. Do not assume ik owns the GPU. Cursor may HTTP to `127.0.0.1:9292` only when `port_9292` is `up` and the task needs a local LLM. Never intern MCP. Do not register `ask_llama`. Local batch (`pytest -n`, `make -j`, compose) only if the repo already has the tool.

Universal, repo-agnostic post-implement audit. Companion to `fly-plan` and
`fly-plan-improve`.

**This is not `fly-plan-improve`.** Improve edits the **plan document** before
execute. Review audits **landed work** after execute and patches P0/P1.

Keep architecture and git judgment in this chat. Optional bounded smoke uses
Read/Grep/Shell on a named repo path.

## Plan mode

This skill does not open a work package. Do not call SwitchMode. Do not call CreatePlan. Do not write `workspace/plans/`.

## When to use

- After the user approved and the WP was implemented.
- User asks to review what landed, check for gaps, or "is this done".
- After a WP, before `fly-handoff` if landed work has not been audited.

## Critical rule

Patch **P0/P1** in the repo. Do **not** `git commit` / `git push` unless the
user asked. Do not rewrite historical research files the plan marked out of
scope.

## Review axes

- **Landed vs plan** — Touch-list files exist with the intended change
- **Better bar** — If the plan was wrong, the better behavior wins
- **Verification** — Named commands actually ran (or you run them now)
- **Bounded smoke** — Optional Read/Grep/Shell on a named repo path
- **Regressions** — Nearby tests/docs/skills still agree
- **Hygiene** — No secrets; no commit unless asked

See [reference.md](reference.md) for the detail behind each axis.

## Workflow

Copy this checklist into your response and check items off as you go:

```
Review progress:
- [ ] 1. Compare landed tree to the plan (or better bar)
- [ ] 2. Run real verification commands
- [ ] 3. Optional bounded smoke (named repo path)
- [ ] 4. Patch P0/P1
- [ ] 5. Report findings; suggest fly-handoff
```

## Steps

1. **Compare** the working tree to the plan's touch list and steps. List
   gaps, extras, and "plan was wrong, this is better."
2. **Verify** with the repo's real commands (same detection as `fly-plan`).
3. **Bounded smoke** when it helps (one named repo path). Confirm claims
   yourself.
4. **Patch P0/P1** (broken gates, missing in-scope files, leftover old skill
   dirs when the WP renamed them, docs that still teach the old id). Defer P2
   to Follow-up unless the user wants them now.
5. **Report** verdict, axes, patches applied, remaining follow-up. If the
   user is closing, suggest `fly-handoff`.

## Output format

1. **Verdict:** `PASS` / `FIXED` / `FAIL` (P0 still open)
2. **Axes table**
3. **Numbered findings** — what was wrong, what you patched, what remains
4. Suggest `fly-handoff` when the WP is actually done
