#!/bin/bash
# SAGCO Menu Integration
# Auto-launch on interactive login

# Determine repository root (adjust path as needed for deployment)
REPO_ROOT="${REPO_ROOT:-/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-}"
SAGCO_MENU="$REPO_ROOT/opt/sagco/bin/sagco-menu.sh"

if [[ -t 0 && -f "$SAGCO_MENU" ]]; then
  # Only run if interactive TTY and menu exists
  "$SAGCO_MENU"
fi
