#!/usr/bin/env python3
"""
TRIG6 Pipe Template Generator
=============================
Generates saddle curves for pipe wye/tee fabrication.

Entity: Strategickhaos DAO LLC
Invention: TRIG6 Projection Curve System
Angel: Pending assignment (Physical Tool category)

Usage:
    python trig6_pipe_template.py --diameter 10 --angle 30 --output template.svg
    python trig6_pipe_template.py --diameter 6 --angle 45 --segments 16
"""

import math
import argparse
from dataclasses import dataclass
from typing import List, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# TRIG6 CORE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TRIG6Vector:
    """Complete trigonometric state at an angle."""
    theta_deg: float
    theta_rad: float
    sin: float
    cos: float
    tan: float
    csc: float
    sec: float
    cot: float
    
    @classmethod
    def from_degrees(cls, theta_deg: float) -> 'TRIG6Vector':
        """Create TRIG6 vector from angle in degrees."""
        theta_rad = math.radians(theta_deg)
        sin_val = math.sin(theta_rad)
        cos_val = math.cos(theta_rad)
        
        # Handle division by zero for reciprocals
        tan_val = sin_val / cos_val if abs(cos_val) > 1e-10 else float('inf')
        csc_val = 1 / sin_val if abs(sin_val) > 1e-10 else float('inf')
        sec_val = 1 / cos_val if abs(cos_val) > 1e-10 else float('inf')
        cot_val = cos_val / sin_val if abs(sin_val) > 1e-10 else float('inf')
        
        return cls(
            theta_deg=theta_deg,
            theta_rad=theta_rad,
            sin=sin_val,
            cos=cos_val,
            tan=tan_val,
            csc=csc_val,
            sec=sec_val,
            cot=cot_val
        )

# ═══════════════════════════════════════════════════════════════════════════════
# SADDLE CURVE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SaddlePoint:
    """A point on the saddle curve."""
    segment: int
    theta_deg: float
    x: float  # Position along unwrapped circumference
    y: float  # Height offset from centerline
    
def generate_saddle_curve(
    diameter: float,
    branch_angle_deg: float,
    num_segments: int = 12
) -> List[SaddlePoint]:
    """
    Generate saddle curve points for a pipe branch.
    
    The saddle curve is the intersection of a cylinder (main pipe)
    with another cylinder (branch pipe) at a given angle.
    
    For a true wye with equal-diameter pipes:
    h(θ) = (D/2) × tan(α) × cos(θ)
    
    Where:
    - D = pipe diameter
    - α = branch angle
    - θ = position around circumference (0 to 2π)
    
    Args:
        diameter: Pipe diameter in inches
        branch_angle_deg: Branch angle in degrees
        num_segments: Number of discrete points
        
    Returns:
        List of SaddlePoint objects
    """
    radius = diameter / 2
    branch_angle_rad = math.radians(branch_angle_deg)
    amplitude = radius * math.tan(branch_angle_rad)
    circumference = math.pi * diameter
    
    points = []
    
    for n in range(num_segments + 1):
        # Angular position around pipe
        theta_deg = (360 * n) / num_segments
        theta_rad = math.radians(theta_deg)
        
        # X position (linear unwrap of circumference)
        x = (circumference * n) / num_segments
        
        # Y position (height offset) - cosine wave
        y = amplitude * math.cos(theta_rad)
        
        points.append(SaddlePoint(
            segment=n,
            theta_deg=theta_deg,
            x=x,
            y=y
        ))
    
    return points

def points_to_table(points: List[SaddlePoint]) -> str:
    """Format points as ASCII table."""
    lines = [
        "┌─────────┬───────────┬────────────┬────────────┐",
        "│ Segment │  θ (deg)  │  X (in)    │  Y (in)    │",
        "├─────────┼───────────┼────────────┼────────────┤"
    ]
    
    for p in points:
        lines.append(
            f"│ {p.segment:>7} │ {p.theta_deg:>9.2f} │ {p.x:>10.3f} │ {p.y:>+10.3f} │"
        )
    
    lines.append("└─────────┴───────────┴────────────┴────────────┘")
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════════════════════
# SVG GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_svg(
    points: List[SaddlePoint],
    diameter: float,
    branch_angle: float,
    scale: float = 10.0
) -> str:
    """Generate SVG template from saddle points."""
    
    circumference = math.pi * diameter
    amplitude = (diameter / 2) * math.tan(math.radians(branch_angle))
    
    # Scale for viewBox
    width = circumference * scale
    height = (amplitude * 2 + 10) * scale
    center_y = height / 2
    
    # Build path data
    path_points = []
    for p in points:
        px = p.x * scale
        py = center_y - (p.y * scale)  # Invert Y for SVG coords
        path_points.append((px, py))
    
    # Create smooth Bézier path
    path_d = f"M {path_points[0][0]:.2f},{path_points[0][1]:.2f}"
    for i in range(1, len(path_points)):
        path_d += f" L {path_points[i][0]:.2f},{path_points[i][1]:.2f}"
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{width/scale}in" 
     height="{height/scale}in" 
     viewBox="0 0 {width:.2f} {height:.2f}">
  
  <title>{branch_angle}° Wye Branch Template</title>
  <desc>
    TRIG6 Projection Curve Stencil
    Entity: Strategickhaos DAO LLC
    Pipe Diameter: {diameter} inches
    Branch Angle: {branch_angle}°
    Segments: {len(points)-1}
  </desc>
  
  <!-- Centerline -->
  <line x1="0" y1="{center_y:.2f}" x2="{width:.2f}" y2="{center_y:.2f}" 
        stroke="#ccc" stroke-width="0.5" stroke-dasharray="5,3"/>
  
  <!-- Saddle Curve -->
  <path d="{path_d}"
        fill="none" 
        stroke="#8b5cf6" 
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"/>
  
  <!-- Projection Points -->
  <g fill="#8b5cf6">
