# SAGCO Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing and deploying the SAGCO CPU VM architecture with LLVM backend.

## Prerequisites

### System Requirements
- Linux-based OS (Ubuntu 20.04+ or Debian 11+ recommended)
- Python 3.8 or later
- Root access for system integration

### Software Dependencies

**For Native Compilation:**
```bash
# Install LLVM toolchain
sudo apt-get update
sudo apt-get install -y llvm clang build-essential

# Install Python LLVM bindings (optional, but recommended)
pip3 install llvmlite
```

**For VM Execution:**
```bash
# Python 3 is the only requirement
python3 --version  # Should be 3.8+
```

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
```

### 2. Create SAGCO Directory Structure

```bash
# Create system directories (requires root)
sudo mkdir -p /opt/sagco/{compiler,vm,artifacts,sbip}

# Copy files to system locations
sudo cp sagco/compiler/flamelang_compiler.py /opt/sagco/compiler/
sudo cp sagco/vm/sagco_cpu_vm.py /opt/sagco/vm/
sudo cp sagco/sbip/sagco-init /opt/sagco/sbip/
sudo cp sagco/sbip/sagco-cpu.service /etc/systemd/system/

# Make scripts executable
sudo chmod +x /opt/sagco/compiler/flamelang_compiler.py
sudo chmod +x /opt/sagco/vm/sagco_cpu_vm.py
sudo chmod +x /opt/sagco/sbip/sagco-init
```

### 3. Create SAGCO User (for systemd service)

```bash
# Create dedicated user for VM service
sudo useradd -r -s /usr/sbin/nologin -d /opt/sagco -c "SAGCO VM Service" sagco

# Set ownership
sudo chown -R sagco:sagco /opt/sagco/artifacts
```

### 4. Enable Systemd Service (Optional)

```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service to start at boot
sudo systemctl enable sagco-cpu.service

# Start service immediately
sudo systemctl start sagco-cpu.service

# Check status
sudo systemctl status sagco-cpu.service
```

## Usage Examples

### Example 1: Compile to Native Code

```bash
# Create a FlameLang source file (placeholder syntax)
cat > test.flame << 'EOF'
# FlameLang source (placeholder)
# In production, this would be valid FlameLang syntax
EOF

# Compile to LLVM IR and native object
cd /opt/sagco/compiler
python3 flamelang_compiler.py native test.flame

# Check outputs
ls -lh /opt/sagco/artifacts/
# Should see: example.ll (LLVM IR), example.o (object file)

# Link to executable (requires clang)
clang /opt/sagco/artifacts/example.o -o /opt/sagco/artifacts/example

# Execute
/opt/sagco/artifacts/example
# Output: (exit code 42, as per placeholder implementation)
```

### Example 2: Compile to Bytecode and Execute in VM

```bash
# Compile to bytecode
cd /opt/sagco/compiler
python3 flamelang_compiler.py vm test.flame

# Check output
ls -lh /opt/sagco/artifacts/
# Should see: example.bc

# Execute in VM (single-shot)
cd /opt/sagco/vm
python3 sagco_cpu_vm.py /opt/sagco/artifacts/example.bc

# Expected output:
# SAGCO CPU VM - Executing: /opt/sagco/artifacts/example.bc
# Result: 8
# Final stack: [8]
```

### Example 3: Run VM in Daemon Mode

```bash
# Start daemon manually (or use systemd service)
cd /opt/sagco/vm
python3 sagco_cpu_vm.py --daemon --load-dir /opt/sagco/artifacts --debug

# In another terminal, add bytecode files
cp example.bc /opt/sagco/artifacts/

# Daemon will automatically detect and execute
# Watch logs:
# - If running via systemd: sudo journalctl -u sagco-cpu.service -f
# - If running manually: output appears in terminal
```

### Example 4: View LLVM IR (Human-Readable)

```bash
# Generate IR only
cd /opt/sagco/compiler
python3 flamelang_compiler.py ir test.flame

# View IR
cat /opt/sagco/artifacts/example.ll
```

## SBIP Integration

### Integration with Initramfs

To integrate SAGCO with your boot process:

1. **Copy sagco-init to initramfs hooks:**

```bash
# For Debian/Ubuntu initramfs-tools
sudo cp /opt/sagco/sbip/sagco-init /etc/initramfs-tools/scripts/init-bottom/sagco-init
sudo chmod +x /etc/initramfs-tools/scripts/init-bottom/sagco-init

# Update initramfs
sudo update-initramfs -u
```

2. **Ensure SAGCO files are included in initramfs:**

```bash
# Create initramfs hook
sudo tee /etc/initramfs-tools/hooks/sagco > /dev/null << 'EOF'
#!/bin/sh
PREREQ=""
prereqs() { echo "$PREREQ"; }
case $1 in prereqs) prereqs; exit 0;; esac

. /usr/share/initramfs-tools/hook-functions

# Copy SAGCO VM and artifacts
mkdir -p "$DESTDIR/opt/sagco/"{vm,artifacts}
copy_exec /opt/sagco/vm/sagco_cpu_vm.py /opt/sagco/vm/
copy_exec /usr/bin/python3 /usr/bin/

# Copy any bootstrap bytecode
if [ -f /opt/sagco/artifacts/bootstrap.bc ]; then
    cp /opt/sagco/artifacts/bootstrap.bc "$DESTDIR/opt/sagco/artifacts/"
fi
EOF

