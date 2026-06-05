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

# GitLens to Discord notification script
# Usage: ./gl2discord.sh TITLE [BODY] [COLOR]
set -euo pipefail

TITLE="${1:-GitLens Notice}"
BODY="${2:-}"
COLOR="${3:-3112951}"

if [[ -z "${DISCORD_WEBHOOK_URL:-}" ]]; then
    echo "Error: DISCORD_WEBHOOK_URL environment variable not set" >&2
    exit 1
fi

curl -sS -H "Content-Type: application/json" \
  -X POST "$DISCORD_WEBHOOK_URL" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" --argjson c "$COLOR" \
        '{embeds:[{title:$t, description:$b, color:$c}]}')"