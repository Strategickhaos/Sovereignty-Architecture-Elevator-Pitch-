# SAGCO Initramfs Scripts

This directory contains early boot scripts for the SAGCO Boot Identity Pipeline (SBIP).

## Scripts

### sagco-verify
Boot-time verification script that runs during initramfs phase (early userspace). This script:

1. Checks if SAGCO mode is enabled via kernel cmdline (`sagco=1`)
2. Verifies core system artifacts using SHA-256 checksums
3. Logs verification results to the system journal

## Installation

To install the initramfs script on a Debian/Ubuntu-based system:

```bash
# Copy script to initramfs hooks directory
sudo cp initramfs/sagco-verify /etc/initramfs-tools/scripts/init-premount/

# Make executable
sudo chmod +x /etc/initramfs-tools/scripts/init-premount/sagco-verify

# Update initramfs
sudo update-initramfs -u

# Update GRUB to enable SAGCO mode (optional)
# Edit /etc/default/grub and add sagco=1 to GRUB_CMDLINE_LINUX_DEFAULT
# Then run:
# sudo update-grub
```

## Manifest File

The verification script looks for `/etc/sagco/manifest.sha256` containing checksums of critical system files. Example format:

```
d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2  /opt/sagco/bin/sagco-runtime
e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3  /opt/sagco/bin/flamelang-compiler
```

Create this file and ensure it's included in the initramfs image.

## Testing

After installation, reboot the system and check the journal for SAGCO verification messages:

```bash
sudo journalctl | grep SAGCO
```

## See Also

- [SBIP Specification](../docs/SBIP_SPEC_v1.0.md) - Complete SBIP v1.0 documentation
- [Services](../services/) - systemd service files
- [FlameLang Compiler](../src/compiler/flamelang_to_llvm.py) - LLVM-based compiler implementation
