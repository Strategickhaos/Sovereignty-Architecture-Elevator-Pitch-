#!/usr/bin/env bash
# Classic Watchdog - simple ping-based health checker

set -euo pipefail

TARGET="${TARGET:-8.8.8.8}"
INTERVAL="${INTERVAL:-5}"

while true; do
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  if ping -c 1 -W 2 "$TARGET" >/dev/null 2>&1; then
    echo "$TIMESTAMP OK"
  else
    echo "$TIMESTAMP FAIL"
  fi
  
  sleep "$INTERVAL"
done
