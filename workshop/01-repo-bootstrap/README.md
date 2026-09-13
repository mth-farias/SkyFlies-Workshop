# Step 1 — Repo bootstrap

You set up a clean, contained workshop repo: documentation, a local
Python virtual environment, git, and Cursor **fly-*** skills.

## Why this step exists

Every student should end with the same layout and a working `.venv`
before writing more code.

## What you generate

| Path | Tracked? |
|------|----------|
| `.venv/` | No (local interpreter) |
| `.git/` | Local only until you commit |
| Skills/rules/hooks already in `.cursor/` | Yes (came with the clone) |

## Prerequisites

- Python **3.11+** on `PATH`
  - Windows: `py -3` or `python` ([installer](https://www.python.org/downloads/), tick **Add python.exe to PATH**)
  - macOS: `python3` ([installer](https://www.python.org/downloads/macos/) or Homebrew)
- Git

## Run

**Windows:** double-click [`run_win.bat`](run_win.bat). A titled Command
Prompt opens. Read the progress bar. Press Enter when asked. Leave the
window open until it says Done.

**macOS:** in Terminal:

```bash
chmod +x workshop/01-repo-bootstrap/run_mac.sh
./workshop/01-repo-bootstrap/run_mac.sh
```

If Terminal.app cannot open a new window, the same script continues in
the current shell (`--here`).

From the repo root you can also run:

```bash
python workshop/_lib/step_runner.py --step 01
```

Use `--yes` to skip Enter pauses.

The runner only upgrades pip inside `.venv`. It does not install extra
packages.

## Done when

- `.venv` exists (`Scripts\python.exe` on Windows, `bin/python` on Mac)
- `git status` works in this folder
- Cursor opened on **this** folder shows `/fly-onboard` (project skill)

Then: new Cursor chat → `/fly-onboard`.

## Cursor skills: instructor vs student

The instructor’s private skills are named `c0-*`. **You use `fly-*`:**

| You type | Role |
|----------|------|
| `/fly-onboard` | Orient at session start |
| `/fly-confirm-align` | Same-page before big work |
| `/fly-plan` | Written plan |
| `/fly-plan-improve` | Critique the plan |
| `/fly-review-plan` | After execute |
| `/fly-handoff` | Close the session |
| `/fly-setup` | Verify this workshop tree |

Do not copy skills into `~/.cursor/skills`. They already live in
`.cursor/skills/` in this repo.

## Hooks: `python` vs `python3`

`.cursor/hooks.json` runs:

```text
python .cursor/hooks/session-start.py
```

If your Mac has only `python3`, either create a `python` alias or change
that one command to `python3 .cursor/hooks/session-start.py`. Fallbacks:
[`.cursor/hooks/session-start.cmd`](../../.cursor/hooks/session-start.cmd)
(Windows) and
[`.cursor/hooks/session-start.sh`](../../.cursor/hooks/session-start.sh)
(macOS) — documented here, not a second hooks.json.

## Verify (optional)

From the repo root, with host Python (venv not required):

```bash
py -3 workshop/_lib/verify_step01.py
```

or `python3 workshop/_lib/verify_step01.py` on Mac.
