#!/usr/bin/env bash
# Run the Emporion nightly batch (EOD -> overnight -> AM candidates) and log it.
#
# Intended to be fired by launchd at 4:30pm EST (13:30 local, DST-safe) after the
# market close. Regenerates artifacts/am-report-latest.json + am-demo.html, which
# the demo server serves live. Idempotent: re-running is safe (the report is
# content-addressed and overwritten atomically).
#
# Logs to LOG_DIR (default: repo artifacts/logs/). A timestamped line is written
# on start and on completion so an operator can see the batch ran and finished.
set -euo pipefail
cd "$(dirname "$0")/.."

LOG_DIR="${NIGHTLY_LOG_DIR:-$PWD/artifacts/logs}"
mkdir -p "$LOG_DIR"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
LOG="$LOG_DIR/nightly-$STAMP.log"

echo "[$STAMP] nightly batch start" | tee "$LOG"
python3 -m hedge_desk.am_demo >>"$LOG" 2>&1
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] nightly batch done" | tee -a "$LOG"

# Keep only the last 30 batch logs so the log dir does not grow unbounded.
ls -1t "$LOG_DIR"/nightly-*.log 2>/dev/null | tail -n +31 | xargs -r rm -f
