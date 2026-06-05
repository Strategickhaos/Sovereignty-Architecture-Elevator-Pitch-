# Bootable USB Image

This directory contains scripts and resources for creating a bootable USB image of the complete Sovereignty Architecture system.

## Quick Start

```bash
cd build-scripts
sudo ./build-sovereignty-usb.sh
```

## What Gets Created

The script creates a bootable USB image with:

- **EFI System Partition (512MB)**: UEFI boot files
- **Boot Partition (2GB)**: Kernel and bootloader
- **Root Partition (20GB)**: SAGCO-OS system files
- **Data Partition (Remaining)**: Projects, documentation, user data

## Directory Structure on USB

```
/
├── bin/                    # System binaries
├── boot/                   # Boot files and kernel
├── opt/
│   ├── flamelang/          # FlameLang compiler
│   ├── trig6/              # TRIG6 math system
│   ├── sister-protocol/    # Sister Protocol
│   └── sagco-hydra/        # Hypervisor
├── home/sovereign/         # User home
└── data/
    ├── projects/           # Project files
    ├── books/              # Documentation
    └── backups/            # Backup storage
```

## Requirements

- 32GB+ USB drive
- Linux system with:
  - `parted`
  - `mkfs.vfat`
  - `mkfs.ext4`
  - `grub-efi`
  - `sudo` access

## Usage

### Build Image

```bash
sudo ./build-scripts/build-sovereignty-usb.sh
```

This creates `sovereignty-os-YYYYMMDD.img` in the current directory.

### Write to USB

**⚠️ WARNING: This will erase all data on the target USB device!**

```bash
# List devices to identify your USB
lsblk

# Write image (replace /dev/sdX with your USB device)
sudo dd if=sovereignty-os-20250125.img of=/dev/sdX bs=4M status=progress && sync
```

### Boot from USB

1. Insert USB into target machine
2. Enter BIOS/UEFI (usually F2, F12, or DEL key)
3. Select USB device as boot device
4. Choose "SAGCO-OS - Sovereignty Mode" from boot menu

## First Boot

On first boot:

1. Setup wizard will run
2. Create user account (default: `sovereign`)
3. Configure network
4. Install additional components (optional)
5. System will reboot

Default credentials after setup:
- Username: `sovereign`
- Password: Set during first boot

## Customization

Edit `build-sovereignty-usb.sh` to customize:

- Partition sizes
- Pre-installed software
- Default configuration
- Boot menu options

## Troubleshooting

**Image creation fails:**
- Ensure sufficient disk space (35GB+ free)
- Check sudo privileges
- Verify required tools are installed

**USB won't boot:**
- Disable Secure Boot in BIOS
- Try different USB port
- Verify image checksum
- Use a different USB drive

**Boot hangs:**
- Try "Safe Mode" from boot menu
- Check BIOS compatibility
- Review boot logs

## Advanced

### Test in QEMU

Before writing to USB, test the image:

```bash
qemu-system-x86_64 \
  -m 4096 \
  -boot d \
  -drive file=sovereignty-os-20250125.img,format=raw \
  -display gtk
```

### Customize Bootloader

Edit the GRUB configuration in the script or after mounting:

```bash
sudo mount /dev/sdX2 /mnt
sudo nano /mnt/boot/grub/grub.cfg
sudo umount /mnt
```

## Files

- `build-scripts/build-sovereignty-usb.sh` - Main build script
- `README.md` - This file

## Support

For issues or questions:
- Open an issue on GitHub
- See main repository documentation
- Check TROUBLESHOOTING section in main README

---

**Built with 🔥 by the Sovereignty Architecture collective**
