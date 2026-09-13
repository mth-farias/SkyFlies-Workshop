# fly-plan-improve — reference

Edits the **plan document** before execute. After the WP lands, use
`fly-review-plan` instead.

## Example output block

```markdown
**Verdict:** REVISED (plan file edited in place)

| Axis | Result (pre-edit) |
|------|--------|
| Completeness | FAIL — verification section missing lint command |
| Internal consistency | PASS |
| Verification coverage | FAIL — named test command doesn't exist in package.json |
| Scope creep | PASS |
| Execution posture | FAIL — steps had no owners |
| Hygiene | PASS |
| Suggested model | FAIL — banner was Grok 4.6 xhigh for a flag add |
| Multitask assignment | FAIL — no Build assignment line |

1. Fixed verification command — `npm test` → `npm run test:unit` per package.json.
2. Added lint command to verification section.
3. Labeled each step owner `agent`.
4. Final model-selection revision — Suggested model Composer 2.5 (lowered).
5. Final multitask assignment — prefer one `/multitask` worker for noisy or multi-file slices; parent briefs and reviews (main orchestrates); no Build in Parallel.

**Do not execute until user approves.**
```

## Review axes detail

- **Completeness:** every deliverable named in the goal has a corresponding
  step; touch list covers every file the steps reference; open items are in
  Open questions or Follow-up work, not silently dropped.
- **Internal consistency:** plan doesn't contradict an existing
  handoff/decisions doc found during discovery; no two sections give
  conflicting instructions.
- **Verification coverage:** commands are checked against the repo's actual
  tooling (`package.json` scripts, `pyproject.toml`, CI config, Makefile), not
  assumed generically.
- **Scope creep:** nothing beyond what the user asked has been folded into the
  plan without being called out.
- **Execution posture:** every step has owner `agent`. Fail missing owners.
  Fail intern leftover owners. Do not require intern discovery.
- **Hygiene:** commit policy, forbidden paths, and style conventions from the
  repo's own docs are respected.
- **Suggested model:** first body content after the title is
  `**Suggested model:** …`. Walk steps from **Composer 2.5** (cheapest
  everyday) up Grok 4.6 `low` / `medium` / `high` / `xhigh` only as far as
  the hardest step needs. Set the banner to that **minimum** (raise or
  lower). One banner; no per-step roster. Do not auto-switch the picker.
  Ask the user to set chat/Build to that model (View Plan → Build picker →
  Inherit Agent Model if Build has stuck on another default).
- **Multitask assignment:** product **Build in Parallel** can fan a fleet.
  Workshop assignment is prefer one `/multitask` worker for noisy or
  multi-file slices; parent briefs and reviews (main orchestrates).
  Write **Build:** prefer one `/multitask` worker for noisy or multi-file
  slices; parent briefs and reviews. Do not emit a `/multitask` ban.
  Do not emit “sequential, one worker” as a ban.
  Never recommend **Build in Parallel** or Cloud `/in-cloud` as a fleet
  while a second Task would run. If Multitask Mode requires
  `run_in_background`, still at most one Task. Parent writes a
  self-contained brief, orchestrates, and reviews; the worker does that
  slice. Tiny or one-shot edits stay in the parent. Never click
  **Build in Parallel**.

## Final pass (mandatory)

Run **after** other plan edits, before the report. Ladder: see
`fly-plan/reference.md`.

1. **Model-selection revision** — start at Composer 2.5; step Grok effort
   only when a remaining step needs it; write one Suggested model line.
2. **Multitask assignment** — serial vs independent notes are fine;
   write **Build:** prefer one `/multitask` worker for noisy or
   multi-file slices; parent briefs and reviews (main orchestrates).
