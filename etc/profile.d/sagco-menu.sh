#!/bin/bash
# SAGCO Menu Integration - Run on interactive login
# This script launches the SAGCO menu on interactive shell login

# Only run for interactive sessions
if [[ $- == *i* ]] && [[ -t 0 ]]; then
  # Check if SAGCO menu is available
  if [[ -x /opt/sagco/bin/sagco-menu.sh ]]; then
    # Launch SAGCO menu
    /opt/sagco/bin/sagco-menu.sh
  fi
fi
