# VirtualBox VM

This directory contains scripts for creating a pre-configured VirtualBox VM with the complete Sovereignty Architecture environment.

## Quick Start

```bash
./build-vm.sh
```

## What Gets Created

The script creates:

- **VirtualBox VM** with optimal settings
- **Virtual disk** (40GB, dynamically allocated)
- **Network adapters** (NAT, Host-Only, Internal)
- **Shared folders** (if host directories exist)
- **OVA export** for easy distribution

## VM Specifications

- **Memory**: 8GB RAM (minimum 4GB)
- **CPUs**: 4 cores (minimum 2)
- **Video Memory**: 128MB
- **Disk**: 40GB (expandable to 100GB with additional data disks)
- **Firmware**: EFI
- **Network**: 3 adapters (NAT, Host-Only, Internal)

## Requirements

- VirtualBox 6.0 or later
- Host system with:
  - 12GB+ RAM (to allocate 8GB to VM)
  - 50GB+ free disk space
  - Virtualization enabled in BIOS

## Usage

### Create VM

```bash
./build-vm.sh
```

This will:
1. Create VM with optimal settings
2. Create virtual disk
3. Configure network adapters
4. Export to OVA format
5. Generate checksums

### Import Existing OVA

```bash
# Download OVA
wget https://github.com/Strategickhaos/.../sovereignty-vm.ova

# Verify checksum
sha256sum -c sovereignty-vm.ova.sha256

# Import
VBoxManage import sovereignty-vm.ova
```

### Start VM

```bash
# Command line
VBoxManage startvm "Sovereignty-Architecture" --type gui

# Or use VirtualBox GUI
# Select VM → Start → Normal Start
```

## Network Configuration

### Adapter 1: NAT
- **Purpose**: Internet access
- **IP**: Assigned by VirtualBox DHCP
- **Use**: Download packages, access external resources

### Adapter 2: Host-Only
- **Purpose**: Local development
- **IP**: 192.168.56.x (auto-assigned)
- **Use**: SSH from host, web development

### Adapter 3: Internal Network "sovereignty"
- **Purpose**: Multi-VM communication
- **IP**: Configure manually
- **Use**: Cluster setups, testing distributed systems

## Shared Folders

If host directories exist, they're automatically configured:

- `~/workspace` → `/home/sovereign/workspace`
- `~/projects` → `/home/sovereign/projects`

Access from VM:
```bash
cd ~/workspace
ls -la
```

## Pre-installed Software

The VM comes with:

### Operating System
- SAGCO-OS (custom Linux)
- Kernel 6.x LTS
- systemd init

### Development Tools
- FlameLang compiler
- GCC 13+, Clang/LLVM 17+
- Rust 1.75+
- Python 3.11+, Node.js 20 LTS
- Java OpenJDK 21

### Editors & IDEs
- VSCode with extensions
- Neovim with LSP
- tmux, screen

### Sovereignty Stack
- TRIG6 mathematical framework
- Sister Protocol
- SAGCO-HYDRA hypervisor
- ValorYield Engine

### AI Tools
- llama.cpp
- ollama
- Local LLM models
- Vector database (qdrant)

## Customization

### Modify VM Settings

```bash
# Change memory
VBoxManage modifyvm "Sovereignty-Architecture" --memory 16384

# Change CPUs
VBoxManage modifyvm "Sovereignty-Architecture" --cpus 8

# Add disk
VBoxManage createhd --filename data.vdi --size 102400
VBoxManage storageattach "Sovereignty-Architecture" \
  --storagectl "SATA" --port 2 --type hdd --medium data.vdi
```

### Export Modified VM

```bash
VBoxManage export "Sovereignty-Architecture" -o my-custom-vm.ova
```

## Troubleshooting

**Import fails:**
- Update VirtualBox to latest version
- Check available disk space
- Try importing with GUI

**VM won't start:**
- Ensure virtualization is enabled in BIOS
- Check VirtualBox error log
- Try reducing memory allocation

**Network not working:**
- Check VirtualBox network settings
- Ensure host-only adapter is created
- Reset network adapters

**Shared folders not accessible:**
- Install VirtualBox Guest Additions
- Add user to `vboxsf` group: `sudo usermod -a -G vboxsf sovereign`
- Restart VM

**Performance issues:**
- Allocate more RAM
- Increase CPU count
- Enable nested paging
- Use SSD for VM disk

## Advanced

### Headless Mode

Run VM without GUI:

```bash
VBoxManage startvm "Sovereignty-Architecture" --type headless

# Connect via SSH
ssh sovereign@192.168.56.x
```

### Snapshots

Create restore points:

```bash
# Create snapshot
VBoxManage snapshot "Sovereignty-Architecture" take "clean-install"

# List snapshots
VBoxManage snapshot "Sovereignty-Architecture" list

# Restore snapshot
VBoxManage snapshot "Sovereignty-Architecture" restore "clean-install"
```

### Clone VM

Create multiple instances:

```bash
VBoxManage clonevm "Sovereignty-Architecture" \
  --name "Sovereignty-Dev" \
  --register
```

## Files

- `build-vm.sh` - VM creation script
- `VM_INFO.txt` - Generated VM information
- `sovereignty-vm-YYYYMMDD.ova` - Exportable VM
- `README.md` - This file

## Support

For issues:
- Check VirtualBox logs: Settings → Logs
- See VirtualBox documentation
- Open issue on GitHub
- Check main repository README

---

**Built with 🔥 by the Sovereignty Architecture collective**
