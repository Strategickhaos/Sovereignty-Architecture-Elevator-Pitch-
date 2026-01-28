#!/usr/bin/env python3
"""
RUBIK'S CUBE GEOSPATIAL MAPPER - EXAMPLE USAGE
Demonstrates the 6-Face Geospatial Computing System
"""

from rubiks_geospatial_mapper import RubiksGeospatialMapper
import json
import math


def example_basic_usage():
    """Example 1: Basic usage - mapping a single sticker"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Usage - Mapping a Single Sticker")
    print("=" * 80)
    
    mapper = RubiksGeospatialMapper()
    
    # Map the center of the UP face (North Pole)
    u5 = mapper.cube_to_geovector('U', 1, 1)
    
    print(f"\nSticker ID: {u5.sticker_id}")
    print(f"Face: {u5.face}")
    print(f"Position: Row {u5.position[0]}, Column {u5.position[1]} ({u5.position_type})")
    print(f"\nGeolocation:")
    print(f"  Decimal: {u5.lat:.6f}°, {u5.long:.6f}°")
    print(f"  DMS: {u5.lat_dms.to_string()}, {u5.long_dms.to_string()}")
    print(f"\n3D Vector (unit sphere):")
    print(f"  (x, y, z) = ({u5.vector_3d[0]:.6f}, {u5.vector_3d[1]:.6f}, {u5.vector_3d[2]:.6f})")
    print(f"\nAngles:")
    print(f"  θ (azimuthal): {u5.theta:.2f}°")
    print(f"  φ (polar): {u5.phi:.2f}°")
    print(f"\nTRIG6 Values:")
    print(f"  sin(θ) = {u5.trig6['sin']:.6f}")
    print(f"  cos(θ) = {u5.trig6['cos']:.6f}")
    print(f"  tan(θ) = {u5.trig6['tan']:.6f}")
    print(f"  csc(θ) = {u5.trig6['csc']:.6f}" if math.isfinite(u5.trig6['csc']) else f"  csc(θ) = inf")
    print(f"  sec(θ) = {u5.trig6['sec']:.6f}")
    print(f"  cot(θ) = {u5.trig6['cot']:.6f}" if math.isfinite(u5.trig6['cot']) else f"  cot(θ) = inf")


def example_face_mapping():
    """Example 2: Map all stickers on one face"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Face Mapping - All 9 Stickers on FRONT Face")
    print("=" * 80)
    
    mapper = RubiksGeospatialMapper()
    mapper.generate_complete_matrix()
    front_face = mapper.get_face_matrix('F')
    
    print(f"\nFRONT Face (Prime Meridian Region):")
    print(f"{'ID':<5} {'Type':<8} {'Latitude':<12} {'Longitude':<12} {'Vector (x,y,z)':<30}")
    print("-" * 80)
    
    for sticker in front_face:
        vec_str = f"({sticker.vector_3d[0]:.3f}, {sticker.vector_3d[1]:.3f}, {sticker.vector_3d[2]:.3f})"
        print(f"{sticker.sticker_id:<5} {sticker.position_type:<8} "
              f"{sticker.lat_dms.to_string():<12} {sticker.long_dms.to_string():<12} "
              f"{vec_str:<30}")


def example_key_positions():
    """Example 3: Key geographic positions on the cube"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Key Geographic Positions")
    print("=" * 80)
    
    mapper = RubiksGeospatialMapper()
    
    positions = [
        ('U', 1, 1, "North Pole", "Center of UP face"),
        ('D', 1, 1, "South Pole", "Center of DOWN face"),
        ('F', 1, 1, "Prime Meridian", "Center of FRONT face"),
        ('B', 1, 1, "Antimeridian", "Center of BACK face"),
        ('L', 1, 1, "West (90°W)", "Center of LEFT face"),
        ('R', 1, 1, "East (90°E)", "Center of RIGHT face"),
    ]
    
    for face, row, col, name, description in positions:
        gv = mapper.cube_to_geovector(face, row, col)
        print(f"\n🌍 {name} ({description}):")
        print(f"   Sticker: {gv.sticker_id}")
        print(f"   Location: {gv.lat_dms.to_string()}, {gv.long_dms.to_string()}")
        print(f"   Vector: ({gv.vector_3d[0]:.6f}, {gv.vector_3d[1]:.6f}, {gv.vector_3d[2]:.6f})")


def example_complete_matrix():
    """Example 4: Generate and display complete 54-sticker matrix"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Complete 54-Sticker Geolocation Matrix")
    print("=" * 80)
    
    mapper = RubiksGeospatialMapper()
    mapper.generate_complete_matrix()
    mapper.print_matrix_table()


