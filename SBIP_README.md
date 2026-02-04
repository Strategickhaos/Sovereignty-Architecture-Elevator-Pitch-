# SBIP v1.0 Implementation

This repository contains the implementation of **Sovereign Boot Integrity Protocol (SBIP) v1.0**, providing LLVM-native compilation, boot-time verification, and sovereign system services.

## 🔥 Key Components

### 1. FlameLang Compiler (`src/flamelang_compiler.py`)

LLVM-native compiler with **critical linking fix**:

**❌ WRONG (breaks portability):**
```python
subprocess.run(["ld", "flamelang.o", "-o", "flamelang_exec"])
```

**✅ CORRECT (SBIP v1.0 compliant):**
```python
subprocess.run(["clang", "flamelang.o", "-o", "flamelang_exec"])
```

**Why this matters:**
- Direct `ld` fails because it skips CRT startup objects (crt1.o, crti.o, crtn.o)
- Missing libc linkage causes undefined references
- Incorrect dynamic loader path breaks cross-platform compatibility
- Using `clang` as linker driver solves all these issues

### 2. SBIP Specification (`docs/SBIP_SPEC_v1.0.md`)

Complete specification covering:
- Boot-time integrity verification
- Identity display system (Plymouth)
- Deterministic toolchain bootstrap
- Service architecture
- Installation and maintenance procedures

### 3. Systemd Services (`services/`)

- **sagco-runtime.service** — Sovereign runtime environment
- **sagco-compiler.service** — Deterministic compiler bootstrap service

### 4. Initramfs Components (`initramfs/`)

- **sagco-verify** — Boot verification script (runs in init-premount)
- **sagco-manifest** — Hook to copy manifest into initramfs

## 📦 Installation

### Prerequisites

```bash
# Install required packages
sudo apt install -y plymouth plymouth-themes clang llvm lld initramfs-tools
```

### Deploy SBIP Components

```bash
# Copy service files
sudo cp services/*.service /etc/systemd/system/

# Copy initramfs scripts
sudo cp initramfs/sagco-verify /etc/initramfs-tools/scripts/init-premount/
sudo cp initramfs/sagco-manifest /etc/initramfs-tools/hooks/
sudo chmod +x /etc/initramfs-tools/scripts/init-premount/sagco-verify
sudo chmod +x /etc/initramfs-tools/hooks/sagco-manifest

# Create SAGCO directory
sudo mkdir -p /etc/sagco

# Generate system manifest (example)
sudo sh -c "sha256sum /usr/bin/clang /usr/bin/llvm-link > /etc/sagco/manifest.sha256"

# Update initramfs and bootloader
sudo update-initramfs -u
sudo update-grub
```

### Enable Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable sagco-runtime.service sagco-compiler.service
```

## 🧪 Testing the Compiler

```bash
# Compile the test program
python3 src/flamelang_compiler.py src/flamelang_test.c flamelang_test

# Run the compiled program
./flamelang_test
```

Expected output:
```
🔥 FlameLang SBIP v1.0 Test
✅ LLVM-native compilation successful
🔗 Linked with clang (not direct ld)
```

## 📊 Verification

### Check Service Status

```bash
systemctl status sagco-runtime.service
systemctl status sagco-compiler.service
```

### View Boot Logs

```bash
# Boot logs via dmesg and initramfs script output
dmesg | grep -i sbip

# System services via journalctl
journalctl -u sagco-runtime -u sagco-compiler --since boot
```

### Verify Initramfs Inclusion

```bash
# Check if manifest was included in initramfs
lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco
```

## 🔒 Security Features

### Boot-Time Verification
- Cryptographic manifest verification before root mount
- SHA256 checksums of critical system binaries
- Plymouth visual feedback during verification

### LLVM-Native Toolchain
- Deterministic compilation across all components
- Avoids toolchain compromise attacks
- Ensures reproducible builds

### Service Hardening
- systemd security features enabled
- Read-only system protection
- Private temporary directories
- Resource limits enforced

## 📖 Documentation

See [`docs/SBIP_SPEC_v1.0.md`](docs/SBIP_SPEC_v1.0.md) for complete specification including:
- Architecture overview
- Detailed component descriptions
- Installation procedures
- Security considerations
- Maintenance guidelines

## 🎯 Prior Art Gap

SBIP v1.0 provides a unique combination:
- **Identity display** + **verification** + **deterministic toolchain bootstrap**

This integration pattern is not found in existing solutions like Secure Boot, measured boot, or reproducible builds alone.

## 🔧 Key Engineering Fixes

### Fix #1: Clang Linker Driver

**Problem:** Direct `ld` invocation fails due to missing CRT objects and libc linkage.

**Solution:** Use `clang` as linker driver for portable, LLVM-native linking.

### Fix #2: Initramfs Manifest Hook

**Problem:** `/etc/sagco/manifest.sha256` not available during boot verification.

**Solution:** Hook script (`sagco-manifest`) copies manifest into initramfs at build time.

### Fix #3: Logging Specification

**Problem:** Initramfs messages don't reliably appear as named systemd unit.

**Solution:** Updated spec to reference "Boot logs via dmesg and initramfs script output; system services via journalctl -u sagco-runtime -u sagco-compiler."

## 📝 License

Proprietary - Strategickhaos DAO LLC  
All rights reserved.

## 🔥 Covenant

*Trust nothing until it survives 100-angle crossfire.*

---

**SBIP v1.0** — Strategickhaos DAO LLC  
**Status:** Production Ready  
**Version:** 1.0  
**Date:** 2026-02-04
