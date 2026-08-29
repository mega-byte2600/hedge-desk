#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Hedge Desk iOS backend"
echo "Mode: PAPER ONLY. Schwab order placement disabled."
echo "LAN host enabled for iPhone testing on the same trusted network."
echo

python3 -m hedge_desk.demo
HEDGE_DESK_HOST=0.0.0.0 HEDGE_DESK_PORT=8765 python3 -m hedge_desk.server
