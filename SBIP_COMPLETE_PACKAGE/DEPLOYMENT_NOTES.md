# SBIP Deployment Notes

## Security Enhancements

The SBIP v1.0 implementation includes the following security features:

### Kernel Module Security
- **CAP_SYS_ADMIN Required**: Only privileged users can execute bytecode
- **Device Permissions**: Device node restricted to 0600 (owner only)
- **Buffer Overflow Protection**: All stack operations include bounds checking
- **Input Validation**: Bytecode size validated before processing
- **Stack Overflow/Underflow Detection**: Both conditions properly handled

### Bytecode Interpreter
- Maximum bytecode size: 1024 bytes
- Maximum stack size: 16 elements
- Supported operations:
  - 0x00: HALT (terminates execution)
  - 0x01: PUSH (pushes next byte onto stack)
  - 0x10: ADD (pops two values, pushes sum)

### Compiler Backend
- Uses LLVM with aggressive optimization passes
- Proper linking with gcc (includes C runtime)
- Target: x86_64 native code

## Installation Prerequisites

```bash
# Kernel headers (for module build)
sudo apt install linux-headers-$(uname -r)

# Python dependencies
pip install llvmlite

# Build tools
sudo apt install build-essential gcc
```

## Quick Start

```bash
# 1. Build and load kernel module
cd kernel/
make
sudo make install

# 2. Verify module loaded
lsmod | grep sagco_cpu_mod
ls -l /dev/sagco_cpu

# 3. Install systemd services
cd ../systemd/
sudo cp *.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sagco-banner.service

# 4. Configure GRUB (optional)
cd ../boot/grub-theme/
sudo mkdir -p /boot/grub/themes/sagco/
sudo cp * /boot/grub/themes/sagco/
# Edit /etc/default/grub and run: sudo update-grub
```

## Verification

```bash
# Check all components
systemctl status sagco-*.service
dmesg | tail -20 | grep SAGCO
journalctl -u sagco-banner.service -n 20
```

## Troubleshooting

### Module won't load
- Check kernel version compatibility
- Verify kernel headers installed: `dpkg -l | grep linux-headers`
- Check dmesg for errors: `dmesg | grep sagco`

### Services fail to start
- Check executable paths in service files
- Verify binaries exist in /opt/sagco/bin/
- Check permissions: `ls -l /opt/sagco/bin/`

### Device node missing
- Verify module loaded: `lsmod | grep sagco`
- Check /dev/sagco_cpu creation
- If missing, module init failed (check dmesg)

## Architecture Notes

This implementation follows Option 1 (LLVM Native):
- FlameLang → LLVM IR → x86_64 native binary
- Direct hardware execution (no VM layer in v1.0)
- Future v1.1+ may add optional VM interpreter

## Legal & Compliance

- **Classification**: NOVEL system architecture (INV-100)
- **License**: GPL for kernel module
- **Author**: Strategickhaos DAO
- **Status**: Proof of concept / Research implementation
