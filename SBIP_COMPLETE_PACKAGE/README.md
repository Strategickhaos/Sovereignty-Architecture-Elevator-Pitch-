# SBIP Complete Package
## Sovereign Boot Identity Pipeline
### Installation and Deployment Guide

---

## OVERVIEW

The SBIP Complete Package includes:

- **Kernel Module:** `sagco_cpu_mod.c` - Prints legal entity at boot
- **LLVM Compiler:** `flamelang_to_llvm.py` - Compiles FlameLang glyphs
- **Systemd Services:** 4 services for boot verification and runtime
- **GRUB Theme:** Sovereignty-branded boot screen
- **Scripts:** Installation and verification tools

---

## CONTENTS

```
SBIP_COMPLETE_PACKAGE/
├── kernel-module/
│   ├── sagco_cpu_mod.c       # Kernel module source
│   └── Makefile              # Build system
├── compiler/
│   ├── flamelang_to_llvm.py  # FlameLang compiler
│   └── glyph_map.json        # Example glyph mapping
├── systemd/
│   ├── sbip-verify.service           # Boot verification
│   ├── sbip-flamelang.service        # FlameLang init
│   ├── sbip-audit-log.service        # Audit logging
│   └── sbip-sovereignty-display.service  # TTY display
├── scripts/
│   ├── sbip-verify.sh        # Verification script
│   ├── flamelang-init.sh     # FlameLang initialization
│   └── sbip-audit-log.sh     # Audit log script
├── grub-theme/
│   └── theme.txt             # GRUB theme config
└── README.md                 # This file
```

---

## PREREQUISITES

### Required

- Linux kernel 5.x or later
- GRUB2 bootloader
- systemd init system
- GCC and kernel headers (`linux-headers-$(uname -r)`)
- Python 3.8+

### Optional

- LLVM/Clang toolchain (for FlameLang compilation to machine code)
- Secure Boot disabled (or kernel module signing setup)

---

## INSTALLATION

### Step 1: Build and Install Kernel Module

```bash
cd kernel-module

# Build the module
make

# Install the module
sudo make install

# Verify installation
lsmod | grep sagco_cpu_mod
```

### Step 2: Install Systemd Services

```bash
cd ../systemd

# Copy service files
sudo cp *.service /etc/systemd/system/

# Copy scripts
sudo cp ../scripts/*.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/sbip-*.sh
sudo chmod +x /usr/local/bin/flamelang-init.sh

# Enable services
sudo systemctl daemon-reload
sudo systemctl enable sbip-verify.service
sudo systemctl enable sbip-flamelang.service
sudo systemctl enable sbip-audit-log.service
sudo systemctl enable sbip-sovereignty-display.service
```

### Step 3: Install FlameLang Compiler

```bash
cd ../compiler

# Install compiler
sudo cp flamelang_to_llvm.py /usr/local/bin/
sudo chmod +x /usr/local/bin/flamelang_to_llvm.py

# Install default glyph map
sudo mkdir -p /etc/flamelang
sudo cp glyph_map.json /etc/flamelang/
```

### Step 4: Install GRUB Theme (Optional)

```bash
cd ../grub-theme

# Create theme directory
sudo mkdir -p /boot/grub/themes/sovereign

# Copy theme
sudo cp theme.txt /boot/grub/themes/sovereign/

# Update GRUB config
echo 'GRUB_THEME="/boot/grub/themes/sovereign/theme.txt"' | sudo tee -a /etc/default/grub

# Regenerate GRUB config
sudo update-grub  # Debian/Ubuntu
# OR
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # Fedora/RHEL
```

### Step 5: Create Directories

```bash
# Create runtime directories
sudo mkdir -p /var/lib/sbip
sudo mkdir -p /var/log/sbip
sudo mkdir -p /var/lib/flamelang
sudo mkdir -p /var/log/flamelang
```

### Step 6: Reboot

```bash
sudo reboot
```

---

## VERIFICATION

After reboot, verify SBIP is working:

### Check Kernel Module

```bash
# Verify module is loaded
lsmod | grep sagco_cpu_mod

# Check kernel log for sovereignty message
dmesg | grep -A 10 "SAGCO SOVEREIGN BOOT"

# Read entity info from /proc
cat /proc/sagco/entity
```

Expected output:
```
Legal Entity: Strategickhaos DAO LLC
Jurisdiction: Wyoming, USA
Entity ID: StrategicKhaos-DAO-2024-WY
Operator: DOM_010101
Declared At: 1738697987123456789 ns
Entity Hash: 0x1234567890abcdef
Verified: Yes
```

### Check Systemd Services

```bash
# Check all SBIP services
systemctl status sbip-verify.service
systemctl status sbip-flamelang.service
systemctl status sbip-audit-log.service
systemctl status sbip-sovereignty-display.service
```

All services should show "active" or "exited (success)".

### Check Audit Log

```bash
# View boot audit log
cat /var/log/sbip/boot_audit.log

# Check last verified boot timestamp
cat /var/lib/sbip/last_verified_boot
```

### Test FlameLang Compiler

```bash
# Create test glyph file
cat > /tmp/test.flame <<'EOF'
{sovereignty⟐verify}
EOF

# Compile to LLVM IR
flamelang_to_llvm.py /etc/flamelang/glyph_map.json /tmp/test.flame

# Check output
cat /tmp/test.ll
```

