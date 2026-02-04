#!/bin/bash
#
# SAGCO OS Installation Script
# Installs SAGCO OS with TUI menu system
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SAGCO_DIR="$SCRIPT_DIR"

echo "============================================================"
echo "SAGCO OS Installer v1.0.0"
echo "Ratio Ex Nihilo - Reason from Nothing"
echo "============================================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Error: This script must be run as root (use sudo)"
    exit 1
fi

echo "[1/5] Installing required packages..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-yaml whiptail jq 2>&1 | grep -v "already the newest version" || true

echo "[2/5] Creating SAGCO directories..."
mkdir -p /opt/sagco/{assets,scripts,services}
mkdir -p /var/log/sagco
mkdir -p /var/lib/sagco

echo "[3/5] Copying SAGCO files..."
cp "$SAGCO_DIR/spm.yml" /opt/sagco/
cp "$SAGCO_DIR/assets/banner.ascii" /opt/sagco/assets/
cp "$SAGCO_DIR/scripts/sagco-menu.sh" /opt/sagco/scripts/
cp "$SAGCO_DIR/scripts/sagco-spm.py" /opt/sagco/scripts/
chmod +x /opt/sagco/scripts/sagco-menu.sh
chmod +x /opt/sagco/scripts/sagco-spm.py

echo "[4/5] Installing systemd services..."
cp "$SAGCO_DIR/services/sagco-banner.service" /etc/systemd/system/
cp "$SAGCO_DIR/services/sagco-runtime.service" /etc/systemd/system/
systemctl daemon-reload

echo "[5/5] Running SPM configuration..."
cd "$SAGCO_DIR"
python3 scripts/sagco-spm.py spm.yml

echo ""
echo "============================================================"
echo "SAGCO OS Installation Complete!"
echo "============================================================"
echo ""
echo "To test the TUI menu, run:"
echo "  sudo /opt/sagco/scripts/sagco-menu.sh"
echo ""
echo "To enable auto-start on login:"
echo "  sudo systemctl enable sagco-banner.service"
echo ""
echo "To start services now:"
echo "  sudo systemctl start sagco-banner.service"
echo "  sudo systemctl start sagco-runtime.service"
echo ""
echo "Logs can be found at:"
echo "  /var/log/sagco/"
echo ""
echo "🔥💜 Ratio Ex Nihilo 🔥💜"
echo ""
