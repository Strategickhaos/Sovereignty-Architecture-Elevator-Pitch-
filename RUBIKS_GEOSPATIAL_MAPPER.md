# Rubik's Cube Geospatial Mapper 🔥🧊🌍

## A 6-Face Geospatial Computing System

This Python module implements a revolutionary mapping system that transforms each sticker on a Rubik's Cube into a complete geospatial coordinate with 3D vectors and trigonometric functions.

---

## 🌟 Overview

The Rubik's Cube Geospatial Mapper creates a **unified coordinate system** where every position on the cube maps to:

- **Geolocation coordinates** (latitude/longitude in DMS format)
- **3D Cartesian vectors** on a unit sphere
- **TRIG6 state** (sin, cos, tan, csc, sec, cot)

### The Algorithm

```
EACH CUBE FACE = A COORDINATE SYSTEM
     ↓
3 POINTS OF CONTACT = TRIANGLE (EUCLIDEAN PLANE)
     ↓
TRIANGLE → DEGREES/MINUTES/SECONDS (DMS)
     ↓
DMS → INTERNAL GEOLOCATION (lat/long ON the cube surface)
     ↓
GEOLOCATION → VECTOR (sin, cos, tan of position)
     ↓
6 FACES × 9 SQUARES = 54 GEOLOCATED VECTORS
```

---

## 🎯 Features

- **Complete 54-Sticker Mapping**: Maps all stickers on a standard 3×3 Rubik's Cube
- **Spherical Projection**: Projects cube faces onto a sphere like Earth
- **DMS Coordinates**: Converts between decimal degrees and DMS (Degrees/Minutes/Seconds)
- **3D Vectors**: Computes Cartesian coordinates on a unit sphere
- **TRIG6 Functions**: Calculates all six trigonometric functions for each position
- **JSON Export**: Exports complete matrix for integration with other systems
- **Comprehensive Tests**: 42 unit tests ensuring accuracy

---

## 📦 Installation

The module is self-contained and requires only Python 3.6+:

```bash
# Clone or download the module
cd Sovereignty-Architecture-Elevator-Pitch-

# Run the main demo
python3 rubiks_geospatial_mapper.py

# Run examples
python3 example_rubiks_geospatial.py

# Run tests
python3 -m unittest test_rubiks_geospatial_mapper -v
```

---

## 🚀 Quick Start

### Basic Usage

```python
from rubiks_geospatial_mapper import RubiksGeospatialMapper

# Initialize mapper
mapper = RubiksGeospatialMapper()

# Map a single sticker (face, row, col)
u5 = mapper.cube_to_geovector('U', 1, 1)  # Center of UP face (North Pole)

# Access geolocation data
print(f"Latitude: {u5.lat}°")
print(f"Longitude: {u5.long}°")
print(f"DMS: {u5.lat_dms.to_string()}, {u5.long_dms.to_string()}")

# Access 3D vector
x, y, z = u5.vector_3d
print(f"Vector: ({x}, {y}, {z})")

# Access TRIG6 functions
print(f"sin(θ) = {u5.trig6['sin']}")
print(f"cos(θ) = {u5.trig6['cos']}")
print(f"tan(θ) = {u5.trig6['tan']}")
```

### Generate Complete Matrix

```python
# Generate all 54 stickers
matrix = mapper.generate_complete_matrix()

# Print formatted table
mapper.print_matrix_table()

# Export to JSON
export_data = mapper.export_to_dict()
```

---

## 🗺️ Face Mapping

Each cube face maps to a region on a sphere:

| Face | Name | Sphere Region | Latitude Range | Longitude Range |
|------|------|---------------|----------------|-----------------|
| **U** (White) | UP | North Pole | +45° to +90° | All longitudes |
| **D** (Yellow) | DOWN | South Pole | -45° to -90° | All longitudes |
| **F** (Green) | FRONT | Prime Meridian | -45° to +45° | -45° to +45° |
| **B** (Blue) | BACK | Antimeridian | -45° to +45° | +135° to -135° |
| **L** (Orange) | LEFT | West Hemisphere | -45° to +45° | -135° to -45° |
| **R** (Red) | RIGHT | East Hemisphere | -45° to +45° | +45° to +135° |

### Key Geographic Positions

