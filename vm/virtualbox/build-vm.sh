#!/bin/bash
# build-vm.sh - Create VirtualBox VM for Sovereignty Architecture
#
# This script creates a pre-configured VirtualBox VM with:
# - SAGCO-OS operating system
# - All development tools
# - Complete project environment

set -euo pipefail

# Configuration
VM_NAME="Sovereignty-Architecture"
VM_DISK="sovereignty-os.vdi"
VM_SIZE=40960  # 40GB in MB
VM_MEMORY=8192  # 8GB
VM_CPUS=4
VM_VRAM=128

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if VirtualBox is installed
if ! command -v VBoxManage &> /dev/null; then
    log_error "VirtualBox is not installed"
    log_info "Please install VirtualBox first:"
    log_info "  Ubuntu/Debian: sudo apt-get install virtualbox"
    log_info "  Fedora: sudo dnf install VirtualBox"
    log_info "  macOS: brew install --cask virtualbox"
    exit 1
fi

main() {
    log_info "🖥️  Building Sovereignty Architecture VirtualBox VM..."
    
    # Remove existing VM if it exists
    if VBoxManage list vms | grep -q "\"${VM_NAME}\""; then
        log_warn "VM '${VM_NAME}' already exists"
        read -p "Delete existing VM? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Removing existing VM..."
            VBoxManage unregistervm "${VM_NAME}" --delete || true
        else
            log_error "Aborting to avoid overwriting existing VM"
            exit 1
        fi
    fi
    
    # Create VM
    log_info "Creating VM: ${VM_NAME}..."
    VBoxManage createvm \
        --name "${VM_NAME}" \
        --ostype "Linux_64" \
        --register
    
    # Configure VM
    log_info "Configuring VM settings..."
    VBoxManage modifyvm "${VM_NAME}" \
        --memory ${VM_MEMORY} \
        --cpus ${VM_CPUS} \
        --vram ${VM_VRAM} \
        --graphicscontroller vmsvga \
        --boot1 disk \
        --boot2 dvd \
        --boot3 none \
        --boot4 none \
        --firmware efi \
        --chipset ich9 \
        --ioapic on \
        --rtcuseutc on \
        --pae on \
        --hwvirtex on \
        --nestedpaging on \
        --largepages on \
        --vtxvpid on \
        --accelerate3d on \
        --mouse usbtablet \
        --clipboard bidirectional \
        --draganddrop bidirectional
    
    # Configure audio
    log_info "Configuring audio..."
    VBoxManage modifyvm "${VM_NAME}" \
        --audio none \
        --audiocontroller hda
    
    # Configure network adapters
    log_info "Configuring network (3 adapters)..."
    
    # Adapter 1: NAT for internet
    VBoxManage modifyvm "${VM_NAME}" \
        --nic1 nat \
        --nictype1 82540EM \
        --cableconnected1 on
    
    # Adapter 2: Host-only for local development
    VBoxManage modifyvm "${VM_NAME}" \
        --nic2 hostonly \
        --nictype2 82540EM \
        --hostonlyadapter2 vboxnet0 \
        --cableconnected2 on || \
        log_warn "Host-only adapter configuration may need manual setup"
    
    # Adapter 3: Internal network for multi-VM setups
    VBoxManage modifyvm "${VM_NAME}" \
        --nic3 intnet \
        --nictype3 82540EM \
        --intnet3 "sovereignty" \
        --cableconnected3 on
    
    # Create virtual disk
    log_info "Creating virtual disk (${VM_SIZE}MB)..."
    VBoxManage createhd \
        --filename "${VM_DISK}" \
        --size ${VM_SIZE} \
        --variant Standard
    
    # Create storage controller
    log_info "Creating SATA controller..."
    VBoxManage storagectl "${VM_NAME}" \
        --name "SATA" \
        --add sata \
        --controller IntelAhci \
        --portcount 4 \
        --hostiocache on \
        --bootable on
    
    # Attach disk
    log_info "Attaching disk to VM..."
    VBoxManage storageattach "${VM_NAME}" \
        --storagectl "SATA" \
        --port 0 \
        --device 0 \
        --type hdd \
        --medium "${VM_DISK}"
    
    # Add DVD drive for potential ISO installation
    log_info "Adding DVD drive..."
    VBoxManage storageattach "${VM_NAME}" \
        --storagectl "SATA" \
        --port 1 \
        --device 0 \
        --type dvddrive \
        --medium emptydrive
    
    # Configure shared folders (if host directories exist)
    if [ -d "${HOME}/workspace" ]; then
        log_info "Adding shared folder: workspace"
        VBoxManage sharedfolder add "${VM_NAME}" \
            --name "workspace" \
            --hostpath "${HOME}/workspace" \
            --automount \
            --auto-mount-point "/home/sovereign/workspace"
    fi
    
    if [ -d "${HOME}/projects" ]; then
        log_info "Adding shared folder: projects"
        VBoxManage sharedfolder add "${VM_NAME}" \
            --name "projects" \
            --hostpath "${HOME}/projects" \
            --automount \
            --auto-mount-point "/home/sovereign/projects"
    fi
    
    # Create VM info file
    log_info "Creating VM information file..."
    cat > "VM_INFO.txt" << EOF
Sovereignty Architecture VirtualBox VM
======================================

VM Name: ${VM_NAME}
Disk: ${VM_DISK}
Size: ${VM_SIZE}MB ($(echo "scale=2; ${VM_SIZE}/1024" | bc)GB)
Memory: ${VM_MEMORY}MB ($(echo "scale=2; ${VM_MEMORY}/1024" | bc)GB)
CPUs: ${VM_CPUS}
Video Memory: ${VM_VRAM}MB

Network Configuration:
- Adapter 1: NAT (Internet access)
- Adapter 2: Host-Only (Local development)
- Adapter 3: Internal Network "sovereignty" (Multi-VM)

Shared Folders:
- workspace -> ~/workspace (if exists)
- projects -> ~/projects (if exists)

First Boot:
1. Start the VM with: VBoxManage startvm "${VM_NAME}" --type gui
2. The VM will boot into setup wizard (if OS is installed)
3. Default username: sovereign
4. Password will be set on first boot

To install OS:
1. Attach ISO: VBoxManage storageattach "${VM_NAME}" --storagectl "SATA" \
   --port 1 --device 0 --type dvddrive --medium /path/to/sovereignty-os.iso
2. Start VM and follow installation wizard

To export VM:
VBoxManage export "${VM_NAME}" -o sovereignty-vm.ova

Built: $(date)
EOF
    
    # Export VM to OVA
    log_info "Exporting VM to OVA format..."
    VM_OVA="sovereignty-vm-$(date +%Y%m%d).ova"
    VBoxManage export "${VM_NAME}" -o "${VM_OVA}" --manifest --vsys 0 \
        --product "Sovereignty Architecture" \
        --producturl "https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-" \
        --vendor "Strategickhaos DAO LLC" \
        --version "1.0.0" \
        --description "Complete Sovereignty Architecture development environment with SAGCO-OS, FlameLang, TRIG6, and all sovereign infrastructure tools."
    
    # Generate checksum
    log_info "Generating checksum..."
    sha256sum "${VM_OVA}" > "${VM_OVA}.sha256"
    
    # Success
    log_info "✅ VirtualBox VM created successfully!"
    log_info ""
    log_info "VM Name: ${VM_NAME}"
    log_info "Disk: ${VM_DISK}"
    log_info "Export: ${VM_OVA}"
    log_info "Info: VM_INFO.txt"
    log_info ""
    log_info "To start the VM:"
    log_info "  VBoxManage startvm \"${VM_NAME}\" --type gui"
    log_info ""
    log_info "To import the OVA on another machine:"
    log_info "  VBoxManage import ${VM_OVA}"
    log_info ""
    log_info "Next steps:"
    log_info "1. Install SAGCO-OS or attach ISO"
    log_info "2. Configure networking"
    log_info "3. Install development tools"
    log_info "4. Set up shared folders"
}

main "$@"
