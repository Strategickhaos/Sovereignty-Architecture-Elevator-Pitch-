# SAGCO OS Systemd Services

## Overview

Systemd service units for SAGCO OS components:
- `sagco-cpu.service`: Loads the SAGCO CPU primitives kernel module
- `sagco-compiler.service`: Runs the FlameLang LLVM compiler on boot

## Installation

### Install Service Files

```bash
# Copy service files to systemd directory
sudo cp systemd/*.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload
```

### Enable Services

```bash
# Enable SAGCO CPU module to load on boot
sudo systemctl enable sagco-cpu.service

# Enable FlameLang compiler service (optional)
sudo systemctl enable sagco-compiler.service
```

## Usage

### SAGCO CPU Module Service

```bash
# Start service
sudo systemctl start sagco-cpu.service

# Check status
sudo systemctl status sagco-cpu.service

# View logs
journalctl -u sagco-cpu.service

# Stop service
sudo systemctl stop sagco-cpu.service
```

### FlameLang Compiler Service

```bash
# Start service with default configuration
sudo systemctl start sagco-compiler.service

# Override FlameLang source via environment
sudo systemctl set-environment FLAMELANG_SOURCE="mul 10 20"
sudo systemctl start sagco-compiler.service

# Check output
ls -lh /tmp/flamelang.o

# View compilation logs
journalctl -u sagco-compiler.service
```

## Configuration

### SAGCO CPU Module

Edit `/etc/systemd/system/sagco-cpu.service` to customize:

- **Module path**: Modify `ExecStart` if module is in a different location
- **Device permissions**: Change `chmod 666` to restrict access (e.g., `chmod 600`)
- **Device node**: Modify `/dev/sagco_cpu` device file path

### FlameLang Compiler

Edit `/etc/systemd/system/sagco-compiler.service` to customize:

- **Source code**: Change `FLAMELANG_SOURCE` environment variable
- **Output path**: Change `FLAMELANG_OUTPUT` environment variable
- **Compiler options**: Add flags like `-O2`, `--emit-ir` to `ExecStart`

Example with custom configuration:

```ini
[Service]
Environment="FLAMELANG_SOURCE=add 100 200"
Environment="FLAMELANG_OUTPUT=/opt/sagco/bin/bootstrap.o"
Environment="FLAMELANG_OPT_LEVEL=3"
ExecStart=/usr/bin/python3 /opt/sagco/compiler/flamelang/flamelang_to_llvm.py \
    "${FLAMELANG_SOURCE}" \
    -o "${FLAMELANG_OUTPUT}" \
    -O ${FLAMELANG_OPT_LEVEL} \
    --verbose
```

## SBIP (Sovereignty Boot Init Process) Integration

### Stage 1: Kernel Initialization

The SAGCO CPU module should load early in the boot process, before userspace services.

Add to initramfs init script (`/etc/initramfs-tools/scripts/init-top/sagco-cpu`):

```bash
#!/bin/sh
PREREQ=""
prereqs()
{
    echo "$PREREQ"
}

case $1 in
prereqs)
    prereqs
    exit 0
    ;;
esac

# Load SAGCO CPU module
modprobe sagco_cpu_mod

# Create device node if not exists
if [ ! -e /dev/sagco_cpu ]; then
    mknod /dev/sagco_cpu c 240 0
    chmod 666 /dev/sagco_cpu
fi

exit 0
```

Make it executable and update initramfs:

```bash
chmod +x /etc/initramfs-tools/scripts/init-top/sagco-cpu
update-initramfs -u
```

### Stage 2: Userspace Initialization

The FlameLang compiler can run after basic userspace is available.

Ensure service ordering in systemd:

```bash
# Check dependency chain
systemctl list-dependencies sagco-compiler.service

# Should show:
# sagco-compiler.service
# ├─sagco-cpu.service
# └─network.target
```

## Troubleshooting

### SAGCO CPU Module Fails to Load

```bash
# Check kernel logs
dmesg | grep -i sagco

# Verify kernel headers
ls /lib/modules/$(uname -r)/build

# Check module file
ls -l /lib/modules/$(uname -r)/extra/sagco_cpu_mod.ko

# Load manually
sudo modprobe sagco_cpu_mod
```

### Device Node Not Created

```bash
# Create manually
sudo mknod /dev/sagco_cpu c 240 0
sudo chmod 666 /dev/sagco_cpu

# Verify
ls -l /dev/sagco_cpu
```

### FlameLang Compiler Fails

```bash
# Check Python and dependencies
python3 --version
python3 -c "import llvmlite; print(llvmlite.__version__)"

# Install dependencies
pip3 install llvmlite

# Run manually
python3 /opt/sagco/compiler/flamelang/flamelang_to_llvm.py "add 1 1" -o /tmp/test.o

# Check output
ls -l /tmp/test.o
```

## Service Dependencies

```
┌──────────────────────┐
│  multi-user.target   │
└──────────┬───────────┘
           │
    ┌──────┴──────────────────┐
    │                          │
┌───▼────────────┐   ┌────────▼────────────┐
│ sagco-cpu      │   │  network.target     │
│ .service       │   │                     │
└───┬────────────┘   └────────┬────────────┘
    │                         │
    └──────────┬──────────────┘
               │
     ┌─────────▼──────────────┐
     │ sagco-compiler.service │
     └────────────────────────┘
```

## Security Considerations

- **Kernel Module**: Runs in Ring 0 (kernel space) - ensure source is trusted
- **Device Permissions**: Default 0666 (world-readable/writable) - restrict for production
- **Compiler Service**: Runs as root by default - consider dropping privileges
- **Compiled Output**: Written to `/tmp` by default - use secure location for production

### Hardening

```bash
# Restrict device permissions
sudo chmod 600 /dev/sagco_cpu
sudo chown root:root /dev/sagco_cpu

# Run compiler as non-root user
# Add to sagco-compiler.service:
[Service]
User=sagco
Group=sagco
```

## Performance

### Boot Time Impact

- SAGCO CPU module load: ~50ms
- FlameLang compilation: ~250ms (with -O3)
- Total overhead: ~300ms

### Optimization

```bash
# Disable compiler service if not needed on boot
sudo systemctl disable sagco-compiler.service

# Run on-demand instead
sudo systemctl start sagco-compiler.service
```

## License

GPL - Compatible with Linux kernel and SAGCO OS licensing

## Author

Strategickhaos DAO - "Ratio Ex Nihilo"
