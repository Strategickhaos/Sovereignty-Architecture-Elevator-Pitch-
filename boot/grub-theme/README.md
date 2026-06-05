# SAGCO GRUB Theme Assets

This directory contains the visual assets for the SAGCO Boot Identity Pipeline GRUB theme.

## Files

- `theme.txt` - GRUB theme configuration
- `grub.cfg.template` - Template for /etc/default/grub
- `ratio_ex_nihilo.png` - SAGCO emblem (trademark V2)
- `select_*.png` - Menu selection graphics (to be added)

## Required Assets

The following image files should be placed in this directory:

1. **ratio_ex_nihilo.png** - Main boot background
   - Recommended size: 1024x768 or 1920x1080
   - Format: PNG with transparency support
   - Content: SAGCO trademark emblem, Math Eye sketch, or entity branding

2. **select_c.png, select_w.png, select_e.png** - Menu selection sprites
   - Size: Match menu item dimensions
   - Format: PNG
   - Optional: Can use solid colors if images not available

## Installation

```bash
# 1. Create theme directory
sudo mkdir -p /boot/grub/themes/sagco

# 2. Copy theme files
sudo cp boot/grub-theme/* /boot/grub/themes/sagco/

# 3. Update GRUB configuration
# Merge settings from grub.cfg.template into /etc/default/grub

# 4. Update GRUB
sudo update-grub

# 5. Reboot to see SAGCO boot identity
sudo reboot
```

## Customization

Edit `theme.txt` to customize:
- Colors (hex color codes)
- Fonts (Unifont or other monospace fonts)
- Layout (position and size of elements)
- Text content (entity information, branding)

## Legal Notice

SAGCO trademark and branding assets are property of Strategickhaos DAO LLC.
Wyoming Entity: 2025-001708194 | EIN: 39-2923503