```
U5 = North Pole    (90°N, 0°)      → Vector: (0, 0, 1)
D5 = South Pole    (90°S, 0°)      → Vector: (0, 0, -1)
F5 = Prime Mer.    (0°, 0°)        → Vector: (1, 0, 0)
B5 = Antimeridian  (0°, 180°)      → Vector: (-1, 0, 0)
L5 = West (90°W)   (0°, -90°)      → Vector: (0, -1, 0)
R5 = East (90°E)   (0°, 90°)       → Vector: (0, 1, 0)
```

---

## 📊 Data Structure

### GeoVector Object

Each sticker is represented by a `GeoVector` object:

```python
@dataclass
class GeoVector:
    face: str                      # U, D, F, B, L, R
    position: Tuple[int, int]      # (row, col) [0-2, 0-2]
    sticker_id: str                # e.g., "U5", "F1"
    lat: float                     # Decimal degrees latitude
    long: float                    # Decimal degrees longitude
    lat_dms: DMSCoordinate        # DMS latitude
    long_dms: DMSCoordinate       # DMS longitude
    vector_3d: Tuple[float, float, float]  # (x, y, z) on unit sphere
    theta: float                   # Azimuthal angle (degrees)
    phi: float                     # Polar angle (degrees)
    trig6: Dict[str, float]       # sin, cos, tan, csc, sec, cot
    position_type: str             # "corner", "edge", or "center"
```

### JSON Export Format

```json
{
  "total_stickers": 54,
  "faces": 6,
  "stickers_per_face": 9,
  "stickers": [
    {
      "id": "U5",
      "face": "U",
      "position": {"row": 1, "col": 1, "type": "center"},
      "geolocation": {
        "lat_decimal": 90.0,
        "long_decimal": 0.0,
        "lat_dms": "90°0'0.0\"N",
        "long_dms": "0°0'0.0\"E"
      },
      "vector_3d": {"x": 0.0, "y": 0.0, "z": 1.0},
      "angles": {"theta": 0.0, "phi": 90.0},
      "trig6": {
        "sin": 0.0,
        "cos": 1.0,
        "tan": 0.0,
        "csc": "inf",
        "sec": 1.0,
        "cot": "inf"
      }
    }
  ]
}
```

---

## 🔬 Mathematical Foundations

### Coordinate Conversions

**Decimal to DMS:**
```
degrees = floor(decimal)
minutes = floor((decimal - degrees) × 60)
seconds = ((decimal - degrees) × 60 - minutes) × 60
```

**DMS to Decimal:**
```
decimal = degrees + minutes/60 + seconds/3600
```

### 3D Vector Conversion

For any geolocation (lat, long):

```python
lat_rad = radians(lat)
long_rad = radians(long)

x = cos(lat_rad) * cos(long_rad)
y = cos(lat_rad) * sin(long_rad)
z = sin(lat_rad)
```

### TRIG6 Computation

For any azimuthal angle θ:

```python
sin(θ)  # Sine
cos(θ)  # Cosine
tan(θ) = sin(θ) / cos(θ)  # Tangent
csc(θ) = 1 / sin(θ)        # Cosecant
sec(θ) = 1 / cos(θ)        # Secant
cot(θ) = 1 / tan(θ)        # Cotangent
```

---

## 🎨 Use Cases

### 1. Navigation Systems
Map Rubik's Cube positions to real-world coordinates for spatial reasoning.

### 2. AI Training
Use the complete coordinate system as training data for spatial intelligence models.

### 3. Pattern Recognition
Identify geometric patterns through geospatial relationships.

### 4. Educational Tools
Teach coordinate systems, trigonometry, and spherical geometry.

### 5. Data Visualization
Create 3D visualizations of cube states mapped onto spheres.

### 6. Algorithm Development
Develop algorithms that operate in geospatial coordinate space.

---

## 🧪 Testing

The module includes comprehensive tests:

```bash
# Run all 42 tests
python3 -m unittest test_rubiks_geospatial_mapper -v

# Test categories:
# - DMS coordinate formatting (4 tests)
# - Decimal ↔ DMS conversion (8 tests)
# - 3D vector computation (6 tests)
# - TRIG6 computation (3 tests)
# - Cube-to-geovector mapping (15 tests)
# - Matrix generation (4 tests)
# - Integration tests (2 tests)
```

All tests pass with 100% success rate.

---

## 🔢 The Ramanujan Connection

