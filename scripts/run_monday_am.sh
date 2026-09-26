#!/usr/bin/env bash
# Monday-morning pre-market report: turn Friday's close + weekend research into a
# fresh AM report ready before the 9:00am EST open.
#
# Fired by launchd (com.emporion.monday-am) at 8:00am EST (5:00 local). Re-runs
# the idempotent nightly batch so the AM report + dashboard carry a Monday
# timestamp and any weekend research, instead of sitting stale from Friday 4:30pm.
set -euo pipefail
cd "$(dirname "$0")/.."

LOG_DIR="${NIGHTLY_LOG_DIR:-$PWD/artifacts/logs}"
mkdir -p "$LOG_DIR"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
LOG="$LOG_DIR/monday-am-$STAMP.log"

echo "[$STAMP] monday-am start" | tee "$LOG"
python3 -m hedge_desk.am_demo >>"$LOG" 2>&1
python3 scripts/build_plotly_dashboard.py >>"$LOG" 2>&1
# Pre-market morning briefing, ready for the 9:00am EST open.
python3 scripts/build_morning_briefing.py >>"$LOG" 2>&1
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] monday-am done" | tee -a "$LOG"

# Keep only the last 30 logs.
ls -1t "$LOG_DIR"/monday-am-*.log 2>/dev/null | tail -n +31 | xargs -r rm -f
