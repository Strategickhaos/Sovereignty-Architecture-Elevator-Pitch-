#!/bin/bash
# SBIP Validation Script
# Checks if SAGCO Boot Identity Pipeline components are properly installed

set -e

COLORS=true
if [ "$1" = "--no-color" ]; then
  COLORS=false
fi

# Color functions
green() { [ "$COLORS" = true ] && echo -e "\e[32m$1\e[0m" || echo "$1"; }
red() { [ "$COLORS" = true ] && echo -e "\e[31m$1\e[0m" || echo "$1"; }
yellow() { [ "$COLORS" = true ] && echo -e "\e[33m$1\e[0m" || echo "$1"; }
blue() { [ "$COLORS" = true ] && echo -e "\e[34m$1\e[0m" || echo "$1"; }

echo "=========================================="
echo "SBIP Installation Validation"
echo "=========================================="
echo ""

WARNINGS=0
ERRORS=0
SUCCESS=0

# Check GRUB theme
echo "$(blue '[1/8]') Checking GRUB theme..."
if [ -f /boot/grub/themes/sagco/theme.txt ]; then
  green "  ✓ GRUB theme file exists"
  SUCCESS=$((SUCCESS + 1))
else
  red "  ✗ GRUB theme file not found"
  ERRORS=$((ERRORS + 1))
fi

if grep -q "sagco=1" /etc/default/grub 2>/dev/null; then
  green "  ✓ GRUB config has sagco=1 parameter"
  SUCCESS=$((SUCCESS + 1))
else
  yellow "  ⚠ GRUB config missing sagco=1 parameter"
  WARNINGS=$((WARNINGS + 1))
fi

# Check Plymouth theme
echo "$(blue '[2/8]') Checking Plymouth theme..."
if [ -d /usr/share/plymouth/themes/sagco ]; then
  green "  ✓ Plymouth theme directory exists"
  SUCCESS=$((SUCCESS + 1))
  
  if [ -f /usr/share/plymouth/themes/sagco/sagco.plymouth ]; then
    green "  ✓ Plymouth theme definition file exists"
    SUCCESS=$((SUCCESS + 1))
  else
    red "  ✗ Plymouth theme definition not found"
    ERRORS=$((ERRORS + 1))
  fi
  
  if [ -f /usr/share/plymouth/themes/sagco/sagco.script ]; then
    green "  ✓ Plymouth script file exists"
    SUCCESS=$((SUCCESS + 1))
  else
    red "  ✗ Plymouth script not found"
    ERRORS=$((ERRORS + 1))
  fi
else
  red "  ✗ Plymouth theme directory not found"
  ERRORS=$((ERRORS + 1))
fi

current_theme=$(plymouth-set-default-theme 2>/dev/null || echo "unknown")
if [ "$current_theme" = "sagco" ]; then
  green "  ✓ SAGCO is the default Plymouth theme"
  SUCCESS=$((SUCCESS + 1))
else
  yellow "  ⚠ SAGCO is not the default theme (current: $current_theme)"
  WARNINGS=$((WARNINGS + 1))
fi

# Check initramfs hook
echo "$(blue '[3/8]') Checking initramfs hook..."
if [ -f /etc/initramfs-tools/scripts/init-top/sagco-init ]; then
  green "  ✓ initramfs hook script exists"
  SUCCESS=$((SUCCESS + 1))
  
  if [ -x /etc/initramfs-tools/scripts/init-top/sagco-init ]; then
    green "  ✓ Hook script is executable"
    SUCCESS=$((SUCCESS + 1))
  else
    red "  ✗ Hook script is not executable"
    ERRORS=$((ERRORS + 1))
  fi
else
  red "  ✗ initramfs hook not found"
  ERRORS=$((ERRORS + 1))
fi

# Check systemd services
echo "$(blue '[4/8]') Checking systemd services..."
services=("sagco-banner" "sagco-runtime" "sagco-compiler" "sagco-cpu")
for service in "${services[@]}"; do
  if [ -f "/etc/systemd/system/${service}.service" ]; then
    green "  ✓ ${service}.service exists"
    SUCCESS=$((SUCCESS + 1))
    
    if systemctl is-enabled "${service}.service" >/dev/null 2>&1; then
      green "  ✓ ${service}.service is enabled"
      SUCCESS=$((SUCCESS + 1))
    else
      yellow "  ⚠ ${service}.service is not enabled"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    red "  ✗ ${service}.service not found"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check runtime directory
