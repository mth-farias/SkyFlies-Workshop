# AGENTS.md

Project-specific guidance for Cursor in **SkyFlies-Workshop**. Keep this
file under 200 lines. Procedures belong in `fly-*` skills, not here.

This folder is the **only write root**. A sibling instructor tree named
SkyFlies is lookup-only. Do not edit it from a student session.

## Reply contract

- First line of every reply: `|-CANARY-|` only (context-degradation
  tripwire). Do not decorate it. Start the answer on the next line. If
  you drop it, say so and recommend a new chat after handoff.
- Lead with the answer. No preamble, no recap of the question, no "I'll
  now…".
- Short by default; complete sentences. Expand only when asked or when a
  decision needs evidence.
- Cite paths; do not paste large files or tool traces.

## Clarify

- Any doubts or clarifications: ask the user before acting. Prefer the
  AskQuestion tool over a chat list.
- Non-trivial work: `fly-confirm-align` first (chat-only alignment;
  wait). The user starts `/fly-plan` when they want a plan.
- Low verbosity. Optimize token use. Do not overwhelm.

## Subagents

- At most one subagent at a time. Prefer `/multitask` for one worker when
  the slice is tool-noisy or multi-file (search, tests, explore, bounded
  implement) (`run_in_background` if Multitask Mode requires it). Parent
  writes a self-contained brief, orchestrates, and reviews. Keep
  judgment, review, and tiny or one-shot edits in the parent. Never
  launch a second while another is running or may still complete.
- Task brief and worker return:
  `.cursor/rules/session-multitask-coordination.mdc` (worker has no chat
  history; parent sees only the final message).
- Do not decide a subagent is frozen. Quiet or slow output is not a
  freeze.
- Only the user may declare a freeze. Then interrupt/stop that agent
  first; only after it is stopped, launch a replacement if they asked.
- Never click **Build in Parallel** (fleet).

## What this project is

SkyFlies Workshop is a standalone student repo. Work from `workshop/`
using open data and AI tools. Files under `data/` except `data/README.md`
are gitignored.

## Working conventions

- Align in chat with `fly-confirm-align`. The user starts `fly-plan`
  then `fly-plan-improve`. After execute, `fly-review-plan`. Close with
  `fly-handoff`.
- Python and JavaScript follow Google style (`STYLE.md`,
  `.cursor/rules/google-style.mdc`).
- Verify before calling anything done: run the actual tests/build/lint,
  don't assume.
- Surgical changes — touch only what the task requires; match existing
  style; no drive-by refactors.
- The human owns `git commit` / `git push` unless they explicitly ask
  otherwise.
- Do not pip into the host interpreter; use repo `.venv`.
- Do not read or print secrets (see `.cursor/rules/no-secrets.mdc`).

## Workspace (`.cursor/workspace/`)

Project `fly-*` skills live in `.cursor/skills/` (tracked). Session
files:

- `workspace/handoffs/handoff.md` — living session snapshot
- `workspace/context/` — durable background, glossary, decisions
- `workspace/journals/` — local append-only log (gitignored)
- `workspace/plans/` — active plans from `fly-plan` (gitignored except
  README)
- `workspace/artifacts/` — temp; wiped on handoff (gitignored except
  README)
- `workspace/archive/` — completed plans (gitignored except README)

Start a cold session with `fly-onboard`; confirm non-trivial work with
`fly-confirm-align`; close with `fly-handoff`.
`.cursor/skills`, `rules`, and `hooks` are tracked. Journals, artifacts,
and files under `data/` (except `data/README.md`) are gitignored.
`AGENTS.md` is the tracked contract.
Durable lessons go in `workspace/context` or `.cursor/rules/*.mdc`, not
this file.
