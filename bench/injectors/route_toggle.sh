#!/usr/bin/env bash
# Route manipulation script for simulating BGP hijacks
set -euo pipefail

SUBCMD="$1"

case "$SUBCMD" in
  hijack)
    TARGET="${2:-8.8.8.8/32}"
    VIA="${3:-10.0.0.1}"
    ip route add "$TARGET" via "$VIA" 2>/dev/null || \
      ip route replace "$TARGET" via "$VIA"
    echo "Route hijacked: $TARGET via $VIA"
    ;;
  
  restore)
    TARGET="${2:-8.8.8.8/32}"
    ip route del "$TARGET" 2>/dev/null || true
    echo "Route restored: $TARGET"
    ;;
  
  show)
    TARGET="${2:-8.8.8.8}"
    ip route get "$TARGET"
    ;;
  
  *)
    echo "usage: $0 hijack <target> <gateway> | restore <target> | show <target>" >&2
    exit 1
    ;;
esac
