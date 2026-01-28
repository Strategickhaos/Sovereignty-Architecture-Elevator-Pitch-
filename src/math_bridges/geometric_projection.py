"""
Bridge 2: Cube Face ↔ Sphere (Geometric Projection)

This bridge legitimizes the mapping between cube faces and spherical coordinates,
enabling geospatial interpretations of discrete cube states.

Formula:
    (x_s, y_s, z_s) = (x_c, y_c, z_c) / √(x_c² + y_c² + z_c²)

This legitimizes:
- Cube faces → lat/long
- Stickers → geovectors
- TRIG6 on cube
"""

import numpy as np
from typing import Tuple


class GeometricProjection:
    """Bridges cube face coordinates and spherical geometry."""
    
    @staticmethod
    def cube_to_sphere(x_c: float, y_c: float, z_c: float) -> Tuple[float, float, float]:
        """
        Project a cube face coordinate to a unit sphere.
        
        Args:
            x_c, y_c, z_c: Cube face coordinates (typically in range [-1, 1])
            
        Returns:
            (x_s, y_s, z_s): Spherical unit vector
        """
        magnitude = np.sqrt(x_c**2 + y_c**2 + z_c**2)
        
        if magnitude == 0:
            raise ValueError("Cannot project zero vector to sphere")
        
        x_s = x_c / magnitude
        y_s = y_c / magnitude
        z_s = z_c / magnitude
        
        return (x_s, y_s, z_s)
    
    @staticmethod
    def sphere_to_latlong(x_s: float, y_s: float, z_s: float) -> Tuple[float, float]:
        """
        Convert spherical coordinates to latitude/longitude.
        
        Args:
            x_s, y_s, z_s: Spherical unit vector
            
        Returns:
            (lat, lon): Latitude and longitude in degrees
        """
        # Latitude from z component
        lat = np.degrees(np.arcsin(z_s))
        
        # Longitude from x and y components
        lon = np.degrees(np.arctan2(y_s, x_s))
        
        return (lat, lon)
    
    @staticmethod
    def cube_to_latlong(x_c: float, y_c: float, z_c: float) -> Tuple[float, float]:
        """
        Direct conversion from cube face to lat/long.
        
        Args:
            x_c, y_c, z_c: Cube face coordinates
            
        Returns:
            (lat, lon): Latitude and longitude in degrees
        """
        x_s, y_s, z_s = GeometricProjection.cube_to_sphere(x_c, y_c, z_c)
        return GeometricProjection.sphere_to_latlong(x_s, y_s, z_s)
    
    @staticmethod
    def rubik_face_to_geovector(face: int, row: int, col: int) -> Tuple[float, float, float]:
        """
        Convert Rubik's cube face/sticker position to a geovector.
        
        Args:
            face: Face index (0-5) representing Front, Back, Left, Right, Up, Down
            row: Row on face (0-2)
            col: Column on face (0-2)
            
        Returns:
            (x, y, z): Unit vector on sphere
        """
        # Map sticker position to [-1, 0, 1] coordinates on cube face
        sticker_x = col - 1  # -1, 0, 1
        sticker_y = 1 - row  # 1, 0, -1
        
        # Map face to cube coordinates
        face_coords = [
            (1, sticker_x, sticker_y),   # Front (0)
            (-1, -sticker_x, sticker_y), # Back (1)
            (-sticker_y, -1, sticker_x), # Left (2)
            (sticker_y, 1, sticker_x),   # Right (3)
            (sticker_x, sticker_y, 1),   # Up (4)
            (sticker_x, -sticker_y, -1), # Down (5)
        ]
        
        if face < 0 or face >= 6:
            raise ValueError(f"Face {face} must be in range [0, 5]")
        
        x_c, y_c, z_c = face_coords[face]
        return GeometricProjection.cube_to_sphere(x_c, y_c, z_c)
    
    @staticmethod
    def latlong_to_sphere(lat: float, lon: float) -> Tuple[float, float, float]:
        """
        Convert latitude/longitude to spherical unit vector.
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            (x, y, z): Unit vector on sphere
        """
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)
        
        x = np.cos(lat_rad) * np.cos(lon_rad)
        y = np.cos(lat_rad) * np.sin(lon_rad)
        z = np.sin(lat_rad)
        
        return (x, y, z)
