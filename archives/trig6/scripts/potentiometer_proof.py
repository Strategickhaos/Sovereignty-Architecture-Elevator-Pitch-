#!/usr/bin/env python3
"""
Potentiometer Proof Integration for TRIG6 Simulations
=====================================================

Hardware → TRIG6 mapping for physical proof of material stability.
Connects Arduino potentiometer readings to TRIG6 engine evaluations.

Hardware Setup:
- Arduino Uno/Nano with potentiometer on A0
- Serial connection at 9600 baud
- Potentiometer provides 0-1023 analog readings

Author: Domenic Gabriel Garza
Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
Date: 2026-01-25
GPG: AE5519579584DEF5
"""

import time
import math
from typing import Dict, Optional
from dataclasses import dataclass

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("Warning: pyserial not installed. Install with: pip install pyserial")

from trig6_engine import TRIG6Engine, TRIG6State


@dataclass
class Recipe:
    """Material recipe with base parameters."""
    name: str
    id: str
    R_base: float
    D_base: float
    N_base: float
    eq: float
    hazard: str = "LOW"


class PotentiometerMode:
    """Mapping modes for potentiometer → TRIG6 parameters."""
    MODE_NOISE = "noise"  # N = pot_norm
    MODE_THETA = "theta"  # θ = pot_norm × 2π
    MODE_ALPHA = "alpha"  # α = pot_norm
    MODE_DRIFT = "drift"  # D = pot_norm


class TRIG6ProofSystem:
    """
    Physical proof system using potentiometer for material validation.
    
    Maps Arduino A0 (0-1023) → normalized (0.0-1.0) values.
    """
    
    def __init__(
        self,
        port: str = 'COM3',
        baud_rate: int = 9600,
        danger_threshold: float = 10.0
    ):
        """
        Initialize the proof system.
        
        Args:
            port: Serial port for Arduino connection
            baud_rate: Serial communication speed
            danger_threshold: TRIG6 danger threshold
        """
        self.port = port
        self.baud_rate = baud_rate
        self.engine = TRIG6Engine(danger_threshold=danger_threshold)
        self.serial_conn = None
        self.simulation_mode = False  # True for testing without hardware
    
    def connect(self) -> bool:
        """
        Establish serial connection to Arduino.
        
        Returns:
            True if connection successful, False otherwise
        """
        if not SERIAL_AVAILABLE:
            print("⚠️  Serial library not available. Entering simulation mode.")
            self.simulation_mode = True
            return True
        
        try:
            self.serial_conn = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"✅ Connected to Arduino on {self.port}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("⚠️  Entering simulation mode.")
            self.simulation_mode = True
            return True
    
    def read_potentiometer(self) -> float:
        """
        Read normalized potentiometer value (0.0 to 1.0).
        
        Returns:
            Normalized potentiometer reading
        """
        if self.simulation_mode:
            # Simulate with sine wave for demonstration
            return (math.sin(time.time()) + 1) / 2
        
        try:
            line = self.serial_conn.readline().decode('utf-8').strip()
            raw_value = int(line)
            normalized = raw_value / 1023.0
            return max(0.0, min(1.0, normalized))
        except Exception as e:
            print(f"Error reading potentiometer: {e}")
            return 0.5  # Default to middle value
    
    def prove_recipe(
        self,
        recipe: Recipe,
        mode: str = PotentiometerMode.MODE_NOISE,
        threshold: float = 0.50,
        max_attempts: int = 100,
        variation_range: float = 0.2
    ) -> Optional[TRIG6State]:
        """
        Loop until pot-driven simulation achieves stable fitness.
        
        Args:
            recipe: Material recipe to prove
            mode: Potentiometer mapping mode
            threshold: Fitness threshold for success
            max_attempts: Maximum attempts before giving up
            variation_range: ±range for parameter variation
        
        Returns:
            TRIG6State if stable basin found, None otherwise
        """
        print(f"\n{'='*70}")
        print(f"PROVING RECIPE: {recipe.name} ({recipe.id})")
        print(f"Mode: {mode} | Threshold: f≥{threshold:.2f}")
        print(f"{'='*70}\n")
        
        attempts = 0
        best_state = None
        best_fitness = -1
        
        while attempts < max_attempts:
            pot_norm = self.read_potentiometer()
            
            # Map potentiometer to TRIG6 parameter based on mode
            if mode == PotentiometerMode.MODE_NOISE:
                N = recipe.N_base + (pot_norm - 0.5) * variation_range
                N = max(0.0, min(1.0, N))
                theta = math.pi / 6  # Default theta
                D = recipe.D_base
            elif mode == PotentiometerMode.MODE_THETA:
                theta = pot_norm * 2 * math.pi
                N = recipe.N_base
                D = recipe.D_base
            elif mode == PotentiometerMode.MODE_DRIFT:
                D = recipe.D_base + (pot_norm - 0.5) * variation_range
                D = max(0.0, min(1.0, D))
                theta = math.pi / 6
                N = recipe.N_base
            elif mode == PotentiometerMode.MODE_ALPHA:
                # Alpha doesn't affect fitness calculation in current model
                theta = math.pi / 6
                N = recipe.N_base
                D = recipe.D_base
            else:
                raise ValueError(f"Unknown mode: {mode}")
            
            # Evaluate state
            state = self.engine.evaluate(
                theta=theta,
                R=recipe.R_base,
                D=D,
                N=N,
                eq=recipe.eq
            )
            
            # Track best state
            if state.fitness > best_fitness:
                best_fitness = state.fitness
                best_state = state
            
            # Check for success
            if state.fitness >= threshold and not state.danger:
                print(f"✅ PROOF ACHIEVED at attempt {attempts + 1}/{max_attempts}")
                print(f"   Potentiometer: {pot_norm:.3f}")
                print(f"   θ={state.theta:.3f}, R={state.R:.2f}, D={state.D:.2f}, N={state.N:.2f}")
                print(f"   Fitness: f={state.fitness:.3f}")
                print(f"   Danger: {'Yes' if state.danger else 'No'}")
                return state
            
            # Progress indicator
            if (attempts + 1) % 10 == 0:
                print(f"  Attempt {attempts + 1}/{max_attempts} - "
                      f"Best fitness: {best_fitness:.3f}")
            
            attempts += 1
            time.sleep(0.1)  # Small delay between readings
        
        print(f"\n❌ No stable basin found after {max_attempts} attempts")
        if best_state:
            print(f"   Best fitness achieved: {best_fitness:.3f}")
            print(f"   (Required: {threshold:.2f})")
        
        return None
    
    def disconnect(self):
        """Close serial connection."""
        if self.serial_conn:
            self.serial_conn.close()
            print("Disconnected from Arduino")