def example_json_export():
    """Example 5: Export to JSON for integration with other systems"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: JSON Export for System Integration")
    print("=" * 80)
    
    mapper = RubiksGeospatialMapper()
    export_data = mapper.export_to_dict()
    
    output_file = '/tmp/rubiks_cube_geospatial_complete.json'
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n✓ Exported complete matrix to: {output_file}")
    print(f"\nSummary:")
    print(f"  Total Stickers: {export_data['total_stickers']}")
    print(f"  Faces: {export_data['faces']}")
    print(f"  Stickers per Face: {export_data['stickers_per_face']}")
    
    # Show a sample sticker from the export
    sample = export_data['stickers'][0]
    print(f"\nSample Sticker (JSON format):")
    print(json.dumps(sample, indent=2))


def example_mathematical_connections():
    """Example 6: Demonstrate mathematical connections"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Mathematical Connections - The Ramanujan Pattern")
    print("=" * 80)
    
    mapper = RubiksGeospatialMapper()
    
    # Show how θ=45° creates resonance (tan=1)
    print("\n🔥 RESONANCE POINTS (tan(θ) ≈ 1):")
    print("These are positions where tangent equals 1, creating mathematical resonance")
    print("-" * 80)
    
    mapper.generate_complete_matrix()
    
    resonance_count = 0
    for gv in mapper.sticker_matrix:
        if abs(gv.trig6['tan'] - 1.0) < 0.01:  # Close to 1
            resonance_count += 1
            print(f"  {gv.sticker_id}: θ={gv.theta:.2f}°, tan(θ)={gv.trig6['tan']:.6f} at {gv.lat_dms.to_string()}, {gv.long_dms.to_string()}")
    
    if resonance_count == 0:
        print("  (Checking absolute values...)")
        for gv in mapper.sticker_matrix:
            if abs(abs(gv.trig6['tan']) - 1.0) < 0.01:  # Close to ±1
                print(f"  {gv.sticker_id}: θ={gv.theta:.2f}°, tan(θ)={gv.trig6['tan']:.6f} at {gv.lat_dms.to_string()}, {gv.long_dms.to_string()}")
    
    print("\n🔢 THE CONNECTION:")
    print("  Ramanujan: e^(π√163) ≈ integer (almost perfect)")
    print("  Rubik's Cube: θ=45° → tan=1 (exactly perfect)")
    print("  54 stickers → 6 faces → 1 solved state")
    print("  Every position in space has a NUMBER.")


def example_coordinate_conversions():
    """Example 7: Coordinate system conversions"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Coordinate System Conversions")
    print("=" * 80)
    
    mapper = RubiksGeospatialMapper()
    
    # Test decimal to DMS and back
    test_values = [45.5, -67.75, 90.0, -180.0, 0.0]
    
    print("\nDecimal Degrees ↔ DMS Conversion Test:")
    print("-" * 80)
    for decimal in test_values:
        dms = mapper.decimal_to_dms(decimal, is_latitude=(abs(decimal) <= 90))
        back_to_decimal = mapper.dms_to_decimal(dms)
        print(f"  {decimal:>8.2f}° → {dms.to_string():<18} → {back_to_decimal:>8.2f}° (diff: {abs(decimal - back_to_decimal):.6f})")


def main():
    """Run all examples"""
    print("🔥" * 40)
    print("RUBIK'S CUBE GEOSPATIAL MAPPER - COMPREHENSIVE EXAMPLES")
    print("6-Face Geospatial Computing System")
    print("🔥" * 40)
    
    # Run all examples
    example_basic_usage()
    example_face_mapping()
    example_key_positions()
    example_complete_matrix()
    example_json_export()
    example_mathematical_connections()
    example_coordinate_conversions()
    
    print("\n" + "=" * 80)
    print("🔥 THE RUBIK'S GEOSPATIAL INVARIANT 🔥")
    print("=" * 80)
    print("\nTHE ALGORITHM YOUR BRAIN IS COMPUTING:")
    print("  EACH CUBE FACE = A COORDINATE SYSTEM")
    print("       ↓")
    print("  3 POINTS OF CONTACT = TRIANGLE (EUCLIDEAN PLANE)")
    print("       ↓")
    print("  TRIANGLE → DEGREES/MINUTES/SECONDS (DMS)")
    print("       ↓")
    print("  DMS → INTERNAL GEOLOCATION (lat/long ON the cube surface)")
    print("       ↓")
    print("  GEOLOCATION → VECTOR (sin, cos, tan of position)")
    print("       ↓")
    print("  6 FACES × 9 SQUARES = 54 GEOLOCATED VECTORS")
    print("\n✓ Every position in space has a NUMBER.")
    print("✓ 54 stickers → 6 faces → 1 solved state")
    print("✓ This is how you see the world, Dom. 🔥🧊🌍")
    print("=" * 80)


if __name__ == "__main__":
    main()
