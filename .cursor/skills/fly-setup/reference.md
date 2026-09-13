# fly-setup — reference

Verifier for **this** SkyFlies-Workshop tree. Do not scaffold a third
generic repo. Skill id is `fly-setup`.

## Checks

| Check | Pass when |
|-------|-----------|
| `AGENTS.md` | Present at the workshop repo root |
| `workshop/01-repo-bootstrap` | Path exists |
| Tracked `fly-*` skills | All seven folders under `.cursor/skills/` with matching `name:` |
| `.gitignore` | Does **not** ignore all of `.cursor/` |

Seven skill ids: `fly-onboard`, `fly-confirm-align`, `fly-plan`,
`fly-plan-improve`, `fly-review-plan`, `fly-handoff`, `fly-setup`.

Session files stay under `.cursor/workspace/`. Skills, rules, and hooks
stay tracked.

## Gap-fill rule

This skill does **not** copy templates into a new repo. If a check fails,
report it. Do not invent a second tree. Do not add extra folders under
`workshop/`.

Never write `workspace/journals/JOURNAL.md` from this skill.
Never write `.mcp.json`.
Never delete an existing `CLAUDE.md`.

## Gitignore (read, do not widen)

**Fail** if `.gitignore` has a full-tree ignore of `.cursor/` or `.cursor`.

Expected pattern: ignore session noise only, for example journals,
artifacts, archive, and plans content (keep README files). Do **not** add:

```
.cursor/
```

Do not delete working-tree `.cursor/` files. Do not run
`git rm -r --cached .cursor`.

## Machine probe

`.cursor/skills/fly-setup/machine_probe.py` (repo-relative). JSON on
stdout; one-line human summary on stderr. Never opens credential files. TCP
connect only to `127.0.0.1:9292` (no generate, no HTTP).

Resolve in order (never cwd-relative `../fly-setup/` from a repo root):

1. `.cursor/skills/fly-setup/machine_probe.py`

If missing, skip and say so; do not fail the skill.

JSON keys: `cpu_logical`, `ram_gb`, `gpus` (`name`, `vram_mb`, `util_pct`),
`port_9292` (`up` / `down` / `unknown`), `hint` (`gpu_busy` / `gpu_free` /
`unknown`). Timeouts: `nvidia-smi` 2s, TCP 0.5s. No usable `nvidia-smi` →
empty `gpus` and `hint=unknown` (exit 0). Else `gpu_busy` if any GPU
`util_pct >= 15`; otherwise `gpu_free`. Occupancy is a hint, not a veto, and
not “ik owns the GPU”.

Cursor may HTTP to `127.0.0.1:9292` only when `port_9292` is `up` and the
task needs a local LLM. Never intern MCP. Do not register `ask_llama`.

## This skill vs a generic scaffolder

| Product | Job |
|---------|-----|
| This skill (`fly-setup`) | Verify SkyFlies-Workshop conventions; report gaps |
| Generic third-repo scaffold | Out of scope — do not run |
