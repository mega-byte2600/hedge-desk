#!/bin/bash
# Keeps the Emporion demo reachable without a human babysitting it.
#
# Why this exists: the demo runs as a process on this Mac, so a crash or an idle sleep
# turns a working URL into a dead one with no warning. This watchdog restarts the server
# if it stops answering, and caffeinate stops macOS from idling the machine to sleep
# while someone might be looking at the demo.
#
# Honest limit: this is a laptop-class safety net, not a host. It cannot survive the Mac
# being shut down, and it is not a substitute for the Render deployment.
set -u

REPO="/Users/astra/workspace/projects/hedge-desk"
PORT=8765
LOG="/tmp/hd-watchdog.log"
SERVER_LOG="/tmp/hd-demo-merged.log"

say() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }

# stop macOS from idle-sleeping while the demo is expected to be up
if ! pgrep -f "caffeinate -i -w" >/dev/null 2>&1; then
  nohup caffeinate -i -w $$ >/dev/null 2>&1 &
  say "caffeinate started (idle sleep blocked)"
fi

say "watchdog started (port $PORT)"

while true; do
  code=$(curl -sS -m 12 -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/api/health" 2>/dev/null)
  if [ "$code" != "200" ]; then
    say "health=$code -- restarting demo server"
    cd "$REPO" || exit 1
    # start detached so it outlives this watchdog's shell
    nohup env PORT=$PORT \
      MEMBERSHIP_DB=/tmp/hd-demo-live.db \
      GP_EMAIL=boltonmd13@gmail.com \
      MEMBERSHIP_SECRET=synthetic-local-secret \
      bash scripts/demo.sh >> "$SERVER_LOG" 2>&1 &
    sleep 25
    code2=$(curl -sS -m 12 -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/api/health" 2>/dev/null)
    say "after restart health=$code2"
  fi
  sleep 45
done
