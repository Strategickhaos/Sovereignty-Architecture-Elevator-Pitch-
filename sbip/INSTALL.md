# SBIP Installation Guide

Complete installation guide for SAGCO Boot Identity Pipeline (SBIP) v1.0.

## Prerequisites

- Linux system (tested on Kali Linux / Debian-based)
- Root access (sudo)
- Plymouth boot splash system
- systemd init system
- GRUB bootloader

Install required packages:
```bash
sudo apt update
sudo apt install plymouth plymouth-themes initramfs-tools grub2-common
```

## Installation Steps

### Step 1: Prepare Emblem Image

First, you need the SAGCO emblem image (`ratio_ex_nihilo.png`). See `EMBLEM_README.md` for details.

For testing, create a simple placeholder:
```bash
# Using ImageMagick (install with: sudo apt install imagemagick)
convert -size 512x512 xc:purple \
  -font Arial -pointsize 48 -fill white -gravity center \
  -annotate +0+0 "SAGCO\nRatio Ex Nihilo" \
  /tmp/ratio_ex_nihilo.png
```

Or use any existing image as placeholder:
```bash
cp /path/to/your/logo.png /tmp/ratio_ex_nihilo.png
```

### Step 2: Install GRUB Theme

```bash
# Create theme directory
sudo mkdir -p /boot/grub/themes/sagco

# Copy theme files
sudo cp sbip/boot/grub/themes/sagco/theme.txt /boot/grub/themes/sagco/

# Copy emblem
sudo cp /tmp/ratio_ex_nihilo.png /boot/grub/themes/sagco/

# Backup original GRUB config
sudo cp /etc/default/grub /etc/default/grub.backup

# Add SAGCO configuration to GRUB
# Edit /etc/default/grub and add or modify these lines:
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash sagco=1"
# GRUB_THEME="/boot/grub/themes/sagco/theme.txt"

# You can do this manually or use sed:
sudo sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash sagco=1"/' /etc/default/grub
echo 'GRUB_THEME="/boot/grub/themes/sagco/theme.txt"' | sudo tee -a /etc/default/grub

# Update GRUB
sudo update-grub
```

### Step 3: Install Plymouth Theme

```bash
# Create theme directory
sudo mkdir -p /usr/share/plymouth/themes/sagco

# Copy theme files
sudo cp sbip/usr/share/plymouth/themes/sagco/sagco.plymouth /usr/share/plymouth/themes/sagco/
sudo cp sbip/usr/share/plymouth/themes/sagco/sagco.script /usr/share/plymouth/themes/sagco/

# Copy emblem
sudo cp /tmp/ratio_ex_nihilo.png /usr/share/plymouth/themes/sagco/

# Set as default theme
sudo plymouth-set-default-theme sagco

# Update initramfs to include the theme
sudo update-initramfs -u
```

Verify Plymouth theme installation:
```bash
plymouth-set-default-theme --list | grep sagco
```

### Step 4: Install initramfs Hook

```bash
# Copy the hook script
sudo cp sbip/etc/initramfs-tools/scripts/init-top/sagco-init /etc/initramfs-tools/scripts/init-top/

# Make it executable
sudo chmod +x /etc/initramfs-tools/scripts/init-top/sagco-init

# (Optional) Create artifact verification files for testing
sudo mkdir -p /etc/sagco
echo "SAGCO Core Artifact v1.0" | sudo tee /etc/sagco/core_artifact
sha256sum /etc/sagco/core_artifact | sudo tee /etc/sagco/core_artifact.sha256

# Update initramfs to include the hook
sudo update-initramfs -u
```

Verify the hook is in initramfs:
```bash
lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco-init
```

### Step 5: Install Runtime Components

```bash
# Create SAGCO directories
sudo mkdir -p /opt/sagco/{artifacts,assets,src}

# Copy runtime components
sudo cp sbip/opt/sagco/runtime.sh /opt/sagco/
sudo cp sbip/opt/sagco/flamelang-compiler /opt/sagco/
sudo cp sbip/opt/sagco/sagco-cpu-vm /opt/sagco/

# Make them executable
sudo chmod +x /opt/sagco/runtime.sh
sudo chmod +x /opt/sagco/flamelang-compiler
sudo chmod +x /opt/sagco/sagco-cpu-vm

# Set ownership (optional, adjust as needed)
sudo chown -R root:root /opt/sagco
```

### Step 6: Install systemd Services

```bash
# Copy service files
sudo cp sbip/etc/systemd/system/sagco-banner.service /etc/systemd/system/
sudo cp sbip/etc/systemd/system/sagco-runtime.service /etc/systemd/system/
sudo cp sbip/etc/systemd/system/sagco-compiler.service /etc/systemd/system/
sudo cp sbip/etc/systemd/system/sagco-cpu.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable services to start at boot
sudo systemctl enable sagco-banner.service
sudo systemctl enable sagco-runtime.service
sudo systemctl enable sagco-compiler.service
sudo systemctl enable sagco-cpu.service
```

## Testing Before Reboot

### Test Plymouth Theme

