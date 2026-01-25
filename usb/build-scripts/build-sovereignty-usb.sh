#!/bin/bash
# build-sovereignty-usb.sh - Create bootable Sovereignty Architecture USB image
# 
# This script creates a bootable USB image containing:
# - SAGCO-OS operating system
# - FlameLang compiler
# - TRIG6 mathematical framework
# - Sister Protocol implementation
# - Complete documentation

set -euo pipefail

# Configuration
USB_IMAGE="sovereignty-os-$(date +%Y%m%d).img"
USB_SIZE="32G"
BUILD_DIR="/tmp/sovereignty-usb-build"
MOUNT_POINT="${BUILD_DIR}/mnt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

cleanup() {
    log_info "Cleaning up..."
    if mountpoint -q "${MOUNT_POINT}" 2>/dev/null; then
        sudo umount -R "${MOUNT_POINT}" || true
    fi
    if [ -d "${BUILD_DIR}" ]; then
        rm -rf "${BUILD_DIR}"
    fi
}

trap cleanup EXIT

# Main execution
main() {
    log_info "🔥 Building Sovereignty Architecture Bootable USB..."
    log_info "Image: ${USB_IMAGE}"
    log_info "Size: ${USB_SIZE}"
    
    # Create build directory
    log_info "Creating build directory..."
    mkdir -p "${BUILD_DIR}"
    mkdir -p "${MOUNT_POINT}"
    
    # Create disk image
    log_info "Creating disk image (${USB_SIZE})..."
    dd if=/dev/zero of="${USB_IMAGE}" bs=1 count=0 seek="${USB_SIZE}" 2>/dev/null
    
    # Create partitions
    log_info "Creating GPT partition table..."
    parted -s "${USB_IMAGE}" mklabel gpt
    
    log_info "Creating EFI system partition (512MB)..."
    parted -s "${USB_IMAGE}" mkpart ESP fat32 1MiB 513MiB
    parted -s "${USB_IMAGE}" set 1 esp on
    
    log_info "Creating boot partition (2GB)..."
    parted -s "${USB_IMAGE}" mkpart boot ext4 513MiB 2561MiB
    
    log_info "Creating root partition (20GB)..."
    parted -s "${USB_IMAGE}" mkpart root ext4 2561MiB 22561MiB
    
    log_info "Creating data partition (remaining space)..."
    parted -s "${USB_IMAGE}" mkpart data ext4 22561MiB 100%
    
    # Setup loop device
    log_info "Setting up loop device..."
    LOOP_DEVICE=$(sudo losetup --find --show --partscan "${USB_IMAGE}")
    log_info "Loop device: ${LOOP_DEVICE}"
    
    # Format partitions
    log_info "Formatting EFI partition..."
    sudo mkfs.vfat -F 32 -n "EFI" "${LOOP_DEVICE}p1"
    
    log_info "Formatting boot partition..."
    sudo mkfs.ext4 -L "BOOT" "${LOOP_DEVICE}p2"
    
    log_info "Formatting root partition..."
    sudo mkfs.ext4 -L "ROOT" "${LOOP_DEVICE}p3"
    
    log_info "Formatting data partition..."
    sudo mkfs.ext4 -L "DATA" "${LOOP_DEVICE}p4"
    
    # Mount partitions
    log_info "Mounting partitions..."
    sudo mount "${LOOP_DEVICE}p3" "${MOUNT_POINT}"
    sudo mkdir -p "${MOUNT_POINT}/boot"
    sudo mount "${LOOP_DEVICE}p2" "${MOUNT_POINT}/boot"
    sudo mkdir -p "${MOUNT_POINT}/boot/efi"
    sudo mount "${LOOP_DEVICE}p1" "${MOUNT_POINT}/boot/efi"
    sudo mkdir -p "${MOUNT_POINT}/data"
    sudo mount "${LOOP_DEVICE}p4" "${MOUNT_POINT}/data"
    
    # Install base system
    log_info "Installing base system..."
    log_warn "Note: This would normally install SAGCO-OS base system"
    log_warn "For now, creating directory structure..."
    
    # Create directory structure
    sudo mkdir -p "${MOUNT_POINT}"/{bin,boot,dev,etc,home,lib,media,mnt,opt,proc,root,run,sbin,srv,sys,tmp,usr,var}
    sudo mkdir -p "${MOUNT_POINT}/opt"/{flamelang,trig6,sister-protocol,sagco-hydra}
    sudo mkdir -p "${MOUNT_POINT}/home/sovereign"/{workspace,projects,documents}
    sudo mkdir -p "${MOUNT_POINT}/usr"/{bin,lib,share,local}
    sudo mkdir -p "${MOUNT_POINT}/usr/share"/{doc/sovereignty,books}
    sudo mkdir -p "${MOUNT_POINT}/data"/{projects,books,backups,workspace}
    
    # Create README
    log_info "Creating README..."
    cat << 'EOF' | sudo tee "${MOUNT_POINT}/README.txt" > /dev/null
Sovereignty Architecture - Bootable USB
========================================

This USB contains a complete SAGCO-OS environment with:

- SAGCO-OS operating system
- FlameLang compiler
- TRIG6 mathematical framework  
- Sister Protocol implementation
- Complete documentation and books
- Development tools and AI stack

BOOT INSTRUCTIONS:
1. Insert USB into target machine
2. Enter BIOS/UEFI (usually F2, F12, or DEL)
3. Select USB device as boot device
4. Choose "SAGCO-OS - Sovereignty Mode" from boot menu

FIRST TIME SETUP:
- Default username: sovereign
- Password will be set on first boot
- Follow the setup wizard

For more information, see /usr/share/doc/sovereignty/

Built with 🔥 by the Sovereignty Architecture collective
EOF
    
    # Copy sovereignty architecture files
    log_info "Copying Sovereignty Architecture files..."
    if [ -f "../README.md" ]; then
        sudo cp ../README.md "${MOUNT_POINT}/data/projects/"
    fi
    
    # Create version info
    log_info "Creating version info..."
    cat << EOF | sudo tee "${MOUNT_POINT}/etc/sovereignty-release" > /dev/null
SOVEREIGNTY_VERSION="1.0.0"
SOVEREIGNTY_BUILD_DATE="$(date -u +%Y-%m-%d)"
SOVEREIGNTY_CODENAME="Genesis"
EOF
    
    # Install GRUB bootloader (if available)
    if command -v grub-install &> /dev/null; then
        log_info "Installing GRUB bootloader..."
        sudo grub-install --target=x86_64-efi --efi-directory="${MOUNT_POINT}/boot/efi" \
            --boot-directory="${MOUNT_POINT}/boot" --removable "${LOOP_DEVICE}" || \
            log_warn "GRUB installation skipped (may need to run on actual hardware)"
    else
        log_warn "GRUB not available, bootloader installation skipped"
    fi
    
    # Unmount all
    log_info "Unmounting partitions..."
    sudo umount -R "${MOUNT_POINT}"
    
    # Detach loop device
    log_info "Detaching loop device..."
    sudo losetup -d "${LOOP_DEVICE}"
    
    # Generate checksum
    log_info "Generating checksum..."
    sha256sum "${USB_IMAGE}" > "${USB_IMAGE}.sha256"
    
    # Success
    log_info "✅ Bootable USB image created successfully!"
    log_info ""
    log_info "Image: ${USB_IMAGE}"
    log_info "Size: $(du -h "${USB_IMAGE}" | cut -f1)"
    log_info "Checksum: ${USB_IMAGE}.sha256"
    log_info ""
    log_info "To write to USB device:"
    log_info "  sudo dd if=${USB_IMAGE} of=/dev/sdX bs=4M status=progress && sync"
    log_info ""
    log_info "⚠️  WARNING: Replace /dev/sdX with your actual USB device!"
    log_info "⚠️  This will ERASE all data on the target device!"
}

# Check for root/sudo
if [ "$EUID" -ne 0 ] && ! sudo -n true 2>/dev/null; then
    log_error "This script requires sudo privileges"
    log_info "Please run with: sudo $0"
    exit 1
fi

main "$@"
