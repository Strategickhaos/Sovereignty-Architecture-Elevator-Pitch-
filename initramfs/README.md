# SAGCO Initramfs Integration

## Overview

Scripts for integrating SAGCO components into the Linux initramfs and early boot process (SBIP - Sovereignty Boot Init Process).

## Files

- `sagco-cpu`: Initramfs hook for loading SAGCO CPU kernel module
- `sagco-init`: Complete SAGCO initialization script for SBIP

## Installation

### Method 1: Initramfs Hook (Recommended)

This method loads the SAGCO CPU module during early kernel initialization.

```bash
# Copy hook to initramfs scripts directory
sudo cp initramfs/sagco-cpu /etc/initramfs-tools/scripts/init-top/sagco-cpu
sudo chmod +x /etc/initramfs-tools/scripts/init-top/sagco-cpu

# Copy kernel module to initramfs
sudo mkdir -p /lib/modules/$(uname -r)/extra
sudo cp kernel/sagco_cpu_mod/sagco_cpu_mod.ko /lib/modules/$(uname -r)/extra/
sudo depmod -a

# Add module to initramfs modules list
echo "sagco_cpu_mod" | sudo tee -a /etc/initramfs-tools/modules

# Rebuild initramfs
sudo update-initramfs -u

# Verify
sudo lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco
```

### Method 2: SBIP Integration Script

This method provides a complete SAGCO initialization script for custom boot processes.

```bash
# Install to /opt/sagco
sudo mkdir -p /opt/sagco
sudo cp -r kernel /opt/sagco/
sudo cp -r compiler /opt/sagco/
sudo cp initramfs/sagco-init /opt/sagco/
sudo chmod +x /opt/sagco/sagco-init

# Run during boot (add to rc.local or systemd)
sudo /opt/sagco/sagco-init
```

## Usage

### Initramfs Hook

The hook runs automatically during boot after kernel initialization:

1. Loads `sagco_cpu_mod` kernel module
2. Creates `/dev/sagco_cpu` device node
3. Sets device permissions

Check boot logs:

```bash
dmesg | grep -i sagco
# Expected output:
# SAGCO_CPU: Loaded - Ratio Ex Nihilo
```

### SBIP Script

Run the SBIP script manually or via systemd:

```bash
# Manual execution
sudo /opt/sagco/sagco-init

# With FlameLang compilation enabled
sudo SAGCO_COMPILE_INITRAMFS=1 /opt/sagco/sagco-init

# Custom SAGCO home directory
sudo SAGCO_HOME=/custom/path /opt/sagco/sagco-init
```

## Configuration

### Environment Variables

- `SAGCO_HOME`: SAGCO installation directory (default: `/opt/sagco`)
- `SAGCO_COMPILE_INITRAMFS`: Enable FlameLang compilation during boot (default: `0`)
- `FLAMELANG_BOOTSTRAP`: Path to FlameLang bootstrap source (default: `${SAGCO_HOME}/bootstrap.flame`)

### FlameLang Bootstrap

Create a bootstrap FlameLang program:

```bash
# Create bootstrap source
cat > /opt/sagco/bootstrap.flame << 'EOF'
add 1 1
mul 2 3
sub 10 5
EOF

# Enable bootstrap compilation
export SAGCO_COMPILE_INITRAMFS=1
```

## SBIP Stages

The SAGCO initialization process follows these stages:

### Stage 1: Kernel Module Loading

- Loads `sagco_cpu_mod.ko` kernel module
- Creates `/dev/sagco_cpu` character device
- Sets device permissions (0666)
- Verifies module registration

### Stage 2: FlameLang Bootstrap (Optional)

- Compiles FlameLang bootstrap source
- Optimizes with LLVM passes (-O3)
- Links to executable binary
- Verifies compiled bootstrap

### Stage 3: Environment Verification

- Checks device accessibility
- Verifies module status
- Reports initialization status

## Integration with Systemd

Combine with systemd services for complete integration:

```bash
# Install systemd services
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable sagco-cpu.service
sudo systemctl enable sagco-compiler.service

# Boot sequence:
# 1. Kernel loads
# 2. Initramfs runs sagco-cpu hook
# 3. Userspace starts
# 4. sagco-cpu.service ensures module loaded
# 5. sagco-compiler.service runs FlameLang compiler
```

## Troubleshooting

### Module not found in initramfs

```bash
# Verify module is included
lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco_cpu_mod

# If not found, rebuild:
sudo update-initramfs -u
```

### Hook not executing

```bash
# Check hook permissions
ls -l /etc/initramfs-tools/scripts/init-top/sagco-cpu

# Should be executable (755)
sudo chmod +x /etc/initramfs-tools/scripts/init-top/sagco-cpu

# Rebuild initramfs
sudo update-initramfs -u
```

### Device node not created

```bash
# Check kernel logs
dmesg | grep sagco

# Manually load module
sudo modprobe sagco_cpu_mod

# Check device
ls -l /dev/sagco_cpu
```

### FlameLang compilation fails

```bash
# Check Python availability
which python3

# Check llvmlite installation
python3 -c "import llvmlite; print('OK')"

# Install dependencies
pip3 install llvmlite

# Test compiler
python3 /opt/sagco/compiler/flamelang/flamelang_to_llvm.py "add 1 1" -o /tmp/test.o
```

## Boot Time Analysis

Measure SAGCO boot overhead:

```bash
# Check systemd boot time
systemd-analyze blame | grep sagco

# Expected:
# ~50ms sagco-cpu.service
# ~250ms sagco-compiler.service (if enabled)
```

## Security Considerations

- **Initramfs Hook**: Runs as root during early boot
- **Device Permissions**: Default 0666 (world-accessible) - adjust for production
- **Module Signature**: Consider signing kernel module for Secure Boot
- **Bootstrap Source**: Validate FlameLang bootstrap source integrity

## Testing

Test the initramfs integration without rebooting:

```bash
# Test sagco-init script
sudo bash -x /opt/sagco/sagco-init

# Test module loading
sudo modprobe sagco_cpu_mod
lsmod | grep sagco_cpu_mod

# Test device creation
ls -l /dev/sagco_cpu

# Test FlameLang compilation
export SAGCO_COMPILE_INITRAMFS=1
cat > /tmp/test.flame << 'EOF'
add 5 10
EOF
export FLAMELANG_BOOTSTRAP=/tmp/test.flame
sudo /opt/sagco/sagco-init
```

## License

GPL - Compatible with Linux kernel licensing

## Author

Strategickhaos DAO - "Ratio Ex Nihilo"
