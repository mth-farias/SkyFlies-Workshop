---
name: fly-plan-improve
description: >-
  Use after fly-plan, whenever the user pastes a plan for critique, asks to
  revise/tighten a plan, or before any "execute this" / "implement the plan"
  message. Review a detailed plan, edit it in place, then a final
  model-selection revision and multitask assignment pass: Composer 2.5
  cheapest; Grok effort only as high as the hardest step; prefer one
  /multitask worker for noisy or multi-file slices (main orchestrates;
  never Build in Parallel). Never
  executes. Not fly-review-plan.
disable-model-invocation: true
---

# Plan improve (edit the plan, not the repo)

## Reply

First line: `|-CANARY-|` only; answer on the next line. Lead with the answer. Short unless this skill requires a structured dump (`fly-plan` family stay thorough **after** the canary line). At most one subagent. Prefer `/multitask` for one worker when the slice is tool-noisy or multi-file (search, tests, explore, bounded implement) (`run_in_background` if Multitask Mode requires it). Parent writes a self-contained brief, orchestrates, and reviews; the worker does that slice. Keep judgment, review, and tiny or one-shot edits in the parent. Never a second Task while another is running or may still complete. Never declare frozen; only the user may, then interrupt before replace. Never two Task calls in one turn. Never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.

## Machine

Run `machine_probe.py` (JSON stdout) when this skill starts. Resolve in order:

1. `.cursor/skills/fly-setup/machine_probe.py`

If missing, skip and say so; do not fail. Never cwd-relative `../fly-setup/` from a repo root. Occupancy is a hint, not a veto: `gpu_busy` prefer CPU/batch or wait; `gpu_free` GPU work allowed. Do not assume ik owns the GPU. Cursor may HTTP to `127.0.0.1:9292` only when `port_9292` is `up` and the task needs a local LLM. Never intern MCP. Do not register `ask_llama`. Local batch (`pytest -n`, `make -j`, compose) only if the repo already has the tool.

Universal, repo-agnostic critique **and revision** of an implementation plan.
Companion to `fly-plan`. Unlike a pure review, this skill fixes what it finds —
the plan document leaves in a better state than it started, not just annotated.

**This is not `fly-review-plan`.** Improve edits the **plan document** before
execute. Review audits **landed work** after execute.

Edit the plan file only. Never execute the work package from this skill.

## Plan mode

If not already in plan mode, SwitchMode to `plan` and wait. Then edit the
existing Cursor plan file and/or `workspace/plans/` in place. Never call
CreatePlan (it would spawn a new plan). Ensure the plan still starts with
**Suggested model**; run the final model-selection revision (raise or lower).
Do not auto-switch the picker.

## When to use

- After `fly-plan`, or when the user pastes a plan for critique.
- User asks to revise/tighten/edit a plan before executing it.
- Before any "execute WP1" / "implement the plan" message from the user.

## Critical rule

**Do not execute** the implementation the plan describes, or run gates beyond
read-only verification, until the user explicitly says to execute (e.g. "go
ahead", "implement it"). Editing the *plan document itself* — fixing gaps,
adding missed detail, tightening scope — is this skill's job and does not
require separate approval; only running the plan's actual steps does.

## Review axes

- **Completeness** — All deliverables, touch list, doc updates covered
- **Internal consistency** — No contradicting the plan or a handoff/decisions doc
- **Verification coverage** — Named commands actually exist in the repo
- **Scope creep** — No unapproved extra work
- **Execution posture** — Every step has owner `agent`
- **Hygiene** — Matches repo conventions (style, commit policy, forbidden paths)
- **Suggested model** — Banner present; cheapest that covers the hardest step
- **Multitask assignment** — Main orchestrates; at most one `/multitask` worker written on the plan

See [reference.md](reference.md) for the detail behind each axis.

## Workflow

Copy this checklist into your response and check items off as you go:

```
Revision progress:
- [ ] 1. Review against every axis
- [ ] 2. Edit the plan in place (or repost revised text if it's chat-only)
- [ ] 3. Confirm no fixable finding was left as just a comment
- [ ] 4. Final model-selection revision
- [ ] 5. Final multitask assignment pass
- [ ] 6. Report the diff-style fix list
```

## Steps

1. **Review** the plan against every axis above; build the findings list.
2. **Edit the plan in place** — if it's a file (typically under
   `.cursor/workspace/plans/` or the Cursor plan file), apply every fix
   directly. If the plan only exists as chat text, post the fully revised
   plan text back. Never write into `.claude/workspace/`.
3. **Never leave a finding as just a comment** if it's fixable in the document
   itself — only genuinely open questions for the user get left as explicit
   rows, not silently dropped or just noted.
4. **Final model-selection revision** — after other edits, walk every
   remaining step from Composer 2.5 up the Grok 4.6 effort ladder. Set
   **Suggested model** to the **cheapest** that still covers the hardest
   step (may lower a too-hot banner). One banner only. User sets the
   chat/Build picker. Do not auto-switch the picker.
5. **Final multitask assignment pass** — mark steps serial vs independent.
   Prefer one `/multitask` worker for noisy or multi-file slices. One
   background Task OK if Multitask Mode requires `run_in_background`.
   Write **Build:** prefer one `/multitask` worker for noisy or multi-file
   slices; parent briefs and reviews (main orchestrates). Do not click
   **Build in Parallel**. Do not emit a `/multitask` ban for this WP.
   Do not emit “sequential, one worker” as a ban.
   Independent-looking steps stay in one agent; do not emit a fleet roster.
6. **Report** what changed (short diff-style summary), not the entire plan again.

## Output format

1. **Verdict after edits:** `REVISED` (changes applied) or `APPROVED` (no changes needed)
2. **Axes table** (pass/fail per axis, pre-edit)
3. **Numbered fix list** — what was changed in the plan and why
4. Line: **"Do not execute until user approves."** After execute, suggest `fly-review-plan`.

See [reference.md](reference.md) for the axes detail and an example output block.
