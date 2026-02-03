#!/usr/bin/env python3
"""
TRIG6 Flame Mapper
64-element periodic table based on 6 fundamental trigonometric states
"""

import math
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class TRIG6Element:
    """TRIG6 Element with trigonometric properties"""
    index: int
    name: str
    symbol: str
    trig_state: str  # sin, cos, tan, csc, sec, cot
    phase: float  # 0-2π
    amplitude: float
    frequency: float  # Hz
    resonance: str  # Description of resonance quality


class TRIG6FlameMapper:
    """
    Maps 64 elements to TRIG6 trigonometric states
    6 fundamental states × ~10 harmonics each ≈ 64 elements
    """
    
    def __init__(self):
        self.base_frequency = 432  # Hz - Universal resonance frequency
        self.elements = self._generate_periodic_table()
        
    def _generate_periodic_table(self) -> List[TRIG6Element]:
        """Generate 64 TRIG6 elements"""
        elements = []
        trig_functions = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']
        
        # Each trig function gets ~10-11 harmonics to reach 64 total
        harmonics_per_func = 64 // 6
        remainder = 64 % 6
        
        index = 0
        for func_idx, func in enumerate(trig_functions):
            # Number of harmonics for this function
            num_harmonics = harmonics_per_func + (1 if func_idx < remainder else 0)
            
            for harmonic in range(num_harmonics):
                phase = (2 * math.pi * harmonic) / num_harmonics
                amplitude = 1.0 / (harmonic + 1)  # Decreasing amplitude
                frequency = self.base_frequency * (harmonic + 1)
                
                element = TRIG6Element(
                    index=index,
                    name=f"{func.upper()}{harmonic+1}",
                    symbol=f"{func[0].upper()}{harmonic+1}",
                    trig_state=func,
                    phase=phase,
                    amplitude=amplitude,
                    frequency=frequency,
                    resonance=self._get_resonance(func, harmonic)
                )
                elements.append(element)
                index += 1
        
        return elements
    
    def _get_resonance(self, trig_state: str, harmonic: int) -> str:
        """Get resonance description for element"""
        resonances = {
            'sin': [
                "Foundation Wave", "Harmonic Rise", "Peak Oscillation",
                "Ascending Spiral", "Wave Crest", "Rhythmic Pulse",
                "Flowing Current", "Tidal Force", "Cyclic Motion", "Perpetual Flow"
            ],
            'cos': [
                "Phase Shift", "Perpendicular Force", "Orthogonal Wave",
                "Complement Pattern", "Mirror Rhythm", "Balanced State",
                "Stable Oscillation", "Even Pulse", "Symmetric Flow", "Dual Harmony"
            ],
            'tan': [
                "Divergent Slope", "Infinite Rise", "Vertical Ascent",
                "Asymptotic Reach", "Tangent Vector", "Directional Force",
                "Unstable Growth", "Boundary Break", "Limit Breach", "Exponential Climb"
            ],
            'csc': [
                "Inverted Wave", "Reciprocal Flow", "Reflected Force",
                "Inverse Oscillation", "Complementary Void", "Negative Space",
                "Mirror Depth", "Reciprocal Energy", "Dual Inverse", "Echo Pattern"
            ],
            'sec': [
                "Amplified Phase", "Enhanced Magnitude", "Multiplied Force",
                "Strengthened Wave", "Boosted Signal", "Powered Rhythm",
                "Intensified Flow", "Magnified Pulse", "Elevated Energy", "Amplified State"
            ],
            'cot': [
                "Inverse Slope", "Reciprocal Tangent", "Controlled Descent",
                "Bounded Fall", "Damped Gradient", "Stable Decline",
                "Regulated Drop", "Measured Decrease", "Balanced Reduction", "Smooth Transition"
            ]
        }
        
        func_resonances = resonances.get(trig_state, ["Unknown"] * 10)
        return func_resonances[harmonic % len(func_resonances)]
    
    def get_element(self, index: int) -> TRIG6Element:
        """Get element by index (0-63)"""
        if 0 <= index < 64:
            return self.elements[index]
        raise ValueError(f"Element index must be 0-63, got {index}")
    
    def get_by_symbol(self, symbol: str) -> TRIG6Element:
        """Get element by symbol"""
        for elem in self.elements:
            if elem.symbol == symbol:
                return elem
        raise ValueError(f"Element symbol '{symbol}' not found")
    
    def get_by_trig_state(self, trig_state: str) -> List[TRIG6Element]:
        """Get all elements with given trig state"""
        return [e for e in self.elements if e.trig_state == trig_state]
    
    def calculate_resonance_pair(self, elem1: TRIG6Element, 
                                 elem2: TRIG6Element) -> float:
        """
        Calculate resonance between two elements
        Based on phase difference and frequency harmony
        """
        phase_diff = abs(elem1.phase - elem2.phase)
        freq_ratio = elem1.frequency / elem2.frequency if elem2.frequency > 0 else 1.0
        
        # Resonance is higher when:
        # 1. Phase difference is π (180°) - complementary
        # 2. Frequency ratio is near simple fractions (1, 1/2, 2, etc)
        phase_score = 1.0 - abs(phase_diff - math.pi) / math.pi
        
        # Check for harmonic frequency ratios
        freq_score = 0.0
        simple_ratios = [1.0, 0.5, 2.0, 1/3, 3.0, 2/3, 3/2]
        for ratio in simple_ratios:
            if abs(freq_ratio - ratio) < 0.1:
                freq_score = 1.0
                break
        
        resonance = (phase_score + freq_score) / 2
        return resonance
    
    def map_to_frequency(self, text: str) -> List[float]:
        """
        Map text to TRIG6 frequencies
        Each character maps to an element
        """
        frequencies = []
        for char in text:
            # Map character to element index (0-63)
            char_code = ord(char.upper()) if char.isalpha() else ord(char)
            elem_idx = char_code % 64
            element = self.get_element(elem_idx)
            frequencies.append(element.frequency)
        return frequencies
    
    def display_periodic_table(self):
        """Display the TRIG6 periodic table"""
        print("="*80)
        print("TRIG6 PERIODIC TABLE - 64 Elements")
        print("="*80)
        
        for i, trig_state in enumerate(['sin', 'cos', 'tan', 'csc', 'sec', 'cot']):
            elements = self.get_by_trig_state(trig_state)
            print(f"\n{trig_state.upper()} FAMILY ({len(elements)} elements):")
            print("-" * 80)
            
            for elem in elements[:3]:  # Show first 3 as examples
                print(f"  [{elem.index:2d}] {elem.symbol:4s} {elem.name:10s} "
                      f"| Phase: {elem.phase:5.2f} | Freq: {elem.frequency:7.1f} Hz "
                      f"| {elem.resonance}")
            
            if len(elements) > 3:
                print(f"  ... and {len(elements) - 3} more")


