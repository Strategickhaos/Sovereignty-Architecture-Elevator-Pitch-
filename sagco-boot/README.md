# SAGCO Boot System Files

This directory contains the systemd service units, verification scripts, and configuration files for the SAGCO Boot Identity Pipeline (SBIP).

## Directory Structure

```
sagco-boot/
├── systemd/              # Systemd service unit files
│   ├── sagco-runtime.service
│   ├── flamelang-compiler.service
│   └── network-sovereignty.service
├── initramfs/            # Initramfs scripts and assets
│   ├── init              # Main init script
│   ├── verify-kernel     # Kernel signature verification
│   ├── verify-initramfs  # Initramfs integrity check
│   ├── verify-artifact   # Generic artifact verification
│   └── sagco-splash      # Identity screen display
├── grub/                 # GRUB configuration and theme
│   ├── grub-config       # GRUB configuration snippet
│   └── theme/            # SAGCO GRUB theme assets
└── docs/                 # Installation and testing guides
    ├── INSTALL.md
    └── TESTING.md
```

## Quick Start

### 1. Install Systemd Services

```bash
# Copy service units to systemd directory
sudo cp sagco-boot/systemd/*.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable sagco-runtime.service
sudo systemctl enable flamelang-compiler.service
sudo systemctl enable network-sovereignty.service
```

### 2. Update GRUB Configuration

```bash
# Append SAGCO configuration to GRUB
sudo cat sagco-boot/grub/grub-config >> /etc/default/grub

# Update GRUB
sudo update-grub
# or on Fedora/RHEL:
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

### 3. Build Custom Initramfs

```bash
# Copy verification scripts
sudo cp sagco-boot/initramfs/* /usr/lib/initcpio/hooks/

# Generate new initramfs
sudo mkinitcpio -p linux
# or on Debian/Ubuntu:
sudo update-initramfs -u
```

### 4. Reboot and Verify

```bash
sudo reboot

# After boot, check SAGCO services
systemctl status sagco-runtime.service
systemctl status flamelang-compiler.service

# Check boot log for SAGCO identity assertion
dmesg | grep SAGCO
```

## Service Dependencies

```
sagco-runtime.service (First, Priority: -1000)
    ↓
flamelang-compiler.service (Depends on runtime)
    ↓
network-sovereignty.service (Monitors network)
    ↓
multi-user.target (System ready)
```

## Security Considerations

1. **GPG Keys**: Generate and install GPG keys for artifact signing
2. **Checksums**: Generate SHA256 checksums for all SAGCO artifacts
3. **Secure Boot**: Enable UEFI Secure Boot for bootloader verification
4. **TPM**: Use TPM 2.0 for hardware root of trust (optional)

## Documentation

- See [SAGCO_BOOT_IDENTITY_PIPELINE.md](../SAGCO_BOOT_IDENTITY_PIPELINE.md) for complete architecture
- See [INV-100_SAGCO_BOOT_IDENTITY_PIPELINE.md](../INV-100_SAGCO_BOOT_IDENTITY_PIPELINE.md) for invention details
- See [SAGCO_CPU_ARCHITECTURE_DECISION.md](../SAGCO_CPU_ARCHITECTURE_DECISION.md) for CPU architecture

## Support

- **Repository**: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- **Entity**: Strategickhaos DAO LLC (EIN: 39-2923503)
- **License**: MIT (See LICENSE file)

---

*Part of the SAGCO Boot Identity Pipeline*  
*Version 1.0 | 2026-02-04*