'''
    
    for i, (px, py) in enumerate(path_points):
        radius = 4 if i % 3 == 0 else 2
        svg += f'    <circle cx="{px:.2f}" cy="{py:.2f}" r="{radius}"/>\n'
    
    svg += f'''  </g>
  
  <!-- Scale bar -->
  <g transform="translate(10, {height - 20})">
    <line x1="0" y1="0" x2="{scale * 10}" y2="0" stroke="#333" stroke-width="1"/>
    <line x1="0" y1="-5" x2="0" y2="5" stroke="#333" stroke-width="1"/>
    <line x1="{scale * 10}" y1="-5" x2="{scale * 10}" y2="5" stroke="#333" stroke-width="1"/>
    <text x="{scale * 5}" y="-8" font-family="Arial" font-size="12" text-anchor="middle">
      10 inches
    </text>
  </g>
  
  <!-- Title -->
  <text x="{width/2:.2f}" y="25" font-family="Arial" font-size="16" 
        text-anchor="middle" fill="#333">
    {branch_angle}° WYE TEMPLATE | D={diameter}" | TRIG6-PCS
  </text>
  
</svg>'''
    
    return svg

# ═══════════════════════════════════════════════════════════════════════════════
# TRIG6 ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_branch_angle(angle_deg: float) -> dict:
    """Analyze a branch angle using TRIG6."""
    t = TRIG6Vector.from_degrees(angle_deg)
    
    return {
        "angle": angle_deg,
        "trig6_vector": {
            "sin": round(t.sin, 4),
            "cos": round(t.cos, 4),
            "tan": round(t.tan, 4) if t.tan != float('inf') else "∞",
            "csc": round(t.csc, 4) if t.csc != float('inf') else "∞",
            "sec": round(t.sec, 4) if t.sec != float('inf') else "∞",
            "cot": round(t.cot, 4) if t.cot != float('inf') else "∞",
        },
        "properties": {
            "is_cardinal": angle_deg % 90 == 0,
            "is_diagonal": angle_deg % 45 == 0 and angle_deg % 90 != 0,
            "quadrant": int(angle_deg // 90) + 1 if angle_deg < 360 else 4,
            "amplitude_factor": round(t.tan, 4) if t.tan != float('inf') else "∞",
        }
    }

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="TRIG6 Pipe Template Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python trig6_pipe_template.py --diameter 10 --angle 30
  python trig6_pipe_template.py --diameter 6 --angle 45 --output template.svg
  python trig6_pipe_template.py --diameter 8 --angle 60 --segments 24

Entity: Strategickhaos DAO LLC
        """
    )
    
    parser.add_argument("-d", "--diameter", type=float, default=10.0,
                        help="Pipe diameter in inches (default: 10)")
    parser.add_argument("-a", "--angle", type=float, default=30.0,
                        help="Branch angle in degrees (default: 30)")
    parser.add_argument("-s", "--segments", type=int, default=12,
                        help="Number of segments (default: 12)")
    parser.add_argument("-o", "--output", type=str,
                        help="Output SVG file path")
    parser.add_argument("--table", action="store_true",
                        help="Print point table to stdout")
    parser.add_argument("--analyze", action="store_true",
                        help="Show TRIG6 analysis of the angle")
    
    args = parser.parse_args()
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    TRIG6 PIPE TEMPLATE GENERATOR                              ║
║                     StrategicKhaos DAO LLC                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Diameter: {args.diameter:>6.2f} inches                                              ║
║  Branch Angle: {args.angle:>6.2f}°                                                   ║
║  Segments: {args.segments:>6}                                                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Generate points
    points = generate_saddle_curve(args.diameter, args.angle, args.segments)
    
    # Calculate key values
    circumference = math.pi * args.diameter
    amplitude = (args.diameter / 2) * math.tan(math.radians(args.angle))
    
    print(f"Circumference: {circumference:.3f} inches")
    print(f"Amplitude (max height): ±{amplitude:.3f} inches")
    print(f"High points at: 0°, 360° (segments 0, {args.segments})")
    print(f"Low point at: 180° (segment {args.segments // 2})")
    print(f"Centerline crossings at: 90°, 270°")
    
    # Show table
    if args.table:
        print("\n" + points_to_table(points))
    
    # Show TRIG6 analysis
    if args.analyze:
        analysis = analyze_branch_angle(args.angle)
        print(f"\nTRIG6 Analysis of {args.angle}°:")
        print(f"  Vector: {analysis['trig6_vector']}")
        print(f"  Quadrant: {analysis['properties']['quadrant']}")
        print(f"  Amplitude factor (tan): {analysis['properties']['amplitude_factor']}")
    
    # Generate SVG
    if args.output:
        svg = generate_svg(points, args.diameter, args.angle)
        with open(args.output, 'w') as f:
            f.write(svg)
        print(f"\n✅ SVG saved to: {args.output}")
    else:
        # Default output name
        default_name = f"wye_{int(args.angle)}deg_d{int(args.diameter)}.svg"
        svg = generate_svg(points, args.diameter, args.angle)
        with open(default_name, 'w') as f:
            f.write(svg)
        print(f"\n✅ SVG saved to: {default_name}")

if __name__ == "__main__":
    main()
