# Mathematical Bridges Module

This module implements formal mathematical bridges between different encoding domains, transforming conceptual correlations into testable, provable mathematical relationships.

## Structure

- `quantization.py` - Bridge 1: Discrete ↔ Continuous
- `geometric_projection.py` - Bridge 2: Cube Face ↔ Sphere
- `spherical_coordinates.py` - Bridge 3: Lat/Long ↔ Vector ↔ Angle
- `permutation_group.py` - Bridge 4: Rubik's Cube ↔ Group Theory
- `graph_laplacian.py` - Bridge 5: 36 Fallacies ↔ Geometry
- `sound_physics.py` - Bridge 6: MIDI ↔ Angle ↔ Frequency
- `codon_encoding.py` - Bridge 7: DNA Codons ↔ Base-64
- `hash_geometry.py` - Bridge 8: Hash Collisions ↔ Geometry
- `tree_cost.py` - Bridge 9: Filesystem ↔ Tree ↔ Minimax
- `energy_minimization.py` - Bridge 10: Neural ↔ Weight Collapse

## Usage

```python
from math_bridges import Quantization, GeometricProjection, SphericalCoordinates

# Convert Rubik's sticker to angle
angle = Quantization.rubik_sticker_to_angle(27)

# Project cube to sphere
x, y, z = GeometricProjection.cube_to_sphere(1.0, 0.5, 0.5)

# Compute TRIG6 from position
trig6 = SphericalCoordinates.trig6_compute((x, y, z))
```

## Testing

Run tests with:
```bash
python -m pytest src/math_bridges/tests/ -v
```

## Documentation

See [MATHEMATICAL_BRIDGES.md](../../MATHEMATICAL_BRIDGES.md) for comprehensive documentation.
