#!/usr/bin/env python3
"""
Wye Curve Template Generator for Pipe Fabrication

Generates accurate branch-end cutting templates for true wye pipe intersections
using the corrected formula: h(φ) = r·tan(α/2)·cos(φ)

This tool produces:
- Digitized point data
- SVG files ready for laser cutting/CNC
- Scaling rules for any pipe diameter

Usage:
    python wye_curve_generator.py --diameter 10 --angle 30 --points 12
"""

import argparse
import math
import sys
from typing import List, Tuple


def generate_wye_curve_points(
    diameter: float, 
    angle: float, 
    num_points: int
) -> List[Tuple[float, float]]:
    """
    Generate digitized points for a wye curve branch end template.
    
    Args:
        diameter: Pipe diameter in inches
        angle: Wye angle in degrees (e.g., 30 for a 30° wye)
        num_points: Number of points to generate around the circumference
        
    Returns:
        List of (x, h) tuples representing the developed curve
    """
    radius = diameter / 2
    alpha_rad = math.radians(angle)
    
    # Corrected amplitude formula: A = r·tan(α/2)
    amplitude = radius * math.tan(alpha_rad / 2)
    
    # Unwrap length is the circumference
    unwrap_length = math.pi * diameter
    
    # Step between points
    step = unwrap_length / num_points
    
    points = []
    for n in range(num_points + 1):
        x = n * step
        # φ = 2π·n/N (angle around circumference)
        phi = 2 * math.pi * n / num_points
        # Corrected height formula: h(φ) = r·tan(α/2)·cos(φ)
        h = amplitude * math.cos(phi)
        points.append((x, h))
    
    return points, amplitude, unwrap_length


def catmull_rom_to_bezier(p0, p1, p2, p3):
    """
    Convert a Catmull-Rom spline segment to cubic Bézier control points.
    
    Args:
        p0, p1, p2, p3: Four consecutive points (as tuples)
        
    Returns:
        Tuple of (control_point_1, control_point_2) for the Bézier curve from p1 to p2
    """
    # Standard Catmull-Rom to Bézier conversion formula
    # First control point (1/6 from p1 towards p2, influenced by p0)
    c1 = (
        p1[0] + (p2[0] - p0[0]) / 6.0,
        p1[1] + (p2[1] - p0[1]) / 6.0
    )
    
    # Second control point (1/6 from p2 back towards p1, influenced by p3)
    c2 = (
        p2[0] - (p3[0] - p1[0]) / 6.0,
        p2[1] - (p3[1] - p1[1]) / 6.0
    )
    
    return c1, c2


def generate_svg(
    points: List[Tuple[float, float]], 
    amplitude: float, 
    unwrap_length: float,
    diameter: float,
    angle: float,
    output_file: str
):
    """
    Generate an SVG file with a smooth curve through the digitized points.
    
    Args:
        points: List of (x, h) tuples
        amplitude: Peak amplitude of the curve
        unwrap_length: Total unwrap length (circumference)
        diameter: Pipe diameter
        angle: Wye angle
        output_file: Path to save the SVG file
    """
    # Shift Y upward by amplitude so curve lives in [0, 2A]
    shifted_points = [(x, h + amplitude) for x, h in points]
    
    # Create extended point list for Catmull-Rom (wrap around)
    extended = [shifted_points[-2], shifted_points[-1]] + shifted_points + [shifted_points[0], shifted_points[1]]
    
    # Build SVG path data using Catmull-Rom to Bézier conversion
    path_commands = []
    
    # Start at first point
    path_commands.append(f"M {shifted_points[0][0]:.6f},{shifted_points[0][1]:.6f}")
    
    # Generate Bézier curves for each segment
    for i in range(1, len(shifted_points)):
        p0 = extended[i]
        p1 = extended[i + 1]
        p2 = extended[i + 2]
        p3 = extended[i + 3]
        
        c1, c2 = catmull_rom_to_bezier(p0, p1, p2, p3)
        
        # Cubic Bézier curve command
        path_commands.append(
            f"C {c1[0]:.6f},{c1[1]:.6f} {c2[0]:.6f},{c2[1]:.6f} {p2[0]:.6f},{p2[1]:.6f}"
        )
    
    path_data = "\n           ".join(path_commands)
    
    # Create SVG content
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg"
     width="{unwrap_length:.6f}in" height="{2 * amplitude:.6f}in"
     viewBox="0 0 {unwrap_length:.6f} {2 * amplitude:.6f}">
  <!-- {angle:.0f}° true-wye branch-end curve (equal diameters)
       D={diameter:.0f}in, N={len(points) - 1}.  h(phi)= (D/2)*tan({angle/2:.0f}°)*cos(phi)
       Y is shifted up by +A so min is 0. -->

  <path d="{path_data}"
        fill="none" stroke="black" stroke-width="0.03"/>
