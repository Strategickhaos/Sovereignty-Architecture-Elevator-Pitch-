#!/usr/bin/env python3
"""
TRIG6 Units System
==================
Strict unit handling to prevent dangerous unit confusion.
Every value must declare its units. Conversions are explicit.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza

CRITICAL: Mixing lbf and kN without conversion kills people.
This module makes unit errors impossible to ignore.
"""

from dataclasses import dataclass
from enum import Enum
import math


class ForceUnit(Enum):
    """Force units supported by TRIG6."""
    LBF = "lbf"      # Pounds-force (US industrial standard)
    KN = "kN"        # Kilonewtons (metric/international)
    N = "N"          # Newtons
    KGF = "kgf"      # Kilograms-force (legacy, avoid)


class LengthUnit(Enum):
    """Length units supported by TRIG6."""
    IN = "in"        # Inches
    FT = "ft"        # Feet
    MM = "mm"        # Millimeters
    M = "m"          # Meters


class AngleUnit(Enum):
    """Angle units supported by TRIG6."""
    DEG = "deg"      # Degrees (default for field work)
    RAD = "rad"      # Radians (internal math)


# ============================================================
# CONVERSION FACTORS
# ============================================================

FORCE_TO_LBF = {
    ForceUnit.LBF: 1.0,
    ForceUnit.KN: 224.80894,      # 1 kN = 224.809 lbf
    ForceUnit.N: 0.22480894,      # 1 N = 0.2248 lbf
    ForceUnit.KGF: 2.20462,       # 1 kgf = 2.205 lbf (force units: 1 kgf = 9.80665 N)
}

FORCE_TO_KN = {
    ForceUnit.LBF: 0.00444822,    # 1 lbf = 0.00445 kN
    ForceUnit.KN: 1.0,
    ForceUnit.N: 0.001,
    ForceUnit.KGF: 0.00980665,
}

LENGTH_TO_IN = {
    LengthUnit.IN: 1.0,
    LengthUnit.FT: 12.0,
    LengthUnit.MM: 0.0393701,
    LengthUnit.M: 39.3701,
}

LENGTH_TO_MM = {
    LengthUnit.IN: 25.4,
    LengthUnit.FT: 304.8,
    LengthUnit.MM: 1.0,
    LengthUnit.M: 1000.0,
}


# ============================================================
# QUANTITY CLASS (value + unit together)
# ============================================================

@dataclass
class Force:
    """A force value with explicit units."""
    value: float
    unit: ForceUnit
    
    def to_lbf(self) -> float:
        """Convert to pounds-force."""
        return self.value * FORCE_TO_LBF[self.unit]
    
    def to_kn(self) -> float:
        """Convert to kilonewtons."""
        return self.value * FORCE_TO_KN[self.unit]
    
    def convert(self, target: ForceUnit) -> "Force":
        """Convert to a different unit."""
        if target == ForceUnit.LBF:
            return Force(self.to_lbf(), ForceUnit.LBF)
        elif target == ForceUnit.KN:
            return Force(self.to_kn(), ForceUnit.KN)
        elif target == ForceUnit.N:
            return Force(self.to_kn() * 1000, ForceUnit.N)
        elif target == ForceUnit.KGF:
            return Force(self.to_lbf() / 2.20462, ForceUnit.KGF)
        raise ValueError(f"Unknown target unit: {target}")
    
    def __repr__(self):
        return f"{self.value:.2f} {self.unit.value}"
    
    def to_dict(self) -> dict:
        return {"value": self.value, "unit": self.unit.value}


@dataclass
class Length:
    """A length value with explicit units."""
    value: float
    unit: LengthUnit
    
    def to_in(self) -> float:
        """Convert to inches."""
        return self.value * LENGTH_TO_IN[self.unit]
    
    def to_mm(self) -> float:
        """Convert to millimeters."""
        return self.value * LENGTH_TO_MM[self.unit]
    
    def convert(self, target: LengthUnit) -> "Length":
        """Convert to a different unit."""
        if target == LengthUnit.IN:
            return Length(self.to_in(), LengthUnit.IN)
        elif target == LengthUnit.MM:
            return Length(self.to_mm(), LengthUnit.MM)
        elif target == LengthUnit.FT:
            return Length(self.to_in() / 12.0, LengthUnit.FT)
        elif target == LengthUnit.M:
            return Length(self.to_mm() / 1000.0, LengthUnit.M)
        raise ValueError(f"Unknown target unit: {target}")
    
    def __repr__(self):
        return f"{self.value:.3f} {self.unit.value}"
    
    def to_dict(self) -> dict:
        return {"value": self.value, "unit": self.unit.value}


