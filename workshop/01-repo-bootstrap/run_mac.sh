#!/bin/sh
# SkyFlies Workshop — Step 1 (macOS). Opens Terminal.app when possible.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TITLE="SkyFlies Workshop - Step 1: repo bootstrap"
HERE_FLAG="${1:-}"

run_python() {
  if command -v python3 >/dev/null 2>&1; then
    python3 "$ROOT/workshop/_lib/step_runner.py" --step 01
    return $?
  fi
  if command -v python >/dev/null 2>&1; then
    python "$ROOT/workshop/_lib/step_runner.py" --step 01
    return $?
  fi
  echo "  [fail] Python 3.11+ not on PATH."
  echo "  Install from https://www.python.org/downloads/macos/"
  return 1
}

if [ "$HERE_FLAG" != "--here" ]; then
  if command -v osascript >/dev/null 2>&1; then
    ESCAPED=$(printf '%s\n' "$ROOT" | sed "s/'/'\\\\''/g")
    osascript <<EOF || exec /bin/sh "$0" --here
tell application "Terminal"
  activate
  do script "printf '\\\\033]0;${TITLE}\\\\007'; cd '${ESCAPED}' && /bin/sh '${ESCAPED}/workshop/01-repo-bootstrap/run_mac.sh' --here"
end tell
EOF
    exit 0
  fi
  exec /bin/sh "$0" --here
fi

printf '\033]0;%s\007' "$TITLE"
echo
echo "  Opening Step 1 in this window. Leave it open until Done."
echo
cd "$ROOT"
set +e
run_python
ERR=$?
set -e
echo
if [ "$ERR" -ne 0 ]; then
  echo "  Step 1 failed. Scroll up, fix, then run this script again."
fi
printf "  Press Enter to close. "
read -r _
exit "$ERR"
