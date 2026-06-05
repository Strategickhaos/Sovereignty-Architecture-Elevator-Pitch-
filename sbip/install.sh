#!/bin/bash
# SBIP Quick Installation Script
# Automates installation of SAGCO Boot Identity Pipeline

set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Error: This script must be run as root (use sudo)"
  exit 1
fi

SBIP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EMBLEM_PATH="${SBIP_DIR}/ratio_ex_nihilo.png"

echo "=========================================="
echo "SBIP Quick Installation"
echo "=========================================="
echo ""
echo "SBIP Directory: $SBIP_DIR"
echo ""

# Ask for confirmation
read -p "Install SAGCO Boot Identity Pipeline? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Installation cancelled."
  exit 0
fi

echo ""
echo "[1/6] Installing GRUB theme..."
mkdir -p /boot/grub/themes/sagco
cp "$SBIP_DIR/boot/grub/themes/sagco/theme.txt" /boot/grub/themes/sagco/
if [ -f "$EMBLEM_PATH" ]; then
  cp "$EMBLEM_PATH" /boot/grub/themes/sagco/
  echo "  ✓ Emblem copied to GRUB theme"
else
  echo "  ⚠ Warning: ratio_ex_nihilo.png not found, skipping emblem"
fi

# Backup and update GRUB config
if [ -f /etc/default/grub ]; then
  cp /etc/default/grub /etc/default/grub.backup.sbip
  echo "  ✓ Backed up GRUB config"
  
  # Update GRUB config
  if ! grep -q "sagco=1" /etc/default/grub; then
    sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash sagco=1"/' /etc/default/grub
  fi
  
  if ! grep -q 'GRUB_THEME="/boot/grub/themes/sagco/theme.txt"' /etc/default/grub; then
    echo 'GRUB_THEME="/boot/grub/themes/sagco/theme.txt"' >> /etc/default/grub
  fi
  
  echo "  ✓ Updated GRUB config"
  update-grub 2>/dev/null || echo "  ⚠ Warning: update-grub failed (might not be available)"
fi

echo ""
echo "[2/6] Installing Plymouth theme..."
mkdir -p /usr/share/plymouth/themes/sagco
cp "$SBIP_DIR/usr/share/plymouth/themes/sagco/sagco.plymouth" /usr/share/plymouth/themes/sagco/
cp "$SBIP_DIR/usr/share/plymouth/themes/sagco/sagco.script" /usr/share/plymouth/themes/sagco/
if [ -f "$EMBLEM_PATH" ]; then
  cp "$EMBLEM_PATH" /usr/share/plymouth/themes/sagco/
  echo "  ✓ Emblem copied to Plymouth theme"
fi

if command -v plymouth-set-default-theme >/dev/null 2>&1; then
  plymouth-set-default-theme sagco
  echo "  ✓ Set SAGCO as default Plymouth theme"
  update-initramfs -u 2>/dev/null || echo "  ⚠ Warning: update-initramfs failed"
else
  echo "  ⚠ Warning: Plymouth not found, skipping theme activation"
fi

echo ""
echo "[3/6] Installing initramfs hook..."
mkdir -p /etc/initramfs-tools/scripts/init-top
cp "$SBIP_DIR/etc/initramfs-tools/scripts/init-top/sagco-init" /etc/initramfs-tools/scripts/init-top/
chmod +x /etc/initramfs-tools/scripts/init-top/sagco-init
echo "  ✓ Copied initramfs hook"

# Create optional verification files
mkdir -p /etc/sagco
if [ ! -f /etc/sagco/core_artifact ]; then
  echo "SAGCO Core Artifact v1.0 - $(date)" > /etc/sagco/core_artifact
  sha256sum /etc/sagco/core_artifact > /etc/sagco/core_artifact.sha256
  echo "  ✓ Created artifact verification files"
fi

if command -v update-initramfs >/dev/null 2>&1; then
  update-initramfs -u
  echo "  ✓ Updated initramfs"
fi

echo ""
echo "[4/6] Installing systemd services..."
cp "$SBIP_DIR/etc/systemd/system/sagco-banner.service" /etc/systemd/system/
cp "$SBIP_DIR/etc/systemd/system/sagco-runtime.service" /etc/systemd/system/
cp "$SBIP_DIR/etc/systemd/system/sagco-compiler.service" /etc/systemd/system/
cp "$SBIP_DIR/etc/systemd/system/sagco-cpu.service" /etc/systemd/system/
echo "  ✓ Copied service files"

systemctl daemon-reload
echo "  ✓ Reloaded systemd"

echo ""
echo "[5/6] Installing runtime components..."
mkdir -p /opt/sagco/{artifacts,assets,src}
cp "$SBIP_DIR/opt/sagco/runtime.sh" /opt/sagco/
cp "$SBIP_DIR/opt/sagco/flamelang-compiler" /opt/sagco/
cp "$SBIP_DIR/opt/sagco/sagco-cpu-vm" /opt/sagco/
chmod +x /opt/sagco/runtime.sh
chmod +x /opt/sagco/flamelang-compiler
chmod +x /opt/sagco/sagco-cpu-vm
echo "  ✓ Installed runtime components"

echo ""
echo "[6/6] Enabling services..."
systemctl enable sagco-banner.service
systemctl enable sagco-runtime.service
systemctl enable sagco-compiler.service
systemctl enable sagco-cpu.service
echo "  ✓ Enabled all SAGCO services"

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Add your emblem: cp your-emblem.png $SBIP_DIR/ratio_ex_nihilo.png"
echo "  2. Re-run this script to copy the emblem"
echo "  3. Reboot to see SBIP in action: sudo reboot"
echo ""
echo "Verify installation: $SBIP_DIR/validate.sh"
echo ""
echo "To start services now (without reboot):"
echo "  sudo systemctl start sagco-banner"
echo "  sudo systemctl start sagco-runtime"
echo "  sudo systemctl start sagco-compiler"
echo "  sudo systemctl start sagco-cpu"
echo ""