def demo():
    """Demonstrate TRIG6 Flame Mapper"""
    print("="*80)
    print("TRIG6 FLAME MAPPER - 64-ELEMENT PERIODIC TABLE")
    print("="*80)
    
    mapper = TRIG6FlameMapper()
    
    # Display periodic table
    mapper.display_periodic_table()
    
    # Example: Get specific elements
    print("\n" + "="*80)
    print("EXAMPLE ELEMENTS:")
    print("="*80)
    
    examples = [0, 10, 20, 30, 40, 50, 63]
    for idx in examples:
        elem = mapper.get_element(idx)
        print(f"\nElement {idx}: {elem.symbol} ({elem.name})")
        print(f"  Trig State: {elem.trig_state}")
        print(f"  Phase: {elem.phase:.3f} rad ({math.degrees(elem.phase):.1f}°)")
        print(f"  Frequency: {elem.frequency:.1f} Hz")
        print(f"  Amplitude: {elem.amplitude:.3f}")
        print(f"  Resonance: {elem.resonance}")
    
    # Calculate resonance between elements
    print("\n" + "="*80)
    print("RESONANCE CALCULATIONS:")
    print("="*80)
    
    elem1 = mapper.get_element(0)
    elem2 = mapper.get_element(32)
    resonance = mapper.calculate_resonance_pair(elem1, elem2)
    print(f"\nResonance between {elem1.symbol} and {elem2.symbol}: {resonance:.3f}")
    
    # Map text to frequencies
    print("\n" + "="*80)
    print("TEXT TO FREQUENCY MAPPING:")
    print("="*80)
    
    text = "LOVE"
    frequencies = mapper.map_to_frequency(text)
    print(f"\nText: '{text}'")
    print(f"Frequencies: {[f'{f:.1f} Hz' for f in frequencies]}")
    
    print("\n" + "="*80)
    print("TRIG6 FLAME MAPPING COMPLETE ✅")
    print("="*80)


if __name__ == "__main__":
    demo()