echo "$(blue '[5/8]') Checking runtime directory..."
if [ -d /opt/sagco ]; then
  green "  ✓ /opt/sagco directory exists"
  SUCCESS=$((SUCCESS + 1))
  
  for file in runtime.sh flamelang-compiler sagco-cpu-vm; do
    if [ -f "/opt/sagco/$file" ]; then
      green "  ✓ $file exists"
      SUCCESS=$((SUCCESS + 1))
      
      if [ -x "/opt/sagco/$file" ]; then
        green "  ✓ $file is executable"
        SUCCESS=$((SUCCESS + 1))
      else
        red "  ✗ $file is not executable"
        ERRORS=$((ERRORS + 1))
      fi
    else
      red "  ✗ $file not found"
      ERRORS=$((ERRORS + 1))
    fi
  done
  
  for dir in artifacts assets; do
    if [ -d "/opt/sagco/$dir" ]; then
      green "  ✓ $dir directory exists"
      SUCCESS=$((SUCCESS + 1))
    else
      yellow "  ⚠ $dir directory not found"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
else
  red "  ✗ /opt/sagco directory not found"
  ERRORS=$((ERRORS + 1))
fi

# Check emblem images
echo "$(blue '[6/8]') Checking emblem images..."
emblem_found=false
if [ -f /boot/grub/themes/sagco/ratio_ex_nihilo.png ]; then
  green "  ✓ GRUB emblem image exists"
  SUCCESS=$((SUCCESS + 1))
  emblem_found=true
else
  yellow "  ⚠ GRUB emblem image not found"
  WARNINGS=$((WARNINGS + 1))
fi

if [ -f /usr/share/plymouth/themes/sagco/ratio_ex_nihilo.png ]; then
  green "  ✓ Plymouth emblem image exists"
  SUCCESS=$((SUCCESS + 1))
  emblem_found=true
else
  yellow "  ⚠ Plymouth emblem image not found"
  WARNINGS=$((WARNINGS + 1))
fi

if [ "$emblem_found" = false ]; then
  yellow "  ℹ No emblem images found - you need to add ratio_ex_nihilo.png"
fi

# Check kernel parameters
echo "$(blue '[7/8]') Checking kernel parameters..."
if grep -q "sagco=1" /proc/cmdline 2>/dev/null; then
  green "  ✓ Kernel booted with sagco=1 parameter"
  SUCCESS=$((SUCCESS + 1))
else
  yellow "  ⚠ Kernel not booted with sagco=1 (requires reboot after GRUB update)"
  WARNINGS=$((WARNINGS + 1))
fi

# Check service status
echo "$(blue '[8/8]') Checking service status..."
for service in "${services[@]}"; do
  if systemctl is-active "${service}.service" >/dev/null 2>&1; then
    green "  ✓ ${service}.service is running"
    SUCCESS=$((SUCCESS + 1))
  else
    status=$(systemctl is-active "${service}.service" 2>&1 || echo "inactive")
    if systemctl list-unit-files "${service}.service" >/dev/null 2>&1; then
      yellow "  ⚠ ${service}.service is $status"
      WARNINGS=$((WARNINGS + 1))
    fi
  fi
done

# Summary
echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
green "Success: $SUCCESS checks passed"
if [ $WARNINGS -gt 0 ]; then
  yellow "Warnings: $WARNINGS issues need attention"
fi
if [ $ERRORS -gt 0 ]; then
  red "Errors: $ERRORS critical issues found"
fi

echo ""
if [ $ERRORS -gt 0 ]; then
  red "❌ SBIP validation failed - fix errors above"
  exit 1
elif [ $WARNINGS -gt 0 ]; then
  yellow "⚠️  SBIP partially installed - review warnings"
  exit 0
else
  green "✅ SBIP fully installed and configured!"
  exit 0
fi
