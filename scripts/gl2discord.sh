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
: "${DISCORD_WEBHOOK_URL:?missing}"
TITLE="${1:-GitLens Notice}"
BODY="${2:-}"
curl -sS -H "Content-Type: application/json" \
  -X POST "$DISCORD_WEBHOOK_URL" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" '{embeds:[{title:$t,description:$b,color:3099199}]}')"