---

## CUSTOMIZATION

### Change Legal Entity

Edit the kernel module source:

```bash
# Edit sagco_cpu_mod.c
vim kernel-module/sagco_cpu_mod.c

# Change these values in sagco_cpu_init():
ret = sagco_declare_entity(
    "Your Organization Name",      # <- Change this
    "Your Jurisdiction",           # <- Change this
    "Your-Entity-ID",              # <- Change this
    "Your-Operator-ID"             # <- Change this
);

# Rebuild and reinstall
cd kernel-module
make clean && make
sudo make install
sudo reboot
```

### Add Custom Glyphs

Edit the glyph map:

```bash
sudo vim /etc/flamelang/glyph_map.json
```

Add new glyph mappings:

```json
{
  "glyphs": {
    "{your_glyph⟐modifier}": "/path/to/your/script.sh"
  }
}
```

### Modify GRUB Theme

Edit the theme configuration:

```bash
sudo vim /boot/grub/themes/sovereign/theme.txt
```

Then regenerate GRUB config:

```bash
sudo update-grub  # or grub2-mkconfig
```

---

## SECURITY CONSIDERATIONS

### Kernel Module Signing (Secure Boot)

If using Secure Boot, you must sign the kernel module:

```bash
# Generate signing key
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv \
  -outform DER -out MOK.der -days 36500 \
  -subj "/CN=Your Organization/"

# Sign module
/usr/src/linux-headers-$(uname -r)/scripts/sign-file \
  sha256 MOK.priv MOK.der kernel-module/sagco_cpu_mod.ko

# Enroll key
sudo mokutil --import MOK.der
# Follow prompts and reboot to enroll
```

### File Permissions

Verify secure permissions:

```bash
# Scripts should be executable only by root
sudo chmod 755 /usr/local/bin/sbip-*.sh
sudo chmod 755 /usr/local/bin/flamelang-init.sh

# Service files should be read-only
sudo chmod 644 /etc/systemd/system/sbip-*.service

# Audit logs should be append-only (optional)
sudo chattr +a /var/log/sbip/boot_audit.log
```

---

## TROUBLESHOOTING

### Kernel Module Won't Load

**Problem:** Module fails to load with "invalid module format"

**Solution:** Rebuild against current kernel headers

```bash
cd kernel-module
make clean
make
sudo make install
```

### /proc/sagco/entity Not Found

**Problem:** /proc interface not created

**Solution:** Check kernel log for errors

```bash
dmesg | grep SAGCO
# Look for error messages

# Try loading module manually
sudo modprobe sagco_cpu_mod
dmesg | tail -20
```

### Services Won't Start

**Problem:** Systemd services fail to start

**Solution:** Check service logs

```bash
journalctl -xeu sbip-verify.service
# Review error messages

# Check script permissions
ls -l /usr/local/bin/sbip-*.sh
# Should be executable
```

### FlameLang Compiler Fails

**Problem:** Compiler can't find glyph in map

**Solution:** Verify glyph map syntax

```bash
# Check JSON syntax
python3 -m json.tool /etc/flamelang/glyph_map.json

# Verify glyph exists in map
cat /etc/flamelang/glyph_map.json | grep "your_glyph"
```

---

## UNINSTALLATION

To remove SBIP:

```bash
# Stop and disable services
sudo systemctl stop sbip-*.service
sudo systemctl disable sbip-*.service

# Remove service files
sudo rm /etc/systemd/system/sbip-*.service
sudo systemctl daemon-reload

# Remove scripts
sudo rm /usr/local/bin/sbip-*.sh
sudo rm /usr/local/bin/flamelang-init.sh
sudo rm /usr/local/bin/flamelang_to_llvm.py

# Uninstall kernel module
cd kernel-module
sudo make uninstall

# Remove GRUB theme
sudo sed -i '/GRUB_THEME.*sovereign/d' /etc/default/grub
sudo update-grub

# Remove directories (optional)
sudo rm -rf /var/lib/sbip
sudo rm -rf /var/log/sbip
sudo rm -rf /var/lib/flamelang
sudo rm -rf /var/log/flamelang
sudo rm -rf /etc/flamelang
sudo rm -rf /boot/grub/themes/sovereign

# Reboot
sudo reboot
```

---

## SUPPORT

For issues or questions:

- GitHub: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- Organization: Strategickhaos DAO LLC
- License: GPL-2.0 (kernel module), MIT (compiler), GPL-3.0 (systemd)

---

## LICENSE

- **Kernel Module:** GPL-2.0 (Linux kernel compatibility)
- **FlameLang Compiler:** MIT (maximum reusability)
- **Systemd Services:** GPL-3.0 (systemd compatibility)
- **GRUB Theme:** CC-BY-SA-4.0 (creative commons)

---

## CREDITS

**Created during DSA Session:** DOM_010101_2025_02_04  
**Operator:** DOM_010101 (Dominick Garza)  
**Organization:** Strategickhaos DAO LLC  
**Methodology:** Dramatic Systems Archaeology (DSA)  

---

🔥 **SOVEREIGN BOOT ACHIEVED** 🔥

*"Trust nothing until it survives 100-angle crossfire."*
