# Plymouth Splash Screen

This directory contains the Plymouth theme for SAGCO Boot Identity Pipeline (SBIP).

## Installation

1. Copy the theme directory to `/usr/share/plymouth/themes/`:
   ```bash
   sudo cp -r themes/sagco /usr/share/plymouth/themes/
   ```

2. Set as default theme:
   ```bash
   sudo plymouth-set-default-theme sagco
   ```

3. Update initramfs:
   ```bash
   sudo update-initramfs -u
   ```

## Required Files

- `sagco.plymouth`: Plymouth theme definition
- `sagco.script`: Script for displaying emblem
- `ratio_ex_nihilo.png`: SAGCO emblem image (place your emblem here)

## Testing

Test the theme without rebooting:
```bash
sudo plymouthd
sudo plymouth --show-splash
# Wait 5 seconds
sudo plymouth quit
```

## Notes

- The emblem should be a PNG file with appropriate dimensions (e.g., 512x512)
- The splash will be displayed during early boot stages
- Ensure Plymouth is installed: `sudo apt install plymouth plymouth-themes`