# Recipe Database - 36 Material Blueprints
RECIPES = {
    # SECTION I: PAPER SIMULATIONS (12)
    'PAPER-REED-001': Recipe('Classic Reed Papyrus', 'PAPER-REED-001', 0.82, 0.18, 0.22, 0.95),
    'PAPER-LIME-002': Recipe('Lime-Infused Papyrus', 'PAPER-LIME-002', 0.86, 0.14, 0.20, 0.98),
    'PAPER-GRASS-003': Recipe('Grass Adaptation', 'PAPER-GRASS-003', 0.78, 0.22, 0.28, 0.90),
    'PAPER-BAMBOO-004': Recipe('Bamboo Hybrid', 'PAPER-BAMBOO-004', 0.80, 0.20, 0.25, 0.92),
    'PAPER-BANANA-005': Recipe('Banana Stem', 'PAPER-BANANA-005', 0.75, 0.25, 0.30, 0.88),
    'PAPER-COTTON-006': Recipe('Cotton Rag', 'PAPER-COTTON-006', 0.88, 0.12, 0.18, 1.0),
    'PAPER-HEMP-007': Recipe('Hemp Fiber', 'PAPER-HEMP-007', 0.85, 0.15, 0.20, 0.95),
    'PAPER-MULBERRY-008': Recipe('Mulberry Bark', 'PAPER-MULBERRY-008', 0.83, 0.17, 0.22, 0.94),
    'PAPER-RICE-009': Recipe('Rice Straw', 'PAPER-RICE-009', 0.76, 0.24, 0.28, 0.88),
    'PAPER-CORN-010': Recipe('Corn Husk', 'PAPER-CORN-010', 0.72, 0.28, 0.32, 0.85),
    'PAPER-BAGASSE-011': Recipe('Sugarcane Bagasse', 'PAPER-BAGASSE-011', 0.74, 0.26, 0.30, 0.87),
    'PAPER-RECYCLED-012': Recipe('Recycled Fiber', 'PAPER-RECYCLED-012', 0.80, 0.20, 0.24, 0.92),
    
    # SECTION III: MATERIAL SIMULATIONS (12) - Selected examples
    'MAT-WHEAT-025': Recipe('Wheat Starch Glue', 'MAT-WHEAT-025', 0.86, 0.14, 0.20, 0.98),
    'MAT-ACACIA-028': Recipe('Acacia Tannin', 'MAT-ACACIA-028', 0.65, 0.35, 0.40, 0.88, 'MEDIUM'),
    'MAT-CHROME-035': Recipe('Chrome-Tanned Leather', 'MAT-CHROME-035', 0.55, 0.45, 0.40, 0.85, 'HIGH'),
}


def main():
    """Example usage of potentiometer proof system."""
    print("=" * 70)
    print("TRIG6 POTENTIOMETER PROOF SYSTEM")
    print("=" * 70)
    
    # Initialize proof system
    proof_system = TRIG6ProofSystem(
        port='COM3',  # Change to your Arduino port
        baud_rate=9600,
        danger_threshold=10.0
    )
    
    # Connect to Arduino
    proof_system.connect()
    
    try:
        # Example 1: Prove Classic Reed Papyrus with noise variation
        papyrus = RECIPES['PAPER-REED-001']
        result = proof_system.prove_recipe(
            recipe=papyrus,
            mode=PotentiometerMode.MODE_NOISE,
            threshold=0.50,
            max_attempts=50
        )
        
        # Example 2: Prove Cotton Rag (highest fitness)
        print("\n" + "=" * 70)
        cotton = RECIPES['PAPER-COTTON-006']
        result = proof_system.prove_recipe(
            recipe=cotton,
            mode=PotentiometerMode.MODE_NOISE,
            threshold=0.60,
            max_attempts=50
        )
        
    finally:
        proof_system.disconnect()
    
    print("\n" + "=" * 70)
    print("Proof session complete")
    print("=" * 70)


if __name__ == '__main__':
    main()
