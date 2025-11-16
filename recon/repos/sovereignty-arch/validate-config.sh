#!/usr/bin/env bash
# validate-config.sh - Validate discovery.yml configuration
set -euo pipefail

CONFIG_FILE="${1:-discovery.yml}"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Configuration file '$CONFIG_FILE' not found"
    exit 1
fi

echo "🔍 Validating $CONFIG_FILE..."

# Check if yq is available for YAML parsing
if ! command -v yq &> /dev/null; then
    echo "⚠️  yq not found - installing..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y yq
    elif command -v brew &> /dev/null; then
        brew install yq
    else
        echo "❌ Please install yq manually: https://github.com/mikefarah/yq"
        exit 1
    fi
fi

# Validation checks
errors=0

# Check required org fields
org_name=$(yq '.org.name' "$CONFIG_FILE")
if [[ "$org_name" == "null" || "$org_name" == '""' ]]; then
    echo "❌ org.name is required"
    ((errors++))
fi

# Check Discord guild_id
guild_id=$(yq '.discord.guild_id' "$CONFIG_FILE")
if [[ "$guild_id" == "null" || "$guild_id" == '""' ]]; then
    echo "❌ discord.guild_id is required"
    ((errors++))
fi

# Check Git org
git_org=$(yq '.git.org' "$CONFIG_FILE")
if [[ "$git_org" == "null" || "$git_org" == '""' ]]; then
    echo "❌ git.org is required"
    ((errors++))
fi

# Check GitLens configuration
gitlens_enabled=$(yq '.git.gitlens.enabled' "$CONFIG_FILE")
if [[ "$gitlens_enabled" == "null" ]]; then
    echo "⚠️  GitLens integration not configured"
fi

# Check event gateway endpoints
endpoints_count=$(yq '.event_gateway.endpoints | length' "$CONFIG_FILE")
if [[ "$endpoints_count" == "0" ]]; then
    echo "❌ No event gateway endpoints configured"
    ((errors++))
fi

# Validate channel configuration
channels=$(yq '.discord.channels | keys' "$CONFIG_FILE")
expected_channels=("prs" "deployments" "dev_feed")
for channel in "${expected_channels[@]}"; do
    if ! echo "$channels" | grep -q "$channel"; then
        echo "⚠️  Recommended channel '#$channel' not configured"
    fi
done

# Summary
if [[ $errors -eq 0 ]]; then
    echo "✅ Configuration validation passed"
    echo ""
    echo "📋 Configuration Summary:"
    echo "   Organization: $(yq '.org.name' "$CONFIG_FILE")"
    echo "   Git Provider: $(yq '.git.provider' "$CONFIG_FILE")"
    echo "   Git Org: $(yq '.git.org' "$CONFIG_FILE")"
    echo "   GitLens Edition: $(yq '.git.gitlens.edition // "not configured"' "$CONFIG_FILE")"
    echo "   Environments: $(yq '.infra.environments[]' "$CONFIG_FILE" | tr '\n' ' ')"
    echo "   Event Endpoints: $endpoints_count"
    echo ""
    echo "🚀 Ready to generate bootstrapping scripts!"
else
    echo "❌ Found $errors configuration errors"
    echo "Please fix the errors above before proceeding"
    exit 1
fi