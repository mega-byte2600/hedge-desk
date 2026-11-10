#!/usr/bin/env bash
# Emporion — demo prep, one command.
#
# Builds the public console, starts the server, checks it is healthy, and prints
# the business reference cheat sheet with the URL to open.
#
#   bash scripts/biz_prep.sh                 # prep + serve on :8765
#   PORT=9000 bash scripts/biz_prep.sh       # different port
#   bash scripts/biz_prep.sh --no-serve      # print the pack only
#   bash scripts/biz_prep.sh --vv            # also run the V&V matrix first
#
# Ctrl-C stops the server.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-8765}"
REFERENCE="docs/biz/EMPORION_BIZ_REFERENCE.md"
SERVE=1
RUN_VV=0
for arg in "$@"; do
  case "$arg" in
    --no-serve) SERVE=0 ;;
    --vv) RUN_VV=1 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

PY="python3"
[ -x .venv/bin/python ] && PY=".venv/bin/python"

echo "== Emporion demo prep =="
echo
echo "-- 1/4 building the console bundle"
"$PY" scripts/build_web.py >/dev/null
echo "   dist/ refreshed"

echo
echo "-- 2/4 test suites"
"$PY" -m unittest discover -s tests 2>&1 | tail -3 | sed 's/^/   /'
if command -v node >/dev/null 2>&1; then
  node --test web/ 2>&1 | grep -E '^. (pass|fail) ' | sed 's/^/   /' || true
fi

if [ "$RUN_VV" = "1" ]; then
  echo
  echo "-- V&V matrix (browser checks)"
  node scripts/vv_console.mjs "http://127.0.0.1:${PORT}" --skip-suites 2>&1 | tail -18 | sed 's/^/   /' || \
    echo "   (browser tooling unavailable - see docs/CONSOLE_VV_SPEC.md)"
fi

echo
echo "-- 3/4 business reference"
echo "   file: $(pwd)/${REFERENCE}"
if [ -f "$REFERENCE" ]; then
  # The pitch and the two modes are what actually get said out loud; print those.
  awk '/^## 1\./,/^## 3\./' "$REFERENCE" | grep -v '^## 3\.' | sed 's/^/   /'
else
  echo "   MISSING - expected ${REFERENCE}"
fi

echo
echo "-- 4/4 checks"
printf "   port %s in use: " "$PORT"
if curl -fsS -m 2 -o /dev/null "http://127.0.0.1:${PORT}/api/health" 2>/dev/null; then
  echo "yes (a server is already running - reusing it)"
  SERVE=0
else
  echo "no"
fi

if [ "$SERVE" = "1" ]; then
  echo
  echo "== starting the desk =="
  echo "   URL:      http://127.0.0.1:${PORT}"
  echo "   public research console; no sign-in required"
  echo "   stop:     Ctrl-C"
  echo
  export PORT
  exec bash scripts/demo.sh
else
  echo
  echo "== ready =="
  echo "   open: http://127.0.0.1:${PORT}"
  echo "   (--no-serve: not starting the server)"
fi
