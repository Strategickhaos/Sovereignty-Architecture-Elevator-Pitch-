#!/usr/bin/env python3
"""
TRIG6 Volume-to-Frequency Codec
===============================
Maps geometric volume through angular phase to musical frequency.

Core transforms:
    Volume → θ (normalized phase 0-2π)
    θ → TRIG6 anchors (sin, cos, tan, csc, sec, cot)
    θ → Frequency via octave mapping

Based on:
    - Watch method: 1 minute = 6°, full circle = 360° = 60 minutes
    - MIDI: f(n) = f0 * 2^(n/12), where f0 = 440 Hz at A4 (MIDI 69)
    - Fractional quantization: 1/32, 1/64 resolution
    - Phase as primary coordinate, not distance

Author: Dom / Strategickhaos DAO LLC
"""

import math
from dataclasses import dataclass
from typing import Tuple, Dict, Optional
from enum import Enum


# =============================================================================
# CONSTANTS - The Anchor Points
# =============================================================================

# TRIG6 canonical angles (degrees)
TRIG6_ANGLES_DEG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]

# TRIG6 anchor values (dimensionless ratios)
TRIG6_ANCHORS = {
    0: 0.0,
    30: 0.5,                    # sin(30°)
    45: math.sqrt(2) / 2,       # sin(45°) = cos(45°) ≈ 0.7071
    60: math.sqrt(3) / 2,       # sin(60°) ≈ 0.8660
    90: 1.0,
    180: 0.0,                   # sin(180°)
    270: -1.0,                  # sin(270°)
    360: 0.0,
}

# MIDI reference: A4 = 440 Hz = MIDI 69
A4_FREQ = 440.0
A4_MIDI = 69

# Quantization resolution (pipefitter standard)
QUANT_32 = 1/32
QUANT_64 = 1/64

# Display thresholds
INFINITY_DISPLAY_THRESHOLD = 1e10  # Values above this are shown as ±∞
MICROTONE_THRESHOLD_CENTS = 5  # Cents deviation to show microtonal notation

# Rubik's cube colors as angular sectors (60° each)
CUBE_COLORS = {
    'white':  0,    # 0° - 60°
    'yellow': 180,  # opposite face
    'red':    90,
    'orange': 270,  # opposite
    'blue':   60,
    'green':  300,  # opposite
}


# =============================================================================
# GEOMETRY MODULE
# =============================================================================

@dataclass
class GeometryInput:
    """Input geometry - circle, sphere, or cylinder."""
    radius: float
    height: Optional[float] = None  # for cylinder
    unit: str = 'inches'

    @property
    def circle_area(self) -> float:
        """A = πr²"""
        return math.pi * self.radius ** 2

    @property
    def sphere_volume(self) -> float:
        """V = (4/3)πr³"""
        return (4/3) * math.pi * self.radius ** 3

    @property
    def cylinder_volume(self) -> float:
        """V = πr²h"""
        if self.height is None:
            raise ValueError("Height required for cylinder volume")
        return math.pi * self.radius ** 2 * self.height

    @property
    def circumference(self) -> float:
        """C = 2πr = πd"""
        return 2 * math.pi * self.radius


# =============================================================================
# TRIG6 CORE FUNCTIONS
# =============================================================================

def trig6_all(theta_deg: float) -> Dict[str, float]:
    """
    Compute all 6 trig functions for a given angle.
    
    Returns dict with sin, cos, tan, csc, sec, cot.
    Handles undefined values (division by zero) as infinity.
    """
    theta_rad = math.radians(theta_deg)
    
    sin_val = math.sin(theta_rad)
    cos_val = math.cos(theta_rad)
    
    # Handle near-zero for reciprocals
    eps = 1e-10
    
    tan_val = sin_val / cos_val if abs(cos_val) > eps else math.inf * (1 if sin_val >= 0 else -1)
    csc_val = 1 / sin_val if abs(sin_val) > eps else math.inf * (1 if sin_val >= 0 else -1)
    sec_val = 1 / cos_val if abs(cos_val) > eps else math.inf * (1 if cos_val >= 0 else -1)
    cot_val = cos_val / sin_val if abs(sin_val) > eps else math.inf * (1 if cos_val >= 0 else -1)
    
    return {
        'sin': sin_val,
        'cos': cos_val,
        'tan': tan_val,
        'csc': csc_val,
        'sec': sec_val,
        'cot': cot_val,
    }


def quantize(value: float, resolution: float = QUANT_64) -> float:
    """Quantize to nearest resolution step (default 1/64)."""
    return round(value / resolution) * resolution


