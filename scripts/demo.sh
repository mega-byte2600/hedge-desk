#!/usr/bin/env bash
# Launch the Emporion desk locally for a demo.
# Usage:  bash scripts/demo.sh          (default port 8765)
#         PORT=9000 bash scripts/demo.sh
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-8765}"
export PORT

echo "== Building the console bundle =="
python3 scripts/build_web.py

echo "== Regenerating the real AM report (EOD -> overnight -> candidates) =="
python3 -m hedge_desk.am_demo

echo
echo "== Emporion desk =="
echo "   URL:        http://127.0.0.1:${PORT}/"
echo "   Public research console; no sign-in required"
echo "   Health:     http://127.0.0.1:${PORT}/api/health"
echo "   Live report http://127.0.0.1:${PORT}/api/report"
echo
echo "   Ctrl-C to stop."
echo
exec python3 -m hedge_desk.server
