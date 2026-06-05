#!/bin/bash
# Quick Start Script for Proto-Elamite Dendritic Visualization Probe

set -e

echo "🧬 Proto-Elamite Dendritic Visualization Probe - Quick Start"
echo "=============================================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Step 1: Run the probe
echo "Step 1: Running dendritic visualization probe..."
echo "------------------------------------------------"
python3 dendritic_viz_probe.py
echo ""

# Step 2: Analyze the output
echo "Step 2: Analyzing probe output..."
echo "----------------------------------"
python3 analyze_dendritic_output.py neurograph/proto_elamite_pelsim1_dendrites.json
echo ""

# Step 3: Show file information
echo "Step 3: Output file details"
echo "----------------------------"
if [ -f "neurograph/proto_elamite_pelsim1_dendrites.json" ]; then
    FILE_SIZE=$(du -h neurograph/proto_elamite_pelsim1_dendrites.json | cut -f1)
    echo "✓ Output file: neurograph/proto_elamite_pelsim1_dendrites.json"
    echo "  Size: $FILE_SIZE"
    echo "  Ready for visualization in:"
    echo "    - Gephi (.gexf export)"
    echo "    - D3.js (direct JSON load)"
    echo "    - Cytoscape (.graphml export)"
    echo "    - vis.js (direct JSON load)"
else
    echo "❌ Output file not found"
    exit 1
fi
echo ""

# Step 4: Next steps
echo "🎯 Next Steps"
echo "-------------"
echo "1. Load neurograph/proto_elamite_pelsim1_dendrites.json in your viewer"
echo "2. Filter edges by color: green (safe), yellow (neutral), red (risky)"
echo "3. Analyze mutation patterns and evolutionary dynamics"
echo "4. Study the fitness landscape and danger zones"
echo ""
echo "📚 Documentation"
echo "----------------"
echo "  Full guide: README_DENDRITIC_PROBE.md"
echo "  Main README: README.md (dendritic probe section)"
echo ""
echo "✓ Quick start complete!"
