#!/bin/bash
# SAGCO Menu - Auto-launch on interactive login
# This script launches the SAGCO tools menu on interactive shell login

# Only run for interactive shells with a TTY
if [[ $- == *i* ]] && [[ -t 0 ]]; then
  # Check if SAGCO menu is available
  if [[ -f /opt/sagco/bin/sagco-menu.sh ]]; then
    # Only launch if not already in SAGCO menu (prevent recursion)
    if [[ -z "$SAGCO_MENU_ACTIVE" ]]; then
      export SAGCO_MENU_ACTIVE=1
      /opt/sagco/bin/sagco-menu.sh
      unset SAGCO_MENU_ACTIVE
    fi
  fi
fi
