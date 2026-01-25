#!/usr/bin/env python3
"""
🔥 FLAMELANG PIPECALC MODULE - PYTHON REFERENCE IMPLEMENTATION
INV-088: SAGCO OMNI-CALC PIPELINE - Pipefitting Domain Extension

This Python implementation serves as a reference for the FlameLang pipecalc module,
allowing validation of the calculations before the full FlameLang compiler is complete.

Strategickhaos DAO LLC | Domain: Pipefitting Calculations
"""

import math
from dataclasses import dataclass
from typing import Tuple


# ═══════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════

PI = math.pi

# Cosecant lookup table for common angles
COSECANT_45 = 1.414  # 1/sin(45°)
COSECANT_30 = 2.000  # 1/sin(30°)
COSECANT_60 = 1.155  # 1/sin(60°)


# ═══════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Offset:
    """Special offset calculation result"""
    bottom_elbow: float  # Bottom elbow angle in degrees
    top_elbow: float     # Top elbow angle in degrees
    travel: float        # Travel distance


@dataclass
class RollOffset:
    """Rolling offset calculation result"""
    travel: float  # Travel distance along pipe
    run: float     # Horizontal run distance


@dataclass
class Combustion:
    """Combustion equation data"""
    fuel: str
    oxygen_moles: float
    co2_moles: float
    water_moles: float
    energy_kj: float


# ═══════════════════════════════════════════════════════════════════
# CORE CALCULATIONS
# ═══════════════════════════════════════════════════════════════════

def special_offset(rise_deg: float, turn_deg: float) -> Offset:
    """
    Special Offset Calculation
    Formula: cos(degree of rise) × cos(degree of turn) = cos(degree of elbow)
    
    Example from Page 77:
      45° rise, 30° turn → 0.707 × 0.866 = 0.6123 → arccos = 52°14'
    
    Args:
        rise_deg: Rise angle in degrees
        turn_deg: Turn angle in degrees
    
    Returns:
        Offset object with bottom_elbow, top_elbow, and travel
    """
    # Convert degrees to radians
    rise_rad = math.radians(rise_deg)
    turn_rad = math.radians(turn_deg)
    
    # Calculate cosines
    cos_rise = math.cos(rise_rad)
    cos_turn = math.cos(turn_rad)
    
    # Apply special offset formula
    cos_elbow = cos_rise * cos_turn
    
    # Convert back to degrees
    bottom_elbow = math.degrees(math.acos(cos_elbow))
    
    # Top elbow calculation: 90° - bottom_elbow + rise
    top_elbow = 90.0 - bottom_elbow + rise_deg
    
    # Calculate travel
    travel = compute_travel(rise_deg)
    
    return Offset(
        bottom_elbow=bottom_elbow,
        top_elbow=top_elbow,
        travel=travel
    )


def rolling_offset(set_distance: float, angle_deg: float) -> RollOffset:
    """
    Rolling Offset Calculation
    Formulas from Pages 11-12:
      TRAVEL = SET × COSECANT(angle)
      RUN = SET / TANGENT(angle)
    
    For 45°: TRAVEL = SET × 1.414
    For 30°: TRAVEL = SET × 2.000
    
    Args:
        set_distance: SET distance in inches
        angle_deg: Angle in degrees
    
    Returns:
        RollOffset object with travel and run distances
    """
    angle_rad = math.radians(angle_deg)
    
    # TRAVEL = SET × COSECANT(angle) = SET / SIN(angle)
    travel = set_distance / math.sin(angle_rad)
    
    # RUN = SET / TANGENT(angle) = SET / TAN(angle)
    run = set_distance / math.tan(angle_rad)
    
    return RollOffset(travel=travel, run=run)


def bend_length(radius: float, degrees: float) -> float:
    """
    Bend Length Calculation
    Formula: length = radius × (degrees / 180°) × π
    
    Standard multipliers:
      90° bends:  Radius × 1.5708  (π/2)
      180° bends: Radius × 3.1416  (π)
      270° bends: Radius × 4.7123  (3π/2)
      360° bends: Radius × 6.2832  (2π)
    
    Args:
        radius: Bend radius in inches
        degrees: Bend angle in degrees
    
    Returns:
        Length of bend in inches
    """
    return radius * (degrees / 180.0) * PI


def setback_45(radius: float) -> float:
    """
    Setback Calculation for 45° Bends
    Setback is the distance from the center of the bend to the tangent point
    For radius > 5": SETBACK = radius × tan(angle/2)
    
    Args:
        radius: Bend radius in inches
    
    Returns:
        Setback distance in inches
    """
    # For 45° bend: tan(45°/2) = tan(22.5°) ≈ 0.4142
    return radius * math.tan(math.radians(22.5))


def setback(radius: float, angle_deg: float) -> float:
    """
    Setback Calculation for any angle
    
    Args:
        radius: Bend radius in inches
        angle_deg: Bend angle in degrees
    
    Returns:
        Setback distance in inches
    """
    half_angle_rad = math.radians(angle_deg / 2.0)
    return radius * math.tan(half_angle_rad)


def compute_travel(rise_deg: float) -> float:
    """
    Compute travel distance based on rise angle
    
    Args:
        rise_deg: Rise angle in degrees
    
    Returns:
        Travel multiplier
    """
    # Lookup table for common angles
    angle_multipliers = {
        45.0: 1.414,
        30.0: 2.000,
        60.0: 1.155,
    }
    
    # Use lookup table if angle is common
    if rise_deg in angle_multipliers:
        return angle_multipliers[rise_deg]
    
    # General formula for other angles: 1/sin(angle)
    rise_rad = math.radians(rise_deg)
    return 1.0 / math.sin(rise_rad)


