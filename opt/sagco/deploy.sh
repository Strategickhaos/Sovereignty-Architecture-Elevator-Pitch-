#!/bin/bash
# SAGCO-MENU v1.1 Deployment Script
# Copies files to system locations and sets up permissions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔥 SAGCO-MENU v1.1 Deployment 🔥"
echo "================================"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)"
   exit 1
fi

echo "📂 Creating directories..."
mkdir -p /opt/sagco/bin
mkdir -p /var/lib/sagco
mkdir -p /etc/profile.d

echo "📄 Copying YAML configuration..."
cp "$REPO_ROOT/opt/sagco/spm.yml" /opt/sagco/spm.yml
chmod 644 /opt/sagco/spm.yml

echo "🐍 Copying Python menu script..."
cp "$REPO_ROOT/opt/sagco/bin/sagco-menu.py" /opt/sagco/bin/sagco-menu.py
chmod 755 /opt/sagco/bin/sagco-menu.py

echo "📜 Copying Bash wrapper..."
cp "$REPO_ROOT/opt/sagco/bin/sagco-menu.sh" /opt/sagco/bin/sagco-menu.sh
chmod 755 /opt/sagco/bin/sagco-menu.sh

echo "🔗 Copying profile integration..."
cp "$REPO_ROOT/etc/profile.d/sagco-menu.sh" /etc/profile.d/sagco-menu.sh
chmod 755 /etc/profile.d/sagco-menu.sh

echo "📋 Copying documentation..."
cp "$REPO_ROOT/opt/sagco/README.md" /opt/sagco/README.md
chmod 644 /opt/sagco/README.md

echo "🔒 Setting permissions..."
chmod 755 /var/lib/sagco
chown -R root:root /opt/sagco
chown -R root:root /etc/profile.d/sagco-menu.sh

echo ""
echo "✅ SAGCO-MENU v1.1 deployed successfully!"
echo ""
echo "📝 Next steps:"
echo "  1. Verify dependencies:"
echo "     - python3 --version"
echo "     - python3 -c 'import yaml'"
echo "     - which whiptail"
echo ""
echo "  2. Test the menu:"
echo "     /opt/sagco/bin/sagco-menu.py categories"
echo "     /opt/sagco/bin/sagco-menu.sh  # (requires TTY)"
echo ""
echo "  3. Customize tools:"
echo "     Edit /opt/sagco/spm.yml"
echo ""
echo "  4. Login to any terminal to see the menu!"
echo ""
echo "📖 Documentation: /opt/sagco/README.md"
