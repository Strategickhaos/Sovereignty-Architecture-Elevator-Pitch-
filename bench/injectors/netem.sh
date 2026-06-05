#!/usr/bin/env bash
set -euo pipefail

IF="${IF:-eth0}"
SUBCMD="$1"

case "$SUBCMD" in
  set)
    DELAY="$2" # ms
    tc qdisc replace dev "$IF" root netem delay "${DELAY}ms"
    ;;
  clear)
    tc qdisc del dev "$IF" root 2>/dev/null || true
    ;;
  *)
    echo "usage: $0 set <ms> | clear" >&2
    exit 1
    ;;
esac
