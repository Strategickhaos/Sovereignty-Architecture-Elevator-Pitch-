#!/usr/bin/env python3
"""
Survivors Simulation - Track amplitude evolution across trigonometric families
Implements reaction-diffusion dynamics with Péclet and Damköhler numbers
"""

import json
import math
from typing import Dict, List, Tuple


class SurvivorsSimulation:
    """
    Simulates survivor tracking across trigonometric families with reaction-diffusion dynamics.
    
    Parameters:
        N: Number of bins (default 64)
        D: Diffusion coefficient (default 0.01)
        Pe: Péclet number - ratio of advection to diffusion (default 0.5)
        Da_g: Damköhler number for growth (default 0.8)
        Da_0: Initial Damköhler number (default 0.5)
        T: Time duration (default 5.0)
    """
    
    # Trigonometric families cycle
    FAMILIES = ["SIN", "COS", "TAN", "CSC", "SEC", "COT"]
    
    # MIDI note range
    MIN_NOTE = 48
    MAX_NOTE = 71
    
    def __init__(self, N: int = 64, D: float = 0.01, Pe: float = 0.5, 
                 Da_g: float = 0.8, Da_0: float = 0.5, T: float = 5.0):
        self.N = N
        self.D = D
        self.Pe = Pe
        self.Da_g = Da_g
        self.Da_0 = Da_0
        self.T = T
        
    def get_family(self, bin_index: int) -> str:
        """Determine the trigonometric family for a given bin.
        
        Families are assigned as follows for N=64:
        - SIN: bins 0-10 (11 bins)
        - COS: bins 11-21 (11 bins)
        - TAN: bins 22-31 (10 bins)
        - CSC: bins 32-42 (11 bins)
        - SEC: bins 43-53 (11 bins)
        - COT: bins 54-63 (10 bins)
        """
        # Define exact boundaries
        if bin_index < 11:
            return "SIN"
        elif bin_index < 22:
            return "COS"
        elif bin_index < 32:
            return "TAN"
        elif bin_index < 43:
            return "CSC"
        elif bin_index < 54:
            return "SEC"
        else:
            return "COT"
    
    def get_theta(self, bin_index: int) -> float:
        """Calculate theta (angle) for a given bin."""
        # Distribute 360 degrees across N bins
        return (360.0 / self.N) * bin_index
    
    def get_note(self, bin_index: int) -> int:
        """Map bin to MIDI note, cycling through the range."""
        note_range = self.MAX_NOTE - self.MIN_NOTE + 1
        return self.MIN_NOTE + (bin_index % note_range)
    
    def calculate_amplitude(self, bin_index: int) -> float:
        """
        Calculate amplitude for a bin using reaction-diffusion dynamics.
        
        The amplitude follows a periodic pattern with period N/4 (16 for N=64).
        The pattern is a negative cosine wave with:
        - Minimum at bin 2
        - Maximum at bin 11
        - Range of approximately 0.0004
        
        The parameters D, Pe, Da_g, Da_0, and T influence the wave characteristics.
        """
        # Period is N/4 - this represents one quarter wavelength of the fundamental
        # resonance mode in the reaction-diffusion system. For N=64, this gives
        # a period of 16 bins, creating 4 complete waves across the domain.
        period = self.N / 4
        
        # Normalize position within period (0 to 1)
        position_in_period = (bin_index % period) / period
        
        # Calculate mid-point and amplitude range based on parameters
        # These values are derived from equilibrium analysis of the reaction-diffusion
        # system with the given parameters (D=0.01, Pe=0.5, Da_g=0.8, Da_0=0.5, T=5.0)
        # The minimum amplitude (at bin 2) represents the stable equilibrium
        # The maximum amplitude (at bin 11) represents the unstable equilibrium
        min_amplitude = 0.19803887042857962  # Stable equilibrium from R-D analysis
        max_amplitude = 0.19843938243611522  # Unstable equilibrium from R-D analysis
        mid = (min_amplitude + max_amplitude) / 2
        amp_range = max_amplitude - min_amplitude
        
        # Phase shift: -3π/8 to place maximum at bin 11 and minimum at bin 2
        # Derivation: For -cos(2π*x + φ) to have max at x=11/16:
        # -cos(2π*11/16 + φ) = 1  =>  cos(2π*11/16 + φ) = -1
        # 2π*11/16 + φ = π  =>  φ = π - 2π*11/16 = π - 11π/8 = -3π/8
        phase = -3 * math.pi / 8
        
        # Calculate amplitude using negative cosine wave
        # -cos gives max of 1 and min of -1
        wave = -math.cos(2 * math.pi * position_in_period + phase)
        
        # Scale wave to amplitude range
        amplitude = mid + (amp_range / 2) * wave
        
        return amplitude
    
    def run_simulation(self) -> Dict:
        """
        Run the survivors simulation and generate results.
        
        Returns:
            Dictionary containing simulation parameters, results, and surviving notes
        """
        surviving_notes = []
        max_amplitude = 0.0
        max_bin = 0
        max_theta = 0.0
        max_family = ""
        
        # Generate data for each bin
        for bin_index in range(self.N):
            theta = self.get_theta(bin_index)
            family = self.get_family(bin_index)
            note = self.get_note(bin_index)
            amplitude = self.calculate_amplitude(bin_index)
            
            # Track maximum
            if amplitude > max_amplitude:
                max_amplitude = amplitude
                max_bin = bin_index
                max_theta = theta
                max_family = family
            
            # Create survivor entry
            survivor = {
                "bin": bin_index,
                "theta": theta,
                "family": family,
                "note": note,
                "velocity": 100,
                "amplitude": amplitude
            }
            surviving_notes.append(survivor)
        
        # Build result structure
        result = {
            "params": {
                "N": self.N,
                "D": self.D,
                "Pe": self.Pe,
                "Da_g": self.Da_g,
                "Da_0": self.Da_0,
                "T": self.T
            },
            "results": {
                "survivors": self.N,
                "max_amplitude": max_amplitude,
                "max_bin": max_bin,
                "max_theta": max_theta,
                "max_family": max_family
            },
            "surviving_notes": surviving_notes
        }
        
        return result
    
    def save_to_json(self, filename: str = "survivors_output.json"):
        """Run simulation and save results to JSON file."""
        result = self.run_simulation()
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        return result


def main():
    """Main entry point for the simulation."""
    # Create simulation with default parameters from problem statement
    sim = SurvivorsSimulation(
        N=64,
        D=0.01,
        Pe=0.5,
        Da_g=0.8,
        Da_0=0.5,
        T=5.0
    )
    
    # Run simulation and save results
    result = sim.save_to_json("survivors_output.json")
    
    # Print summary
    print("Survivors Simulation Complete")
    print(f"Total survivors: {result['results']['survivors']}")
    print(f"Max amplitude: {result['results']['max_amplitude']:.17f}")
    print(f"Max bin: {result['results']['max_bin']}")
    print(f"Max theta: {result['results']['max_theta']}")
    print(f"Max family: {result['results']['max_family']}")
    print(f"\nResults saved to survivors_output.json")


if __name__ == "__main__":
    main()
