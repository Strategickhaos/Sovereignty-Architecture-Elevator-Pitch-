#!/bin/bash
# SOPHIA MIND Quick Start Script
# Part of Strategickhaos Sovereignty Architecture

set -e

echo "🧠 SOPHIA MIND Brain Visualizer - Quick Start"
echo "============================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
cd python-core
pip3 install -r requirements.txt --quiet || pip3 install -r requirements.txt

# Run tests
echo ""
echo "🧪 Running tests..."
python3 test_sophia.py

# Success message
echo ""
echo "✨ SOPHIA MIND is ready!"
echo ""
cd ..
echo "Next steps:"
echo "1. Parse your vault:"
echo "   cd sophia-mind"
echo "   python3 python-core/sophia_parser.py ~/ObsidianVault ./graph_data.json"
echo ""
echo "2. Set up sync (optional):"
echo "   python3 python-core/sophia_sync.py ~/ObsidianVault \\"
echo "     --proton ~/ProtonDrive/ObsidianSync \\"
echo "     --git ~/Repositories/knowledge-base"
echo ""
echo "3. Load in Unity:"
echo "   - Copy unity-scripts/*.cs to your Unity project"
echo "   - Copy graph_data.json to Unity project root"
echo "   - Add SophiaGraphManager component to a GameObject"
echo "   - Press Play!"
echo ""
echo "📖 Full documentation: docs/DEPLOYMENT.md"
echo "🔥 Empire Eternal! ⚔️∞"
