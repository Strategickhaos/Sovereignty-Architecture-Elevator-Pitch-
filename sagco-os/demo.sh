#!/bin/bash
#
# SAGCO OS Demo Script
# Demonstrates the TUI menu system without installing
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "============================================================"
echo "SAGCO OS Demo"
echo "============================================================"
echo ""

# Show banner
echo "1. Banner Display:"
echo "-------------------"
cat "$SCRIPT_DIR/assets/banner.ascii"
echo ""

# Show tools from YAML
echo "2. Available Tool Categories:"
echo "----------------------------"
python3 << 'EOF'
import yaml
import sys
sys.path.insert(0, '.')

with open('spm.yml', 'r') as f:
    config = yaml.safe_load(f)
    tools = config.get('tools', {})
    
    for name, data in tools.items():
        desc = data.get('description', name)
        items = data.get('items', [])
        print(f"\n📁 {name.upper()}: {desc}")
        print("   Tools:")
        for item in items:
            print(f"   • {item['name']}: {item['description']}")
            print(f"     Command: {item['command']}")
EOF

echo ""
echo "============================================================"
echo "3. Menu System Features:"
echo "----------------------------"
echo "✓ YAML-driven tool configuration"
echo "✓ Kali/Parrot-style categories"
echo "✓ Whiptail TUI for navigation"
echo "✓ Auto-start on login via systemd"
echo "✓ Supports nested menus"
echo "✓ Returns to menu after tool execution"
echo ""

echo "============================================================"
echo "To install SAGCO OS, run:"
echo "  sudo ./install.sh"
echo ""
echo "To test the menu (requires whiptail):"
echo "  sudo /opt/sagco/scripts/sagco-menu.sh"
echo ""
echo "🔥💜 Ratio Ex Nihilo 🔥💜"
echo "============================================================"