sudo chmod +x /etc/initramfs-tools/hooks/sagco
sudo update-initramfs -u
```

3. **Reboot to test:**

```bash
sudo reboot
# Watch boot messages for SAGCO banner and initialization
```

### Custom Kernel Banner (Optional)

To add a SAGCO banner to kernel boot:

1. **Patch kernel (advanced):**

```bash
# This requires kernel source and recompilation
# See docs/KERNEL_CUSTOMIZATION.md for full instructions

# Brief overview:
# 1. Get kernel source: apt source linux-image-$(uname -r)
# 2. Edit init/main.c, add to start_kernel() or do_initcalls():
#    printk(KERN_INFO "SAGCO OS - Ratio Ex Nihilo - Bootstrapping Toolchain\n");
# 3. Compile: make -j$(nproc) deb-pkg
# 4. Install: dpkg -i ../linux-image-*.deb
# 5. Update GRUB: update-grub
# 6. Reboot
```

## Troubleshooting

### Issue: llvmlite not installed

**Symptom:** Warning message about llvmlite missing

**Solution:**
```bash
pip3 install llvmlite
# or
sudo apt-get install python3-llvmlite
```

### Issue: Systemd service fails to start

**Symptom:** `systemctl status sagco-cpu.service` shows failed

**Solution:**
```bash
# Check logs
sudo journalctl -u sagco-cpu.service -n 50

# Common issues:
# 1. User doesn't exist:
sudo useradd -r -s /usr/sbin/nologin sagco

# 2. Permissions:
sudo chown -R sagco:sagco /opt/sagco/artifacts

# 3. Python not found:
# Edit service file to use correct Python path
sudo nano /etc/systemd/system/sagco-cpu.service
# Change: ExecStart=/usr/bin/python3 ...
# To: ExecStart=/usr/bin/env python3 ...
sudo systemctl daemon-reload
```

### Issue: Bytecode not executing

**Symptom:** VM daemon running but not processing .bc files

**Solution:**
```bash
# Check file permissions
ls -la /opt/sagco/artifacts/

# Files should be readable by sagco user
sudo chmod 644 /opt/sagco/artifacts/*.bc

# Check daemon is running
sudo systemctl status sagco-cpu.service

# Watch logs in real-time
sudo journalctl -u sagco-cpu.service -f

# Test manually
sudo -u sagco /opt/sagco/vm/sagco_cpu_vm.py /opt/sagco/artifacts/example.bc
```

### Issue: Native compilation fails

**Symptom:** clang errors when compiling

**Solution:**
```bash
# Ensure LLVM installed
llvm-config --version
clang --version

# If not installed:
sudo apt-get install llvm clang

# Try manual compilation
cd /opt/sagco/artifacts
clang -v example.o -o example
```

## Testing

### Unit Tests

```bash
# Test compiler (bytecode mode)
cd /opt/sagco/compiler
python3 flamelang_compiler.py vm
ls /opt/sagco/artifacts/example.bc || echo "FAILED"

# Test VM execution
cd /opt/sagco/vm
python3 sagco_cpu_vm.py /opt/sagco/artifacts/example.bc
# Should output: Result: 8

# Test compiler (native mode) - requires llvmlite
python3 flamelang_compiler.py native
ls /opt/sagco/artifacts/example.ll || echo "FAILED"
```

### Integration Tests

```bash
# Test systemd service
sudo systemctl restart sagco-cpu.service
sudo systemctl status sagco-cpu.service | grep "active (running)"

# Test daemon processing
echo "01 05 01 03 10 FF" | xxd -r -p > /tmp/test.bc
sudo cp /tmp/test.bc /opt/sagco/artifacts/
sleep 2
sudo journalctl -u sagco-cpu.service -n 20 | grep "Result: 8"
```

## Performance Tuning

### Native Mode Optimization

```bash
# Use LLVM optimization flags (future enhancement)
# Edit flamelang_compiler.py to add optimization passes:
# - O1, O2, O3 levels
# - Link-time optimization (LTO)
# - Architecture-specific tuning (-march=native)
```

### VM Mode Optimization

```bash
# For production, consider:
# 1. JIT compilation of hot paths (future)
# 2. Bytecode precompilation and caching
# 3. Resource limit tuning in systemd service
sudo systemctl edit sagco-cpu.service
# Add:
# [Service]
# MemoryLimit=1G
# CPUQuota=50%
```

## Security Considerations

### Artifact Verification

Always verify bytecode and binaries before execution:

```bash
# Generate hash
sha256sum /opt/sagco/artifacts/example.bc > /opt/sagco/artifacts/example.bc.sha256

# Verify hash
sha256sum -c /opt/sagco/artifacts/example.bc.sha256
```

### Systemd Hardening

The sagco-cpu.service is pre-configured with security features:
- `NoNewPrivileges=true` - Prevents privilege escalation
- `ProtectSystem=strict` - Read-only system directories
- `ProtectHome=true` - No home directory access
- `RestrictNamespaces=true` - Limited namespace usage
- Memory and CPU limits

Review and adjust as needed:
```bash
sudo systemctl edit sagco-cpu.service
```

## Further Reading

- **CPU Layer Capstone**: `sagco/docs/CPU_LAYER_CAPSTONE.md`
- **SBIP Specification**: `sagco/docs/CPU_LAYER_SBIP_SPEC.md`
- **Attorney Memo**: `sagco/docs/CPU_LAYER_ATTORNEY_MEMO.md`
- **FlameLang Specification**: `FLAMELANG_SPECIFICATION.md`

## Support

For issues or questions:
- Open an issue on GitHub: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- Check existing documentation in `sagco/docs/`
- Review systemd logs: `sudo journalctl -u sagco-cpu.service`

---

*SAGCO Implementation Guide v1.0 - Part of the Sovereignty Architecture*
