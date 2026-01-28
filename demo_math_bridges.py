#!/usr/bin/env python3
"""
Mathematical Bridges Demonstration

This script demonstrates all 10 mathematical bridges in action,
showing how they transform conceptual correlations into testable mathematics.
"""

import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from math_bridges import (
    Quantization,
    GeometricProjection,
    SphericalCoordinates,
    PermutationGroup,
    GraphLaplacian,
    SoundPhysics,
    CodonEncoding,
    HashGeometry,
    TreeCost,
    EnergyMinimization
)


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def demo_quantization():
    """Demonstrate Bridge 1: Discrete ↔ Continuous."""
    print_section("Bridge 1: Discrete ↔ Continuous (Quantization)")
    
    print("\n1. Rubik's sticker to angle:")
    sticker = 27
    angle = Quantization.rubik_sticker_to_angle(sticker)
    print(f"   Sticker {sticker} → {angle:.2f}°")
    
    print("\n2. Angle to 64th-inch bin:")
    angle_rad = np.pi
    bin_idx = Quantization.radians_to_fraction_64(angle_rad)
    print(f"   {angle_rad:.4f} radians → Bin {bin_idx}/64")
    
    print("\n3. MIDI to pitch space:")
    midi_note = 69  # A4
    pitch = Quantization.midi_to_pitch_space(midi_note)
    print(f"   MIDI note {midi_note} (A4) → Pitch {pitch:.4f}")
    
    print("\n✓ Without this bridge, 54 ≠ 64 ≠ 360 is hand-waving.")


def demo_geometric_projection():
    """Demonstrate Bridge 2: Cube Face ↔ Sphere."""
    print_section("Bridge 2: Cube Face ↔ Sphere (Geometric Projection)")
    
    print("\n1. Cube face to sphere projection:")
    x_c, y_c, z_c = 1.0, 0.5, 0.5
    x_s, y_s, z_s = GeometricProjection.cube_to_sphere(x_c, y_c, z_c)
    print(f"   Cube ({x_c}, {y_c}, {z_c}) → Sphere ({x_s:.4f}, {y_s:.4f}, {z_s:.4f})")
    
    print("\n2. Cube to latitude/longitude:")
    lat, lon = GeometricProjection.cube_to_latlong(1.0, 0.5, 0.5)
    print(f"   Cube (1.0, 0.5, 0.5) → Lat {lat:.2f}°, Lon {lon:.2f}°")
    
    print("\n3. Rubik's face sticker to geovector:")
    face, row, col = 0, 1, 1  # Center of front face
    geo_vec = GeometricProjection.rubik_face_to_geovector(face, row, col)
    print(f"   Face {face}, Row {row}, Col {col} → Geovector ({geo_vec[0]:.4f}, {geo_vec[1]:.4f}, {geo_vec[2]:.4f})")
    
    print("\n✓ This legitimizes: Cube faces → lat/long, Stickers → geovectors")


def demo_spherical_coordinates():
    """Demonstrate Bridge 3: Lat/Long ↔ Vector ↔ Angle."""
    print_section("Bridge 3: Lat/Long ↔ Vector ↔ Angle (TRIG6)")
    
    print("\n1. Lat/Long to Cartesian vector:")
    lat, lon = 45.0, -122.0  # Portland, OR
    x, y, z = SphericalCoordinates.latlong_to_vector_degrees(lat, lon)
    print(f"   ({lat}°, {lon}°) → ({x:.4f}, {y:.4f}, {z:.4f})")
    
    print("\n2. Recover azimuth angle:")
    theta = SphericalCoordinates.vector_to_azimuth(x, y)
    print(f"   Vector ({x:.4f}, {y:.4f}) → Azimuth {np.degrees(theta):.2f}°")
    
    print("\n3. Compute TRIG6 (all 6 trig values):")
    trig6 = SphericalCoordinates.trig6_compute((x, y, z))
    print(f"   sin(θ)={trig6[0]:.4f}, cos(θ)={trig6[1]:.4f}, tan(θ)={trig6[2]:.4f}")
    print(f"   sin(φ)={trig6[3]:.4f}, cos(φ)={trig6[4]:.4f}, tan(φ)={trig6[5]:.4f}")
    
    print("\n✓ Now TRIG6 is not symbolic, it's computed.")


