#!/usr/bin/env bash
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