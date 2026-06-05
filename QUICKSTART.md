# Sovereignty Architecture - Quick Start Guide

Welcome to the Sovereignty Architecture project! This guide will help you get started with the various distribution formats.

## 🚀 Choose Your Distribution Format

We provide multiple ways to use Sovereignty Architecture:

### 1. 📦 Bootable USB
**Best for**: Running on physical hardware, maximum portability

```bash
# Download the USB image
wget https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases/latest/download/sovereignty-os.img

# Verify checksum
sha256sum -c sovereignty-os.img.sha256

# Write to USB (⚠️ DANGER: This will erase all data on /dev/sdX)
sudo dd if=sovereignty-os.img of=/dev/sdX bs=4M status=progress && sync

# Boot from USB
# 1. Insert USB into target machine
# 2. Enter BIOS/UEFI (F2, F12, or DEL)
# 3. Select USB device
# 4. Choose "SAGCO-OS - Sovereignty Mode"
```

### 2. 🖥️ VirtualBox VM
**Best for**: Testing, development, running alongside existing OS

```bash
# Download the VM
wget https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases/latest/download/sovereignty-vm.ova

# Verify checksum
sha256sum -c sovereignty-vm.ova.sha256

# Import into VirtualBox
VBoxManage import sovereignty-vm.ova

# Start the VM
VBoxManage startvm "Sovereignty-Architecture" --type gui

# Or use VirtualBox GUI:
# File → Import Appliance → Select sovereignty-vm.ova
```

### 3. 🐙 GitHub Repository
**Best for**: Development, contributions, latest updates

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Install dependencies (varies by component)
# See component-specific README files

# Build from source
./tools/build-all.sh
```

### 4. ☁️ Proton Drive Backup
**Best for**: Secure offline backup, disaster recovery

```bash
# Set up Proton Drive
# 1. Mount Proton Drive (using rclone or native client)
# 2. Configure backup script

# Run backup
./backups/scripts/backup-to-proton.sh

# Restore from backup
# 1. Download encrypted backups from Proton Drive
# 2. Decrypt: gpg --decrypt code-snapshot.tar.gz.gpg > code-snapshot.tar.gz
# 3. Extract: tar xzf code-snapshot.tar.gz
```

## 📚 Documentation

- **Distribution Guide**: See `DISTRIBUTION_ARTIFACTS.md` for complete technical specifications
- **Movie Storyboard**: See `media/movie/storyboard/STORYBOARD.md` for documentary production plan
- **Main README**: See `README.md` for project overview

## 🎯 Common Tasks

### Building a Bootable USB
```bash
cd usb/build-scripts
sudo ./build-sovereignty-usb.sh
```

### Creating a VirtualBox VM
```bash
cd vm/virtualbox
./build-vm.sh
```

### Generating Backups
```bash
./backups/scripts/backup-to-proton.sh
```

### Building All Artifacts
```bash
./tools/build-all.sh
```

## 🔐 Security

### Verify Downloads
Always verify checksums before using downloaded artifacts:

```bash
sha256sum -c checksums.txt
```

### Verify GPG Signatures
If available, verify GPG signatures:

```bash
gpg --verify checksums.txt.asc
```

### Encryption
All backups are encrypted with GPG. To decrypt:

```bash
gpg --decrypt file.tar.gz.gpg > file.tar.gz
```

## 🆘 Troubleshooting

### USB Won't Boot
- Verify BIOS/UEFI is set to boot from USB
- Ensure Secure Boot is disabled
- Try different USB ports
- Verify image integrity with checksum

### VM Import Fails
- Update VirtualBox to latest version
- Ensure enough disk space
- Check VirtualBox error log
- Try manual VM creation with build-vm.sh

### Build Fails
- Install required dependencies
- Check available disk space
- Review error messages
- Ensure sudo privileges where needed

## 🤝 Contributing

See `CONTRIBUTING.md` in the main repository for contribution guidelines.

## 📄 License

See `LICENSE` in the main repository.

## 🔗 Links

- Repository: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- Issues: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues
- Releases: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/releases

---

**Built with 🔥 by the Sovereignty Architecture collective**

*"This is not randomness. This is cognitive sovereignty."*