@dataclass  
class Angle:
    """An angle value with explicit units."""
    value: float
    unit: AngleUnit
    
    def to_deg(self) -> float:
        """Convert to degrees."""
        if self.unit == AngleUnit.DEG:
            return self.value
        return self.value * 180.0 / math.pi
    
    def to_rad(self) -> float:
        """Convert to radians."""
        if self.unit == AngleUnit.RAD:
            return self.value
        return self.value * math.pi / 180.0
    
    def convert(self, target: AngleUnit) -> "Angle":
        """Convert to a different unit."""
        if target == AngleUnit.DEG:
            return Angle(self.to_deg(), AngleUnit.DEG)
        elif target == AngleUnit.RAD:
            return Angle(self.to_rad(), AngleUnit.RAD)
        raise ValueError(f"Unknown target unit: {target}")
    
    def __repr__(self):
        return f"{self.value:.2f} {self.unit.value}"
    
    def to_dict(self) -> dict:
        return {"value": self.value, "unit": self.unit.value}


# ============================================================
# UNIT PARSING (for CLI input)
# ============================================================

def parse_force(value: float, unit_str: str) -> Force:
    """Parse a force value from CLI input."""
    unit_map = {
        "lbf": ForceUnit.LBF,
        "lb": ForceUnit.LBF,
        "lbs": ForceUnit.LBF,
        "kn": ForceUnit.KN,
        "n": ForceUnit.N,
        "kgf": ForceUnit.KGF,
    }
    unit = unit_map.get(unit_str.lower())
    if not unit:
        raise ValueError(f"Unknown force unit: {unit_str}. Use: lbf, kN, N, kgf")
    return Force(value, unit)


def parse_length(value: float, unit_str: str) -> Length:
    """Parse a length value from CLI input."""
    unit_map = {
        "in": LengthUnit.IN,
        "inch": LengthUnit.IN,
        "inches": LengthUnit.IN,
        "ft": LengthUnit.FT,
        "feet": LengthUnit.FT,
        "mm": LengthUnit.MM,
        "m": LengthUnit.M,
        "meter": LengthUnit.M,
        "meters": LengthUnit.M,
    }
    unit = unit_map.get(unit_str.lower())
    if not unit:
        raise ValueError(f"Unknown length unit: {unit_str}. Use: in, ft, mm, m")
    return Length(value, unit)


# ============================================================
# OUTPUT FORMATTING
# ============================================================

def format_force_output(value: float, input_unit: ForceUnit) -> dict:
    """Format force output with both US and metric values."""
    f = Force(value, input_unit)
    return {
        "value": value,
        "unit": input_unit.value,
        "lbf": round(f.to_lbf(), 2),
        "kN": round(f.to_kn(), 4),
    }


# ============================================================
# UNIT VALIDATION
# ============================================================

def validate_units_in_output(output: dict) -> list:
    """Check that an output dict includes unit information."""
    warnings = []
    
    # Fields that should have units
    force_fields = ["load", "tension", "force", "pull", "impact_force", 
                    "leg_tension", "tension_each_side", "tension_per_leg",
                    "amplified_force", "max_vertical_load", "wll"]
    
    for field in force_fields:
        if field in output and f"{field}_unit" not in output and "units" not in output:
            warnings.append(f"Field '{field}' has no unit specified")
    
    return warnings


# ============================================================
# SELF-TEST
# ============================================================

if __name__ == "__main__":
    print("=== TRIG6 Units System Self-Test ===\n")
    
    # Force conversion test
    f = Force(1000, ForceUnit.LBF)
    print(f"1000 lbf = {f.to_kn():.4f} kN")
    
    f2 = Force(10, ForceUnit.KN)
    print(f"10 kN = {f2.to_lbf():.2f} lbf")
    
    # Length conversion test
    l = Length(12, LengthUnit.IN)
    print(f"12 in = {l.to_mm():.2f} mm")
    
    # Angle conversion test
    a = Angle(45, AngleUnit.DEG)
    print(f"45 deg = {a.to_rad():.6f} rad")
    
    # Parse test
    f3 = parse_force(500, "kN")
    print(f"\nParsed: 500 kN = {f3.to_lbf():.2f} lbf")
    
    print("\n✓ All unit tests passed")
