#!/bin/bash
# Example usage script for wye curve generator
# Demonstrates various pipe configurations

echo "=== Wye Curve Generator Examples ==="
echo ""

echo "1. Standard 30° wye for 10\" pipe (as specified):"
python3 wye_curve_generator.py -d 10 -a 30 -n 12 -o examples/PCS-1_30deg_wye_curve.svg --no-table
echo ""

echo "2. 45° wye for 6\" pipe with fine resolution:"
python3 wye_curve_generator.py -d 6 -a 45 -n 16 -o examples/wye_6in_45deg.svg --no-table
echo ""

echo "3. 30° wye for 8\" pipe:"
python3 wye_curve_generator.py -d 8 -a 30 -n 12 -o examples/wye_8in_30deg.svg --no-table
echo ""

echo "4. 60° wye for 4\" pipe:"
python3 wye_curve_generator.py -d 4 -a 60 -n 12 -o examples/wye_4in_60deg.svg --no-table
echo ""

echo "=== All examples generated successfully! ==="
echo "Check the examples/ directory for SVG files."
