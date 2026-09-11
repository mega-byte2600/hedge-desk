#!/usr/bin/env bash
# Launch the Emporion desk locally for a demo.
# Usage:  bash scripts/demo.sh          (default port 8765)
#         PORT=9000 bash scripts/demo.sh
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-8765}"
export PORT
# Demo defaults: local SQLite stores, a fixed secret, and no external services.
export MEMBERSHIP_SECRET="${MEMBERSHIP_SECRET:-demo-secret-please-rotate}"
export BROKER_LINK_KEY="${BROKER_LINK_KEY:-demo-broker-key-please-rotate}"
export GP_EMAIL="${GP_EMAIL:-gp@example.com}"
# Set these to your own address to be treated as the GP in the demo.
export MEMBERSHIP_DB="${MEMBERSHIP_DB:-$PWD/data/membership.db}"

echo "== Building the console bundle =="
python3 scripts/build_web.py

echo
echo "== Emporion desk =="
echo "   URL:        http://127.0.0.1:${PORT}/"
echo "   GP console: sign in as ${GP_EMAIL}, then open the account menu"
echo "   Health:     http://127.0.0.1:${PORT}/api/health"
echo "   Live report http://127.0.0.1:${PORT}/api/report"
echo
echo "   Sign-in codes print to this terminal (dev mail fallback)."
echo "   Ctrl-C to stop."
echo
exec python3 -m hedge_desk.server
