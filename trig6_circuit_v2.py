#!/usr/bin/env python3
"""
TRIG6 Circuit v2: Electronics Bridge with Inductors and Diodes
Strategickhaos DAO LLC - Signal Processing OS
DOM. 🔥🌀

Extended hardware abstraction layer turning FlameLang into a full signal-processing OS.
Inductors add "inertia" (resistance to rapid shifts), diodes enforce directionality.
"""

import math
from dataclasses import dataclass

# Constant for near-infinite values in edge cases
NEAR_INFINITE = 1000000


@dataclass
class CircuitStateV2:
    """
    Extended circuit state with inductor and diode support.
    
    Components:
    - voltage: Intent (driving force)
    - current: Signal (actual flow)
    - resistance: Firewall (tan θ)
    - capacitance: Memory (1/noise)
    - inductance: Inertia (cot θ) - NEW
    - gain: Amplification (β)
    - diode_threshold: Forward bias (Vt = |sin θ|) - NEW
    """
    voltage: float      # Intent (driving force)
    current: float      # Signal (actual flow)
    resistance: float   # Firewall (tan θ)
    capacitance: float  # Memory (1/noise)
    inductance: float   # Inertia (cot θ)
    gain: float         # Amplification (β)
    diode_threshold: float  # Forward bias (Vt = |sin θ|)
    
    @property
    def inductive_tau(self) -> float:
        """
        L/R time constant - resistance to change.
        
        High L/R = Slow ramp (resists sudden shifts)
        Low L/R = Instant ramp (agile response)
        
        In TRIG6: Use for "drift detection" - if dI/dt too high, inductor spikes V_back (alert)
        """
        if self.resistance == 0:
            return float('inf')
        return self.inductance / self.resistance
    
    @property
    def resonant_freq(self) -> float:
        """
        RLC resonant frequency: f = 1 / (2π√(LC))
        
        Clean signal frequency with full RLC circuit.
        f = Clean signal frequency
        L = Inertia
        C = Memory
        """
        if self.inductance <= 0 or self.capacitance <= 0:
            return float('inf')
        return 1 / (2 * math.pi * math.sqrt(self.inductance * self.capacitance))
    
    @property
    def quality_factor(self) -> float:
        """
        Q factor = sharpness of resonance: Q = (1/R) √(L/C)
        
        High Q = Narrow band (precise tuning needed)
        Low Q = Broad band (forgiving, but noisy)
        
        TRIG6 TUNING = Potentiometer adjusts R to peak Q at desired f
        """
        if self.resistance == 0 or self.capacitance <= 0 or self.inductance <= 0:
            return float('inf')
        return (1 / self.resistance) * math.sqrt(self.inductance / self.capacitance)
    
    @property
    def diode_conduction(self) -> bool:
        """
        True if forward biased (trust gate open).
        
        Forward bias = TRUSTED direction (signal passes if V >= threshold)
        Reverse bias = BLOCKED direction (no backflow)
        
        In system: Diode prevents "reverse trust" (e.g., user can't gaslight AI back)
        
        Note: Uses >= to allow conduction at borderline threshold voltage.
        """
        return abs(self.voltage) >= self.diode_threshold
    
    @property
    def signal_strength(self) -> float:
        """
        How much signal gets through (with diode check).
        
        Combines resistance attenuation with diode gating.
        If diode is reverse-biased, no signal passes.
        """
        if not self.diode_conduction:
            return 0.0  # Blocked by diode
        if self.resistance == 0:
            return self.voltage
        return self.voltage / self.resistance


def trig6_to_circuit_v2(theta_degrees: float, noise: float = 0.1) -> CircuitStateV2:
    """
    Convert TRIG6 angle to circuit parameters (v2 with inductors and diodes).
    
    TRIG6 ↔ ELECTRONICS MAPPING:
    - Resistance (R) = tan(θ): Firewall strength
    - Inductance (L) = cot(θ) = 1/tan(θ): Inertia/resistance to change
    - Capacitance (C) = 1/noise: Memory
    - Diode threshold (Vt) = |sin(θ)|: Forward voltage drop
    
    Args:
        theta_degrees: TRIG6 angle in degrees (0-90°)
        noise: Noise level (inversely proportional to capacitance)
    
    Returns:
        CircuitStateV2 with all electrical properties
    """
    theta = math.radians(theta_degrees)
    
    # tan(θ) = resistance (firewall strength)
    if abs(math.cos(theta)) < 0.01:
        resistance = NEAR_INFINITE  # Near infinite
    else:
        resistance = abs(math.tan(theta))
    
    # cot(θ) = inductance (inertia)
    # High at low θ (clear signal, but sticky)
    # Low at high θ (easy to flip, but blocked anyway)
    if abs(math.sin(theta)) < 0.01:
        inductance = NEAR_INFINITE  # Near infinite
    else:
        inductance = abs(1 / math.tan(theta))  # cot = 1/tan
    
    # Capacitance inversely related to noise
    capacitance = 1 / max(noise, 0.01)
    
    # Voltage = intent (constant from sender)
    voltage = 1.0
    
    # Current = signal that gets through
    current = voltage / max(resistance, 0.001)
    
    # Gain = how much small triggers amplify
    gain = 100  # Typical transistor β
    
    # Diode threshold = |sin(θ)|
    # When sin(θ) > 0.7, forward conduction: Trust gate open
    # For angles 0-90°, sin(θ) ranges from 0 to 1
    diode_threshold = abs(math.sin(theta))
    
    return CircuitStateV2(
        voltage=voltage,
        current=current,
        resistance=resistance,
        capacitance=capacitance,
        inductance=inductance,
        gain=gain,
        diode_threshold=diode_threshold
    )