def demo_permutation_group():
    """Demonstrate Bridge 4: Rubik's Cube ↔ Group Theory."""
    print_section("Bridge 4: Rubik's Cube ↔ Group Theory (Permutations)")
    
    print("\n1. Create permutation matrix:")
    perm = [1, 2, 0, 3]  # Cyclic permutation
    P = PermutationGroup.create_permutation_matrix(perm)
    print(f"   Permutation {perm}")
    print(f"   Matrix shape: {P.shape}")
    
    print("\n2. Extract angular direction:")
    angle = PermutationGroup.permutation_angle(P)
    print(f"   Permutation direction: {np.degrees(angle):.2f}°")
    
    print("\n3. Algorithm to direction:")
    algorithm = ["R", "U", "R'", "U'"]
    direction = PermutationGroup.algorithm_to_direction(algorithm)
    print(f"   Algorithm {algorithm} → Direction {np.degrees(direction):.2f}°")
    
    print("\n4. OLL case to geometry:")
    oll_case = 23
    x, y = PermutationGroup.oll_case_to_geometry(oll_case)
    print(f"   OLL case {oll_case} → Position ({x:.4f}, {y:.4f})")
    
    print("\n✓ This is how algorithms gain 'direction'.")


def demo_graph_laplacian():
    """Demonstrate Bridge 5: 36 Fallacies ↔ Geometry."""
    print_section("Bridge 5: 36 Fallacies ↔ Geometry (Graph Laplacian)")
    
    print("\n1. Create chess board adjacency (6x6):")
    A = GraphLaplacian.create_chess_board_adjacency()
    print(f"   Chess board adjacency matrix: {A.shape}")
    
    print("\n2. Compute Laplacian:")
    L = GraphLaplacian.compute_laplacian(A)
    print(f"   Laplacian matrix: {L.shape}")
    
    print("\n3. Map fallacy to chess position:")
    fallacy_idx = 15
    row, col = GraphLaplacian.fallacy_to_chess_position(fallacy_idx)
    print(f"   Fallacy {fallacy_idx} → Chess position ({row}, {col})")
    
    print("\n4. Compute fallacy distance:")
    distance = GraphLaplacian.compute_fallacy_distance(5, 12)
    print(f"   Distance between fallacies 5 and 12: {distance:.4f}")
    
    print("\n✓ Now: 36 fallacies → 2D geometry, Chess board mapping is measurable")


def demo_sound_physics():
    """Demonstrate Bridge 6: MIDI ↔ Angle ↔ Frequency."""
    print_section("Bridge 6: MIDI ↔ Angle ↔ Frequency (Sound Physics)")
    
    print("\n1. MIDI to frequency:")
    midi_note = 69  # A4
    freq = SoundPhysics.midi_to_frequency(midi_note)
    print(f"   MIDI {midi_note} (A4) → {freq:.2f} Hz")
    
    print("\n2. Frequency to angular velocity:")
    omega = SoundPhysics.frequency_to_angular_velocity(freq)
    print(f"   {freq:.2f} Hz → {omega:.2f} rad/s")
    
    print("\n3. Circle of fifths angle:")
    step = 5
    angle = SoundPhysics.circle_of_fifths_angle(step)
    print(f"   Step {step} on circle of fifths → {np.degrees(angle):.2f}°")
    
    print("\n4. MIDI chord to geometry:")
    root = 60  # Middle C
    intervals = [0, 4, 7]  # Major triad
    points = SoundPhysics.midi_chord_to_geometry(root, intervals)
    print(f"   Major chord at C → Points on circle:")
    for i, (x, y) in enumerate(points):
        print(f"     Note {i}: ({x:.4f}, {y:.4f})")
    
    print("\n✓ Now: MIDI ↔ radians ↔ oscillation, Circle of fifths ↔ rotation group")


