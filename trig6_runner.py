#!/usr/bin/env python3
"""
TRIG6 Runner - Integration Pipeline for Loihi EEG and Genomics
Orchestrates the complete neuralink infusion pipeline from EEG to DNA

Author: Dominic Garza (Strategickhaos DAO LLC)
Version: 1.0.0
"""

import numpy as np
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import our modules
from loihi_eeg_processor import LoihiEEGProcessor
from loihi_snn_simulator import LoihiSNNSimulator, LIFNeuronConfig, STDPConfig
from genomics_recon import GenomicsReconstructor


class TRIG6Evaluator:
    """
    TRIG6 Cognitive Metrics Evaluator
    
    Evaluates neural embeddings against TRIG6 predicates:
    - Θ (Theta): Temporal coherence
    - R: Reflexive integrity
    - I: Information density
    - G: Generative capacity
    - 6: Sixth sense (anomaly detection)
    """
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_theta(self, eeg_data: np.ndarray, embeddings: np.ndarray) -> float:
        """
        Calculate Θ (Theta) - Temporal coherence from phase-locking
        
        Args:
            eeg_data: Preprocessed EEG epochs
            embeddings: Neural embeddings from Loihi
            
        Returns:
            Theta score (0-1)
        """
        # Simplified: Use correlation between EEG channels as coherence proxy
        # In production, would use proper phase-locking value (PLV)
        
        if eeg_data.shape[0] == 0:
            return 0.0
        
        # Calculate inter-channel correlation
        flat_eeg = eeg_data.reshape(eeg_data.shape[0], -1)
        if flat_eeg.shape[1] < 2:
            return 0.0
        
        corr_matrix = np.corrcoef(flat_eeg.T)
        theta_score = float(np.mean(np.abs(corr_matrix)))
        
        return np.clip(theta_score, 0, 1)
    
    def calculate_R(self, embeddings: np.ndarray) -> float:
        """
        Calculate R - Reflexive integrity via embedding coherence
        
        Args:
            embeddings: Neural embeddings (time x features)
            
        Returns:
            R score (0-1)
        """
        if embeddings.shape[0] < 2:
            return 0.0
        
        # Calculate temporal stability (smoothness of embeddings)
        differences = np.diff(embeddings, axis=0)
        stability = 1.0 / (1.0 + np.mean(np.abs(differences)))
        
        return float(np.clip(stability, 0, 1))
    
    def calculate_I(self, embeddings: np.ndarray) -> float:
        """
        Calculate I - Information density from spike entropy
        
        Args:
            embeddings: Neural embeddings
            
        Returns:
            I score (0-1)
        """
        if embeddings.shape[0] == 0:
            return 0.0
        
        # Calculate spike entropy
        spike_counts = np.sum(embeddings > 0.5, axis=0)
        total_spikes = np.sum(spike_counts)
        
        if total_spikes == 0:
            return 0.0
        
        # Probability distribution
        probs = spike_counts / total_spikes
        probs = probs[probs > 0]  # Remove zeros
        
        # Shannon entropy
        entropy = -np.sum(probs * np.log2(probs))
        max_entropy = np.log2(len(spike_counts))
        
        if max_entropy == 0:
            return 0.0
        
        normalized_entropy = entropy / max_entropy
        
        return float(np.clip(normalized_entropy, 0, 1))
    
    def calculate_G(self, weight_history: List[np.ndarray]) -> float:
        """
        Calculate G - Generative capacity (learning stability)
        
        Args:
            weight_history: History of network weights during learning
            
        Returns:
            G score (0-1)
        """
        if len(weight_history) < 2:
            return 0.5  # Neutral if no learning occurred
        
        # Calculate weight change rate
        weight_changes = []
        for i in range(1, len(weight_history)):
            change = np.mean(np.abs(weight_history[i] - weight_history[i-1]))
            weight_changes.append(change)
        
        # Stability = inverse of change rate
        avg_change = np.mean(weight_changes)
        stability = 1.0 / (1.0 + avg_change * 10)  # Scale factor
        
        return float(np.clip(stability, 0, 1))
    
    def calculate_sixth_sense(self, embeddings: np.ndarray) -> float:
        """
        Calculate 6th sense - Anomaly detection score
        
        Args:
            embeddings: Neural embeddings
            
        Returns:
            Anomaly score (0-1, higher = more anomalous)
        """
        if embeddings.shape[0] < 3:
            return 0.0
        
        # Simple anomaly detection: Distance from mean
        mean_embedding = np.mean(embeddings, axis=0)
        distances = np.linalg.norm(embeddings - mean_embedding, axis=1)
        
        # Normalize by standard deviation
        std_distance = np.std(distances)
        if std_distance == 0:
            return 0.0
        
        # Last embedding's anomaly score
        last_distance = distances[-1]
        anomaly_score = last_distance / (std_distance + 1e-8)
        
        # Normalize to 0-1
        anomaly_normalized = 1.0 / (1.0 + np.exp(-anomaly_score + 2))
        
        return float(np.clip(anomaly_normalized, 0, 1))
    
    def evaluate(self, eeg_data: np.ndarray, embeddings: np.ndarray, 
                 weight_history: Optional[List[np.ndarray]] = None) -> Dict:
        """
        Full TRIG6 evaluation
        
        Args:
            eeg_data: EEG epochs
            embeddings: Neural embeddings from Loihi
            weight_history: Optional weight history for G calculation
            
        Returns:
            TRIG6 metrics dictionary
        """
        print("\n--- TRIG6 EVALUATION ---")
        
        theta = self.calculate_theta(eeg_data, embeddings)
        R = self.calculate_R(embeddings)
        I = self.calculate_I(embeddings)
        G = self.calculate_G(weight_history) if weight_history else 0.5
        sixth = self.calculate_sixth_sense(embeddings)
        
        print(f"  Θ (Theta - Coherence):       {theta:.3f}")
        print(f"  R (Reflexive Integrity):     {R:.3f}")
        print(f"  I (Information Density):     {I:.3f}")
        print(f"  G (Generative Capacity):     {G:.3f}")
        print(f"  6 (Sixth Sense - Anomaly):   {sixth:.3f}")
        
        # Determine cognitive state
        state = self._classify_state(theta, R, I, sixth)
        print(f"\n  Cognitive State: {state}")
        
        metrics = {
            'theta': float(theta),
            'R': float(R),
            'I': float(I),
            'G': float(G),
            'sixth_sense': float(sixth),
            'aggregate': float(np.mean([theta, R, I, G])),
            'state': state,
            'timestamp': datetime.now().isoformat()
        }
        
        return metrics
    
    def _classify_state(self, theta: float, R: float, I: float, sixth: float) -> str:
        """Classify cognitive state based on TRIG6 metrics"""
        
        # Hyperfocus: High coherence, high integrity
        if theta > 0.7 and R > 0.6:
            return "hyperfocus"
        
        # Drift: Low coherence, low integrity
        elif theta < 0.4 and R < 0.4:
            return "drift"
        
        # Burst: High information density
        elif I > 0.8:
            return "burst"
        
        # Overload: High anomaly
        elif sixth > 0.7:
            return "overload"
        
        # Balanced
        else:
            return "balanced"


