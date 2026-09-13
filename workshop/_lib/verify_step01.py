#!/usr/bin/env python3
"""Host-Python gate for workshop Step 1 (no venv, no ripgrep).

Fails if instructor skill names leaked, if ``.gitignore`` ignores all of
``.cursor/``, if ``workshop/`` has extra lesson folders, if ``data/``
has extra files, or if duck0 absolute paths appear under project skills.
"""

from __future__ import annotations

import sys
from pathlib import Path

_DUCK0_MARKERS = (
    "O:\\duck0",
    "O:/duck0",
    r"mth-farias\duck0",
    "mth-farias/duck0",
)
_C0_NAMES = (
    "c0-onboard",
    "c0-confirm-align",
    "c0-plan",
    "c0-plan-improve",
    "c0-review-plan",
    "c0-handoff",
    "c0-setup",
)


def repo_root() -> Path:
    """Return the workshop repository root."""
    return Path(__file__).resolve().parents[2]


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def _ok(msg: str) -> None:
    print(f"ok: {msg}")


def check_no_c0_skill_dirs(root: Path) -> None:
    """Fail if any ``c0-*`` directory exists under project skills."""
    skills = root / ".cursor" / "skills"
    if not skills.is_dir():
        _fail("missing .cursor/skills")
    leaked = sorted(
        p.name
        for p in skills.iterdir()
        if p.is_dir() and p.name.startswith("c0-")
    )
    if leaked:
        _fail("c0-* skill dirs: " + ", ".join(leaked))
    _ok("no c0-* skill directories")


def check_gitignore(root: Path) -> None:
    """Fail if gitignore drops the entire ``.cursor/`` tree."""
    path = root / ".gitignore"
    if not path.is_file():
        _fail("missing .gitignore")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("#") or not line:
            continue
        if line in {".cursor/", ".cursor", "/.cursor/", "/.cursor"}:
            _fail(f".gitignore ignores all of .cursor/: {line}")
    _ok(".gitignore does not ignore all of .cursor/")


def check_workshop_dirs(root: Path) -> None:
    """Fail if ``workshop/`` contains unexpected directories."""
    workshop = root / "workshop"
    allowed = {"_lib", "01-repo-bootstrap"}
    extra = []
    if workshop.is_dir():
        for p in workshop.iterdir():
            if p.is_dir() and p.name not in allowed:
                extra.append(p.name)
    if extra:
        _fail("unexpected workshop dirs: " + ", ".join(sorted(extra)))
    _ok("workshop dirs are _lib and 01-repo-bootstrap")


def check_data_tree(root: Path) -> None:
    """Fail if ``data/`` contains files other than README.md."""
    data = root / "data"
    extra = []
    if data.is_dir():
        for p in data.rglob("*"):
            if p.is_file() and p.name != "README.md":
                extra.append(p.relative_to(root).as_posix())
    if extra:
        _fail("unexpected data files: " + ", ".join(sorted(extra)))
    _ok("data/ has only README.md")


def check_skills_text(root: Path) -> None:
    """Fail on duck0 paths or ``name: c0-`` in project skills."""
    skills = root / ".cursor" / "skills"
    for path in skills.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".py", ".txt", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        if "name: c0-" in text:
            _fail(f"name: c0- in {rel}")
        for marker in _DUCK0_MARKERS:
            if marker in text:
                _fail(f"duck0 path {marker!r} in {rel}")
        # machine_probe.py is allowed to be generic; skill markdown is not
        if path.name == "SKILL.md" or path.name == "reference.md":
            for name in _C0_NAMES:
                if name in text:
                    _fail(f"{name} leaked in {rel}")
    _ok("skills text has no c0- names or duck0 paths")


def check_required(root: Path) -> None:
    """Fail if Step 1 tracked files are missing."""
    required = [
        "AGENTS.md",
        "README.md",
        "LICENSE",
        "NOTICE",
        "STYLE.md",
        "pyproject.toml",
        "workshop/01-repo-bootstrap/README.md",
        "workshop/01-repo-bootstrap/run_win.bat",
        "workshop/01-repo-bootstrap/run_mac.sh",
        "workshop/_lib/step_runner.py",
        ".cursor/hooks/session-start.py",
        ".cursor/skills/fly-setup/machine_probe.py",
        ".cursor/skills/fly-plan/reference.md",
        "data/README.md",
    ]
    missing = [rel for rel in required if not (root / rel).is_file()]
    if missing:
        _fail("missing: " + ", ".join(missing))
    _ok("required Step 1 files present")


def main() -> int:
    """Run all Step 1 gates; return 0 on success."""
    root = repo_root()
    print(f"verify_step01 root={root}")
    check_required(root)
    check_no_c0_skill_dirs(root)
    check_gitignore(root)
    check_workshop_dirs(root)
    check_data_tree(root)
    check_skills_text(root)
    print("verify_step01: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