def demo_codon_encoding():
    """Demonstrate Bridge 7: DNA Codons ↔ Base-64."""
    print_section("Bridge 7: DNA Codons ↔ Base-64 (Legitimate Encoding)")
    
    print("\n1. Codon to index:")
    codon = "ATG"
    idx = CodonEncoding.codon_to_index(codon)
    print(f"   Codon '{codon}' → Index {idx}")
    
    print("\n2. Index to codon:")
    idx = 42
    codon = CodonEncoding.index_to_codon(idx)
    print(f"   Index {idx} → Codon '{codon}'")
    
    print("\n3. Codon to 6-bit binary:")
    codon = "ATG"
    binary = CodonEncoding.codon_to_6bit(codon)
    print(f"   Codon '{codon}' → Binary '{binary}'")
    
    print("\n4. Codon to 2D coordinates (8x8 grid):")
    row, col = CodonEncoding.codon_to_coordinates(codon)
    print(f"   Codon '{codon}' → Grid position ({row}, {col})")
    
    print("\n✓ Now: 64 codons ↔ 6-bit space, Matches 64 grid formally")


def demo_hash_geometry():
    """Demonstrate Bridge 8: Hash Collisions ↔ Geometry."""
    print_section("Bridge 8: Hash Collisions ↔ Geometry (Security Link)")
    
    print("\n1. Birthday bound probability:")
    k, N = 100, 1000
    prob = HashGeometry.birthday_bound_probability(k, N)
    print(f"   With {k} samples from {N} bins → Collision prob: {prob:.4f}")
    
    print("\n2. Samples for 50% collision (birthday paradox):")
    N = 365
    k = HashGeometry.samples_for_collision_probability(0.5, N)
    print(f"   Need {k} people for 50% birthday collision (out of {N} days)")
    
    print("\n3. Hash to angular bin:")
    hash_val = 12345
    N = 360
    angle = HashGeometry.hash_to_angular_bin(hash_val, N)
    print(f"   Hash {hash_val} → Angle {np.degrees(angle):.2f}°")
    
    print("\n4. Hash distribution entropy:")
    hashes = [hash(i) for i in range(100)]
    entropy = HashGeometry.hash_distribution_entropy(hashes, N=64)
    print(f"   Entropy of 100 hashes over 64 bins: {entropy:.4f} bits")
    
    print("\n✓ Collision = overlapping arc lengths")


def demo_tree_cost():
    """Demonstrate Bridge 9: Filesystem ↔ Tree ↔ Minimax."""
    print_section("Bridge 9: Filesystem ↔ Tree ↔ Minimax (Decision Trees)")
    
    print("\n1. Path cost:")
    depth = 5
    cost = TreeCost.path_cost(depth)
    print(f"   Depth {depth} → Path cost {cost}")
    
    print("\n2. Total cost (A* formula):")
    total = TreeCost.total_cost(depth=3, current_state=[1, 2], goal_state=[5, 6])
    print(f"   Total cost J(n) = g(n) + h(n) = {total:.4f}")
    
    print("\n3. Filesystem depth:")
    path = "/home/user/documents/file.txt"
    depth = TreeCost.filesystem_depth_cost(path)
    print(f"   Path '{path}' → Depth {depth}")
    
    print("\n4. Angle-based heuristic:")
    h = TreeCost.angle_based_heuristic(current_angle=1.5, goal_angle=0.0)
    print(f"   Angular heuristic: {h:.4f} radians")
    
    print("\n✓ Same formula runs: Chess minimax, Linux trees, Cube solving")