class NeuralinkInfusionPipeline:
    """
    Main pipeline orchestrator for TRIG6 SAGCO-OS Neuralink Infusion
    
    Integrates:
    - EEG processing
    - Loihi neuromorphic SNN
    - TRIG6 evaluation
    - Genomics reconstruction
    """
    
    def __init__(self, config_path: str = "neuralink_infusion_pipeline.yaml"):
        """
        Initialize pipeline
        
        Args:
            config_path: Path to pipeline configuration
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize components
        self.eeg_processor = LoihiEEGProcessor(config_path)
        self.trig6_evaluator = TRIG6Evaluator()
        self.genomics_reconstructor = GenomicsReconstructor()
        
        # Results storage
        self.results = {}
        
        print("=" * 80)
        print("TRIG6 SAGCO-OS NEURALINK INFUSION PIPELINE")
        print("=" * 80)
        print(f"✓ Loaded configuration from: {config_path}")
    
    def _load_config(self) -> Dict:
        """Load pipeline configuration"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def run_full_pipeline(self, eeg_input: Optional[str] = None,
                         target_gene: Optional[str] = "SCN1A",
                         eeg_markers: Optional[List[str]] = None) -> Dict:
        """
        Run complete pipeline: EEG → Loihi → TRIG6 → Genomics
        
        Args:
            eeg_input: Path to EEG data (None for simulated)
            target_gene: Gene to analyze for genomics
            eeg_markers: Observed EEG markers for correlation
            
        Returns:
            Complete pipeline results
        """
        print("\n" + "=" * 80)
        print("STAGE 1: EEG INGEST & PREPROCESSING")
        print("=" * 80)
        
        # Process EEG
        eeg_results = self.eeg_processor.process(input_path=eeg_input)
        self.results['eeg_processing'] = eeg_results['statistics']
        
        # Save EEG outputs
        self.eeg_processor.save_output(eeg_results, "data/processed")
        
        print("\n" + "=" * 80)
        print("STAGE 2: LOIHI SNN DEPLOYMENT")
        print("=" * 80)
        
        # Get Loihi config
        loihi_stage = next((s for s in self.config['pipeline']['stages'] 
                          if s['name'] == 'loihi_deploy'), None)
        
        network_config = loihi_stage['config']['network']
        layer_sizes = [layer['neurons'] for layer in network_config['layers']]
        
        # Create Loihi simulator
        neuron_cfg = LIFNeuronConfig(
            tau_membrane=network_config['layers'][1]['tau_membrane'],
            threshold=network_config['layers'][1]['threshold'],
            refractory_period=network_config['layers'][1]['refractory_period']
        )
        
        plasticity_cfg = network_config['plasticity']
        stdp_cfg = STDPConfig(
            enabled=plasticity_cfg['enabled'],
            learning_rate=plasticity_cfg['learning_rate'],
            tau_plus=plasticity_cfg['tau_plus'],
            tau_minus=plasticity_cfg['tau_minus']
        )
        
        loihi_sim = LoihiSNNSimulator(
            layer_sizes=layer_sizes,
            neuron_config=neuron_cfg,
            stdp_config=stdp_cfg,
            dt=0.001
        )
        
        # Run spike trains through Loihi
        spike_trains = eeg_results['spike_trains']
        
        # Flatten epochs for continuous processing
        flat_spikes = spike_trains.reshape(-1, spike_trains.shape[-1])
        
        loihi_results = loihi_sim.run(flat_spikes, verbose=True)
        self.results['loihi_processing'] = loihi_results
        
        # Get embeddings
        embeddings = loihi_sim.get_embeddings()
        
        # Save Loihi outputs
        output_dir = Path("data/loihi")
        output_dir.mkdir(parents=True, exist_ok=True)
        np.save(output_dir / "neural_embeddings.npy", embeddings)
        
        loihi_sim.save_model("data/loihi/eeg_snn_model.json")
        loihi_sim.export_for_loihi_hardware("data/loihi/lava_eeg_network.py")
        
        print("\n" + "=" * 80)
        print("STAGE 3: TRIG6 EVALUATION")
        print("=" * 80)
        
        # Evaluate with TRIG6
        trig6_results = self.trig6_evaluator.evaluate(
            eeg_data=eeg_results['preprocessed'],
            embeddings=embeddings
        )
        
        self.results['trig6_evaluation'] = trig6_results
        
        # Save TRIG6 results
        trig6_dir = Path("data/trig6")
        trig6_dir.mkdir(parents=True, exist_ok=True)
        with open(trig6_dir / "eval_results.json", 'w') as f:
            json.dump(trig6_results, f, indent=2)
        
        print("\n" + "=" * 80)
        print("STAGE 4: GENOMICS RECONSTRUCTION")
        print("=" * 80)
        
        # Genomics analysis
        if not eeg_markers:
            # Infer markers from TRIG6 state
            state = trig6_results['state']
            if state == "overload":
                eeg_markers = ["gamma_excess", "hyperexcitability"]
            elif state == "drift":
                eeg_markers = ["theta_slowing", "reduced_coherence"]
            elif state == "burst":
                eeg_markers = ["spike_wave", "polyspike"]
            else:
                eeg_markers = ["normal_background"]
        
        genomics_report = self.genomics_reconstructor.generate_neurogenetic_report(
            target_gene,
            eeg_markers=eeg_markers
        )
        
        self.results['genomics_analysis'] = genomics_report
        
        # Save genomics results
        self.genomics_reconstructor.save_report(genomics_report, "data/genomics")
        
        print("\n" + "=" * 80)
        print("PIPELINE COMPLETE")
        print("=" * 80)
        
        # Generate summary
        self._generate_summary()
        
        return self.results
    
    def _generate_summary(self):
        """Generate pipeline execution summary"""
        
        print("\n" + "=" * 80)
        print("EXECUTION SUMMARY")
        print("=" * 80)
        
        # EEG Summary
        if 'eeg_processing' in self.results:
            eeg = self.results['eeg_processing']
            print(f"\n📊 EEG Processing:")
            print(f"  • Epochs: {eeg['num_epochs']}")
            print(f"  • Channels: {eeg['num_channels']}")
            print(f"  • Total spikes: {eeg['total_spikes']}")
            print(f"  • Spike rate: {eeg['spike_rate_percent']:.2f}%")
        
        # Loihi Summary
        if 'loihi_processing' in self.results:
            loihi = self.results['loihi_processing']
            print(f"\n🧠 Loihi SNN:")
            print(f"  • Output spikes: {loihi['total_output_spikes']}")
            print(f"  • Avg spike rate: {loihi['avg_spike_rate']:.2f} Hz")
            print(f"  • Power consumption: {loihi['avg_power_mw']:.4f} mW")
            print(f"  • Energy/inference: {loihi['energy_per_inference_uj']:.4f} µJ")
        
        # TRIG6 Summary
        if 'trig6_evaluation' in self.results:
            trig6 = self.results['trig6_evaluation']
            print(f"\n🎯 TRIG6 Metrics:")
            print(f"  • Θ (Coherence): {trig6['theta']:.3f}")
            print(f"  • R (Integrity): {trig6['R']:.3f}")
            print(f"  • I (Information): {trig6['I']:.3f}")
            print(f"  • G (Generative): {trig6['G']:.3f}")
            print(f"  • 6 (Anomaly): {trig6['sixth_sense']:.3f}")
            print(f"  • State: {trig6['state'].upper()}")
        
        # Genomics Summary
        if 'genomics_analysis' in self.results:
            genomics = self.results['genomics_analysis']
            if 'gene' in genomics:
                print(f"\n🧬 Genomics Analysis:")
                print(f"  • Gene: {genomics['gene']['name']}")
                print(f"  • Disease: {genomics['gene']['disease']}")
                print(f"  • Variants detected: {genomics['variants']['total_detected']}")
                print(f"  • Pathogenic: {len(genomics['variants']['pathogenic_variants'])}")
        
        print(f"\n✅ All outputs saved to data/ directory")
        print(f"🔥 TRIG6 SAGCO-OS Neuralink Infusion Pipeline Complete!")
        
        # Save complete results
        results_path = Path("data/pipeline_results.json")
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📁 Complete results: {results_path}")


def main():
    """Main execution"""
    
    # Create pipeline
    pipeline = NeuralinkInfusionPipeline("neuralink_infusion_pipeline.yaml")
    
    # Run full pipeline
    results = pipeline.run_full_pipeline(
        eeg_input=None,  # Use simulated EEG
        target_gene="SCN1A",
        eeg_markers=["spike_wave", "polyspike", "generalized_seizures"]
    )
    
    print("\n" + "=" * 80)
    print("🎉 NEURALINK INFUSION COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Review TRIG6 metrics in data/trig6/")
    print("  2. Analyze genomics report in data/genomics/")
    print("  3. Deploy to actual Loihi hardware via Lava")
    print("  4. Integrate with SAGCO-OS for cognitive augments")
    print("\n🧠🧬🔥 Bridging hardware brains to bio-code!")


if __name__ == "__main__":
    main()
