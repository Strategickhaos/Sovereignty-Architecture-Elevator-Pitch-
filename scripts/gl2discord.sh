#!/usr/bin/env bash
set -euo pipefail
# Skip silently if the webhook secret is not configured in this environment
[[ -z "${DISCORD_WEBHOOK_URL:-}" ]] && { echo "DISCORD_WEBHOOK_URL not set — skipping notification"; exit 0; }
TITLE="${1:-GitLens Notice}"
BODY="${2:-}"
curl -sS -H "Content-Type: application/json" \
  -X POST "$DISCORD_WEBHOOK_URL" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" '{embeds:[{title:$t,description:$b,color:3099199}]}')"