def quantize_to_fraction(value: float, max_denom: int = 64) -> Tuple[int, int]:
    """
    Convert decimal to nearest binary fraction (power-of-2 denominators).
    
    Only checks denominators that are powers of 2 (2, 4, 8, 16, 32, 64)
    as per pipefitter standard for fractional inch measurements.
    """
    # Normalize to 0-1 range if needed
    normalized = value % 1.0 if value > 1 else value
    
    best_num = 0
    best_denom = 1
    best_error = abs(normalized)
    
    for denom in [2, 4, 8, 16, 32, 64]:
        if denom > max_denom:
            break
        num = round(normalized * denom)
        error = abs(normalized - num/denom)
        if error < best_error:
            best_error = error
            best_num = num
            best_denom = denom
    
    # Simplify fraction to lowest terms
    if best_num > 0 and best_denom > 1:
        from math import gcd
        divisor = gcd(best_num, best_denom)
        best_num //= divisor
        best_denom //= divisor
    
    return (best_num, best_denom)


# =============================================================================
# VOLUME → θ MAPPING
# =============================================================================

def volume_to_theta(volume: float, v_min: float = 0.0, v_max: float = 100.0) -> float:
    """
    Map volume to angular position (0-360°).
    
    Linear mapping: θ = (V - V_min) / (V_max - V_min) * 360°
    
    Args:
        volume: The volume value
        v_min: Minimum volume (maps to 0°)
        v_max: Maximum volume (maps to 360°)
    
    Returns:
        Angle in degrees (0-360)
    """
    if v_max <= v_min:
        raise ValueError("v_max must be greater than v_min")
    
    # Normalize to 0-1
    normalized = (volume - v_min) / (v_max - v_min)
    
    # Clamp to valid range
    normalized = max(0.0, min(1.0, normalized))
    
    # Map to degrees
    theta = normalized * 360.0
    
    return theta


def volume_to_theta_log(volume: float, v_ref: float = 1.0, octaves: int = 8) -> float:
    """
    Map volume to angular position using logarithmic scaling.
    
    Like musical octaves: each doubling of volume = one octave = 30° (or configurable).
    
    Args:
        volume: The volume value (must be > 0)
        v_ref: Reference volume (maps to 0°)
        octaves: Number of octaves to span 360°
    
    Returns:
        Angle in degrees (0-360, wrapping)
    """
    if volume <= 0:
        raise ValueError("Volume must be positive for logarithmic mapping")
    
    # How many octaves from reference?
    octave_offset = math.log2(volume / v_ref)
    
    # Degrees per octave
    deg_per_octave = 360.0 / octaves
    
    # Map to angle (with wrapping)
    theta = (octave_offset * deg_per_octave) % 360.0
    
    return theta


# =============================================================================
# θ → FREQUENCY MAPPING
# =============================================================================

def theta_to_midi(theta_deg: float, base_midi: int = 60, theta_per_semitone: float = 30.0) -> float:
    """
    Map angle to MIDI note number.
    
    Default: 30° = 1 semitone, so 360° = 12 semitones = 1 octave
    
    Args:
        theta_deg: Angle in degrees
        base_midi: MIDI number at θ=0° (default 60 = C4)
        theta_per_semitone: Degrees per semitone (default 30° = 12 semitones per circle)
    
    Returns:
        MIDI note number (can be fractional for microtones)
    """
    semitones = theta_deg / theta_per_semitone
    return base_midi + semitones


def midi_to_freq(midi_note: float) -> float:
    """
    Convert MIDI note number to frequency.
    
    f = 440 * 2^((n - 69) / 12)
    """
    return A4_FREQ * (2 ** ((midi_note - A4_MIDI) / 12))


def theta_to_freq(theta_deg: float, base_midi: int = 60, theta_per_semitone: float = 30.0) -> float:
    """
    Direct mapping: θ → frequency.
    
    Combines theta_to_midi and midi_to_freq.
    """
    midi = theta_to_midi(theta_deg, base_midi, theta_per_semitone)
    return midi_to_freq(midi)


def freq_to_midi(freq: float) -> float:
    """
    Convert frequency to MIDI note number.
    
    n = 69 + 12 * log2(f / 440)
    """
    if freq <= 0:
        raise ValueError("Frequency must be positive")
    return A4_MIDI + 12 * math.log2(freq / A4_FREQ)


def freq_to_theta(freq: float, base_midi: int = 60, theta_per_semitone: float = 30.0) -> float:
    """
    Inverse mapping: frequency → θ.
    """
    midi = freq_to_midi(freq)
    theta = (midi - base_midi) * theta_per_semitone
    return theta % 360.0


# =============================================================================
# WATCH METHOD (from pipefitter's manual)
# =============================================================================

def watch_angle_to_minutes(theta_deg: float) -> float:
    """
    Convert angle to watch minutes.
    
    Each minute = 6°
    30° = 5 minutes
    45° = 7.5 minutes
    60° = 10 minutes
    """
    return theta_deg / 6.0