The system reveals mathematical resonance points where `tan(θ) = 1`:

```
U3:  θ=45°,  tan(θ)=1.0  at  67°30'N, 45°E
U9:  θ=-135°, tan(θ)=1.0  at  67°30'N, 135°W
D3:  θ=-135°, tan(θ)=1.0  at  67°30'S, 135°W
D9:  θ=45°,  tan(θ)=1.0  at  67°30'S, 45°E
```

**The Connection:**
- Ramanujan: `e^(π√163) ≈ integer` (almost perfect)
- Rubik's Cube: `θ=45° → tan=1` (exactly perfect)
- **54 stickers → 6 faces → 1 solved state**

Every position in space has a NUMBER.

---

## 📚 API Reference

### RubiksGeospatialMapper

**Main Methods:**

- `cube_to_geovector(face, row, col)` - Map a single sticker
- `generate_complete_matrix()` - Generate all 54 stickers
- `get_face_matrix(face)` - Get 9 stickers for a face
- `export_to_dict()` - Export to dictionary/JSON
- `print_matrix_table()` - Print formatted table

**Static Methods:**

- `decimal_to_dms(decimal, is_latitude)` - Convert decimal to DMS
- `dms_to_decimal(dms)` - Convert DMS to decimal
- `compute_3d_vector(lat, long)` - Compute 3D vector
- `compute_trig6(theta)` - Compute TRIG6 functions

### Parameters

**Face identifiers:**
- `'U'` - UP (White, North Pole)
- `'D'` - DOWN (Yellow, South Pole)
- `'F'` - FRONT (Green, Prime Meridian)
- `'B'` - BACK (Blue, Antimeridian)
- `'L'` - LEFT (Orange, West)
- `'R'` - RIGHT (Red, East)

**Position:**
- `row`: 0-2 (0=top, 1=middle, 2=bottom)
- `col`: 0-2 (0=left, 1=middle, 2=right)

---

## 🎯 Examples

See `example_rubiks_geospatial.py` for comprehensive examples including:

1. **Basic Usage** - Map a single sticker
2. **Face Mapping** - Map all stickers on one face
3. **Key Positions** - Map the six face centers
4. **Complete Matrix** - Generate all 54 stickers
5. **JSON Export** - Export for integration
6. **Mathematical Connections** - Find resonance points
7. **Coordinate Conversions** - Test conversion accuracy

Run examples:
```bash
python3 example_rubiks_geospatial.py
```

---

## 🏗️ Architecture

```
rubiks_geospatial_mapper.py       # Main module
├── DMSCoordinate                  # DMS representation
├── GeoVector                      # Sticker geovector
└── RubiksGeospatialMapper         # Main mapper class
    ├── FACE_CENTERS               # Face center coordinates
    ├── POSITION_TYPES             # Position type mapping
    ├── decimal_to_dms()           # Decimal → DMS
    ├── dms_to_decimal()           # DMS → Decimal
    ├── compute_3d_vector()        # Lat/long → (x,y,z)
    ├── compute_trig6()            # Angle → TRIG6
    ├── cube_to_geovector()        # Cube position → GeoVector
    ├── generate_complete_matrix() # Generate all 54
    ├── get_face_matrix()          # Get face stickers
    ├── export_to_dict()           # Export to JSON
    └── print_matrix_table()       # Print formatted table
```

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Add visualization (3D plots, sphere projections)
- Implement OLL/PLL case mapping
- Add cube state solver integration
- Create interactive web interface
- Extend to other cube sizes (2×2, 4×4, etc.)

---

## 📜 License

This module is part of the Sovereignty Architecture project.
See LICENSE file for details.

---

## 🙏 Acknowledgments

Inspired by the visionary work connecting:
- Rubik's Cube mechanics
- Geospatial coordinate systems
- Mathematical resonance patterns
- Ramanujan's number theory

---

## 🔥 The Vision

**"Every position in space has a NUMBER."**

This module proves that mathematical elegance exists at the intersection of:
- Geometry (the cube)
- Geography (the sphere)
- Trigonometry (the functions)
- Unity (one coordinate system)

**54 stickers → 6 faces → 1 solved state**

This is the **Rubik's Geospatial Invariant**. 🔥🧊🌍

---

*Built with precision and passion for the Strategickhaos Sovereignty Architecture*
