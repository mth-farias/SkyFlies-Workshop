#!/bin/sh
# Fallback Cursor hook launcher when `python` is not on PATH.
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$DIR/session-start.py" "$@"
fi
exec python "$DIR/session-start.py" "$@"
