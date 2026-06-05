# Wye Curve Template Examples

This directory contains example SVG templates generated using the wye curve generator.

## Files

### PCS-1_30deg_wye_curve.svg
- **Diameter**: 10 inches
- **Angle**: 30°
- **Points**: 12
- **Peak Amplitude**: ±1.339746 inches
- **Usage**: Standard example from specification

### wye_6in_45deg.svg
- **Diameter**: 6 inches
- **Angle**: 45°
- **Points**: 16
- **Peak Amplitude**: ±1.242641 inches
- **Usage**: Higher angle, smaller diameter with fine resolution

### wye_8in_30deg.svg
- **Diameter**: 8 inches
- **Angle**: 30°
- **Points**: 12
- **Peak Amplitude**: ±1.071797 inches
- **Usage**: Medium diameter standard angle

### wye_4in_60deg.svg
- **Diameter**: 4 inches
- **Angle**: 60°
- **Points**: 12
- **Peak Amplitude**: ±1.154701 inches
- **Usage**: Small diameter, high angle wye

## Regenerating Examples

To regenerate all examples:

```bash
./generate_wye_examples.sh
```

## Using These Templates

1. Open the SVG file in a laser cutting software (LightBurn, RDWorks) or CAD program (Inkscape, Fusion 360)
2. Scale if needed (dimensions are in inches)
3. Print or cut on appropriate material
4. Wrap the template around the branch pipe
5. Mark the cut line following the curve
6. Cut along the marked line

## Notes

- All templates are for **branch end** cutting (wrap around branch pipe)
- Y coordinates are shifted so minimum is at 0 (easier for cutting)
- Stroke width is set to 0.03 for precision
- Curves use smooth Catmull-Rom spline interpolation