def demo_energy_minimization():
    """Demonstrate Bridge 10: Neural ↔ Weight Collapse."""
    print_section("Bridge 10: Neural ↔ Weight Collapse (Energy Minimization)")
    
    print("\n1. Compute energy:")
    weights = np.array([0.5, 0.3, 0.2])
    inputs = np.array([1.0, 2.0, 3.0])
    E = EnergyMinimization.energy(weights, inputs)
    print(f"   E = w·x = {E:.4f}")
    
    print("\n2. Gradient descent step:")
    grad = EnergyMinimization.gradient_energy(weights, inputs)
    new_weights = EnergyMinimization.gradient_descent_step(weights, grad, learning_rate=0.01)
    print(f"   Weights: {weights} → {new_weights}")
    
    print("\n3. Optimize weights:")
    final_weights, history = EnergyMinimization.optimize_weights(
        initial_weights=weights, inputs=inputs, iterations=10
    )
    print(f"   Initial energy: {history[0]:.4f}")
    print(f"   Final energy: {history[-1]:.4f}")
    print(f"   Convergence: {len(history)} iterations")
    
    print("\n4. Collapse singularity (pruning):")
    original = np.array([0.5, 0.05, 0.3, 0.01, 0.2])
    pruned = EnergyMinimization.collapse_singularity(original, threshold=0.1)
    print(f"   Original:  {original}")
    print(f"   Pruned:    {pruned}")
    
    print("\n✓ This is why: You feel 'collapse', You prune paths, Singularities matter")


def demo_integration():
    """Demonstrate how multiple bridges work together."""
    print_section("INTEGRATION: Multiple Bridges Working Together")
    
    print("\nStarting with angle 180°, flowing through all bridges:")
    
    # 1. Quantize angle to sticker
    angle = 180.0
    sticker = Quantization.angle_to_rubik_sticker(angle)
    print(f"\n1. Angle {angle}° → Rubik's sticker {sticker}")
    
    # 2. Convert to geovector
    face = sticker // 9
    row = (sticker % 9) // 3
    col = (sticker % 9) % 3
    geo_vec = GeometricProjection.rubik_face_to_geovector(face, row, col)
    print(f"2. Sticker {sticker} → Geovector ({geo_vec[0]:.3f}, {geo_vec[1]:.3f}, {geo_vec[2]:.3f})")
    
    # 3. Compute TRIG6
    trig6 = SphericalCoordinates.trig6_compute(geo_vec)
    print(f"3. Geovector → TRIG6 (sin θ={trig6[0]:.3f}, cos θ={trig6[1]:.3f}, ...)")
    
    # 4. Map to codon
    codon_idx = sticker % 64
    codon = CodonEncoding.index_to_codon(codon_idx)
    grid_pos = CodonEncoding.codon_to_coordinates(codon)
    print(f"4. Sticker {sticker} → Codon '{codon}' at grid {grid_pos}")
    
    # 5. Hash collision
    collision_prob = HashGeometry.birthday_bound_probability(k=sticker, N=64)
    print(f"5. With {sticker} samples → Collision probability {collision_prob:.4f}")
    
    # 6. MIDI mapping
    midi_note = sticker % 128
    freq = SoundPhysics.midi_to_frequency(midi_note)
    omega = SoundPhysics.frequency_to_angular_velocity(freq)
    print(f"6. Sticker {sticker} → MIDI {midi_note} → {freq:.1f} Hz → {omega:.1f} rad/s")
    
    print("\n✓ All bridges working together: Discrete → Continuous → Geometric → Encoded → Physical")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("  MATHEMATICAL BRIDGES DEMONSTRATION")
    print("  State Encoding Kernel v0.1")
    print("="*70)
    print("\nThis script demonstrates all 10 mathematical bridges that transform")
    print("conceptual correlations into testable, provable mathematical relationships.")
    
    try:
        demo_quantization()
        demo_geometric_projection()
        demo_spherical_coordinates()
        demo_permutation_group()
        demo_graph_laplacian()
        demo_sound_physics()
        demo_codon_encoding()
        demo_hash_geometry()
        demo_tree_cost()
        demo_energy_minimization()
        demo_integration()
        
        print("\n" + "="*70)
        print("  ✓ ALL BRIDGES DEMONSTRATED SUCCESSFULLY")
        print("="*70)
        print("\nThe system is now:")
        print("  • Testable: Each bridge has formal mathematical basis")
        print("  • Extensible: New bridges can be added to the framework")
        print("  • Grounded: Conceptual correlations are now provable")
        print("\nThe cube is no longer symbolic — it's a state engine.")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
