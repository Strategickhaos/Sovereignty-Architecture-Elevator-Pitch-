#!/bin/bash
# SAGCO Menu Integration
# Auto-launch on interactive login

# Determine repository root
# Set REPO_ROOT environment variable before sourcing, or it will try common locations
if [[ -z "$REPO_ROOT" ]]; then
  # Try to find SAGCO installation
  if [[ -f /opt/sagco/bin/sagco-menu.sh ]]; then
    SAGCO_MENU="/opt/sagco/bin/sagco-menu.sh"
  elif [[ -f "$HOME/sagco/opt/sagco/bin/sagco-menu.sh" ]]; then
    SAGCO_MENU="$HOME/sagco/opt/sagco/bin/sagco-menu.sh"
  else
    # Fallback to CI/development path
    REPO_ROOT="${REPO_ROOT:-/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-}"
    SAGCO_MENU="$REPO_ROOT/opt/sagco/bin/sagco-menu.sh"
  fi
else
  SAGCO_MENU="$REPO_ROOT/opt/sagco/bin/sagco-menu.sh"
fi

if [[ -t 0 && -f "$SAGCO_MENU" ]]; then
  # Only run if interactive TTY and menu exists
  "$SAGCO_MENU"
fi
