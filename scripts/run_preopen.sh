#!/usr/bin/env bash
# Pre-open report: fresh AM report + morning briefing ready before the 9:00am
# EST open, every trading day. The 4:30pm job ingests the close; this job turns
# the overnight/weekend research into the pre-open briefing.
set -euo pipefail
cd "$(dirname "$0")/.."

LOG_DIR="${NIGHTLY_LOG_DIR:-$PWD/artifacts/logs}"
mkdir -p "$LOG_DIR"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
LOG="$LOG_DIR/preopen-$STAMP.log"

echo "[$STAMP] preopen start" | tee "$LOG"
python3 -m hedge_desk.am_demo >>"$LOG" 2>&1
python3 scripts/build_plotly_dashboard.py >>"$LOG" 2>&1
python3 scripts/build_morning_briefing.py >>"$LOG" 2>&1
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] preopen done" | tee -a "$LOG"

ls -1t "$LOG_DIR"/preopen-*.log 2>/dev/null | tail -n +31 | xargs -r rm -f
