#!/usr/bin/env python3
"""
FlameLang Integration Examples
Demonstrates integration with existing Strategickhaos systems
"""

import json
from typing import List, Dict
from dataclasses import asdict

from flamelang import (
    glyph_to_wave,
    ParadoxWeaver,
    calculate_wave_energy,
    WaveSpike
)


class SynapseBusIntegration:
    """
    Integration with SynapseBus event system
    Broadcasts wave spikes as neural events
    """
    
    def __init__(self):
        self.events = []
    
    def broadcast_spike(self, spike: WaveSpike) -> Dict:
        """
        Convert wave spike to SynapseBus event format
        
        Args:
            spike: WaveSpike to broadcast
        
        Returns:
            Event dictionary
        """
        event = {
            'type': 'wave_spike',
            'timestamp': 'ISO-8601-timestamp',
            'source': 'flamelang',
            'data': {
                'input': spike.input,
                'glyphs': spike.glyphs,
                'frequencies': spike.frequencies,
                'mean_frequency': spike.metadata['mean_frequency'],
                'energy': calculate_wave_energy(spike)['total_energy']
            }
        }
        
        self.events.append(event)
        return event
    
    def get_event_stream(self) -> List[Dict]:
        """Get all broadcasted events"""
        return self.events


class EventHorizonVisualizer:
    """
    Integration with EventHorizon UI
    Generates visualization data for wave dashboards
    """
    
    @staticmethod
    def format_for_dashboard(spike: WaveSpike) -> Dict:
        """
        Format wave spike for EventHorizon dashboard
        
        Args:
            spike: WaveSpike to visualize
        
        Returns:
            Dashboard data structure
        """
        energy = calculate_wave_energy(spike)
        
        return {
            'title': f"Wave: {spike.input}",
            'visualization': {
                'type': 'wave_spectrum',
                'data': {
                    'frequencies': spike.frequencies,
                    'amplitudes': spike.amplitudes,
                    'energy_levels': energy['individual_energies']
                }
            },
            'metadata': spike.metadata,
            'stats': {
                'glyph_count': len(spike.glyphs),
                'mean_frequency': spike.metadata['mean_frequency'],
                'total_energy': energy['total_energy'],
                'compression_ratio': spike.metadata['compression_ratio']
            }
        }


class ARSSovereignPackage:
    """
    Integration with ARS (Adaptive Reasoning System) Sovereign Package
    Compresses data using FlameLang encoding
    """
    
    @staticmethod
    def compress_text(text: str, script: str = 'cuneiform') -> Dict:
        """
        Compress text using FlameLang glyph encoding
        
        Args:
            text: Text to compress
            script: Glyph script to use
        
        Returns:
            Compression result
        """
        spike = glyph_to_wave(text, script=script, include_wave_samples=False)
        
        return {
            'original': text,
            'compressed': spike.glyphs,
            'unicode_hex': spike.unicode_hex,
            'compression_ratio': spike.metadata['compression_ratio'],
            'original_size': len(text.replace(' ', '')),
            'compressed_size': len(spike.glyphs),
            'recoverable': True  # Can be decoded back
        }
    
    @staticmethod
    def create_package(data: Dict, script: str = 'cuneiform') -> Dict:
        """
        Create ARS package with FlameLang compression
        
        Args:
            data: Data dictionary to package
            script: Glyph script to use
        
        Returns:
            ARS package
        """
        # Compress text fields
        compressed_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                compressed_data[key] = ARSSovereignPackage.compress_text(value, script)
            else:
                compressed_data[key] = value
        
        return {
            'package_type': 'ARS_SOVEREIGN',
            'flamelang_version': '1.0.0',
            'script': script,
            'data': compressed_data,
            'metadata': {
                'total_fields': len(data),
                'compressed_fields': sum(1 for v in data.values() if isinstance(v, str))
            }
        }


class HackerToolParadoxResolver:
    """
    Integration with 36 Hacker Tools
    Resolves contradictions between offensive and defensive security
    """
    
    def __init__(self):
        self.weaver = ParadoxWeaver(
            script='cuneiform',
            initial_temp=100.0,
            cooling_rate=0.95,
            min_temp=0.5
        )
    
    def resolve_security_paradox(self, 
                                  offensive_tool: str,
                                  defensive_goal: str) -> Dict:
        """
        Resolve paradox between offensive tool and defensive goal
        
        Args:
            offensive_tool: Name/description of offensive security tool
            defensive_goal: Description of defensive security goal
        
        Returns:
            Resolution with creative synthesis
        """
        contradictions = [
            f"{offensive_tool} offensive capability",
            f"{defensive_goal} defensive protection"
        ]
        
        resolution = self.weaver.weave(contradictions)
        
        return {
            'offensive': offensive_tool,
            'defensive': defensive_goal,
            'synthesis': resolution.creative_output,
            'energy_reduction': resolution.metadata['energy_reduction'],
            'wave_analysis': {
                'offensive_freq': resolution.wave_spikes[0].metadata['mean_frequency'],
                'defensive_freq': resolution.wave_spikes[1].metadata['mean_frequency']
            },
            'recommendation': self._generate_recommendation(resolution)
        }
    
    def _generate_recommendation(self, resolution) -> str:
        """Generate actionable recommendation from resolution"""
        energy_reduction = resolution.metadata['energy_reduction']
        
        if energy_reduction > 0.8:
            return "High synergy detected - integrate tool into defensive framework"
        elif energy_reduction > 0.6:
            return "Moderate synergy - use tool with careful controls"
        else:
            return "Low synergy - consider alternative approaches"


