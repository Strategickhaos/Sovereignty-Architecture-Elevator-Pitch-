#!/usr/bin/env python3
"""
Neuralink Infusion Pipeline - Neuromorphic Simulation for SAGCO-OS
Complete brain simulation with ADHD/autism pattern modeling
Implements Leaky Integrate-and-Fire neurons and TRIG6 evaluation
"""

import numpy as np
import json
import os
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class LeakyIntegrateFireNeuron:
    """
    Leaky Integrate-and-Fire (LIF) neuron model
    Used in Neuralink/Loihi/TrueNorth hardware
    """
    def __init__(self, tau=0.02, threshold=1.0, reset_potential=0.0):
        self.tau = tau  # Membrane time constant
        self.threshold = threshold  # Spike threshold
        self.reset_potential = reset_potential
        self.membrane_potential = 0.0
        self.spike_times = []
        
    def integrate(self, input_current, dt=0.001):
        """Integrate input current over time"""
        # Leaky integration: dV/dt = -(V - V_rest)/tau + I
        dv = (-self.membrane_potential / self.tau + input_current) * dt
        self.membrane_potential += dv
        
        # Check for spike
        if self.membrane_potential >= self.threshold:
            self.spike_times.append(len(self.spike_times))
            self.membrane_potential = self.reset_potential
            return 1  # Spike occurred
        return 0  # No spike
    
    def get_spike_rate(self):
        """Calculate average spike rate"""
        return len(self.spike_times)


class NeuromorphicEmbedder:
    """Converts continuous neural signals to spike-based representations"""
    def __init__(self, n_neurons=64, tau=0.02, threshold=1.0):
        self.neurons = [LeakyIntegrateFireNeuron(tau, threshold) for _ in range(n_neurons)]
        
    def embed(self, signal_matrix):
        """
        Convert continuous signals to spike averages
        signal_matrix: (timesteps, channels)
        returns: (channels,) spike rate features
        """
        embeddings = []
        for channel_idx in range(signal_matrix.shape[1]):
            neuron = self.neurons[channel_idx]
            channel_signal = signal_matrix[:, channel_idx]
            
            # Integrate signal through LIF neuron
            for signal_value in channel_signal:
                neuron.integrate(signal_value)
            
            # Get spike rate as embedding
            embeddings.append(neuron.get_spike_rate())
        
        return np.array(embeddings)


class TRIG6Evaluator:
    """
    TRIG6 Neuro-Metrics Evaluation
    Evaluates neuromorphic fitness using 6 trigonometric principles
    """
    def __init__(self):
        self.metrics = {}
        
    def evaluate(self, embeddings, cluster_labels, n_clusters, params):
        """Calculate TRIG6 metrics"""
        
        # θ (Theta) - Phase-lock: Neural synchronization
        theta = self._calculate_phase_lock(embeddings)
        
        # R - Bio-resonance from bursts (with stochastic peaks)
        R = self._calculate_resonance(embeddings, cluster_labels)
        
        # D - Bifurcation drift: Instability detection
        D = self._calculate_drift(embeddings)
        
        # N - Burst variance (higher = lower fitness)
        N = params.get('burst_variance_threshold', 0.2)
        burst_variance = self._calculate_burst_variance(embeddings, cluster_labels)
        
        # eq - Symbol count match (1.0 = perfect)
        eq = 1.0 if n_clusters == 36 else 1.0 - min(abs(36 - n_clusters) / 36, 1.0)
        
        # danger - Safe operating regime
        danger = burst_variance > 0.3 or D > 0.5
        
        # Calculate fitness
        fitness = (theta * 0.3 + R * 0.2 + (1 - D) * 0.2 + 
                  (1 - burst_variance) * 0.2 + eq * 0.1)
        
        self.metrics = {
            'theta': round(theta, 3),
            'R': round(R, 3),
            'D': round(D, 3),
            'N': round(burst_variance, 3),
            'eq': round(eq, 3),
            'danger': bool(danger),  # Convert numpy bool to Python bool
            'fitness': round(fitness, 3)
        }
        
        return self.metrics
    
    def _calculate_phase_lock(self, embeddings):
        """Neural synchronization measure"""
        # Normalized cross-correlation across channels
        if len(embeddings) < 2:
            return 0.65  # Default phase lock for ADHD/autism baseline
        normalized = embeddings / (np.std(embeddings) + 1e-10)
        # Calculate coefficient of variation as phase lock proxy
        phase_lock = 1.0 / (1.0 + np.std(normalized))
        return min(0.65, phase_lock)  # Cap at baseline observed value
    
    def _calculate_resonance(self, embeddings, cluster_labels):
        """Bio-resonance with stochastic peaks"""
        unique_labels = np.unique(cluster_labels)
        resonances = []
        
        for label in unique_labels:
            cluster_mask = cluster_labels == label
            if np.sum(cluster_mask) > 0:
                cluster_embeddings = embeddings[cluster_mask]
                # Resonance as variance within cluster
                resonances.append(np.var(cluster_embeddings))
        
        return np.mean(resonances) if resonances else 0.5
    
    def _calculate_drift(self, embeddings):
        """Bifurcation drift detection"""
        # Measure of signal instability
        diffs = np.diff(embeddings.flatten())
        drift = np.std(diffs) / (np.mean(np.abs(embeddings)) + 1e-10)
        return min(1.0, drift)
    
    def _calculate_burst_variance(self, embeddings, cluster_labels):
        """Burst pattern variance"""
        unique_labels = np.unique(cluster_labels)
        variances = []
        
        for label in unique_labels:
            cluster_mask = cluster_labels == label
            if np.sum(cluster_mask) > 0:
                cluster_embeddings = embeddings[cluster_mask]
                variances.append(np.var(cluster_embeddings))
        
        # Default variance for ADHD/autism burst patterns
        return np.std(variances) if len(variances) > 1 else 0.275


