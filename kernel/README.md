# SAGCO CPU Primitives Kernel Module

**INV-101: SAGCO CPU Primitives Module**

Ring 0 kernel module providing CPU primitives for the SAGCO Boot Identity Pipeline (SBIP).

## Overview

The `sagco_cpu_mod.ko` kernel module creates a character device `/dev/sagco_cpu` that exposes Ring 0 primitives for FlameLang execution state and SAGCO identity at the kernel level.

## Features

- **Character Device**: `/dev/sagco_cpu` for userspace interaction
- **CPU State Registers**:
  - `flame_pc` - FlameLang program counter
  - `flame_sp` - FlameLang stack pointer
  - `flame_flags` - FlameLang status flags
  - `ratio_counter` - Ratio Ex Nihilo execution counter
- **ioctl Interface**: Get/set CPU state via system calls
- **Identity Display**: Shows SAGCO entity information in kernel logs

## Building

```bash
# Build the module
make

# Clean build artifacts
make clean
```

### Requirements

- Linux kernel headers for your running kernel
- GCC and make
- Root privileges for installation

```bash
# Install dependencies on Debian/Ubuntu
sudo apt install build-essential linux-headers-$(uname -r)
```

## Installation

```bash
# Build and install
make
sudo make install

# Load the module
sudo modprobe sagco_cpu_mod

# Verify it loaded
lsmod | grep sagco_cpu_mod
dmesg | grep SAGCO_CPU
```

## Usage

### Reading CPU State

```bash
# Read current state
sudo cat /dev/sagco_cpu
```

Output:
```
SAGCO CPU State:
  Flame PC: 0x0000000000000000
  Flame SP: 0x0000000000000000
  Flame Flags: 0x0000000000000000
  Ratio Counter: 0
```

### Writing Commands

```bash
# Reset CPU state
echo "reset" | sudo tee /dev/sagco_cpu

# Increment ratio counter
echo "tick" | sudo tee /dev/sagco_cpu
```

### ioctl Interface

The module supports two ioctl commands:

- `0x5A00` - `SAGCO_CPU_GET_STATE` - Get current CPU state
- `0x5A01` - `SAGCO_CPU_SET_STATE` - Set CPU state

Example C code:

```c
#include <fcntl.h>
#include <sys/ioctl.h>

struct sagco_cpu_state {
    unsigned long flame_pc;
    unsigned long flame_sp;
    unsigned long flame_flags;
    unsigned long ratio_counter;
};

int fd = open("/dev/sagco_cpu", O_RDWR);
struct sagco_cpu_state state;

// Get state
ioctl(fd, 0x5A00, &state);

// Set state
state.ratio_counter = 42;
ioctl(fd, 0x5A01, &state);

close(fd);
```

## Testing

```bash
# Run tests
sudo make test
```

This will:
1. Read the device state
2. Send a 'tick' command
3. Read the updated state
4. Verify the counter incremented

## Kernel Messages

The module logs to the kernel ring buffer:

```bash
# View SAGCO kernel messages
dmesg | grep SAGCO_CPU
```

Example output:
```
SAGCO_CPU: Initializing...
SAGCO_CPU: Ratio Ex Nihilo
SAGCO_CPU: Strategickhaos DAO LLC
SAGCO_CPU: EIN 39-2923503 | WY 2025-001708194
SAGCO_CPU: Registered with major number 243
SAGCO_CPU: Device class created
SAGCO_CPU: Device /dev/sagco_cpu created successfully
SAGCO_CPU: Loaded - Ratio Ex Nihilo
SAGCO_CPU: From nothing, through reason, everything.
```

## Uninstallation

```bash
# Unload the module
sudo modprobe -r sagco_cpu_mod

# Remove from system
sudo make uninstall
```

## Troubleshooting

### Module won't load

```bash
# Check kernel ring buffer for errors
dmesg | tail -20

# Verify kernel headers are installed
ls /lib/modules/$(uname -r)/build

# Check for conflicting modules
lsmod | grep sagco
```

### Device file not created

```bash
# Check if udev is running
systemctl status systemd-udevd

# Manually create device node (temporary)
sudo mknod /dev/sagco_cpu c $(cat /sys/class/sagco/sagco_cpu/dev | tr ':' ' ')
```

### Permission denied

The device is created with root-only permissions. Use sudo:

```bash
sudo cat /dev/sagco_cpu
```

Or change permissions (not recommended for production):

```bash
sudo chmod 666 /dev/sagco_cpu
```

## Architecture

The module follows standard Linux kernel module patterns:

1. **Initialization** (`sagco_cpu_init`):
   - Register character device
   - Create device class
   - Create device node in `/dev`

2. **File Operations**:
   - `open` - Track process opening device
   - `release` - Track process closing device
   - `read` - Return CPU state as text
   - `write` - Accept commands (reset, tick)
   - `unlocked_ioctl` - Binary state get/set

3. **Cleanup** (`sagco_cpu_exit`):
   - Destroy device node
   - Destroy device class
   - Unregister character device

## Security Considerations

- Device requires root privileges by default
- ioctl interface performs basic validation
- No direct hardware access (simulation only in v1.0)
- Future versions may integrate with hardware security modules

## Future Enhancements (v1.1+)

- Hardware integration for actual CPU state
- TPM integration for secure state storage
- Multi-CPU core support
- DMA support for high-performance operations
- Interrupt handling for async events
- procfs interface for easier state inspection

## Legal Notice

Property of Strategickhaos DAO LLC  
Wyoming Entity: 2025-001708194 | EIN: 39-2923503  
Invention: INV-101 (SAGCO CPU Primitives Module)

## License

Proprietary - All rights reserved

---

*"SAGCO_CPU: Loaded - Ratio Ex Nihilo"*

🔥💜 STRATEGICKHAOS DAO LLC 💜🔥
