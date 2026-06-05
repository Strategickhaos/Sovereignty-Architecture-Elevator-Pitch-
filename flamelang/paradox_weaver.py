"""
Paradox Weaver: Convert Contradiction into Creation
Uses wave superposition and simulated annealing to resolve paradoxical inputs
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np

try:
    import astropy.units as u
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False
    u = None

from .wave_layer import WaveSpike, glyph_to_wave, wave_superposition


@dataclass
class ParadoxResolution:
    """
    Result of paradox resolution process
    
    Attributes:
        input_contradictions: Original contradictory inputs
        wave_spikes: Generated wave spikes for each input
        superposed_wave: Result of wave superposition
        annealed_state: Final state after simulated annealing
        creative_output: Generated creative solution
        energy_trajectory: Energy levels during annealing
        metadata: Additional resolution metadata
    """
    input_contradictions: List[str]
    wave_spikes: List[WaveSpike]
    superposed_wave: np.ndarray
    annealed_state: Dict
    creative_output: str
    energy_trajectory: List[float]
    metadata: Dict


class ParadoxWeaver:
    """
    Paradox Weaver: Quantum-inspired resolution of contradictions
    
    Treats contradictory inputs as waves in superposition, then uses simulated
    annealing to "cool" the high-entropy state into a creative solution.
    
    Based on:
    - Wave mechanics (Astropy)
    - Simulated annealing optimization
    - Quantum superposition metaphor
    """
    
    def __init__(self,
                 script: str = 'cuneiform',
                 initial_temp: float = 100.0,
                 cooling_rate: float = 0.95,
                 min_temp: float = 0.1,
                 iterations_per_temp: int = 10):
        """
        Initialize Paradox Weaver
        
        Args:
            script: Glyph script to use ('meroitic' or 'cuneiform')
            initial_temp: Starting temperature for annealing
            cooling_rate: Cooling factor (< 1.0)
            min_temp: Minimum temperature threshold
            iterations_per_temp: Iterations at each temperature
        """
        if not ASTROPY_AVAILABLE:
            raise ImportError("Astropy is required for ParadoxWeaver")
        
        self.script = script
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.iterations_per_temp = iterations_per_temp
    
    def weave(self, contradictions: List[str]) -> ParadoxResolution:
        """
        Weave contradictions into creative resolution
        
        Process:
        1. Map each contradiction to glyph → wave
        2. Superpose waves (quantum metaphor)
        3. Apply simulated annealing to high-entropy state
        4. Extract creative solution from annealed state
        
        Args:
            contradictions: List of contradictory statements/concepts
        
        Returns:
            ParadoxResolution object
        """
        # Step 1: Transform contradictions to wave spikes
        wave_spikes = []
        for contradiction in contradictions:
            spike = glyph_to_wave(
                contradiction,
                script=self.script,
                include_wave_samples=False
            )
            wave_spikes.append(spike)
        
        # Step 2: Superpose waves
        superposed = wave_superposition(wave_spikes)
        
        # Step 3: Simulated annealing
        annealed_state, energy_trajectory = self._simulated_annealing(
            superposed, wave_spikes
        )
        
        # Step 4: Generate creative output
        creative_output = self._generate_creative_solution(
            annealed_state, wave_spikes
        )
        
        # Metadata
        metadata = {
            'num_contradictions': len(contradictions),
            'total_glyphs': sum(len(spike.glyphs) for spike in wave_spikes),
            'annealing_steps': len(energy_trajectory),
            'final_energy': energy_trajectory[-1] if energy_trajectory else 0.0,
            'initial_energy': energy_trajectory[0] if energy_trajectory else 0.0,
            'energy_reduction': (
                (energy_trajectory[0] - energy_trajectory[-1]) / energy_trajectory[0]
                if energy_trajectory and energy_trajectory[0] != 0 else 0.0
            )
        }
        
        return ParadoxResolution(
            input_contradictions=contradictions,
            wave_spikes=wave_spikes,
            superposed_wave=superposed,
            annealed_state=annealed_state,
            creative_output=creative_output,
            energy_trajectory=energy_trajectory,
            metadata=metadata
        )
    
    def _simulated_annealing(self,
                            superposed_wave: np.ndarray,
                            wave_spikes: List[WaveSpike]) -> Tuple[Dict, List[float]]:
        """
        Apply simulated annealing to resolve high-entropy wave state
        
        Args:
            superposed_wave: Superposed wave array
            wave_spikes: Original wave spikes
        
        Returns:
            Tuple of (annealed_state dict, energy_trajectory list)
        """
        # Initial state: use mean frequency from all spikes
        all_frequencies = []
        for spike in wave_spikes:
            all_frequencies.extend(spike.frequencies)
        
        current_state = {
            'frequency': np.mean(all_frequencies) if all_frequencies else 500.0,
            'amplitude': 1.0,
            'phase': 0.0
        }
        
        current_energy = self._calculate_energy(current_state, superposed_wave)
        
        best_state = current_state.copy()
        best_energy = current_energy
        
        temperature = self.initial_temp
        energy_trajectory = [current_energy]
        
        # Annealing loop
        while temperature > self.min_temp:
            for _ in range(self.iterations_per_temp):
                # Generate neighbor state (small perturbation)
                neighbor_state = self._generate_neighbor(current_state)
                neighbor_energy = self._calculate_energy(neighbor_state, superposed_wave)
                
                # Acceptance probability
                delta_energy = neighbor_energy - current_energy
                
                if delta_energy < 0:
                    # Always accept better solutions
                    current_state = neighbor_state
                    current_energy = neighbor_energy
                else:
                    # Accept worse solutions with probability exp(-ΔE/T)
                    acceptance_prob = np.exp(-delta_energy / temperature)
                    if np.random.random() < acceptance_prob:
                        current_state = neighbor_state
                        current_energy = neighbor_energy
                
                # Track best solution
                if current_energy < best_energy:
                    best_state = current_state.copy()
                    best_energy = current_energy
                
                energy_trajectory.append(current_energy)
            
            # Cool down
            temperature *= self.cooling_rate
        
        return best_state, energy_trajectory
    
    def _calculate_energy(self, state: Dict, target_wave: np.ndarray) -> float:
        """
        Calculate energy of current state relative to target wave
        Uses mean squared error as energy metric
        
        Args:
            state: Current state dict with frequency, amplitude, phase
            target_wave: Target wave pattern
        
        Returns:
            Energy value (lower is better)
        """
        # Generate wave from current state
        t = np.linspace(0, 1, len(target_wave))
        generated_wave = state['amplitude'] * np.sin(
            2 * np.pi * state['frequency'] * t + state['phase']
        )
        
        # Mean squared error as energy
        energy = np.mean((generated_wave - target_wave) ** 2)
        
        return energy
    
    def _generate_neighbor(self, state: Dict) -> Dict:
        """
        Generate neighboring state with small random perturbation
        
        Args:
            state: Current state
        
        Returns:
            Neighbor state
        """
        neighbor = state.copy()
        
        # Perturb frequency (±10%)
        neighbor['frequency'] = state['frequency'] * (1 + np.random.uniform(-0.1, 0.1))
        neighbor['frequency'] = max(1.0, min(1000.0, neighbor['frequency']))  # Clamp
        
        # Perturb amplitude (±10%)
        neighbor['amplitude'] = state['amplitude'] * (1 + np.random.uniform(-0.1, 0.1))
        neighbor['amplitude'] = max(0.1, min(2.0, neighbor['amplitude']))  # Clamp
        
        # Perturb phase (±π/4)
        neighbor['phase'] = state['phase'] + np.random.uniform(-np.pi/4, np.pi/4)
        neighbor['phase'] = neighbor['phase'] % (2 * np.pi)  # Wrap to [0, 2π]
        
        return neighbor
    
    def _generate_creative_solution(self,
                                    annealed_state: Dict,
                                    wave_spikes: List[WaveSpike]) -> str:
        """
        Generate creative solution from annealed state
        
        Combines elements from original contradictions based on annealed parameters
        
        Args:
            annealed_state: Final annealed state
            wave_spikes: Original wave spikes
        
        Returns:
            Creative solution string
        """
        # Extract key frequencies from annealed state
        freq = annealed_state['frequency']
        amp = annealed_state['amplitude']
        
        # Find wave spikes closest to annealed frequency
        closest_spikes = sorted(
            wave_spikes,
            key=lambda spike: abs(np.mean(spike.frequencies) - freq)
        )
        
        # Combine elements from top matching spikes
        solution_parts = []
        for i, spike in enumerate(closest_spikes[:2]):  # Top 2
            # Extract key words from input
            words = spike.input.split()
            if words:
                # Take first and last word
                if len(words) == 1:
                    solution_parts.append(words[0])
                else:
                    solution_parts.append(words[0])
                    solution_parts.append(words[-1])
        
        # Create synthesis
        if solution_parts:
            base_solution = " + ".join(solution_parts)
            creative_output = f"Sovereign synthesis: {base_solution} → "
            creative_output += f"Resonance at {freq:.1f} Hz with amplitude {amp:.2f}"
        else:
            creative_output = f"Creative resolution at {freq:.1f} Hz"
        
        return creative_output
    
    def analyze_contradiction_space(self, contradictions: List[str]) -> Dict:
        """
        Analyze the contradiction space without full resolution
        
        Args:
            contradictions: List of contradictory statements
        
        Returns:
            Analysis dictionary with metrics
        """
        # Generate wave spikes
        wave_spikes = []
        for contradiction in contradictions:
            spike = glyph_to_wave(contradiction, script=self.script, include_wave_samples=False)
            wave_spikes.append(spike)
        
        # Calculate metrics
        all_frequencies = []
        for spike in wave_spikes:
            all_frequencies.extend(spike.frequencies)
        
        frequency_variance = np.var(all_frequencies) if all_frequencies else 0.0
        frequency_range = (
            np.ptp(all_frequencies) if all_frequencies else 0.0
        )
        
        return {
            'num_contradictions': len(contradictions),
            'total_glyphs': sum(len(spike.glyphs) for spike in wave_spikes),
            'frequency_variance': frequency_variance,
            'frequency_range': frequency_range,
            'mean_frequency': np.mean(all_frequencies) if all_frequencies else 0.0,
            'entropy_estimate': frequency_variance / (frequency_range + 1e-10),
            'wave_spikes': wave_spikes
        }
