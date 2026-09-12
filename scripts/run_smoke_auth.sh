#!/bin/bash
# Runs the auth lifecycle smoke against the local demo server.
#
# The server's GP address is read from the running server process's own environment
# rather than typed here, so PII never enters the command line, the transcript, or a log.
set -u
cd /Users/astra/workspace/projects/hedge-desk

PID=$(lsof -nP -iTCP:8765 -t 2>/dev/null | head -1)
if [ -z "$PID" ]; then echo "no server on 8765"; exit 1; fi

GP=$(ps eww -p "$PID" 2>/dev/null | tr ' ' '\n' | grep '^GP_EMAIL=' | head -1 | cut -d= -f2-)
if [ -z "$GP" ]; then
  echo "server process env did not expose GP_EMAIL; running without the GP lane check"
else
  echo "GP lane: address resolved from the server environment (not printed)"
fi

export GP_EMAIL="$GP"
exec node scripts/smoke_auth.mjs http://127.0.0.1:8765 /tmp/hd-demo-merged.log
