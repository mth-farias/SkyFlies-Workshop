#!/usr/bin/env python3
"""Stdlib console runner for SkyFlies Workshop lessons.

This module is the shared UI for ``run_win.bat`` and ``run_mac.sh``. It
prints a titled banner, a progress bar, and numbered checks. Step 1
creates a repo ``.venv``, upgrades pip, and initializes git only when
``.git`` is missing.

Requires Python 3.11+ on PATH. No third-party packages.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path

_MIN_PY = (3, 11)
_BAR_WIDTH = 28
_PIP_INDEX = "https://pypi.org/simple"


def _print(msg: str = "", *, err: bool = False) -> None:
    """Write a line and flush so popup terminals keep up with pip."""
    stream = sys.stderr if err else sys.stdout
    print(msg, file=stream, flush=True)


class StepError(RuntimeError):
    """A student-facing failure with a short fix hint."""


def repo_root() -> Path:
    """Return the workshop repository root (parent of ``workshop/``)."""
    return Path(__file__).resolve().parents[2]


def _which(names: Sequence[str]) -> str | None:
    """Return the first executable name found on PATH."""
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def resolve_host_python() -> Path:
    """Find a host Python 3.11+ interpreter.

    Order: ``py -3`` (Windows), ``python``, ``python3``, then
    ``sys.executable`` if it already meets the floor.

    Returns:
        Path to the interpreter.

    Raises:
        StepError: If no suitable interpreter is on PATH.
    """
    candidates: list[list[str]] = []
    if os.name == "nt" and _which(("py",)):
        candidates.append(["py", "-3"])
    for name in ("python", "python3"):
        found = _which((name,))
        if found:
            candidates.append([found])
    candidates.append([sys.executable])

    seen: set[str] = set()
    last_err = "Python 3.11+ not found"
    for cmd in candidates:
        key = " ".join(cmd)
        if key in seen:
            continue
        seen.add(key)
        try:
            version = _python_version(cmd)
        except (OSError, StepError) as exc:
            last_err = str(exc)
            continue
        if version >= _MIN_PY:
            if cmd[0] == "py":
                return Path("py")
            return Path(cmd[0])
        last_err = (
            f"{' '.join(cmd)} is Python {version[0]}.{version[1]}; "
            "need 3.11+ (https://www.python.org/downloads/)"
        )
    raise StepError(last_err)


def _python_version(cmd: Sequence[str]) -> tuple[int, int]:
    """Return ``(major, minor)`` for ``cmd``."""
    try:
        proc = subprocess.run(
            [
                *cmd,
                "-c",
                "import sys; print('%d.%d' % (sys.version_info[0], "
                "sys.version_info[1]))",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except subprocess.TimeoutExpired as exc:
        raise StepError(f"timed out probing {' '.join(cmd)}") from exc
    if proc.returncode != 0:
        raise StepError(proc.stderr.strip() or f"{' '.join(cmd)} failed")
    line = proc.stdout.strip()
    major_s, _, minor_s = line.partition(".")
    try:
        return int(major_s), int(minor_s)
    except ValueError as exc:
        raise StepError(f"could not parse version from {line!r}") from exc


def host_python_argv(host: Path) -> list[str]:
    """Return argv prefix for the resolved host interpreter."""
    if host.name.lower() == "py":
        return ["py", "-3"]
    return [str(host)]


def venv_python(root: Path) -> Path:
    """Return the venv interpreter path for this OS."""
    if os.name == "nt":
        return root / ".venv" / "Scripts" / "python.exe"
    return root / ".venv" / "bin" / "python"


def _banner(title: str) -> None:
    """Print a boxed title so the popup terminal is obvious."""
    line = "=" * max(len(title) + 4, 52)
    _print()
    _print(line)
    _print(f"  {title}")
    _print(line)
    _print("  Follow each line. Do not close this window until Done.")
    _print()


def _bar(done: int, total: int, label: str) -> None:
    """Print a single-line progress bar."""
    frac = 0 if total <= 0 else done / total
    filled = int(_BAR_WIDTH * frac)
    body = "#" * filled + "-" * (_BAR_WIDTH - filled)
    pct = int(100 * frac)
    print(f"  [{body}] {pct:3d}%  {label}", flush=True)


def _ok(msg: str) -> None:
    _print(f"  [ok] {msg}")


def _pause(prompt: str, assume_yes: bool) -> None:
    """Wait for Enter unless ``--yes`` or stdin is not a TTY."""
    if assume_yes or not sys.stdin.isatty():
        print(f"  {prompt} (auto)", flush=True)
        return
    input(f"  {prompt} ")


def _run(argv: Sequence[str], cwd: Path) -> None:
    """Run a subprocess; raise StepError on non-zero exit."""
    print(f"  $ {' '.join(argv)}", flush=True)
    proc = subprocess.run(list(argv), cwd=cwd, check=False)
    if proc.returncode != 0:
        raise StepError(f"command failed ({proc.returncode}): {' '.join(argv)}")


def _ensure_venv(root: Path, host_argv: Sequence[str]) -> Path:
    """Create ``.venv`` if missing; return the venv interpreter."""
    py = venv_python(root)
    if py.is_file():
        _ok(f"venv already exists: {py}")
        return py
    _run([*host_argv, "-m", "venv", str(root / ".venv")], cwd=root)
    if not py.is_file():
        raise StepError(f"venv created but interpreter missing: {py}")
    _ok(f"created {py}")
    return py


def _upgrade_pip(py: Path, root: Path) -> None:
    """Upgrade pip inside the venv only (no requirements.txt)."""
    _run(
        [str(py), "-m", "pip", "install", "--upgrade", "pip", "-i", _PIP_INDEX],
        cwd=root,
    )
    _ok("pip upgraded in .venv (no third-party packages in Step 1)")


def _maybe_git_init(root: Path) -> None:
    """Initialize git only when ``.git`` is missing."""
    git_dir = root / ".git"
    if git_dir.exists():
        _ok("git already initialized")
        return
    git = shutil.which("git")
    if not git:
        raise StepError("git not found on PATH (https://git-scm.com/)")
    _run([git, "init"], cwd=root)
    _ok("git init (clone already having .git skips this)")


def _confirm_layout(root: Path) -> None:
    """Fail if the Step 1 tree is incomplete."""
    required = (
        root / "AGENTS.md",
        root / "workshop" / "01-repo-bootstrap" / "README.md",
        root / ".cursor" / "skills" / "fly-onboard" / "SKILL.md",
        root / ".cursor" / "hooks" / "session-start.py",
        root / ".gitignore",
    )
    missing = [str(p.relative_to(root)) for p in required if not p.is_file()]
    if missing:
        raise StepError("missing files: " + ", ".join(missing))
    ignore = (root / ".gitignore").read_text(encoding="utf-8")
    for raw in ignore.splitlines():
        line = raw.strip()
        if line in {".cursor/", ".cursor"} or line.startswith(".cursor/"):
            # Allowed: .cursor/workspace/... only
            rest = line[len(".cursor/") :] if line.startswith(".cursor/") else ""
            if line in {".cursor/", ".cursor"} or rest == "":
                raise StepError(".gitignore ignores all of .cursor/")
            continue
    _ok("layout + .gitignore (skills/rules/hooks stay tracked)")


def run_step_01(root: Path, assume_yes: bool) -> None:
    """Run workshop lesson 01: repo bootstrap."""
    title = "SkyFlies Workshop - Step 1: repo bootstrap"
    if os.name == "nt":
        os.system("title " + title)
    _banner(title)
    _print("  This lesson: Python venv, git if needed, confirm Cursor files.")
    _print()
    _pause("Press Enter to start.", assume_yes)

    steps: list[tuple[str, Callable[[], None]]] = []
    host_holder: dict[str, list[str]] = {}

    def find_python() -> None:
        host = resolve_host_python()
        argv = host_python_argv(host)
        host_holder["argv"] = argv
        ver = _python_version(argv)
        _print(f"  interpreter: {' '.join(argv)} (Python {ver[0]}.{ver[1]})")

    def make_venv() -> None:
        py = _ensure_venv(root, host_holder["argv"])
        host_holder["venv"] = [str(py)]

    def pip_up() -> None:
        _upgrade_pip(Path(host_holder["venv"][0]), root)

    def git_maybe() -> None:
        _maybe_git_init(root)

    def layout() -> None:
        _confirm_layout(root)

    def next_action() -> None:
        _print()
        _print("  Next:")
        _print("    1. Open this folder in Cursor (SkyFlies-Workshop only).")
        _print("    2. New chat, run /fly-onboard")
        _print("    3. If hooks fail on Mac, see README (python vs python3).")
        time.sleep(0.2)

    steps = [
        ("Find Python 3.11+", find_python),
        ("Create .venv", make_venv),
        ("Upgrade pip in .venv", pip_up),
        ("git init if missing", git_maybe),
        ("Confirm tracked layout", layout),
        ("Print next student action", next_action),
    ]

    total = len(steps)
    for i, (label, fn) in enumerate(steps, start=1):
        _print()
        _bar(i - 1, total, label)
        _print(f"  -- {i}/{total} {label}")
        fn()
        _bar(i, total, "done")
    _print()
    _print("  Done. You can close this window.")
    _print()


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry: ``--step 01``."""
    parser = argparse.ArgumentParser(
        description="SkyFlies Workshop step runner (stdlib)."
    )
    parser.add_argument(
        "--step",
        required=True,
        help="Lesson id, currently only 01",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip Enter prompts (used by verify).",
    )
    args = parser.parse_args(argv)
    root = repo_root()
    os.chdir(root)
    try:
        if args.step in {"01", "1", "repo-bootstrap"}:
            run_step_01(root, assume_yes=args.yes)
            return 0
        raise StepError(f"unknown step {args.step!r}; only 01 exists")
    except StepError as exc:
        _print(f"  [fail] {exc}", err=True)
        _print(
            "  Fix the message above, then re-run run_win.bat or run_mac.sh.",
            err=True,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
