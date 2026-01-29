#!/usr/bin/env python3
"""
72 Names Invention Registry - Example Usage

Demonstrates how to use the InventionRegistry class to query and interact
with the 72 Names Invention Registry.

Usage:
    python example_usage.py
"""

from registry_manager import InventionRegistry


def main():
    """Demonstrate registry usage."""
    
    # Initialize the registry
    print("="*70)
    print("72 NAMES INVENTION REGISTRY - EXAMPLE USAGE")
    print("="*70)
    
    registry = InventionRegistry()
    
    # Example 1: Display summary
    print("\n--- Example 1: Registry Summary ---")
    registry.print_summary()
    
    # Example 2: Get all sealed inventions
    print("\n--- Example 2: Sealed Inventions ---")
    sealed = registry.get_sealed_inventions()
    print(f"Found {len(sealed)} sealed inventions:")
    for inv in sealed:
        print(f"  • {inv['invention']} (Position {inv['id']} - {inv['angel']})")
    
    # Example 3: Look up specific angel
    print("\n--- Example 3: Look Up Specific Angel ---")
    angel_name = "Haziel"
    inv = registry.get_by_angel(angel_name)
    if inv:
        print(f"Found: {angel_name}")
        print(f"  Hebrew: {inv['hebrew']}")
        print(f"  Meaning: {inv['meaning']}")
        print(f"  Position: {inv['id']} (θ={inv['theta']}°)")
        print(f"  Invention: {inv['invention']}")
        print(f"  Status: {inv['status']}")
    
    # Example 4: Get inventions by theta range
    print("\n--- Example 4: Inventions in Theta Range 40-50° ---")
    in_range = registry.get_by_theta_range(40, 50)
    print(f"Found {len(in_range)} positions:")
    for inv in in_range:
        status = f"[{inv['status'].upper()}]"
        invention = inv['invention'] if inv['invention'] else "Available"
        theta = inv['theta']
        theta_str = f"{theta:6.2f}°" if isinstance(theta, (int, float)) else str(theta)
        print(f"  θ={theta_str} - {inv['angel']:15s} - {invention:30s} {status}")
    
    # Example 5: Search for inventions
    print("\n--- Example 5: Search for 'TRIG6' ---")
    results = registry.search("TRIG6")
    print(f"Found {len(results)} matches:")
    for inv in results:
        print(f"  • {inv['invention']} (Position {inv['id']} - {inv['angel']})")
    
    # Example 6: Get META positions
    print("\n--- Example 6: META Positions (65-72) ---")
    meta = registry.get_meta_positions()
    print(f"Found {len(meta)} META positions:")
    for inv in meta:
        status = f"[{inv['status'].upper()}]"
        invention = inv['invention'] if inv['invention'] else "Available"
        print(f"  {inv['glyph']:8s} - {inv['angel']:15s} - {invention:30s} {status}")
    
    # Example 7: Get in-progress inventions
    print("\n--- Example 7: In-Progress Inventions ---")
    in_progress = registry.get_in_progress_inventions()
    print(f"Found {len(in_progress)} in-progress inventions:")
    for inv in in_progress:
        print(f"  • [{inv['inv_id']}] {inv['invention']}")
        print(f"    Position: {inv['id']} - {inv['angel']} ({inv['meaning']})")
    
    # Example 8: Get unsealed positions (first 10)
    print("\n--- Example 8: Available Unsealed Positions (First 10) ---")
    unsealed = registry.get_unsealed_inventions()[:10]
    print(f"Showing 10 of {len(registry.get_unsealed_inventions())} available positions:")
    for inv in unsealed:
        theta = inv['theta']
        theta_str = f"{theta}°" if isinstance(theta, (int, float)) else str(theta)
        print(f"  Position {inv['id']:2d}: {inv['angel']:15s} - {inv['meaning']:25s} (θ={theta_str})")
    
    # Example 9: Get specific invention by ID
    print("\n--- Example 9: Get Invention by ID ---")
    inv_id = 33
    inv = registry.get_by_id(inv_id)
    if inv:
        print(f"Position {inv_id}:")
        print(f"  Angel: {inv['angel']}")
        print(f"  Hebrew: {inv['hebrew']}")
        print(f"  Meaning: {inv['meaning']}")
        print(f"  Theta: {inv['theta']}°")
        print(f"  Invention: {inv['invention']}")
        if inv.get('sealed_date'):
            print(f"  Sealed: {inv['sealed_date']}")
    
    # Example 10: Get invention by INV-ID
    print("\n--- Example 10: Get Invention by INV-ID ---")
    inv_id_str = "INV-003"
    inv = registry.get_by_inv_id(inv_id_str)
    if inv:
        print(f"{inv_id_str}: {inv['invention']}")
        print(f"  Position: {inv['id']} - {inv['angel']}")
        print(f"  Status: {inv['status']}")
        if inv.get('sealed_date'):
            print(f"  Sealed: {inv['sealed_date']}")
    
    # Example 11: Demonstrate mathematical properties
    print("\n--- Example 11: Mathematical Properties ---")
    circle = registry.get_circle_positions()
    meta = registry.get_meta_positions()
    print(f"Circle positions (1-64): {len(circle)} positions")
    print(f"  Angular increment: 360° / 64 = 5.625°")
    print(f"  Range: 0° to 354.375°")
    print(f"\nMETA positions (65-72): {len(meta)} positions")
    print(f"  Theta: ∞ (infinity)")
    print(f"  Representing transcendent inventions")
    
    # Example 12: Key positions
    print("\n--- Example 12: Key Positions at Major Angles ---")
    key_angles = [0, 45, 90, 180, 270, 315]
    print("Major cardinal and inter-cardinal angles:")
    for angle in key_angles:
        for inv in circle:
            if inv['theta'] == angle:
                status = f"[{inv['status'].upper()}]"
                invention = inv['invention'] if inv['invention'] else "Available"
                print(f"  θ={angle:3d}° - Position {inv['id']:2d}: {inv['angel']:15s} - {invention:30s} {status}")
    
    print("\n" + "="*70)
    print("End of examples")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
