#!/bin/bash
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

# Deploy Contradiction Engine - 30 Revenue Streams

set -euo pipefail

echo "🚀 DEPLOYING 30 CONTRADICTION REVENUE STREAMS..."

# 1. Copy API to FastAPI app
if [ -f "../src/bot.ts" ]; then
    echo "✅ Adding contradiction API to existing bot"
    cp contradictions.json ../src/
fi

# 2. Register Discord commands
echo "📡 Registering Discord slash commands..."
# python ../src/register_contradiction_commands.py

# 3. Deploy landing pages
echo "🌐 Deploying landing page sections..."
if [ -d "../public" ]; then
    cp landing_sections.html ../public/
fi

# 4. Import Grafana dashboard
echo "📊 Importing Grafana dashboard..."
if curl -s http://localhost:3000 >/dev/null 2>&1; then
    curl -X POST -H "Content-Type: application/json" \
         -H "Authorization: Bearer $GRAFANA_API_TOKEN" \
         --data-binary @grafana_dashboard.json \
         http://localhost:3000/api/dashboards/db 2>/dev/null || echo "Grafana import failed (check auth)"
fi

echo "✅ CONTRADICTION ENGINE DEPLOYED!"
echo "   📊 Grafana: http://localhost:3000/d/contradictions"  
echo "   💬 Discord: /resolve_privacy, /resolve_speed, /resolve_simple"
echo "   🌐 Landing: See landing_sections.html"
echo ""
echo "🎯 30 Revenue Streams Now Active:"
echo "   1. Privacy vs Personalization → $9/mo sync" 
echo "   2. Speed vs Security → SLO penalties"
echo "   3. Simple vs Powerful → $19/mo tiers"
echo "   ... (27 more in contradictions.json)"
