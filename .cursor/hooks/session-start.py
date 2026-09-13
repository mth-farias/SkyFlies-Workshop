#!/usr/bin/env python3
"""Emit a capped handoff head as Cursor additional_context.

Stdout is a single JSON object. Never write files. Always exit 0.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_MAX_LINES = 30
_MAX_BYTES = 2048
_FALLBACK = "fly-workshop: no handoff.md yet"


def _write_additional_context(text: str) -> None:
    """Print Cursor hook JSON to stdout."""
    sys.stdout.write(json.dumps({"additional_context": text}, separators=(",", ":")))


def _capped_handoff(path: Path, max_lines: int, max_bytes: int) -> str:
    """Return the start of path, capped by lines and UTF-8 bytes."""
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    out: list[str] = []
    used = 0
    for line in raw_lines[:max_lines]:
        chunk = line + "\n"
        n = len(chunk.encode("utf-8"))
        if used + n > max_bytes:
            remain = max_bytes - used
            if remain > 0:
                encoded = chunk.encode("utf-8")[:remain]
                out.append(encoded.decode("utf-8", errors="ignore").rstrip())
            break
        out.append(line)
        used += n
    return "\n".join(out)


def _repo_root() -> Path:
    """Resolve the workshop root from env or this file's location."""
    for key in ("CURSOR_PROJECT_DIR", "CLAUDE_PROJECT_DIR"):
        value = os.environ.get(key)
        if value:
            candidate = Path(value)
            if candidate.is_dir():
                return candidate.resolve()
    return Path(__file__).resolve().parents[2]


def main() -> int:
    """Load a capped handoff and print hook JSON."""
    if not sys.stdin.isatty():
        try:
            sys.stdin.read()
        except OSError:
            pass
    try:
        handoff = _repo_root() / ".cursor" / "workspace" / "handoffs" / "handoff.md"
        if not handoff.is_file():
            _write_additional_context(_FALLBACK)
            return 0
        text = _capped_handoff(handoff, _MAX_LINES, _MAX_BYTES)
        if not text.strip():
            _write_additional_context(_FALLBACK)
            return 0
        _write_additional_context(text)
    except Exception:
        _write_additional_context(_FALLBACK)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