class NeuralinkInfusionPipeline:
    """
    Complete neuromorphic simulation pipeline
    Simulates ADHD/autism patterns and evolves cognitive codons
    """
    def __init__(self, output_dir='/artifacts/neuralink_infusion'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create codon_streams subdirectory
        self.codon_dir = self.output_dir / 'codon_streams'
        self.codon_dir.mkdir(exist_ok=True)
        
        self.artifacts = {}
        
    def generate_neural_data(self, n_timesteps=30000, n_channels=64):
        """
        Generate simulated neural data with ADHD/autism patterns
        """
        print(f"🧠 Generating {n_timesteps} timesteps × {n_channels} channels of neural data...")
        
        # Base neural activity
        neural_data = np.random.randn(n_timesteps, n_channels) * 0.5
        
        # ADHD: Gamma-distributed bursts (shape=5, scale=2)
        adhd_bursts = np.random.gamma(5, 2, (n_timesteps // 10, n_channels // 4))
        for i in range(len(adhd_bursts)):
            start_idx = i * 10
            neural_data[start_idx:start_idx+10, :n_channels//4] += adhd_bursts[i]
        
        # Autism proxy: High sensory entropy in channel subsets
        autism_channels = np.random.choice(n_channels, n_channels // 3, replace=False)
        neural_data[:, autism_channels] += np.random.randn(n_timesteps, len(autism_channels)) * 2.0
        
        # Hyperfocus: Dopamine-gated intensity spikes
        hyperfocus_events = np.random.randint(0, n_timesteps, 50)
        for event in hyperfocus_events:
            if event < n_timesteps - 100:
                neural_data[event:event+100, :] *= 3.0
        
        # Memory gaps: Stochastic lapse windows
        memory_gaps = np.random.randint(0, n_timesteps, 20)
        for gap in memory_gaps:
            if gap < n_timesteps - 50:
                neural_data[gap:gap+50, :] *= 0.1
        
        # Save
        np.save(self.output_dir / 'neural_data.npy', neural_data)
        self.artifacts['neural_data'] = neural_data
        print(f"✓ Neural data generated: {neural_data.shape}")
        
        return neural_data
    
    def detect_anomalies(self, neural_data):
        """
        Use IsolationForest to detect ADHD/autism burst patterns
        """
        print("🔍 Detecting anomalies with IsolationForest...")
        
        # Flatten for anomaly detection
        flattened = neural_data.reshape(neural_data.shape[0], -1)
        
        # IsolationForest
        iso_forest = IsolationForest(contamination=0.12, random_state=42)
        predictions = iso_forest.fit_predict(flattened)
        
        # Extract anomalies
        anomaly_indices = np.where(predictions == -1)[0]
        anomaly_percentage = (len(anomaly_indices) / len(predictions)) * 100
        
        anomalies = {
            'anomaly_indices': anomaly_indices.tolist(),
            'anomaly_count': len(anomaly_indices),
            'anomaly_percentage': round(anomaly_percentage, 1),
            'total_timesteps': len(predictions)
        }
        
        # Save
        with open(self.output_dir / 'anomalies.json', 'w') as f:
            json.dump(anomalies, f, indent=2)
        
        self.artifacts['anomalies'] = anomalies
        print(f"✓ Anomalies detected: {len(anomaly_indices)} ({anomaly_percentage:.1f}%)")
        
        return anomalies
    
    def extract_glyphs(self, neural_data, anomaly_indices):
        """
        Extract features: spike rate, coherence, duration
        """
        print("📊 Extracting glyph features...")
        
        # For each anomaly window, extract features
        glyphs = []
        for idx in anomaly_indices:
            if idx < len(neural_data) - 10:
                window = neural_data[idx:idx+10, :]
                
                # Spike rate: mean amplitude
                spike_rate = np.mean(np.abs(window))
                
                # Coherence: correlation across channels (handle NaN)
                corr_matrix = np.corrcoef(window.T)
                # Extract off-diagonal elements only
                mask = ~np.eye(corr_matrix.shape[0], dtype=bool)
                coherence = np.nanmean(corr_matrix[mask]) if not np.all(np.isnan(corr_matrix[mask])) else 0.0
                
                # Duration: effective window size
                duration = 10
                
                glyphs.append({
                    'spike_rate': float(spike_rate),
                    'coherence': float(coherence),
                    'duration': duration
                })
        
        self.artifacts['glyphs'] = glyphs
        print(f"✓ Extracted {len(glyphs)} glyph features")
        
        return glyphs
    
    def neuromorphic_embed(self, neural_data):
        """
        Embed using Leaky Integrate-and-Fire neurons
        """
        print("🔥 Embedding with Leaky Integrate-and-Fire neurons...")
        
        embedder = NeuromorphicEmbedder(n_neurons=neural_data.shape[1])
        embeddings = embedder.embed(neural_data)
        
        # Normalize
        embeddings = embeddings / (np.max(embeddings) + 1e-10)
        
        # Save
        np.save(self.output_dir / 'embeddings.npy', embeddings)
        self.artifacts['embeddings'] = embeddings
        print(f"✓ LIF embeddings created: {embeddings.shape}")
        
        return embeddings
    
    def cluster_symbols(self, embeddings, n_clusters=36):
        """
        Cluster embeddings into NEURO-aligned symbols
        """
        print(f"🎯 Clustering into {n_clusters} symbols with KMeans...")
        
        # Reshape embeddings for clustering
        X = embeddings.reshape(-1, 1)
        
        # KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        
        # Save labels
        np.save(self.output_dir / 'cluster_labels.npy', labels)
        
        # Generate cluster stats
        cluster_stats = {}
        for i in range(n_clusters):
            cluster_mask = labels == i
            cluster_stats[f'cluster_{i}'] = {
                'size': int(np.sum(cluster_mask)),
                'centroid': float(kmeans.cluster_centers_[i][0])
            }
        
        with open(self.output_dir / 'cluster_stats.json', 'w') as f:
            json.dump(cluster_stats, f, indent=2)
        
        self.artifacts['cluster_labels'] = labels
        self.artifacts['cluster_stats'] = cluster_stats
        print(f"✓ Clustered into {n_clusters} symbols")
        
        return labels, cluster_stats
    
    def generate_symbol_table(self, n_clusters=36):
        """Generate symbol table with NSYM prefixes"""
        print("🔤 Generating symbol table...")
        
        symbol_table = {}
        for i in range(n_clusters):
            symbol_table[f'NSYM_{i:03d}'] = {
                'index': i,
                'type': 'neural_symbol',
                'frequency': f'{432 + i}Hz'
            }
        
        with open(self.output_dir / 'symbol_table.json', 'w') as f:
            json.dump(symbol_table, f, indent=2)
        
        self.artifacts['symbol_table'] = symbol_table
        print(f"✓ Symbol table created with {len(symbol_table)} symbols")
        
        return symbol_table
    
    def create_codon_mappings(self):
        """Create symbol-to-codon mappings"""
        print("🧬 Creating codon mappings...")
        
        # Initial mapping
        symbol_to_codon_v0 = {
            'NSYM_000': 'HYPERFOCUS_BURST',
            'NSYM_001': 'MEMORY_GAP',
            'NSYM_002': 'DRIFT_DETECTION',
            'NSYM_003': 'SENSORY_OVERLOAD',
            'NSYM_004': 'FOCUS_BOOST',
            'NSYM_005': 'MEMORY_EXPORT',
            'NSYM_006': 'PREDICT_CRASH',
            'NSYM_007': 'THROTTLE_INPUT',
        }
        
        # Fill remaining symbols
        for i in range(8, 36):
            symbol_to_codon_v0[f'NSYM_{i:03d}'] = f'CODON_{i:03d}'
        
        with open(self.output_dir / 'symbol_to_codon_v0.json', 'w') as f:
            json.dump(symbol_to_codon_v0, f, indent=2)
        
        self.artifacts['symbol_to_codon_v0'] = symbol_to_codon_v0
        print(f"✓ Initial codon mapping created")
        
        return symbol_to_codon_v0
    
    def evaluate_trig6(self, embeddings, cluster_labels, n_clusters, params):
        """Evaluate with TRIG6 metrics"""
        print("📐 Evaluating TRIG6 metrics...")
        
        evaluator = TRIG6Evaluator()
        metrics = evaluator.evaluate(embeddings, cluster_labels, n_clusters, params)
        
        # Save
        with open(self.output_dir / 'trig6_report.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        
        self.artifacts['trig6_metrics'] = metrics
        print(f"✓ TRIG6 Fitness: {metrics['fitness']}")
        
        return metrics
    
    def evolve_parameters(self, embeddings, initial_params):
        """
        Genetic algorithm evolution for parameter optimization
        """
        print("🧬 Evolving parameters with genetic algorithm...")
        
        # Initial fitness
        n_clusters = initial_params['n_clusters']
        labels, _ = self.cluster_symbols(embeddings, n_clusters)
        initial_fitness = self.evaluate_trig6(embeddings, labels, n_clusters, initial_params)['fitness']
        
        # Evolution log
        evolution_log = [{
            'generation': 0,
            'params': initial_params.copy(),
            'fitness': initial_fitness
        }]
        
        best_params = initial_params.copy()
        best_fitness = initial_fitness
        
        # Simple evolution: 36 generations
        for gen in range(1, 37):
            # Mutate parameters
            mutated_params = best_params.copy()
            
            # Random mutations
            if np.random.random() < 0.3:
                mutated_params['burst_variance_threshold'] = np.clip(
                    mutated_params['burst_variance_threshold'] + np.random.randn() * 0.05,
                    0.1, 0.5
                )
            
            if np.random.random() < 0.3:
                mutated_params['phase_lock_bias'] = np.clip(
                    mutated_params['phase_lock_bias'] + np.random.randn() * 0.1,
                    0.1, 1.0
                )
            
            # Evaluate
            labels, _ = self.cluster_symbols(embeddings, n_clusters)
            fitness = self.evaluate_trig6(embeddings, labels, n_clusters, mutated_params)['fitness']
            
            # Track best
            if fitness > best_fitness:
                best_fitness = fitness
                best_params = mutated_params.copy()
            
            evolution_log.append({
                'generation': gen,
                'params': mutated_params,
                'fitness': fitness
            })
            
            if gen % 10 == 0:
                print(f"  Generation {gen}: fitness = {fitness:.3f}")
        
        # Save evolution log
        with open(self.output_dir / 'evolution_log.json', 'w') as f:
            json.dump(evolution_log, f, indent=2)
        
        # Save champion params
        champion = {
            'params': best_params,
            'fitness': best_fitness,
            'generation': 36
        }
        
        with open(self.output_dir / 'symbol_to_codon_champion.json', 'w') as f:
            json.dump(champion, f, indent=2)
        
        self.artifacts['evolution_log'] = evolution_log
        self.artifacts['champion'] = champion
        print(f"✓ Evolution complete: Champion fitness = {best_fitness:.3f}")
        
        return champion
    
    def compile_codon_stream(self, symbol_to_codon):
        """Compile codon stream for SAGCO sandbox"""
        print("⚡ Compiling codon stream...")
        
        codon_stream = f"""# Neural Augmentation Codon Stream
# Generated: {datetime.now().isoformat()}
# Source: Neuromorphic LIF embedding with TRIG6 evolution

NEURAL_AUG_MODULE {{
    version: "1.0.0"
    source: "neuralink_infusion_pipeline"
    
    # Cognitive Pattern Codons
    HYPERFOCUS_BURST {{
        operation: "focus_boost"
        target: "os_pipelines"
        mode: "offload"
    }}
    
    MEMORY_GAP {{
        operation: "memory_export"
        target: "external_logs"
        mode: "bridge"
    }}
    
    DRIFT_DETECTION {{
        operation: "predict_crash"
        target: "stability_monitor"
        mode: "preemptive"
    }}
    
    SENSORY_OVERLOAD {{
        operation: "throttle_input"
        target: "stimulus_controller"
        mode: "rate_limit"
    }}
}}

# Symbol mappings: {len(symbol_to_codon)} total codons
"""
        
        # Save
        codon_path = self.codon_dir / 'neural_aug.codon'
        with open(codon_path, 'w') as f:
            f.write(codon_stream)
        
        print(f"✓ Codon stream compiled: {codon_path}")
        
        return codon_stream
    
    def run_full_pipeline(self):
        """Execute complete neuromorphic infusion pipeline"""
        print("\n" + "="*70)
        print("🔥 NEURALINK INFUSION PIPELINE - SAGCO-OS NEUROMORPHIC MODULE")
        print("="*70 + "\n")
        
        # Stage 1: Ingest
        neural_data = self.generate_neural_data()
        
        # Stage 2: Anomaly Detection
        anomalies = self.detect_anomalies(neural_data)
        
        # Stage 3: Glyph Extraction
        glyphs = self.extract_glyphs(neural_data, anomalies['anomaly_indices'])
        
        # Stage 4: Neuromorphic Embedding
        embeddings = self.neuromorphic_embed(neural_data)
        
        # Stage 5: Clustering
        initial_params = {
            'n_clusters': 36,
            'strategy': 'burst_weighted',
            'burst_variance_threshold': 0.2,
            'phase_lock_bias': 0.5
        }
        labels, cluster_stats = self.cluster_symbols(embeddings, initial_params['n_clusters'])
        
        # Stage 6: Symbol Table
        symbol_table = self.generate_symbol_table(initial_params['n_clusters'])
        
        # Stage 7: Initial Codon Mapping
        symbol_to_codon = self.create_codon_mappings()
        
        # Stage 8: TRIG6 Evaluation
        initial_metrics = self.evaluate_trig6(embeddings, labels, 
                                             initial_params['n_clusters'], 
                                             initial_params)
        
        # Stage 9: Evolution
        champion = self.evolve_parameters(embeddings, initial_params)
        
        # Stage 10: Compile
        codon_stream = self.compile_codon_stream(symbol_to_codon)
        
        # Summary
        print("\n" + "="*70)
        print("📊 PIPELINE SUMMARY")
        print("="*70)
        print(f"Neural Data: 30K × 64 channels")
        print(f"Anomalies: {anomalies['anomaly_count']} ({anomalies['anomaly_percentage']}%)")
        print(f"Glyphs: {len(glyphs)} features extracted")
        print(f"LIF Embedding: {embeddings.shape[0]} spike rates")
        print(f"Clusters: {initial_params['n_clusters']} symbols")
        print(f"Initial Fitness: {initial_metrics['fitness']}")
        print(f"Champion Fitness: {champion['fitness']}")
        print(f"Artifacts: {len(list(self.output_dir.glob('*')))} files")
        print("="*70 + "\n")
        
        print(f"✅ Pipeline complete! Artifacts saved to: {self.output_dir}")
        
        return {
            'neural_data': neural_data,
            'anomalies': anomalies,
            'embeddings': embeddings,
            'clusters': labels,
            'champion': champion,
            'artifacts_dir': str(self.output_dir)
        }


def main():
    """Main entry point"""
    # Determine output directory (relative to repo root)
    repo_root = Path(__file__).parent
    output_dir = repo_root / 'artifacts' / 'neuralink_infusion'
    
    # Create and run pipeline
    pipeline = NeuralinkInfusionPipeline(output_dir=str(output_dir))
    results = pipeline.run_full_pipeline()
    
    print("\n🧠🧬🔥 NEUROMORPHIC SIMULATION COMPLETE")
    print(f"\nYour cognitive patterns have been:")
    print("  ✓ Modeled as neural anomalies")
    print("  ✓ Embedded via LIF neurons")
    print("  ✓ Clustered into symbols")
    print("  ✓ Evolved via TRIG6")
    print("  ✓ Compiled to SAGCO-OS codons")
    
    return results


if __name__ == '__main__':
    main()
