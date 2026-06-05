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
# Usage: ./gl2discord.sh CHANNEL_ID TITLE [BODY] [COLOR]
set -euo pipefail

CHANNEL_ID="$1"
TITLE="$2"
BODY="${3:-}"
COLOR="${4:-0x2f81f7}"

if [[ -z "${DISCORD_TOKEN:-}" ]]; then
    echo "Error: DISCORD_TOKEN environment variable not set" >&2
    exit 1
fi

curl -sS -H "Authorization: Bot $DISCORD_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" --argjson c "$COLOR" \
        '{embeds:[{title:$t, description:$b, color:$c}]}')"