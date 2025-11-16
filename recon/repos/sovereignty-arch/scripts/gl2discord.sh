#!/usr/bin/env bash
set -euo pipefail
: "${DISCORD_TOKEN:?missing}"
: "${CHANNEL_ID:?missing}"
TITLE="${1:-GitLens Notice}"
BODY="${2:-}"
curl -sS -H "Authorization: Bot $DISCORD_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" '{embeds:[{title:$t,description:$b,color:3099199}]}')"