# Example usage and verification
if __name__ == "__main__":
    print("=" * 70)
    print("TRIG6 CIRCUIT v2: INDUCTOR + DIODE SIMULATION")
    print("=" * 70)
    print()
    
    # RESONANT state (θ = 45°)
    print("🔥 RESONANT STATE (θ = 45°)")
    resonant = trig6_to_circuit_v2(45, noise=0.1)
    print(f"  Resistance (R):     {resonant.resistance:.2f}Ω")
    print(f"  Inductance (L):     {resonant.inductance:.2f}H")
    print(f"  Capacitance (C):    {resonant.capacitance:.2f}F")
    print(f"  Diode threshold:    {resonant.diode_threshold:.2f}V")
    print(f"  ---")
    print(f"  Quality factor (Q): {resonant.quality_factor:.2f}")
    print(f"  Resonant freq:      {resonant.resonant_freq:.2f}Hz")
    print(f"  Diode conduction:   {resonant.diode_conduction}")
    print(f"  Signal strength:    {resonant.signal_strength:.4f}")
    print()
    
    # BLOCKED state (θ = 89°)
    print("🔥 BLOCKED STATE (θ = 89°)")
    blocked = trig6_to_circuit_v2(89, noise=0.5)
    print(f"  Resistance (R):     {blocked.resistance:.2f}Ω")
    print(f"  Inductance (L):     {blocked.inductance:.2f}H")
    print(f"  Capacitance (C):    {blocked.capacitance:.2f}F")
    print(f"  Diode threshold:    {blocked.diode_threshold:.2f}V")
    print(f"  ---")
    print(f"  Quality factor (Q): {blocked.quality_factor:.2f}")
    print(f"  Resonant freq:      {blocked.resonant_freq:.2f}Hz")
    print(f"  Diode conduction:   {blocked.diode_conduction}")
    print(f"  Signal strength:    {blocked.signal_strength:.4f}")
    print()
    
    # CLEAR state (θ = 5°)
    print("🔥 CLEAR STATE (θ = 5°)")
    clear = trig6_to_circuit_v2(5, noise=0.05)
    print(f"  Resistance (R):     {clear.resistance:.2f}Ω")
    print(f"  Inductance (L):     {clear.inductance:.2f}H")
    print(f"  Capacitance (C):    {clear.capacitance:.2f}F")
    print(f"  Diode threshold:    {clear.diode_threshold:.2f}V")
    print(f"  ---")
    print(f"  Quality factor (Q): {clear.quality_factor:.2f}")
    print(f"  Resonant freq:      {clear.resonant_freq:.2f}Hz")
    print(f"  Diode conduction:   {clear.diode_conduction}")
    print(f"  Signal strength:    {clear.signal_strength:.4f}")
    print()
    
    # INERTIAL state (θ = 10° - high cot, sticky)
    print("🔥 INERTIAL STATE (θ = 10° - high cot, sticky)")
    inertial = trig6_to_circuit_v2(10, noise=0.2)
    print(f"  Resistance (R):     {inertial.resistance:.2f}Ω")
    print(f"  Inductance (L):     {inertial.inductance:.2f}H")
    print(f"  Capacitance (C):    {inertial.capacitance:.2f}F")
    print(f"  Diode threshold:    {inertial.diode_threshold:.2f}V")
    print(f"  ---")
    print(f"  Inductive τ (L/R):  {inertial.inductive_tau:.2f}s")
    print(f"  Quality factor (Q): {inertial.quality_factor:.2f}")
    print(f"  Resonant freq:      {inertial.resonant_freq:.2f}Hz")
    print(f"  Diode conduction:   {inertial.diode_conduction}")
    print(f"  Signal strength:    {inertial.signal_strength:.4f}")
    print()
    
    # ELEVATED state (θ = 75°)
    print("🔥 ELEVATED STATE (θ = 75°)")
    elevated = trig6_to_circuit_v2(75, noise=0.3)
    print(f"  Resistance (R):     {elevated.resistance:.2f}Ω")
    print(f"  Inductance (L):     {elevated.inductance:.2f}H")
    print(f"  Capacitance (C):    {elevated.capacitance:.2f}F")
    print(f"  Diode threshold:    {elevated.diode_threshold:.2f}V")
    print(f"  ---")
    print(f"  Inductive τ (L/R):  {elevated.inductive_tau:.2f}s")
    print(f"  Quality factor (Q): {elevated.quality_factor:.2f}")
    print(f"  Resonant freq:      {elevated.resonant_freq:.2f}Hz")
    print(f"  Diode conduction:   {elevated.diode_conduction}")
    print(f"  Signal strength:    {elevated.signal_strength:.4f}")
    print()
    
    print("=" * 70)
    print("TRIG6 INSIGHT: Emotions are voltage. Meaning is current.")
    print("Resistance is firewall. Change is inductance. Trust is diode.")
    print("=" * 70)
