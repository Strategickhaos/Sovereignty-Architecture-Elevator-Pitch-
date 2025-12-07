#!/bin/bash
# INVENTION #35: SHADOW MIRROR - Demonstration Script
# Shows the complete API Recon → MCP Tool Pipeline

set -e

echo "======================================================================"
echo "⚔️  SHADOW MIRROR - API Reconnaissance → MCP Tool Pipeline"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "api_recon/requirements.txt" ]; then
    echo "Error: Run this script from the repository root"
    exit 1
fi

echo "${BLUE}Step 1: Install Dependencies${NC}"
echo "Installing Python packages..."
pip install -q -r api_recon/requirements.txt
echo "${GREEN}✓ Dependencies installed${NC}"
echo ""

echo "${BLUE}Step 2: Parse Captured API Patterns${NC}"
echo "Using sample GCP Console capture..."
python -m api_recon.capture api_recon/examples/gcp_console_sample.json -o /tmp/shadow_mirror_patterns.json
echo "${GREEN}✓ API patterns parsed and normalized${NC}"
echo ""

echo "${BLUE}Step 3: Generate MCP Tools${NC}"
echo "Generating sovereign MCP tools..."
python -m api_recon.mcp_generator /tmp/shadow_mirror_patterns.json -o api_recon/generated_tools/
echo "${GREEN}✓ MCP tools generated${NC}"
echo ""

echo "${BLUE}Step 4: List Generated Tools${NC}"
if [ -d "api_recon/generated_tools" ]; then
    echo "Generated tools:"
    ls -1 api_recon/generated_tools/*.py 2>/dev/null | while read file; do
        echo "  - $(basename $file)"
    done
    echo ""
fi

echo "${BLUE}Step 5: Start Sovereign Console${NC}"
echo "Starting KhaosConsole on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
echo "${YELLOW}Open http://localhost:8000 in your browser to see the sovereign console${NC}"
echo ""

# Start the console
python -m api_recon.sovereign_console --tools-dir api_recon/generated_tools/