</svg>
'''
    
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"SVG file generated: {output_file}")


def print_point_table(points: List[Tuple[float, float]], amplitude: float):
    """
    Print a formatted table of digitized points.
    
    Args:
        points: List of (x, h) tuples
        amplitude: Peak amplitude for display
    """
    print("\nDigitized Point Data:")
    print("=" * 50)
    print(f"n\tx (in)\th (in)")
    print("-" * 50)
    
    for i, (x, h) in enumerate(points):
        print(f"{i}\t{x:.3f}\t{h:.3f}")
    
    print("=" * 50)
    print(f"\nPeak amplitude: ±{amplitude:.6f} inches")


def print_scaling_rules(diameter: float, angle: float):
    """
    Print scaling rules for general use.
    
    Args:
        diameter: Pipe diameter
        angle: Wye angle
    """
    print("\n" + "=" * 50)
    print("SCALING RULES FOR GENERAL USE")
    print("=" * 50)
    print("\nFor any pipe diameter D and wye angle α:")
    print(f"\n1. Radius: r = D/2")
    print(f"2. Unwrap length: L = π·D")
    print(f"3. Step (for N points): Δx = π·D/N")
    print(f"4. Amplitude: A = r·tan(α/2)")
    print(f"5. Height at point n: h(φₙ) = A·cos(2π·n/N)")
    print(f"6. For non-negative Y in SVG: shift up by +A")
    print("\n" + "=" * 50)
    
    # Calculate values for current parameters
    radius = diameter / 2
    alpha_rad = math.radians(angle)
    amplitude = radius * math.tan(alpha_rad / 2)
    unwrap_length = math.pi * diameter
    
    print(f"\nCurrent calculation (D={diameter}in, α={angle}°):")
    print(f"  r = {radius:.3f} in")
    print(f"  L = {unwrap_length:.6f} in")
    print(f"  A = {amplitude:.6f} in")
    print(f"  tan({angle/2}°) = {math.tan(alpha_rad/2):.6f}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate wye curve templates for pipe fabrication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a 30° wye curve for 10" diameter pipe with 12 points
  python wye_curve_generator.py --diameter 10 --angle 30 --points 12

  # Generate a 45° wye curve for 6" diameter pipe
  python wye_curve_generator.py -d 6 -a 45 -n 16 -o wye_6in_45deg.svg
        """
    )
    
    parser.add_argument(
        '-d', '--diameter',
        type=float,
        required=True,
        help='Pipe diameter in inches'
    )
    
    parser.add_argument(
        '-a', '--angle',
        type=float,
        required=True,
        help='Wye angle in degrees (e.g., 30 for 30° wye)'
    )
    
    parser.add_argument(
        '-n', '--points',
        type=int,
        default=12,
        help='Number of points around circumference (default: 12)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output SVG filename (default: wye_<D>in_<angle>deg.svg)'
    )
    
    parser.add_argument(
        '--no-table',
        action='store_true',
        help='Suppress point table output'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.diameter <= 0:
        print("Error: Diameter must be positive", file=sys.stderr)
        sys.exit(1)
    
    if args.angle <= 0 or args.angle >= 90:
        print("Error: Angle must be between 0° and 90°", file=sys.stderr)
        sys.exit(1)
    
    if args.points < 4:
        print("Error: Need at least 4 points", file=sys.stderr)
        sys.exit(1)
    
    # Generate default output filename if not specified
    if args.output is None:
        args.output = f"wye_{int(args.diameter)}in_{int(args.angle)}deg.svg"
    
    print(f"\nGenerating {args.angle}° wye curve template")
    print(f"Diameter: {args.diameter} inches")
    print(f"Number of points: {args.points}")
    
    # Generate points
    points, amplitude, unwrap_length = generate_wye_curve_points(
        args.diameter, 
        args.angle, 
        args.points
    )
    
    # Print point table
    if not args.no_table:
        print_point_table(points, amplitude)
    
    # Generate SVG
    generate_svg(
        points, 
        amplitude, 
        unwrap_length,
        args.diameter,
        args.angle,
        args.output
    )
    
    # Print scaling rules
    print_scaling_rules(args.diameter, args.angle)
    
    print("\n✅ Template generation complete!")
    print(f"\nThis template is for the branch end (wrap around branch).")
    print("Use it to mark the cut line on the branch pipe.")


if __name__ == '__main__':
    main()
