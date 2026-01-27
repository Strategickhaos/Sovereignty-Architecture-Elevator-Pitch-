#!/usr/bin/env python3
"""
SAGCO Decrypt Sim - Linear Elamite Gematria Simulation
Phase 4.22: TRIG6 Linear Elamite Sim Extension

This module simulates gematria mappings for ancient scripts (Linear Elamite, Proto-Cuneiform)
and projects them to TRIG6 metrics for structure detection and evolution.

Mathematical Formalization:
- Gematria Mapping: G(l) = Σ v(l_j), where v(l_j) = tanh(tan θ) · cos(e_sym, e_hebrew)
- TRIG6 Projection: m = r · (1-d) · (1-n) · eq, θ = G(l) mod (2π)
"""

import math
import random
import argparse
import json
from typing import List, Dict, Tuple


class LinearElamiteSimulator:
    """Simulator for Linear Elamite gematria and TRIG6 projection"""
    
    def __init__(self):
        # Gematria mappings inspired by Hebrew numerology
        # Values range from 1-400 for different sign components
        self.gematria_base = {
            'aleph': 1, 'bet': 2, 'gimel': 3, 'dalet': 4, 'he': 5,
            'vav': 6, 'zayin': 7, 'chet': 8, 'tet': 9, 'yod': 10,
            'kaf': 20, 'lamed': 30, 'mem': 40, 'nun': 50, 'samech': 60,
            'ayin': 70, 'pe': 80, 'tsadi': 90, 'qof': 100, 'resh': 200,
            'shin': 300, 'tav': 400
        }
        
        # Linear Elamite sign mappings (placeholder values from partial deciphers)
        self.elamite_signs = {
            'Pu-zu-r': 200 + 6 + 200,  # 406
            'I-n-shu-shi-na-k': 10 + 50 + 300 + 300 + 50 + 1 + 20,  # 731
            'Shi-l-ha-ha': 300 + 10 + 30 + 5 + 5,  # 350
            'E-ba-r-ti': 5 + 2 + 1 + 200 + 400 + 10,  # 618
            'Na-pi-r-ri-sha': 50 + 1 + 80 + 10 + 200 + 200 + 10 + 300 + 5,  # 856
            'Ha-ta-m-ti': 5 + 1 + 400 + 1 + 40 + 400 + 10,  # 857
            'Kuk-Kirmash': 20 + 6 + 20 + 20 + 10 + 200 + 40 + 1 + 300,  # 617
            'Hutelutush-Inshushinak': 5 + 6 + 400 + 5 + 30 + 6 + 400 + 6 + 300 + 10 + 50 + 300 + 6 + 300 + 10 + 50 + 1 + 20,  # 1905
            'Shilhak-Inshushinak': 300 + 10 + 30 + 5 + 1 + 20 + 10 + 50 + 300 + 6 + 300 + 10 + 50 + 1 + 20,  # 1113
            'Temti-Agun': 400 + 5 + 40 + 400 + 10 + 1 + 3 + 6 + 50,  # 915
        }
        
        # Proto-Cuneiform baseline (higher noise, accounting signs)
        self.proto_cuneiform_signs = {
            'ŠE': 10,  # barley
            'UDU': 10,  # sheep
            'DU₇': 10,
            'SAL': 10,
            'SUH₃': 10,
            'NIGIN': 10,
            'ERIN': 10,
            'KU₆': 15,
            'DIN': 15,
            'BULUG': 15,
            'NI₂': 15,
            'IGI': 15,
        }
    
    def compute_gematria(self, signs: List[str], script_type: str = 'elamite') -> int:
        """
        Compute gematria sum for a sequence of signs
        
        Args:
            signs: List of sign strings
            script_type: 'elamite' or 'proto_cuneiform'
        
        Returns:
            Total gematria value
        """
        total = 0
        sign_map = self.elamite_signs if script_type == 'elamite' else self.proto_cuneiform_signs
        
        for sign in signs:
            if sign in sign_map:
                total += sign_map[sign]
            else:
                # Unknown signs get random value 1-100
                total += random.randint(1, 100)
        
        return total
    
    def trig6_projection(self, gematria_sum: int) -> Dict[str, float]:
        """
        Project gematria sum to TRIG6 metrics
        
        Formula: θ = G(l) mod (2π)
                 r = cos(θ) (resonance)
                 d = sin(θ) (drift)
                 n = pictographic_noise (0-1)
                 eq = vital_equivalence (0-1)
                 m = r · (1-d) · (1-n) · eq (fitness metric)
        
        Args:
            gematria_sum: Total gematria value
        
        Returns:
            Dictionary of TRIG6 metrics
        """
        # Compute theta from gematria sum
        theta = (gematria_sum % (2 * math.pi * 100)) / 100.0  # Scale to 2π range
        
        # Compute base metrics
        r = abs(math.cos(theta))  # Resonance (pattern alignment)
        d = abs(math.sin(theta))  # Drift (temporal shift)
        
        # Noise estimation (random for undeciphered portions)
        # Lower for structured scripts, higher for proto-writing
        n = random.uniform(0.3, 0.7)
        
        # Vital equivalence (pattern consistency)
        eq = random.uniform(0.4, 0.8)
        
        # Fitness metric
        fitness = r * (1 - d) * (1 - n) * eq
        
        # Danger metric (tan infinity risk at π/2)
        danger = abs(math.tan(theta)) if abs(theta - math.pi/2) > 0.1 else 10.0
        
        return {
            'theta': round(theta, 2),
            'resonance': round(r, 2),
            'drift': round(d, 2),
            'noise': round(n, 2),
            'equivalence': round(eq, 2),
            'fitness': round(fitness, 3),
            'danger': round(danger, 2)
        }
    
    def simulate(self, signs: List[str], script_type: str = 'elamite') -> Dict:
        """
        Run full simulation on sign sequence
        
        Args:
            signs: List of sign strings
            script_type: 'elamite' or 'proto_cuneiform'
        
        Returns:
            Complete simulation results
        """
        gematria_sum = self.compute_gematria(signs, script_type)
        metrics = self.trig6_projection(gematria_sum)
        
        return {
            'signs': signs,
            'script_type': script_type,
            'gematria_sum': gematria_sum,
            'metrics': metrics
        }
    
    def mutate_mapping(self, sign: str, current_value: int, 
                       mutation_rate: float = 0.1) -> int:
        """
        Mutate gematria value for evolution
        
        Args:
            sign: Sign string
            current_value: Current gematria value
            mutation_rate: Probability of mutation
        
        Returns:
            Mutated value or original
        """
        if random.random() < mutation_rate:
            # Small perturbation ±20%
            delta = int(current_value * random.uniform(-0.2, 0.2))
            new_value = max(1, current_value + delta)
            return new_value
        return current_value
    
    def explain_gematria(self, signs: List[str], script_type: str = 'elamite') -> str:
        """
        Generate explanation of gematria computation
        
        Args:
            signs: List of sign strings
            script_type: 'elamite' or 'proto_cuneiform'
        
        Returns:
            Human-readable explanation
        """
        sign_map = self.elamite_signs if script_type == 'elamite' else self.proto_cuneiform_signs
        explanation = []
        
        for sign in signs:
            value = sign_map.get(sign, random.randint(1, 100))
            explanation.append(f"{sign}={value}")
        
        total = self.compute_gematria(signs, script_type)
        breakdown = " + ".join(explanation)
        reduced = total % 9 if total % 9 != 0 else 9
        
        return f"{breakdown} = {total} (reduced {reduced})"


