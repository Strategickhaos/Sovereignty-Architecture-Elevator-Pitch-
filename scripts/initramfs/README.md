# SAGCO initramfs Scripts

This directory contains scripts that integrate with the initramfs (initial RAM filesystem) to verify SAGCO artifacts during early boot.

## Files

- `sagco-verify` - Main verification script (runs during init-premount)
- `sagco-hook` - Hook script to include SAGCO scripts in initramfs

## Purpose

The initramfs stage (Stage 2 in SBIP) performs:
1. Display SAGCO identity information
2. Verify core artifacts using SHA256 checksums
3. Check for `sagco=1` kernel command line flag
4. Prepare for root filesystem mount

## Installation

```bash
# 1. Install verification script
sudo mkdir -p /usr/local/share/sagco/scripts
sudo cp scripts/initramfs/sagco-verify /usr/local/share/sagco/scripts/
sudo chmod +x /usr/local/share/sagco/scripts/sagco-verify

# 2. Install initramfs hook
sudo cp scripts/initramfs/sagco-hook /etc/initramfs-tools/hooks/sagco
sudo chmod +x /etc/initramfs-tools/hooks/sagco

# 3. Update initramfs to include SAGCO scripts
sudo update-initramfs -u

# 4. Verify inclusion (optional)
lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco
```

## How It Works

1. During `update-initramfs`, the hook script (`sagco-hook`) is executed
2. The hook copies `sagco-verify` into the initramfs at `/scripts/init-premount/`
3. During boot, initramfs runs all scripts in `/scripts/init-premount/`
4. `sagco-verify` displays SAGCO identity and performs artifact checks
5. Boot continues to mount root filesystem

## Verification Process

Currently, the verification process:
- Displays SAGCO identity banner
- Calculates SHA256 hashes of critical artifacts
- Logs verification attempts
- Checks for `sagco=1` kernel parameter

In production deployments, enhance with:
- Signed artifact verification
- TPM (Trusted Platform Module) integration
- Secure boot chain validation
- Alert on verification failure

## Debugging

View initramfs messages during boot:
```bash
# Check dmesg for SAGCO messages
dmesg | grep SAGCO

# View all boot messages
journalctl -b | grep -i sagco
```

## Security Considerations

- Hash values should be stored securely and signed
- Consider using TPM for secure hash storage
- Implement proper failure handling (halt boot on verification failure)
- Regular updates to hash values when components are updated

## Legal Notice

Property of Strategickhaos DAO LLC
Wyoming Entity: 2025-001708194 | EIN: 39-2923503
