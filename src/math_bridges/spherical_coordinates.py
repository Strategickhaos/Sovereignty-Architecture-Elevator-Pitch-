"""
Bridge 3: Lat/Long ↔ Vector ↔ Angle (TRIG6 Grounding)

This bridge closes the geolocation → trig loop, making TRIG6 computed rather than symbolic.

Formulas:
    x = cos(φ) * cos(λ)
    y = cos(φ) * sin(λ)
    z = sin(φ)
    
    θ = atan2(y, x)

Now TRIG6 is not symbolic, it's computed.
"""

import numpy as np
from typing import Tuple


class SphericalCoordinates:
    """Bridges geolocation, vectors, and trigonometric angles."""
    
    @staticmethod
    def latlong_to_vector(phi: float, lambda_: float) -> Tuple[float, float, float]:
        """
        Convert spherical coordinates (lat/long) to Cartesian vector.
        
        Args:
            phi: Latitude in radians
            lambda_: Longitude in radians
            
        Returns:
            (x, y, z): Unit vector
        """
        x = np.cos(phi) * np.cos(lambda_)
        y = np.cos(phi) * np.sin(lambda_)
        z = np.sin(phi)
        
        return (x, y, z)
    
    @staticmethod
    def latlong_to_vector_degrees(lat: float, lon: float) -> Tuple[float, float, float]:
        """
        Convert spherical coordinates (lat/long in degrees) to Cartesian vector.
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            (x, y, z): Unit vector
        """
        phi = np.radians(lat)
        lambda_ = np.radians(lon)
        return SphericalCoordinates.latlong_to_vector(phi, lambda_)
    
    @staticmethod
    def vector_to_azimuth(x: float, y: float) -> float:
        """
        Recover azimuth angle from vector components.
        
        Args:
            x: X component of vector
            y: Y component of vector
            
        Returns:
            theta: Azimuth angle in radians
        """
        theta = np.arctan2(y, x)
        return theta
    
    @staticmethod
    def vector_to_elevation(x: float, y: float, z: float) -> float:
        """
        Compute elevation angle from vector.
        
        Args:
            x, y, z: Vector components
            
        Returns:
            elevation: Elevation angle in radians
        """
        r = np.sqrt(x**2 + y**2)
        elevation = np.arctan2(z, r)
        return elevation
    
    @staticmethod
    def vector_to_spherical(x: float, y: float, z: float) -> Tuple[float, float]:
        """
        Convert Cartesian vector to spherical coordinates (phi, lambda).
        
        Args:
            x, y, z: Vector components
            
        Returns:
            (phi, lambda_): Latitude and longitude in radians
        """
        phi = SphericalCoordinates.vector_to_elevation(x, y, z)
        lambda_ = SphericalCoordinates.vector_to_azimuth(x, y)
        
        return (phi, lambda_)
    
    @staticmethod
    def trig6_compute(position: Tuple[float, float, float]) -> Tuple[float, float, float, float, float, float]:
        """
        Compute all 6 trigonometric values from a 3D position.
        
        TRIG6 = (sin(θ), cos(θ), tan(θ), sin(φ), cos(φ), tan(φ))
        
        Args:
            position: (x, y, z) position vector
            
        Returns:
            (sin_theta, cos_theta, tan_theta, sin_phi, cos_phi, tan_phi)
        """
        x, y, z = position
        
        # Azimuth angle θ
        theta = SphericalCoordinates.vector_to_azimuth(x, y)
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        tan_theta = np.tan(theta) if cos_theta != 0 else np.inf
        
        # Elevation angle φ
        phi = SphericalCoordinates.vector_to_elevation(x, y, z)
        sin_phi = np.sin(phi)
        cos_phi = np.cos(phi)
        tan_phi = np.tan(phi) if cos_phi != 0 else np.inf
        
        return (sin_theta, cos_theta, tan_theta, sin_phi, cos_phi, tan_phi)
    
    @staticmethod
    def angle_distance(phi1: float, lambda1: float, phi2: float, lambda2: float) -> float:
        """
        Compute great circle distance between two points on a sphere.
        
        Uses the Haversine formula.
        
        Args:
            phi1, lambda1: First point (lat, lon) in radians
            phi2, lambda2: Second point (lat, lon) in radians
            
        Returns:
            Angular distance in radians
        """
        dphi = phi2 - phi1
        dlambda = lambda2 - lambda1
        
        a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return c