Test the Plymouth splash without rebooting:
```bash
# Start Plymouth daemon
sudo plymouthd

# Show splash screen
sudo plymouth --show-splash

# Wait a few seconds to see the emblem
sleep 5

# Quit Plymouth
sudo plymouth quit
```

### Test systemd Services

Test services individually:
```bash
# Start banner service
sudo systemctl start sagco-banner.service
sudo systemctl status sagco-banner.service

# Check the banner output
sudo journalctl -u sagco-banner.service -n 20

# Start runtime (will keep running)
sudo systemctl start sagco-runtime.service
sudo systemctl status sagco-runtime.service

# Start compiler (will keep running)
sudo systemctl start sagco-compiler.service
sudo systemctl status sagco-compiler.service

# Start CPU VM (will keep running)
sudo systemctl start sagco-cpu.service
sudo systemctl status sagco-cpu.service

# View all SAGCO services
sudo systemctl status sagco-*

# Follow logs in real-time
sudo journalctl -u sagco-* -f
```

Stop services after testing:
```bash
sudo systemctl stop sagco-cpu.service
sudo systemctl stop sagco-compiler.service
sudo systemctl stop sagco-runtime.service
```

## Full Boot Test

Once you've tested individual components, reboot to see the full SBIP in action:

```bash
sudo reboot
```

## Post-Boot Verification

After rebooting, verify SBIP is working:

### 1. Check Kernel Parameters
```bash
cat /proc/cmdline | grep sagco=1
```
Should show: `sagco=1` in the kernel command line.

### 2. Check Boot Logs
```bash
# View all SAGCO-related boot messages
sudo journalctl -b | grep -i sagco

# View SBIP initramfs messages
sudo journalctl -b | grep "SAGCO Boot Identity Pipeline"
```

### 3. Check Service Status
```bash
# Check all SAGCO services
sudo systemctl status sagco-*

# Should show all services as active (running)
```

### 4. Check Service Logs
```bash
# Banner service
sudo journalctl -u sagco-banner.service

# Runtime service
sudo journalctl -u sagco-runtime.service -n 50

# Compiler service
sudo journalctl -u sagco-compiler.service -n 50

# CPU VM service
sudo journalctl -u sagco-cpu.service -n 50
```

### 5. Check Runtime Directories
```bash
ls -la /opt/sagco/
ls -la /opt/sagco/artifacts/
ls -la /opt/sagco/assets/
```

## Troubleshooting

### Plymouth Theme Not Showing

1. Check if Plymouth is installed:
   ```bash
   which plymouth
   ```

2. Check theme is set:
   ```bash
   plymouth-set-default-theme --list
   plymouth-set-default-theme
   ```

3. Verify initramfs was updated:
   ```bash
   lsinitramfs /boot/initrd.img-$(uname -r) | grep -i plymouth | head
   ```

4. Rebuild initramfs:
   ```bash
   sudo update-initramfs -u -k all
   ```

### Services Not Starting

1. Check for syntax errors:
   ```bash
   sudo systemd-analyze verify /etc/systemd/system/sagco-*.service
   ```

2. Check dependencies:
   ```bash
   sudo systemctl list-dependencies sagco-cpu.service
   ```

3. View detailed logs:
   ```bash
   sudo journalctl -xe -u sagco-runtime.service
   ```

### initramfs Hook Not Running

1. Check hook is executable:
   ```bash
   ls -l /etc/initramfs-tools/scripts/init-top/sagco-init
   ```

2. Check initramfs contains the hook:
   ```bash
   lsinitramfs /boot/initrd.img-$(uname -r) | grep sagco
   ```

3. Rebuild initramfs:
   ```bash
   sudo update-initramfs -u -k all
   ```

## Uninstallation

To remove SBIP:

```bash
# Stop and disable services
sudo systemctl stop sagco-*
sudo systemctl disable sagco-*

# Remove service files
sudo rm /etc/systemd/system/sagco-*.service
sudo systemctl daemon-reload

# Remove runtime components
sudo rm -rf /opt/sagco

# Remove initramfs hook
sudo rm /etc/initramfs-tools/scripts/init-top/sagco-init
sudo update-initramfs -u

# Remove Plymouth theme
sudo rm -rf /usr/share/plymouth/themes/sagco
# Restore default Plymouth theme
sudo plymouth-set-default-theme --reset
sudo update-initramfs -u

# Remove GRUB theme
sudo rm -rf /boot/grub/themes/sagco

# Restore GRUB config
sudo cp /etc/default/grub.backup /etc/default/grub
sudo update-grub

# Remove SAGCO config directory
sudo rm -rf /etc/sagco
```

## Next Steps

1. Replace the placeholder emblem with your official SAGCO trademark image
2. Customize the ASCII banner in `sagco-banner.service`
3. Implement actual FlameLang compiler logic in `/opt/sagco/flamelang-compiler`
4. Implement actual VM logic in `/opt/sagco/sagco-cpu-vm`
5. Add artifact signing and verification
6. Consider creating a full ISO with SBIP pre-installed

## Support

For issues and questions, see:
- `SPECIFICATION.md` - Complete SBIP specification
- `README.md` files in each subdirectory
- Repository issues: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues

---

**SAGCO OS v1.0** - *"From Nothing, Through Reason"*
