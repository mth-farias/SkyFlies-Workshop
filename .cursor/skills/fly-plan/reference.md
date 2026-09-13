# fly-plan — reference

## Suggested-model ladder

Pick the **cheapest** that still covers the hardest step (not the hottest
by default). User sets the picker. Do not auto-switch. Improve may **lower**
a too-hot banner.

- **Composer 2.5** — mechanical copy/rename, existing tests, cheap everyday
- **Grok 4.6 low** — small contained edits that still need judgment
- **Grok 4.6 medium** — multi-file contained work
- **Grok 4.6 high** — named-model default for non-trivial WPs
- **Grok 4.6 xhigh** — policy, skill contracts, architecture, multi-repo

## Machine

Before drafting, run `.cursor/skills/fly-setup/machine_probe.py` (resolve
order in that skill). Occupancy is a hint. Local batch only if the repo already has the
tool. Prefer one `/multitask` worker for noisy or multi-file slices; parent orchestrates; tiny edits stay in parent; never **Build in Parallel**. Cursor may HTTP to
`127.0.0.1:9292` only when `port_9292` is `up` and the task needs a local LLM.

## Plan section template

- **Suggested model** — one line; cheapest that covers the hardest step
- **Scope** — in / out; link to spec/ticket if any
- **Discovery notes** — what existing code/docs/decisions this plan builds on
- **Touch list** — full file list with reason for each (bullets, not tables)
- **Implementation steps** — ordered; dependency-aware; each step owner `agent`
- **Verification** — real commands detected from the repo (test/lint/build/CI)
- **Risks** — concrete failure modes and mitigations
- **Open questions** — explicit rows — no silent TBD
- **Follow-up work** — deferred items with enough detail to pick up later

## Worked example (compact)

```markdown
# Add sync dry-run

**Suggested model:** Composer 2.5. Set this in the chat/Build picker before execute.

## Scope
In: add a `--dry-run` flag to the `sync` CLI command.
Out: no change to `push`/`pull`.

## Touch list
- `src/cli/sync.py` — Add `--dry-run` flag; skip the write step when set
- `tests/test_sync.py` — Add a test asserting no writes occur under `--dry-run`

## Implementation steps
1. Confirm flag name unused in `src/cli/sync.py`. Owner: **agent**.
2. `src/cli/sync.py` — add the flag and guard the write call. Owner: **agent**.
3. `tests/test_sync.py` — add the test. Owner: **agent**.

## Verification
`pytest tests/test_sync.py -k dry_run` (detected from `pyproject.toml`'s `[tool.pytest]` config)

## Risks
Flag name could collide with a global option — checked `sync.py`'s existing `argparse` setup, no collision.

## Open questions
None.

## Follow-up work
None.

Do not execute until user approves.
```

## Cursor CreatePlan

- First line of the plan body is a level-1 title.
- Next line is `**Suggested model:** …`
- No markdown tables in the CreatePlan body (use bullets).
- Optional todos on CreatePlan.
- Dual-write the same bullets to `.cursor/workspace/plans/` when that folder exists.

## Mandatory self-audit (before presenting the plan as final)

Self-check every item; fix the plan text until it passes. This is a feedback
loop — run this list, fix what fails, run it again, and only stop once
everything passes:

1. **No silent deferrals** — every open item is either resolved, in **Open
   questions**, or in **Follow-up work**.
2. **Touch list completeness** — every file the steps reference appears in
   the list.
3. **Verification is real** — the named commands actually exist in this repo
   (checked, not assumed) and cover the changed surface.
4. **Owners** — every implementation step has owner `agent`. Fail intern
   leftover owners. Do not require intern discovery.
5. **Scope creep check** — nothing crept in beyond what the user asked;
   anything adjacent-but-tempting goes to Follow-up work instead of the plan.
6. **Ends with the approval gate** — plan text ends with "Do not execute until
   user approves" and points at `fly-plan-improve`.
7. **Suggested model present** — banner exists; it is the cheapest of the
   ladder that still covers the hardest step, not a per-step roster.

## Placeholders

- Work package / goal — user message or linked spec
- Scope files — user, or inferred from discovery — confirm with user if inferred
- Verification commands — detected from repo tooling, not assumed
