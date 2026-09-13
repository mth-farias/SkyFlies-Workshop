# decisions

Durable architectural and scope decisions, dated, with the reasoning
behind each one. Append a row when a choice is locked. Do not relitigate
locked rows. Do not put secrets here.

| Date | Decision | Why |
|------|----------|-----|
| 2026-09-13 | This repo is the student product; SkyFlies is instructor lookup. | Do not edit or copy a sibling SkyFlies tree. |
| 2026-09-13 | Track `.cursor/skills`, `rules`, and `hooks`; gitignore journals, artifacts, archive bodies, local plans, `.venv`, and `data/**` except `data/README.md`. | Students need `fly-*` from the clone. |
| 2026-09-13 | Skill prefix is `fly-*`, not `c0-*`. | Avoid clashing with instructor global skills. |
| 2026-09-13 | Step runners are `run_win.bat` / `run_mac.sh` plus shared stdlib Python. | Windows and Mac workshop machines; one UI. |
| 2026-09-13 | Python 3.11+ in repo `.venv`. | Isolation; no host pip. |
| 2026-09-13 | Google Python/JS style. | Teaching a single documented standard. |
| 2026-09-13 | MIT + NOTICE. | This repo ships original workshop text, runners, and skills. |
