#!/usr/bin/env bash
set -euo pipefail

IF="${IF:-tun0}"
CMD="$1"

case "$CMD" in
  down)
    ip link set "$IF" down
    ;;
  up)
    ip link set "$IF" up
    ;;
  *)
    echo "usage: $0 {up|down}" >&2
    exit 1
    ;;
esac
