#!/usr/bin/env bash
set -euo pipefail
: "${DISCORD_WEBHOOK_URL:?missing}"
TITLE="${1:-GitLens Notice}"
BODY="${2:-}"
curl -sS -H "Content-Type: application/json" \
  -X POST "$DISCORD_WEBHOOK_URL" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" '{embeds:[{title:$t,description:$b,color:3099199}]}')"