def watch_minutes_to_angle(minutes: float) -> float:
    """
    Convert watch minutes to angle.
    
    Each minute = 6°
    """
    return minutes * 6.0


# =============================================================================
# COMPLETE CODEC: Volume → θ → TRIG6 → Frequency
# =============================================================================

@dataclass
class TRIG6Result:
    """Complete result from TRIG6 codec."""
    # Input
    volume: float
    geometry_type: str
    
    # Phase
    theta_deg: float
    theta_rad: float
    watch_minutes: float
    
    # TRIG6 values
    sin: float
    cos: float
    tan: float
    csc: float
    sec: float
    cot: float
    
    # Frequency
    midi_note: float
    frequency_hz: float
    note_name: str
    
    # Quantized
    theta_fraction: Tuple[int, int]
    
    # Cube color sector
    color_sector: str


def get_note_name(midi: float) -> str:
    """Convert MIDI number to note name (e.g., C4, F#5)."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    midi_int = int(round(midi))
    octave = (midi_int // 12) - 1
    note_idx = midi_int % 12
    
    # Indicate if microtonal
    cents_off = (midi - midi_int) * 100
    if abs(cents_off) > MICROTONE_THRESHOLD_CENTS:
        return f"{notes[note_idx]}{octave} {cents_off:+.0f}¢"
    return f"{notes[note_idx]}{octave}"


def get_color_sector(theta_deg: float) -> str:
    """
    Determine which Rubik's cube color sector the angle falls in.
    
    Maps 360° into six 60° sectors corresponding to cube faces.
    Note: CUBE_COLORS constant above shows reference positions,
    but this function maps the full angular sweep sequentially.
    """
    theta_normalized = theta_deg % 360
    
    # 60° sectors mapped sequentially around the circle
    if 0 <= theta_normalized < 60:
        return 'white'
    elif 60 <= theta_normalized < 120:
        return 'blue'
    elif 120 <= theta_normalized < 180:
        return 'red'
    elif 180 <= theta_normalized < 240:
        return 'yellow'
    elif 240 <= theta_normalized < 300:
        return 'orange'
    else:
        return 'green'


def volume_to_frequency(
    geometry: GeometryInput,
    geometry_type: str = 'sphere',
    v_min: float = 0.0,
    v_max: float = 100.0,
    use_log: bool = False,
    base_midi: int = 60
) -> TRIG6Result:
    """
    Complete TRIG6 codec: Volume → θ → Frequency
    
    Args:
        geometry: GeometryInput with radius (and height for cylinder)
        geometry_type: 'circle', 'sphere', or 'cylinder'
        v_min, v_max: Volume range for linear mapping
        use_log: Use logarithmic mapping (octave-based)
        base_midi: MIDI note at θ=0°
    
    Returns:
        TRIG6Result with all computed values
    """
    # Get volume based on geometry type
    if geometry_type == 'circle':
        volume = geometry.circle_area
    elif geometry_type == 'sphere':
        volume = geometry.sphere_volume
    elif geometry_type == 'cylinder':
        volume = geometry.cylinder_volume
    else:
        raise ValueError(f"Unknown geometry type: {geometry_type}")
    
    # Volume → θ
    if use_log and volume > 0:
        theta_deg = volume_to_theta_log(volume, v_ref=v_min if v_min > 0 else 1.0)
    else:
        theta_deg = volume_to_theta(volume, v_min, v_max)
    
    theta_rad = math.radians(theta_deg)
    
    # TRIG6 computation
    trig_vals = trig6_all(theta_deg)
    
    # θ → Frequency
    midi_note = theta_to_midi(theta_deg, base_midi)
    frequency_hz = midi_to_freq(midi_note)
    note_name = get_note_name(midi_note)
    
    # Quantization
    theta_normalized = theta_deg / 360.0
    theta_fraction = quantize_to_fraction(theta_normalized)
    
    # Watch method
    watch_minutes = watch_angle_to_minutes(theta_deg)
    
    # Color sector
    color_sector = get_color_sector(theta_deg)
    
    return TRIG6Result(
        volume=volume,
        geometry_type=geometry_type,
        theta_deg=theta_deg,
        theta_rad=theta_rad,
        watch_minutes=watch_minutes,
        sin=trig_vals['sin'],
        cos=trig_vals['cos'],
        tan=trig_vals['tan'],
        csc=trig_vals['csc'],
        sec=trig_vals['sec'],
        cot=trig_vals['cot'],
        midi_note=midi_note,
        frequency_hz=frequency_hz,
        note_name=note_name,
        theta_fraction=theta_fraction,
        color_sector=color_sector,
    )


# =============================================================================
# DISPLAY / OUTPUT
# =============================================================================

def print_result(result: TRIG6Result):
    """Pretty print TRIG6 result."""
    print("=" * 60)
    print("TRIG6 VOLUME → FREQUENCY CODEC")
    print("=" * 60)
    print(f"\n[GEOMETRY]")
    print(f"  Type:   {result.geometry_type}")
    print(f"  Volume: {result.volume:.6f}")
    
    print(f"\n[PHASE]")
    print(f"  θ (deg):     {result.theta_deg:.4f}°")
    print(f"  θ (rad):     {result.theta_rad:.6f}")
    print(f"  θ (watch):   {result.watch_minutes:.2f} minutes")
    print(f"  θ (frac):    {result.theta_fraction[0]}/{result.theta_fraction[1]}")
    print(f"  Color:       {result.color_sector}")
    
    print(f"\n[TRIG6]")
    print(f"  sin(θ): {result.sin:+.6f}")
    print(f"  cos(θ): {result.cos:+.6f}")
    print(f"  tan(θ): {result.tan:+.6f}" if abs(result.tan) < INFINITY_DISPLAY_THRESHOLD else f"  tan(θ): ±∞")
    print(f"  csc(θ): {result.csc:+.6f}" if abs(result.csc) < INFINITY_DISPLAY_THRESHOLD else f"  csc(θ): ±∞")
    print(f"  sec(θ): {result.sec:+.6f}" if abs(result.sec) < INFINITY_DISPLAY_THRESHOLD else f"  sec(θ): ±∞")
    print(f"  cot(θ): {result.cot:+.6f}" if abs(result.cot) < INFINITY_DISPLAY_THRESHOLD else f"  cot(θ): ±∞")
    
    print(f"\n[FREQUENCY]")
    print(f"  MIDI:  {result.midi_note:.2f}")
    print(f"  Hz:    {result.frequency_hz:.4f}")
    print(f"  Note:  {result.note_name}")
    
    print("=" * 60)


# =============================================================================
# MAIN - DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TRIG6 VOLUME-FREQUENCY CODEC - DEMONSTRATION")
    print("=" * 60)
    
    # Example 1: Sphere with radius 2 inches
    print("\n>>> Example 1: Sphere, r = 2 inches")
    geo1 = GeometryInput(radius=2.0, unit='inches')
    result1 = volume_to_frequency(geo1, geometry_type='sphere', v_min=0, v_max=100)
    print_result(result1)
    
    # Example 2: Cylinder (pipe) with radius 1 inch, height 10 inches
    print("\n>>> Example 2: Cylinder (pipe), r = 1 inch, h = 10 inches")
    geo2 = GeometryInput(radius=1.0, height=10.0, unit='inches')
    result2 = volume_to_frequency(geo2, geometry_type='cylinder', v_min=0, v_max=100)
    print_result(result2)
    
    # Example 3: Circle area as "volume proxy", r = 4 inches
    print("\n>>> Example 3: Circle area, r = 4 inches")
    geo3 = GeometryInput(radius=4.0, unit='inches')
    result3 = volume_to_frequency(geo3, geometry_type='circle', v_min=0, v_max=100)
    print_result(result3)
    
    # Example 4: Logarithmic mapping (octave-based)
    print("\n>>> Example 4: Sphere r=3, logarithmic mapping")
    geo4 = GeometryInput(radius=3.0)
    result4 = volume_to_frequency(geo4, geometry_type='sphere', use_log=True, v_min=1.0)
    print_result(result4)
    
    # Example 5: The pipefitter's circumference check
    # P = π × 8 = 25.1328 (from your drawing)
    print("\n>>> Example 5: Pipe circumference verification")
    pipe_d = 8.0  # diameter
    pipe_r = pipe_d / 2
    pipe_geo = GeometryInput(radius=pipe_r)
    print(f"  Diameter:      {pipe_d} inches")
    print(f"  Circumference: {pipe_geo.circumference:.4f} inches")
    print(f"  (Expected:     {math.pi * pipe_d:.4f} = π × {pipe_d})")
    
    # Example 6: Sweep through angles showing TRIG6 anchors
    print("\n>>> Example 6: TRIG6 anchor points")
    print(f"{'θ (deg)':<10} {'sin':<10} {'cos':<10} {'tan':<12}")
    print("-" * 42)
    for angle in [0, 30, 45, 60, 90, 180, 270]:
        t = trig6_all(angle)
        tan_str = f"{t['tan']:.4f}" if abs(t['tan']) < INFINITY_DISPLAY_THRESHOLD else "±∞"
        print(f"{angle:<10} {t['sin']:<10.4f} {t['cos']:<10.4f} {tan_str:<12}")
    
    print("\n" + "=" * 60)
    print("CODEC READY")
    print("=" * 60)
