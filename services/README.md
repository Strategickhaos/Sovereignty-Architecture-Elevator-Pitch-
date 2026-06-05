# SAGCO Services

This directory contains systemd service files for the SAGCO Boot Identity Pipeline (SBIP).

## Services

### sagco-runtime.service
Bootstrap service that initializes the SAGCO runtime environment, loads tools, and sets up the execution environment.

### sagco-compiler.service
FlameLang compiler daemon that watches for source files and compiles them to native x86_64 binaries via LLVM.

## Installation

To install these services on a Linux system with systemd:

```bash
# Copy service files to systemd directory
sudo cp services/*.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable services to start at boot
sudo systemctl enable sagco-runtime.service
sudo systemctl enable sagco-compiler.service

# Start services immediately (optional)
sudo systemctl start sagco-runtime.service
sudo systemctl start sagco-compiler.service

# Check service status
sudo systemctl status sagco-runtime.service
sudo systemctl status sagco-compiler.service
```

## Prerequisites

These services expect the following binaries to exist:
- `/opt/sagco/bin/sagco-runtime` - Runtime bootstrap script
- `/opt/sagco/bin/flamelang-compiler` - Compiler daemon executable

Ensure these are installed before starting the services.

## See Also

- [SBIP Specification](../docs/SBIP_SPEC_v1.0.md) - Complete SBIP v1.0 documentation
- [Initramfs Script](../initramfs/sagco-verify) - Boot-time verification script
- [FlameLang Compiler](../src/compiler/flamelang_to_llvm.py) - LLVM-based compiler implementation
