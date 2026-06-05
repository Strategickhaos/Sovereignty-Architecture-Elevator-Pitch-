# SAGCO Plymouth Theme

Plymouth boot splash theme for the SAGCO Boot Identity Pipeline.

## Files

- `sagco.plymouth` - Theme configuration
- `sagco.script` - Plymouth script for splash rendering
- `README.md` - This file

## Required Assets

Place these image files in the theme directory:
- `ratio_ex_nihilo.png` - SAGCO logo/emblem
- `progress_box.png` - Progress bar background
- `progress_bar.png` - Progress bar fill

## Installation

```bash
# 1. Install Plymouth if not already installed
sudo apt install plymouth plymouth-themes

# 2. Create theme directory
sudo mkdir -p /usr/share/plymouth/themes/sagco

# 3. Copy theme files
sudo cp plymouth/* /usr/share/plymouth/themes/sagco/

# 4. Install theme
sudo plymouth-set-default-theme sagco

# 5. Update initramfs to include new theme
sudo update-initramfs -u

# 6. Test theme (if X is running)
sudo plymouthd
sudo plymouth show-splash
# Wait a few seconds
sudo plymouth quit
```

## Customization

Edit `sagco.script` to customize:
- Colors (RGB values 0.0 to 1.0)
- Text content and positioning
- Animation sequences
- Progress bar appearance

## Fallback

If Plymouth fails (e.g., no GPU), the system falls back to text mode boot.
SAGCO identity is still displayed via initramfs scripts.

## Debugging

```bash
# View Plymouth logs
journalctl -u plymouth-start.service

# Check current theme
plymouth-set-default-theme --list
plymouth-set-default-theme

# Test theme rendering
sudo plymouthd --debug --debug-file=/tmp/plymouth-debug.log
```

## Legal Notice

Property of Strategickhaos DAO LLC
Wyoming Entity: 2025-001708194 | EIN: 39-2923503