def methane_combustion() -> Combustion:
    """
    Methane combustion equation
    CH₄ + 2O₂ → CO₂ + 2H₂O + Energy
    
    Returns:
        Combustion object with equation data
    """
    return Combustion(
        fuel="CH₄",
        oxygen_moles=2.0,
        co2_moles=1.0,
        water_moles=2.0,
        energy_kj=890.0
    )


# ═══════════════════════════════════════════════════════════════════
# DEMO / TEST RUNNER
# ═══════════════════════════════════════════════════════════════════

def run_demo():
    """Run demonstration of all pipecalc functions"""
    
    print("═" * 67)
    print("🔥 FLAMELANG PIPECALC MODULE - PYTHON REFERENCE IMPLEMENTATION")
    print("INV-088: SAGCO OMNI-CALC PIPELINE - Pipefitting Extension")
    print("═" * 67)
    print()
    
    # ───────────────────────────────────────────────────────────────
    # SPECIAL OFFSET CALCULATIONS
    # ───────────────────────────────────────────────────────────────
    
    print("📐 SPECIAL OFFSET CALCULATIONS")
    print("─" * 67)
    
    # Example 1: 45° rise, 30° turn
    offset1 = special_offset(45.0, 30.0)
    print("Example 1: 45° rise × 30° turn")
    print("  cos(45°) × cos(30°) = 0.707 × 0.866 = 0.6123")
    print(f"  Bottom elbow: {offset1.bottom_elbow:.2f}° (Expected: ~52.24°, or 52°14')")
    print(f"  Top elbow: {offset1.top_elbow:.2f}°")
    print(f"  Travel: {offset1.travel:.3f}")
    print()
    
    # Example 2: 45° rise, 60° turn
    offset2 = special_offset(45.0, 60.0)
    print("Example 2: 45° rise × 60° turn")
    print("  cos(45°) × cos(60°) = 0.707 × 0.500 = 0.3535")
    print(f"  Bottom elbow: {offset2.bottom_elbow:.2f}° (Expected: ~69.30°, or 69°18')")
    print(f"  Top elbow: {offset2.top_elbow:.2f}°")
    print(f"  Travel: {offset2.travel:.3f}")
    print()
    
    # ───────────────────────────────────────────────────────────────
    # ROLLING OFFSET CALCULATIONS
    # ───────────────────────────────────────────────────────────────
    
    print("📐 ROLLING OFFSET CALCULATIONS")
    print("─" * 67)
    
    # Example 3: SET = 12", 45° angle
    roll1 = rolling_offset(12.0, 45.0)
    print("Example 3: SET = 12\", Angle = 45°")
    print("  TRAVEL = SET × 1.414")
    print(f"  Travel: {roll1.travel:.3f}\" (Expected: ~16.968\")")
    print(f"  Run: {roll1.run:.3f}\"")
    print()
    
    # Example 4: SET = 12", 30° angle
    roll2 = rolling_offset(12.0, 30.0)
    print("Example 4: SET = 12\", Angle = 30°")
    print("  TRAVEL = SET × 2.000")
    print(f"  Travel: {roll2.travel:.3f}\" (Expected: ~24.000\")")
    print(f"  Run: {roll2.run:.3f}\"")
    print()
    
    # ───────────────────────────────────────────────────────────────
    # BEND LENGTH CALCULATIONS
    # ───────────────────────────────────────────────────────────────
    
    print("📐 BEND LENGTH CALCULATIONS")
    print("─" * 67)
    
    radius = 6.0  # 6" radius
    
    bend_90 = bend_length(radius, 90.0)
    print(f"90° Bend (radius {radius}\"): {bend_90:.4f}\" (Expected: {radius * 1.5708:.4f}\")")
    
    bend_180 = bend_length(radius, 180.0)
    print(f"180° Bend (radius {radius}\"): {bend_180:.4f}\" (Expected: {radius * 3.1416:.4f}\")")
    
    bend_270 = bend_length(radius, 270.0)
    print(f"270° Bend (radius {radius}\"): {bend_270:.4f}\" (Expected: {radius * 4.7123:.4f}\")")
    
    bend_360 = bend_length(radius, 360.0)
    print(f"360° Bend (radius {radius}\"): {bend_360:.4f}\" (Expected: {radius * 6.2832:.4f}\")")
    print()
    
    # ───────────────────────────────────────────────────────────────
    # SETBACK CALCULATIONS
    # ───────────────────────────────────────────────────────────────
    
    print("📐 SETBACK CALCULATIONS")
    print("─" * 67)
    
    setback_6 = setback_45(6.0)
    print(f"45° Bend, 6\" radius: Setback = {setback_6:.4f}\"")
    
    setback_8 = setback(8.0, 90.0)
    print(f"90° Bend, 8\" radius: Setback = {setback_8:.4f}\"")
    print()
    
    # ───────────────────────────────────────────────────────────────
    # COMBUSTION CHEMISTRY
    # ───────────────────────────────────────────────────────────────
    
    print("🔥 METHANE COMBUSTION")
    print("─" * 67)
    
    combustion = methane_combustion()
    print(f"{combustion.fuel} + {combustion.oxygen_moles}O₂ → ", end="")
    print(f"{combustion.co2_moles}CO₂ + {combustion.water_moles}H₂O")
    print(f"Energy Released: {combustion.energy_kj} kJ/mol")
    print()
    
    print("═" * 67)
    print("✅ Neural Sync Complete. Resonance Achieved.")
    print("🔥 SAGCO-HYDRA Pipefitting Module Operational")
    print("═" * 67)


if __name__ == "__main__":
    run_demo()
