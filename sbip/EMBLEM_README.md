# Ratio Ex Nihilo - SAGCO Emblem

This is a placeholder for the SAGCO emblem image.

## Required Image Specifications

- **Filename**: `ratio_ex_nihilo.png`
- **Format**: PNG with transparency
- **Recommended Size**: 512x512 pixels (for Plymouth)
- **For GRUB**: Can be larger (e.g., 1920x1080 background)
- **Design**: The circular sigil with lightning motif from your Images 1/3/4

## Where to Place

This emblem should be copied to:
1. `/boot/grub/themes/sagco/ratio_ex_nihilo.png` (for bootloader)
2. `/usr/share/plymouth/themes/sagco/ratio_ex_nihilo.png` (for splash)

## Creating the Emblem

Replace this placeholder with your actual SAGCO trademark emblem image:

```bash
# Copy your emblem to GRUB theme
sudo cp your-emblem.png /boot/grub/themes/sagco/ratio_ex_nihilo.png

# Copy your emblem to Plymouth theme
sudo cp your-emblem.png /usr/share/plymouth/themes/sagco/ratio_ex_nihilo.png
```

## Temporary Placeholder

For testing purposes, you can create a simple placeholder:

```bash
# Create a simple colored square as placeholder (requires ImageMagick)
convert -size 512x512 xc:purple \
  -font Arial -pointsize 48 -fill white -gravity center \
  -annotate +0+0 "SAGCO\nRatio Ex Nihilo" \
  ratio_ex_nihilo.png
```

Or use any existing logo/image as a temporary placeholder until the official emblem is ready.
