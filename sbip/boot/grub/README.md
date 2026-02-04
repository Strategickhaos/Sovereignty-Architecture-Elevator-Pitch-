# GRUB Bootloader Configuration

This directory contains the GRUB theme for SAGCO Boot Identity Pipeline (SBIP).

## Installation

1. Copy the theme directory to `/boot/grub/themes/`:
   ```bash
   sudo cp -r themes/sagco /boot/grub/themes/
   ```

2. Add the following to `/etc/default/grub`:
   ```
   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash sagco=1"
   GRUB_THEME="/boot/grub/themes/sagco/theme.txt"
   ```

3. Update GRUB configuration:
   ```bash
   sudo update-grub
   ```

## Required Files

- `theme.txt`: GRUB theme configuration
- `ratio_ex_nihilo.png`: SAGCO emblem image (place your emblem here)

## Notes

- The `sagco=1` kernel parameter enables SAGCO boot mode
- The emblem should be placed in this directory before installation
