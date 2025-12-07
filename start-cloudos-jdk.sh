#!/usr/bin/env bash
# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================

set -euo pipefail

case "${1:-}" in
  start)
    echo "Starting CloudOS JDK workspace (OpenJDK 21)..."
    docker compose up -d jdk-workspace
    docker compose logs -f jdk-workspace | grep -m 1 "Started" || true
    echo "Ready! http://java.localhost → app, :5005 → debug"
    ;;
  shell)
    docker exec -it cloudos-jdk bash
    ;;
  stop)
    docker compose down jdk-workspace
    ;;
  *)
    echo "Usage: $0 start|shell|stop"
    ;;
esac
