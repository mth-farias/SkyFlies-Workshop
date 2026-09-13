# SkyFlies Workshop

A hands-on workshop: use **open-source data** and **AI tools** to help
develop artwork.

## Start here

Work from [`workshop/`](workshop/README.md). Read the lesson README,
then run the Windows or Mac runner.

**This lesson:**
[`workshop/01-repo-bootstrap/`](workshop/01-repo-bootstrap/README.md)

## What you need

- Python **3.11+** on `PATH` (`py -3` or `python` on Windows, `python3`
  on macOS)
- [Git](https://git-scm.com/)
- [Cursor](https://cursor.com/) (project skills live in `.cursor/skills/`
  as `fly-*`)

Do not install packages into the system Python. The lesson runner creates
a repo `.venv`.

## Layout

- `workshop/` — student path (docs + runners)
- `data/` — local files (gitignored except `data/README.md`)
- `.cursor/` — tracked skills, rules, and hooks
- `.venv/` — local interpreter (gitignored)

## Style

Python and JavaScript follow Google style. See [`STYLE.md`](STYLE.md).
Agent contract: [`AGENTS.md`](AGENTS.md).
