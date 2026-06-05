# initramfs Boot Hook

This directory contains the initramfs hook script for SAGCO Boot Identity Pipeline (SBIP).

## Installation

1. Copy the hook script:
   ```bash
   sudo cp init-top/sagco-init /etc/initramfs-tools/scripts/init-top/
   sudo chmod +x /etc/initramfs-tools/scripts/init-top/sagco-init
   ```

2. (Optional) Create artifact verification files:
   ```bash
   sudo mkdir -p /etc/sagco
   # Create example artifact
   echo "SAGCO Core Artifact" | sudo tee /etc/sagco/core_artifact
   # Generate hash
   sha256sum /etc/sagco/core_artifact | sudo tee /etc/sagco/core_artifact.sha256
   ```

3. Update initramfs:
   ```bash
   sudo update-initramfs -u
   ```

## What It Does

The `sagco-init` script runs during early boot (Stage 2) and:
1. Checks if SAGCO boot mode is enabled (`sagco=1` kernel parameter)
2. Displays the SAGCO identity message
3. Verifies core artifacts using SHA256 hashes (if configured)
4. Logs the boot pipeline progress

## Verification

After installation, rebuild the initramfs and check it contains the hook:
```bash
lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco-init
```

## Notes

- The script requires the `sagco=1` kernel parameter to activate
- Artifact verification is optional but recommended for production
- Log messages appear in system journal: `journalctl -b | grep SAGCO`
