---
name: fly-handoff
description: >-
  Produce an end-of-session handoff in any repo: review the diff, run the
  repo's real verification commands if warranted, then either manage the
  fly-setup .cursor/workspace (update handoff.md in place, append JOURNAL,
  archive completed plans, wipe artifacts) or, if that scaffold isn't present,
  update whatever journal/handoff convention the repo already has - never
  inventing a new tracked file unprompted. Never commits unless asked. Use at
  session end, after completing a substantial piece of work, or when the user
  asks for a handoff / "update the handoff" / "wrap up this session".
disable-model-invocation: true
---

# Handoff

## Reply

First line: `|-CANARY-|` only; answer on the next line. Lead with the answer. Short unless this skill requires a structured dump (`fly-plan` family stay thorough **after** the canary line). At most one subagent. Prefer `/multitask` for one worker when the slice is tool-noisy or multi-file (search, tests, explore, bounded implement) (`run_in_background` if Multitask Mode requires it). Parent writes a self-contained brief, orchestrates, and reviews; the worker does that slice. Keep judgment, review, and tiny or one-shot edits in the parent. Never a second Task while another is running or may still complete. Never declare frozen; only the user may, then interrupt before replace. Never two Task calls in one turn. Never click **Build in Parallel** (fleet). Task brief and worker return: `session-multitask-coordination.mdc`.

Universal, repo-agnostic session close-out. Companion to `fly-onboard` — what
this skill writes is what that one reads next time.

After a substantial WP, prefer `fly-review-plan` first if a WP landed and
has not been audited.

## When to use

- User ends a session, or asks for a handoff / "update handoff" / "wrap up".
- After completing a substantial piece of work worth recording.

## Workflow

Copy this checklist into your response and check items off as you go:

```
Handoff progress:
- [ ] 1. Review diff
- [ ] 2. Run real verification commands (if code changed)
- [ ] 3. Check for the .cursor/workspace tree
- [ ] 4. Workspace cleanup OR update the repo's existing convention
- [ ] 5. Self-improve capture (propose only; do not apply unless asked)
- [ ] 6. Report the handoff packet
```

## Steps

1. **Review diff** — summarize what changed, and call out anything uncommitted.
2. **Verification** — if code changed, run the repo's real test/lint/build
   commands (same detection as `fly-plan` — don't assume a fixed gate list);
   report pass/fail with the actual command run.
3. **Check for `.cursor/workspace/`**. If present,
   follow §"Workspace cleanup" below. If not, follow §"No scaffold" below.

### Workspace cleanup (`.cursor/workspace/` present)

- **`workspace/artifacts/`** — delete its contents (keep the folder and
  `README.md`).
- **`workspace/plans/`** — for each plan that's now complete or superseded
  (confirm with the user if it's ambiguous which ones), move it to
  `workspace/archive/<YYYY-MM-DD>-<original-name>.md`. Leave still-active
  plans in place.
- **`workspace/handoffs/handoff.md`** — update **in place** (date, HEAD, focus,
  TL;DR, starter prompt). Do not emit dated extra handoff files.
- **`workspace/journals/JOURNAL.md`** — create if missing, then append a dated
  entry (newest-first) for any non-obvious failure→fix or decision this
  session. Don't touch older entries. This file is gitignored.
- **`workspace/context/`** — append `decisions.md` / `glossary.md` only if
  something durable changed; leave untouched otherwise.

### No scaffold

- Prefer `.cursor/workspace/` when present. If missing, reuse whatever
  `fly-onboard` would have found (including `.claude/workspace/`, session
  folders, a `HANDOFF.md`, `docs/journal/`, a CHANGELOG). If one exists,
  update it in place following its own format.
- If nothing exists, do not invent a new tracked file unprompted — produce
  the handoff summary in chat and ask the user whether they want it saved,
  and where (mention `fly-setup` can verify the expected workshop tree).
- Never write new session files into `.claude/workspace/` from this skill
  unless that was already the repo's living convention and you are updating
  it in place.

### Self-improve capture

If the operator corrected the agent this session, propose patches to
`workspace/context` or `.cursor/rules/`. **Do not apply** those patches
unless the user asks. Never rewrite `AGENTS.md` from this step.

## Output: handoff packet

- What changed (files + intent)
- What to run first next session
- What **not** to touch
- Open questions / next steps
- Copy-paste starter block confirmation (if `handoff.md` was updated)

## Pass criteria

- `workspace/handoffs/handoff.md` is current (in place), if the Cursor
  workspace is in use.
- `workspace/artifacts/` is empty (folder + README kept) after cleanup.
- Verification commands actually ran (not assumed) when code changed.
- Commit **only when the user asks**. Never commit `JOURNAL.md` or artifacts.

## Plan mode

This skill does not open a work package. Do not call SwitchMode. Do not call CreatePlan. Do not write `workspace/plans/`.

## Do not

- Commit without being asked.
- Delete or archive a plan the user hasn't confirmed is done — ask if unsure.
- Touch `journals/`, `context/`, except to append.
- Fabricate a session/journal convention that doesn't exist in the repo.
- Create `.cursor/` from this skill — `fly-setup` verifies the existing workshop tree.
