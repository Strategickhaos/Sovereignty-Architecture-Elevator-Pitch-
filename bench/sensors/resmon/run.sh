#!/usr/bin/env bash
# /bench/sensors/resmon/run.sh
#
# ResMon Sensor - Deterministic VPN State Classification
# Produces measurable, reproducible state classifications for benchmarking
#
# State Classification Rules:
#   Resonant:   latency < 200ms, all checks pass
#   Dissonant:  200-500ms latency, checks pass
#   Collapsed:  TCP down, interface down, or latency >= 500ms

set -euo pipefail

# Configuration (can be overridden by environment)
CHECK_HOST=${CHECK_HOST:-10.8.0.1}
CHECK_PORT=${CHECK_PORT:-22}
IF="tun0"
STATE_FILE="/bench/sensors/resmon/state.json"
LOG_FILE="/bench/sensors/resmon/log.jsonl"

# Ensure output directory exists
mkdir -p "$(dirname "$STATE_FILE")"

echo "Starting ResMon sensor..."
echo "Monitoring interface: $IF"
echo "Target host: $CHECK_HOST:$CHECK_PORT"
echo "Output: $STATE_FILE"
echo "Log: $LOG_FILE"

while true; do
  up=false
  route_ok=false
  tcp_ok=1  # Default to failure
  latency=999
  
  # 1. Interface check - is tun0 up?
  if ip link show "$IF" 2>/dev/null | grep -q "state UP"; then
      up=true
  fi

  # 2. Route check - does traffic to target route via VPN?
  if [ "$up" = true ]; then
      route=$(ip route get "$CHECK_HOST" 2>/dev/null || echo "")
      if [[ $route == *"$IF"* ]]; then
          route_ok=true
      fi
  fi

  # 3. TCP probe - can we connect to the target?
  if [ "$up" = true ] && [ "$route_ok" = true ]; then
      if nc -z -w 2 "$CHECK_HOST" "$CHECK_PORT" >/dev/null 2>&1; then
          tcp_ok=0
      fi
  fi

  # 4. Latency measurement (ms) using ping average
  if [ "$up" = true ] && [ "$route_ok" = true ] && [ $tcp_ok -eq 0 ]; then
      # Extract average latency from ping output
      # Example: "rtt min/avg/max/mdev = 10.123/25.456/40.789/15.321 ms"
      latency_output=$(ping -c3 -W1 "$CHECK_HOST" 2>/dev/null | tail -1 | awk -F '/' '{print $5}')
      if [ -n "$latency_output" ]; then
          latency=$latency_output
      fi
  fi

  # 5. State Classification using deterministic thresholds
  state="Collapsed"  # Default to worst state
  
  if [ "$up" = true ] && [ "$route_ok" = true ] && [ $tcp_ok -eq 0 ]; then
      # All checks pass, classify by latency
      if (( $(echo "$latency < 200" | bc -l 2>/dev/null || echo 0) )); then
          state="Resonant"
      elif (( $(echo "$latency >= 200 && $latency < 500" | bc -l 2>/dev/null || echo 0) )); then
          state="Dissonant"
      else
          state="Collapsed"
      fi
  fi

  # 6. Generate timestamp
  ts=$(date -Is)

  # 7. Append to JSONL log for time-series analysis
  echo "{\"ts\":\"$ts\",\"state\":\"$state\",\"latency\":$latency,\"interface_up\":$up,\"route_ok\":$route_ok,\"tcp_ok\":$([ $tcp_ok -eq 0 ] && echo true || echo false)}" >> "$LOG_FILE"

  # 8. Emit canonical ResMon JSON state file
  # This is the "current state" that can be queried by benchmarks
  jq -n \
    --arg st "$state" \
    --arg ts "$ts" \
    --arg host "$CHECK_HOST" \
    --arg ifname "$IF" \
    --arg up "$up" \
    --arg route_ok "$route_ok" \
    --argjson tcp_ok "$([ $tcp_ok -eq 0 ] && echo true || echo false)" \
    --arg latency "$latency" \
    '{
      seq: (now|floor),
      timestamp: $ts,
      state: $st,
      interface: {
        name: $ifname,
        up: ($up == "true")
      },
      route: {
        target: $host,
        via_vpn: ($route_ok == "true")
      },
      transport: {
        latency_ms: ($latency | tonumber),
        tcp_check: $tcp_ok
      }
    }' > "$STATE_FILE"

  # Log state change to console
  echo "[$(date -Is)] State: $state | Latency: ${latency}ms | IF: $up | Route: $route_ok | TCP: $([ $tcp_ok -eq 0 ] && echo OK || echo FAIL)"

  # Sleep before next check
  sleep 1
done
