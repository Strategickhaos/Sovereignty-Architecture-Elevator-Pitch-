#!/usr/bin/env bash
# ResMon sensor runner
# Monitors /flamelang/membrane/net_watchdog/state.json and logs state changes

set -euo pipefail

LOG_FILE="${LOG_FILE:-/bench/sensors/resmon/log.jsonl}"
STATE_FILE="${STATE_FILE:-/flamelang/membrane/net_watchdog/state.json}"
POLL_INTERVAL="${POLL_INTERVAL:-1}"

mkdir -p "$(dirname "$LOG_FILE")"

PREV_STATE=""

# Generate ISO 8601 timestamp with millisecond precision
get_timestamp() {
  # Try GNU date first (Linux)
  if date --version >/dev/null 2>&1; then
    date -u +"%Y-%m-%dT%H:%M:%S.%3NZ"
  else
    # Fallback for BSD/macOS date
    python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))"
  fi
}

while true; do
  if [ -f "$STATE_FILE" ]; then
    CURR_STATE=$(jq -r '.state' "$STATE_FILE" 2>/dev/null || echo "")
    
    if [ -n "$CURR_STATE" ] && [ "$CURR_STATE" != "$PREV_STATE" ]; then
      TIMESTAMP=$(get_timestamp)
      echo "{\"ts\":\"$TIMESTAMP\",\"state\":\"$CURR_STATE\"}" >> "$LOG_FILE"
      PREV_STATE="$CURR_STATE"
    fi
  fi
  
  sleep "$POLL_INTERVAL"
done