class BrainArsenalSimulation:
    """
    Integration with Brain Arsenal
    Uses FlameLang waves for cognitive modeling
    """
    
    @staticmethod
    def model_cognitive_state(thoughts: List[str], script: str = 'meroitic') -> Dict:
        """
        Model cognitive state from thought patterns
        
        Args:
            thoughts: List of thought strings
            script: Glyph script to use
        
        Returns:
            Cognitive state model
        """
        spikes = [glyph_to_wave(thought, script=script, include_wave_samples=False) 
                  for thought in thoughts]
        
        # Calculate cognitive metrics
        all_frequencies = []
        for spike in spikes:
            all_frequencies.extend(spike.frequencies)
        
        return {
            'thought_count': len(thoughts),
            'cognitive_load': len(all_frequencies),
            'frequency_variance': float(sum((f - sum(all_frequencies)/len(all_frequencies))**2 
                                            for f in all_frequencies) / len(all_frequencies)),
            'dominant_frequency': float(max(all_frequencies)),
            'coherence': 1.0 / (1.0 + float(sum((f - sum(all_frequencies)/len(all_frequencies))**2 
                                                 for f in all_frequencies) / len(all_frequencies))),
            'wave_spikes': [spike.to_dict() for spike in spikes]
        }


# Example usage demonstrations
def demo_synapsebus_integration():
    """Demonstrate SynapseBus integration"""
    print("\n=== SynapseBus Integration ===\n")
    
    bus = SynapseBusIntegration()
    
    # Broadcast some spikes
    inputs = ["security event detected", "network anomaly", "threat mitigated"]
    for input_text in inputs:
        spike = glyph_to_wave(input_text, script='cuneiform')
        event = bus.broadcast_spike(spike)
        print(f"Event: {event['type']}")
        print(f"  Input: {event['data']['input']}")
        print(f"  Mean Frequency: {event['data']['mean_frequency']:.2f} Hz")
        print(f"  Energy: {event['data']['energy']:.4f}\n")
    
    print(f"Total events broadcasted: {len(bus.get_event_stream())}")


def demo_eventhorizon_integration():
    """Demonstrate EventHorizon UI integration"""
    print("\n=== EventHorizon UI Integration ===\n")
    
    spike = glyph_to_wave("Sovereignty Architecture", script='cuneiform')
    dashboard_data = EventHorizonVisualizer.format_for_dashboard(spike)
    
    print(f"Dashboard: {dashboard_data['title']}")
    print(f"\nVisualization Type: {dashboard_data['visualization']['type']}")
    print(f"\nStats:")
    for key, value in dashboard_data['stats'].items():
        print(f"  {key}: {value}")


def demo_ars_package_integration():
    """Demonstrate ARS Sovereign Package integration"""
    print("\n=== ARS Sovereign Package Integration ===\n")
    
    # Compress single text
    text = "Strategickhaos DAO sovereign architecture design"
    compressed = ARSSovereignPackage.compress_text(text)
    
    print(f"Original: {compressed['original']}")
    print(f"Compressed: {compressed['compressed']}")
    print(f"Compression Ratio: {compressed['compression_ratio']:.2f}x")
    print(f"Size: {compressed['original_size']} → {compressed['compressed_size']} chars")
    
    # Create full package
    print("\nCreating ARS Package...")
    data = {
        'title': 'FlameLang Integration',
        'description': 'Wave layer with Astropy physics',
        'version': '1.0.0'
    }
    package = ARSSovereignPackage.create_package(data)
    print(f"Package created with {package['metadata']['compressed_fields']} compressed fields")


def demo_hacker_tool_resolution():
    """Demonstrate hacker tool paradox resolution"""
    print("\n=== Hacker Tool Paradox Resolution ===\n")
    
    resolver = HackerToolParadoxResolver()
    
    # Resolve some paradoxes
    tools = [
        ("Sliver C2 framework", "secure endpoint protection"),
        ("Scapy packet crafting", "network integrity"),
        ("Bettercap MITM", "communication privacy")
    ]
    
    for offensive, defensive in tools:
        result = resolver.resolve_security_paradox(offensive, defensive)
        print(f"\nOffensive: {result['offensive']}")
        print(f"Defensive: {result['defensive']}")
        print(f"Synthesis: {result['synthesis']}")
        print(f"Recommendation: {result['recommendation']}")


def demo_brain_arsenal_integration():
    """Demonstrate Brain Arsenal cognitive modeling"""
    print("\n=== Brain Arsenal Cognitive Modeling ===\n")
    
    thoughts = [
        "analyze security threat",
        "design defense strategy",
        "implement countermeasures"
    ]
    
    cognitive_state = BrainArsenalSimulation.model_cognitive_state(thoughts)
    
    print(f"Thought Count: {cognitive_state['thought_count']}")
    print(f"Cognitive Load: {cognitive_state['cognitive_load']}")
    print(f"Dominant Frequency: {cognitive_state['dominant_frequency']:.2f} Hz")
    print(f"Coherence: {cognitive_state['coherence']:.4f}")


def main():
    """Run all integration demonstrations"""
    print("\n" + "="*70)
    print("  🔥 FLAMELANG INTEGRATION EXAMPLES 🔥")
    print("  Strategickhaos DAO LLC - System Integrations")
    print("="*70)
    
    demo_synapsebus_integration()
    demo_eventhorizon_integration()
    demo_ars_package_integration()
    demo_hacker_tool_resolution()
    demo_brain_arsenal_integration()
    
    print("\n" + "="*70)
    print("  ✓ All Integrations Demonstrated")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
