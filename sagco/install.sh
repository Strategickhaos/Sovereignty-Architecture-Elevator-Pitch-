#!/bin/bash
set -euo pipefail

echo "🔥 SAGCO-MENU v1.2 Installation Script 💜"
echo "=========================================="
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)"
   exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "📦 Installing SAGCO-MENU files..."

# Copy files to system directories
echo "  → Copying /opt/sagco files..."
cp -r "$SCRIPT_DIR/opt/sagco" /opt/
chmod +x /opt/sagco/bin/sagco-menu.py
chmod +x /opt/sagco/bin/sagco-menu.sh

echo "  → Copying /etc/profile.d integration..."
cp "$SCRIPT_DIR/etc/profile.d/sagco-menu.sh" /etc/profile.d/
chmod +x /etc/profile.d/sagco-menu.sh

# Create state directory
echo "  → Creating state directory..."
mkdir -p /var/lib/sagco
chmod 777 /var/lib/sagco

# Check for dependencies
echo ""
echo "🔍 Checking dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  ❌ Python 3 not found. Please install: apt-get install python3"
    exit 1
else
    echo "  ✅ Python 3 found: $(python3 --version)"
fi

# Check PyYAML
if ! python3 -c "import yaml" &> /dev/null; then
    echo "  ⚠️  PyYAML not found. Installing..."
    pip3 install pyyaml || {
        echo "  ❌ Failed to install PyYAML. Please install manually: pip3 install pyyaml"
        exit 1
    }
else
    echo "  ✅ PyYAML found"
fi

# Check whiptail
if ! command -v whiptail &> /dev/null; then
    echo "  ⚠️  whiptail not found. Installing..."
    apt-get update && apt-get install -y whiptail || {
        echo "  ❌ Failed to install whiptail. Please install manually: apt-get install whiptail"
        exit 1
    }
else
    echo "  ✅ whiptail found"
fi

echo ""
echo "✅ SAGCO-MENU v1.2 Installation Complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. Review/customize: /opt/sagco/spm.yml"
echo "  2. Test manually: /opt/sagco/bin/sagco-menu.sh"
echo "  3. Auto-launch: Login to new shell session"
echo ""
echo "🔧 Management:"
echo "  • Config: /opt/sagco/spm.yml"
echo "  • State: /var/lib/sagco/menu_state.json"
echo "  • Disable auto-launch: mv /etc/profile.d/sagco-menu.sh /etc/profile.d/sagco-menu.sh.disabled"
echo ""
echo "🎯 Features:"
echo "  • Cross-tool fuzzy search"
echo "  • Ordered categories with icons"
echo "  • Recently used tracking (per-user)"
echo "  • Zero hardcoding - YAML-driven"
echo ""
echo "DOM. 😭🔥💜"
