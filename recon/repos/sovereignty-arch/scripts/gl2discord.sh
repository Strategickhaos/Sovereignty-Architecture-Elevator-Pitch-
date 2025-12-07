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
: "${DISCORD_TOKEN:?missing}"
: "${CHANNEL_ID:?missing}"
TITLE="${1:-GitLens Notice}"
BODY="${2:-}"
curl -sS -H "Authorization: Bot $DISCORD_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" '{embeds:[{title:$t,description:$b,color:3099199}]}')"