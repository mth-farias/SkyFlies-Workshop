---
name: fly-plan
description: >-
  Use when the user wants a detailed plan for a feature, refactor, or
  multi-file change, or names a work package / ticket to plan out. Produce a
  Cursor CreatePlan work package: Suggested model banner, discovery, scope,
  touch list, ordered steps with owner agent, risks, and real verification
  commands from the repo. Ends with "do not execute until user approves" and
  suggests fly-plan-improve. Not from fly-confirm-align — only when the user
  asks to plan.
disable-model-invocation: true
---

# Detailed planning

## Reply

First line: `|-CANARY-|` only; answer on the next line. Lead with the answer. Short unless this skill requires a structured dump (`fly-plan` family stay thorough **after** the canary line). At most one subagent. Prefer `/multitask` for one worker when the slice is tool-noisy or multi-file (search, tests, explore, bounded implement) (`run_in_background` if Multitask Mode requires it). Parent writes a self-contained brief, orchestrates, and reviews; the worker does that slice. Keep judgment, review, and tiny or one-shot edits in the parent. Never a second Task while another is running or may still complete. Never declare frozen; only the user may, then interrupt before replace. Never two Task calls in one turn. Never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.

## Machine

Run `machine_probe.py` (JSON stdout) when this skill starts. Resolve in order:

1. `.cursor/skills/fly-setup/machine_probe.py`

If missing, skip and say so; do not fail. Never cwd-relative `../fly-setup/` from a repo root. Occupancy is a hint, not a veto: `gpu_busy` prefer CPU/batch or wait; `gpu_free` GPU work allowed. Do not assume ik owns the GPU. Cursor may HTTP to `127.0.0.1:9292` only when `port_9292` is `up` and the task needs a local LLM. Never intern MCP. Do not register `ask_llama`. Local batch (`pytest -n`, `make -j`, compose) only if the repo already has the tool.

Universal, repo-agnostic detailed-planning workflow. Produces a plan good
enough to hand to `fly-plan-improve` for critique before anything executes.
Use only when the user asks to plan — not from `fly-confirm-align`.

Do not edit repo code from this skill. Never write into `.claude/workspace/`.

## Plan mode

If not already in Cursor plan mode, call SwitchMode `target_mode_id=plan`
and wait for the user to approve the switch. Then produce the WP with
CreatePlan: first line a level-1 title, then immediately a Suggested model
line, then the rest (bullets not markdown tables, optional todos).

If `.cursor/workspace/plans/` exists, write the same bullet content there.
If that folder is missing, CreatePlan (or chat) only and mention `fly-setup`.

If SwitchMode is unavailable or declined: do not edit repo code; write
`workspace/plans/` when present, else post the plan in chat.

Never call CreatePlan again from `fly-plan-improve` (that skill edits in
place). Prefer `/multitask` for one worker when the slice is tool-noisy
or multi-file; parent writes a self-contained brief. Never click
**Build in Parallel** (fleet).

## Suggested model

Pick the **cheapest** that still covers the hardest step, from Composer 2.5
(cheapest everyday) up through Grok 4.6 `low` / `medium` / `high` /
`xhigh`. User sets the chat/Build picker before execute. Do not auto-switch
the picker. Ladder: see [reference.md](reference.md).

## When to use

- User names a goal, feature, or work package to plan.
- Multi-file or multi-doc change expected.

## Inputs

- User's goal, and any spec/ticket/issue text they point at.
- Explicit **in scope** vs **out of scope** boundaries — ask if not given.

## Workflow

Copy this checklist into your response and check items off as you go:

```
Plan progress:
- [ ] 1. Discovery
- [ ] 2. Scope boundaries
- [ ] 3. Touch list
- [ ] 4. Ordered implementation steps (owner agent)
- [ ] 5. Risks and mitigations
- [ ] 6. Verification commands
- [ ] 7. Execution posture
- [ ] 8. Self-audit loop (reference.md) — repeat until it passes
```

**Step 1 — Discovery.** Read the relevant code/docs; check for an existing spec,
handoff, or decisions log (see `fly-onboard`, including `.cursor/workspace/` if
present) rather than starting cold.

**Step 2 — Scope boundaries.** What's in/out. No silent deferrals — anything
unresolved goes in an explicit **Open questions** or **Follow-up work** section.

**Step 3 — Touch list.** Every file (code, config, docs) the plan expects to
change, with a one-line reason each. Use bullets, not markdown tables.

- `src/auth/session.py` — Add token-refresh check before the existing expiry check
- `tests/test_session.py` — Add a test for the refresh path

**Step 4 — Ordered implementation steps.** File-level, with dependencies between
steps made explicit. **Every step has owner `agent`.** A plan with missing
owners **fails** self-audit. Do not reintroduce intern-shaped owners.

**Step 5 — Risks and mitigations.**

**Step 6 — Verification.** Detect the repo's *actual* test/lint/build commands
(`package.json` scripts, `pyproject.toml`/`tox.ini`/`Makefile`, CI config, etc.)
instead of assuming a fixed gate list. Name the specific command each step
should pass — see the self-audit in [reference.md](reference.md).

**Step 7 — Execution posture.** State owners on the steps (step 4). Keep
architecture, git, and judgment with the agent in this chat. Do not edit repo
code from this skill (plans directory and CreatePlan only).

**Step 8 — Self-audit loop.** Run the checklist in [reference.md](reference.md)
against the plan. Fix whatever fails. Run it again. Only present the plan once
every item passes.

## Output format

- After the title: `**Suggested model:** …`
- Structured plan with **bullets** for the touch list, steps, and verification
  commands (no markdown tables in the Cursor CreatePlan body).
- Each implementation step names owner `agent`.
- Dual-write CreatePlan + `.cursor/workspace/plans/` when that folder exists.
- End with: **"Do not execute until user approves"** and suggest `fly-plan-improve`.

## Do not

- Start coding without an approved plan.
- Silently defer open items — they go in **Open questions** or **Follow-up work**.
- Assume a fixed gate/test command list — detect the repo's real ones.
- Write into `.claude/workspace/` from this skill.
- Reintroduce intern-shaped owners or intern discovery briefs.
- Auto-switch the user's model picker.
- Click **Build in Parallel** (fleet). One `/multitask` worker is allowed.
