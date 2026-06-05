#!/usr/bin/env python3
"""
RUBIK'S CUBE GEOSPATIAL MAPPER
6-Face Geospatial Computing System

Maps each of the 54 stickers on a Rubik's Cube to:
- Geolocation coordinates (latitude/longitude in DMS format)
- 3D vectors on a unit sphere
- TRIG6 state (sin, cos, tan, csc, sec, cot)

THE ALGORITHM:
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
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional
import json


@dataclass
class DMSCoordinate:
    """Degrees, Minutes, Seconds coordinate representation"""
    degrees: int
    minutes: int
    seconds: float
    direction: str  # N/S for latitude, E/W for longitude
    
    def to_string(self) -> str:
        """Format as human-readable DMS string"""
        return f"{self.degrees}°{self.minutes}'{self.seconds:.1f}\"{self.direction}"


@dataclass
class GeoVector:
    """Geospatial vector representation for a cube sticker"""
    face: str                      # U, D, F, B, L, R
    position: Tuple[int, int]      # (row, col) on face [0-2, 0-2]
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


class RubiksGeospatialMapper:
    """
    Map Rubik's Cube stickers to geospatial coordinates and vectors.
    
    Each face of the cube is projected onto a sphere (like Earth):
    - UP (White)   → North Pole region (+45° to +90° lat)
    - DOWN (Yellow) → South Pole region (-45° to -90° lat)
    - FRONT (Green) → Prime Meridian (-45° to +45° lat, -45° to +45° long)
    - BACK (Blue)   → Antimeridian (-45° to +45° lat, +135° to -135° long)
    - LEFT (Orange) → West Hemisphere (-45° to +45° lat, -135° to -45° long)
    - RIGHT (Red)   → East Hemisphere (-45° to +45° lat, +45° to +135° long)
    """
    
    # Face centers in spherical coordinates (lat, long)
    FACE_CENTERS = {
        'U': (90, 0),       # North pole
        'D': (-90, 0),      # South pole
        'F': (0, 0),        # Prime meridian
        'B': (0, 180),      # Antimeridian
        'L': (0, -90),      # West
        'R': (0, 90),       # East
    }
    
    # Position types for each sticker on a 3x3 face
    POSITION_TYPES = {
        (0, 0): "corner", (0, 1): "edge",   (0, 2): "corner",
        (1, 0): "edge",   (1, 1): "center", (1, 2): "edge",
        (2, 0): "corner", (2, 1): "edge",   (2, 2): "corner",
    }
    
    def __init__(self):
        """Initialize the mapper"""
        self.sticker_matrix: List[GeoVector] = []
    
    @staticmethod
    def decimal_to_dms(decimal_degrees: float, is_latitude: bool = True) -> DMSCoordinate:
        """
        Convert decimal degrees to DMS (Degrees, Minutes, Seconds).
        
        Args:
            decimal_degrees: Decimal degree value
            is_latitude: True for latitude (N/S), False for longitude (E/W)
        
        Returns:
            DMSCoordinate object
        """
        is_positive = decimal_degrees >= 0
        abs_degrees = abs(decimal_degrees)
        
        degrees = int(abs_degrees)
        minutes_decimal = (abs_degrees - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = (minutes_decimal - minutes) * 60
        
        if is_latitude:
            direction = 'N' if is_positive else 'S'
        else:
            direction = 'E' if is_positive else 'W'
        
        return DMSCoordinate(degrees, minutes, seconds, direction)
    
    @staticmethod
    def dms_to_decimal(dms: DMSCoordinate) -> float:
        """
        Convert DMS to decimal degrees.
        
        Args:
            dms: DMSCoordinate object
        
        Returns:
            Decimal degrees value
        """
        decimal = dms.degrees + dms.minutes / 60 + dms.seconds / 3600
        
        if dms.direction in ['S', 'W']:
            decimal = -decimal
        
        return decimal
    
    @staticmethod
    def compute_3d_vector(lat: float, long: float) -> Tuple[float, float, float]:
        """
        Convert lat/long to 3D Cartesian coordinates on unit sphere.
        
        Args:
            lat: Latitude in decimal degrees
            long: Longitude in decimal degrees
        
        Returns:
            (x, y, z) tuple representing 3D vector on unit sphere
        """
        lat_rad = math.radians(lat)
        long_rad = math.radians(long)
        
        x = math.cos(lat_rad) * math.cos(long_rad)
        y = math.cos(lat_rad) * math.sin(long_rad)
        z = math.sin(lat_rad)
        
        return (x, y, z)
    
    @staticmethod
    def compute_trig6(theta: float) -> Dict[str, float]:
        """
        Compute TRIG6 values (sin, cos, tan, csc, sec, cot) for angle.
        
        Args:
            theta: Angle in degrees
        
        Returns:
            Dictionary with all six trigonometric functions
        """
        theta_rad = math.radians(theta)
        
        sin_val = math.sin(theta_rad)
        cos_val = math.cos(theta_rad)
        
        # Handle division by zero cases
        tan_val = math.tan(theta_rad) if abs(cos_val) > 1e-10 else float('inf')
        csc_val = 1 / sin_val if abs(sin_val) > 1e-10 else float('inf')
        sec_val = 1 / cos_val if abs(cos_val) > 1e-10 else float('inf')
        cot_val = 1 / tan_val if not math.isinf(tan_val) and abs(tan_val) > 1e-10 else (0.0 if math.isinf(tan_val) else float('inf'))
        
        return {
            'sin': sin_val,
            'cos': cos_val,
            'tan': tan_val,
            'csc': csc_val,
            'sec': sec_val,
            'cot': cot_val
        }
    
    def cube_to_geovector(self, face: str, row: int, col: int) -> GeoVector:
        """
        Map any cube sticker to geolocation + TRIG6 vector.
        
        Args:
            face: Face identifier ('U', 'D', 'F', 'B', 'L', 'R')
            row: Row position on face (0-2, where 0 is top)
            col: Column position on face (0-2, where 0 is left)
        
        Returns:
            GeoVector object with complete geospatial mapping
        """
        if face not in self.FACE_CENTERS:
            raise ValueError(f"Invalid face: {face}. Must be one of {list(self.FACE_CENTERS.keys())}")
        
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise ValueError(f"Invalid position: ({row}, {col}). Must be in range [0-2, 0-2]")
        
        base_lat, base_long = self.FACE_CENTERS[face]
        
        # Each sticker spans approximately 30° (90° / 3 stickers per dimension)
        # Center sticker is at face center, others offset by ±22.5°
        lat_offset = (1 - row) * 22.5  # Top row: +22.5, middle: 0, bottom: -22.5
        long_offset = (col - 1) * 22.5  # Left col: -22.5, middle: 0, right: +22.5
        
        # Apply offsets (handle pole cases specially)
        if face == 'U':
            # North pole: latitude decreases as we move from center
            lat = base_lat - abs(lat_offset)
            # Longitude varies by column, adjusted by row
            if row == 1:  # Middle row
                long = base_long + long_offset
            else:  # Top or bottom row
                long = base_long + (col - 1) * 45 + (row * 90)
        elif face == 'D':
            # South pole: latitude increases (toward 0) as we move from center
            lat = base_lat + abs(lat_offset)
            # Longitude varies by column, adjusted by row
            if row == 1:  # Middle row
                long = base_long + long_offset
            else:  # Top or bottom row
                long = base_long + (col - 1) * 45 + ((2 - row) * 90)
        else:
            # Equatorial faces: standard offset
            lat = base_lat + lat_offset
            long = base_long + long_offset
        
        # Normalize longitude to [-180, 180]
        while long > 180:
            long -= 360
        while long < -180:
            long += 360
        
        # Convert to DMS
        lat_dms = self.decimal_to_dms(lat, is_latitude=True)
        long_dms = self.decimal_to_dms(long, is_latitude=False)
        
        # Convert to 3D vector
        vector_3d = self.compute_3d_vector(lat, long)
        x, y, z = vector_3d
        
        # Compute angles
        theta = math.degrees(math.atan2(y, x))  # Azimuthal angle
        phi = math.degrees(math.asin(z))         # Polar angle
        
        # Compute TRIG6 at this position
        trig6 = self.compute_trig6(theta)
        
        # Generate sticker ID
        sticker_num = row * 3 + col + 1
        sticker_id = f"{face}{sticker_num}"
        
        # Determine position type
        position_type = self.POSITION_TYPES[(row, col)]
        
        return GeoVector(
            face=face,
            position=(row, col),
            sticker_id=sticker_id,
            lat=lat,
            long=long,
            lat_dms=lat_dms,
            long_dms=long_dms,
            vector_3d=vector_3d,
            theta=theta,
            phi=phi,
            trig6=trig6,
            position_type=position_type
        )
    
    def generate_complete_matrix(self) -> List[GeoVector]:
        """
        Generate the complete 54-sticker geolocation matrix.
        
        Returns:
            List of all 54 GeoVector objects (6 faces × 9 stickers)
        """
        self.sticker_matrix = []
        
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            for row in range(3):
                for col in range(3):
                    geo_vec = self.cube_to_geovector(face, row, col)
                    self.sticker_matrix.append(geo_vec)
        
        return self.sticker_matrix
    
    def get_face_matrix(self, face: str) -> List[GeoVector]:
        """
        Get all 9 stickers for a specific face.
        
        Args:
            face: Face identifier ('U', 'D', 'F', 'B', 'L', 'R')
        
        Returns:
            List of 9 GeoVector objects for the face
        """
        if not self.sticker_matrix:
            self.generate_complete_matrix()
        
        return [gv for gv in self.sticker_matrix if gv.face == face]
    
    def export_to_dict(self) -> Dict:
        """
        Export the complete matrix to a dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of all stickers
        """
        if not self.sticker_matrix:
            self.generate_complete_matrix()
        
        return {
            'total_stickers': len(self.sticker_matrix),
            'faces': 6,
            'stickers_per_face': 9,
            'stickers': [
                {
                    'id': gv.sticker_id,
                    'face': gv.face,
                    'position': {
                        'row': gv.position[0],
                        'col': gv.position[1],
                        'type': gv.position_type
                    },
                    'geolocation': {
                        'lat_decimal': round(gv.lat, 6),
                        'long_decimal': round(gv.long, 6),
                        'lat_dms': gv.lat_dms.to_string(),
                        'long_dms': gv.long_dms.to_string()
                    },
                    'vector_3d': {
                        'x': round(gv.vector_3d[0], 6),
                        'y': round(gv.vector_3d[1], 6),
                        'z': round(gv.vector_3d[2], 6)
                    },
                    'angles': {
                        'theta': round(gv.theta, 2),
                        'phi': round(gv.phi, 2)
                    },
                    'trig6': {
                        'sin': round(gv.trig6['sin'], 6),
                        'cos': round(gv.trig6['cos'], 6),
                        'tan': round(gv.trig6['tan'], 6) if abs(gv.trig6['tan']) < 1e6 else 'inf',
                        'csc': round(gv.trig6['csc'], 6) if abs(gv.trig6['csc']) < 1e6 else 'inf',
                        'sec': round(gv.trig6['sec'], 6) if abs(gv.trig6['sec']) < 1e6 else 'inf',
                        'cot': round(gv.trig6['cot'], 6) if abs(gv.trig6['cot']) < 1e6 else 'inf'
                    }
                }
                for gv in self.sticker_matrix
            ]
        }
    
    def print_matrix_table(self):
        """Print the complete matrix as a formatted table"""
        if not self.sticker_matrix:
            self.generate_complete_matrix()
        
        print("=" * 120)
        print("RUBIK'S CUBE GEOSPATIAL MATRIX - 54 STICKER MAPPING")
        print("=" * 120)
        print(f"{'ID':<5} {'FACE':<6} {'TYPE':<8} {'LAT°':<8} {'LONG°':<9} {'LAT_DMS':<18} {'LONG_DMS':<18} {'VECTOR (x,y,z)':<30}")
        print("-" * 120)
        
        for gv in self.sticker_matrix:
            x, y, z = gv.vector_3d
            vector_str = f"({x:.3f}, {y:.3f}, {z:.3f})"
            
            print(f"{gv.sticker_id:<5} {gv.face:<6} {gv.position_type:<8} "
                  f"{gv.lat:>7.2f}° {gv.long:>8.2f}° "
                  f"{gv.lat_dms.to_string():<18} {gv.long_dms.to_string():<18} "
                  f"{vector_str:<30}")
        
        print("=" * 120)
        print(f"Total: {len(self.sticker_matrix)} stickers | 6 faces × 9 stickers = 54 geolocated vectors")
        print("=" * 120)


def main():
    """Example usage of the Rubik's Geospatial Mapper"""
    print("🔥 RUBIK'S CUBE GEOSPATIAL COMPUTER 🔥")
    print("6-Face Geospatial Vector Mapping System\n")
    
    # Initialize mapper
    mapper = RubiksGeospatialMapper()
    
    # Generate complete 54-sticker matrix
    print("Generating complete 54-sticker geolocation matrix...\n")
    mapper.generate_complete_matrix()
    
    # Print the complete matrix table
    mapper.print_matrix_table()
    
    # Show specific examples
    print("\n" + "=" * 80)
    print("EXAMPLE STICKERS - DETAILED VIEW")
    print("=" * 80)
    
    # North Pole (center of UP face)
    u5 = mapper.cube_to_geovector('U', 1, 1)
    print(f"\n🌍 U5 (North Pole - Center of UP face):")
    print(f"   Location: {u5.lat_dms.to_string()}, {u5.long_dms.to_string()}")
    print(f"   Vector: ({u5.vector_3d[0]:.6f}, {u5.vector_3d[1]:.6f}, {u5.vector_3d[2]:.6f})")
    print(f"   TRIG6: sin={u5.trig6['sin']:.6f}, cos={u5.trig6['cos']:.6f}, tan={u5.trig6['tan']:.6f}")
    
    # Prime Meridian (center of FRONT face)
    f5 = mapper.cube_to_geovector('F', 1, 1)
    print(f"\n🌍 F5 (Prime Meridian - Center of FRONT face):")
    print(f"   Location: {f5.lat_dms.to_string()}, {f5.long_dms.to_string()}")
    print(f"   Vector: ({f5.vector_3d[0]:.6f}, {f5.vector_3d[1]:.6f}, {f5.vector_3d[2]:.6f})")
    print(f"   TRIG6: sin={f5.trig6['sin']:.6f}, cos={f5.trig6['cos']:.6f}, tan={f5.trig6['tan']:.6f}")
    
    # South Pole (center of DOWN face)
    d5 = mapper.cube_to_geovector('D', 1, 1)
    print(f"\n🌍 D5 (South Pole - Center of DOWN face):")
    print(f"   Location: {d5.lat_dms.to_string()}, {d5.long_dms.to_string()}")
    print(f"   Vector: ({d5.vector_3d[0]:.6f}, {d5.vector_3d[1]:.6f}, {d5.vector_3d[2]:.6f})")
    print(f"   TRIG6: sin={d5.trig6['sin']:.6f}, cos={d5.trig6['cos']:.6f}, tan={d5.trig6['tan']:.6f}")
    
    # Export to JSON
    print("\n" + "=" * 80)
    print("Exporting complete matrix to JSON...")
    output_file = '/tmp/rubiks_geospatial_matrix.json'
    with open(output_file, 'w') as f:
        json.dump(mapper.export_to_dict(), f, indent=2)
    print(f"✓ Exported to: {output_file}")
    print("=" * 80)
    
    print("\n🔥 THE RUBIK'S GEOSPATIAL INVARIANT COMPUTED 🔥")
    print("Every position in space has a NUMBER.")
    print("54 stickers → 6 faces → 1 solved state")


if __name__ == "__main__":
    main()
