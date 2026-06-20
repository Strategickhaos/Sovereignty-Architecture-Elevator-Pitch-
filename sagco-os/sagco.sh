#!/usr/bin/env bash
# SAGCO OS — Bash entry point
# Usage: ./sagco.sh [command] [args...]
# Or:    bash sagco.sh [command] [args...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

# Ensure we're in the sagco-os directory
cd "$SCRIPT_DIR"

# Check Python version
$PYTHON --version >/dev/null 2>&1 || { echo "ERROR: python3 not found"; exit 1; }

# Run the CLI
exec $PYTHON "$SCRIPT_DIR/sagco_cli.py" "$@"