def main():
    """Main CLI for simulation"""
    parser = argparse.ArgumentParser(
        description='SAGCO Decrypt Sim - Linear Elamite Gematria Simulation'
    )
    parser.add_argument(
        '--scripts',
        type=str,
        default='linear_elamite proto_cuneiform',
        help='Space-separated script types to simulate'
    )
    parser.add_argument(
        '--mutate',
        action='store_true',
        help='Enable mutation mode for evolution'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output JSON file path'
    )
    
    args = parser.parse_args()
    
    sim = LinearElamiteSimulator()
    results = []
    
    print("=" * 80)
    print("SAGCO DECRYPT SIM - Phase 4.22: TRIG6 Linear Elamite Gematria")
    print("=" * 80)
    
    # Run Linear Elamite simulation
    if 'linear_elamite' in args.scripts:
        print("\n[LINEAR ELAMITE SIMULATION]")
        elamite_signs = list(sim.elamite_signs.keys())
        result = sim.simulate(elamite_signs, 'elamite')
        
        print(f"Simulated Linear Elamite text: {result['signs']}")
        print(f"Gematria sum: {result['gematria_sum']}")
        print(f"Theta: {result['metrics']['theta']} (low tan)")
        print(f"Metrics: R={result['metrics']['resonance']}, "
              f"D={result['metrics']['drift']}, "
              f"N={result['metrics']['noise']}, "
              f"eq={result['metrics']['equivalence']}")
        print(f"Fitness: {result['metrics']['fitness']}")
        print(f"Danger: {result['metrics']['danger']}")
        
        results.append(result)
    
    # Run Proto-Cuneiform baseline
    if 'proto_cuneiform' in args.scripts:
        print("\n[PROTO-CUNEIFORM BASELINE]")
        proto_signs = list(sim.proto_cuneiform_signs.keys())[:5]
        result = sim.simulate(proto_signs, 'proto_cuneiform')
        
        print(f"Simulated Proto-Cuneiform text: {result['signs']}")
        print(f"Gematria sum: {result['gematria_sum']}")
        print(f"Metrics: R={result['metrics']['resonance']}, "
              f"D={result['metrics']['drift']}, "
              f"N={result['metrics']['noise']}, "
              f"eq={result['metrics']['equivalence']}")
        print(f"Fitness: {result['metrics']['fitness']}")
        
        results.append(result)
    
    # Mutation mode
    if args.mutate:
        print("\n[MUTATION MODE]")
        print("Evolving gematria mappings...")
        
        # Simulate mutation on first 3 elamite signs
        for sign in list(sim.elamite_signs.keys())[:3]:
            current = sim.elamite_signs[sign]
            mutated = sim.mutate_mapping(sign, current, mutation_rate=0.5)
            if mutated != current:
                print(f"  {sign}: {current} -> {mutated}")
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults written to {args.output}")
    
    print("\n" + "=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
