#!/usr/bin/env python3
"""
Neuralink Infusion Pipeline Runner
TRIG6 SAGCO-OS Brain-Computer Interface Simulation
Author: Domenic Gabriel Garza (Strategickhaos DAO LLC)
Version: 1.0.0

Simulates BCI augmentation for ADHD/Autism patterns by:
1. Generating synthetic neural data (ADHD bursts, autism patterns)
2. Extracting neural glyphs from simulated brain signals
3. Clustering patterns into symbols
4. Mapping to augmented codons
5. Evolving via TRIG6 evaluation
6. Emitting OS-actionable augmentations
"""

import os
import sys
import json
import yaml
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import argparse

import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy.stats import gamma, entropy
from scipy.signal import hilbert, butter, filtfilt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class NeuralDataSimulator:
    """Simulate BCI neural data with ADHD/Autism characteristics"""
    
    # Configurable parameters for neural simulation
    HYPERFOCUS_THRESHOLD = 0.98  # Probability threshold for hyperfocus events
    SPIKE_THRESHOLD = 2.0        # Standard deviations above mean for spike detection
    
    def __init__(self, channels: int = 1024, sampling_rate: int = 1000, seed: int = 2026):
        self.channels = channels
        self.sampling_rate = sampling_rate
        np.random.seed(seed)
        logger.info(f"Initialized Neural Simulator: {channels} channels @ {sampling_rate} Hz")
    
    def generate_adhd_bursts(self, duration_sec: float = 300) -> np.ndarray:
        """
        Generate ADHD-like burst patterns using Gamma distribution
        High variance bursts modeling attention fluctuations
        """
        n_samples = int(duration_sec * self.sampling_rate)
        
        # Base signal with low-frequency drift (attention waning)
        t = np.linspace(0, duration_sec, n_samples)
        drift = 0.5 * np.sin(2 * np.pi * 0.05 * t)  # 0.05 Hz drift
        
        # ADHD burst noise - Gamma distribution for positive bursts
        shape, scale = 2.0, 0.5
        burst_noise = np.random.gamma(shape, scale, (n_samples, self.channels))
        
        # Add occasional hyperfocus peaks
        hyperfocus_events = np.random.rand(n_samples, self.channels) > self.HYPERFOCUS_THRESHOLD
        burst_noise[hyperfocus_events] *= 3.0
        
        # Combine drift and bursts
        neural_signal = drift[:, np.newaxis] + burst_noise
        
        logger.info(f"Generated ADHD burst data: {neural_signal.shape}")
        return neural_signal.astype(np.float32)
    
    def add_autism_patterns(self, signal: np.ndarray) -> np.ndarray:
        """
        Add autism-characteristic patterns:
        - Heightened sensory sensitivity (high entropy in certain channels)
        - Pattern recognition (strong coherence in subsets)
        """
        # Sensory overload channels (random subset)
        n_overload = int(0.15 * self.channels)
        overload_channels = np.random.choice(self.channels, n_overload, replace=False)
        signal[:, overload_channels] *= np.random.uniform(1.5, 2.5, n_overload)
        
        # Pattern recognition - add coherent oscillations to subsets
        n_coherent = int(0.2 * self.channels)
        coherent_channels = np.random.choice(self.channels, n_coherent, replace=False)
        t = np.arange(signal.shape[0]) / self.sampling_rate
        theta_osc = 0.3 * np.sin(2 * np.pi * 6 * t)  # 6 Hz theta rhythm
        signal[:, coherent_channels] += theta_osc[:, np.newaxis]
        
        logger.info(f"Added autism patterns: {n_overload} overload + {n_coherent} coherent channels")
        return signal
    
    def simulate(self, duration_sec: float = 300) -> np.ndarray:
        """Generate complete neural simulation"""
        logger.info(f"Starting neural simulation: {duration_sec}s")
        signal = self.generate_adhd_bursts(duration_sec)
        signal = self.add_autism_patterns(signal)
        logger.info(f"Neural simulation complete: {signal.shape}")
        return signal


class NeuralGlyphExtractor:
    """Extract glyphs (features) from neural signals"""
    
    # Configurable parameters for feature extraction
    SPIKE_THRESHOLD = 2.0       # Standard deviations above mean
    ANOMALY_WINDOW_SIZE = 1000  # Samples per anomaly window
    MAX_ANOMALIES = 100         # Maximum anomalies to process
    ENTROPY_BINS = 20           # Bins for entropy calculation
    ENTROPY_EPSILON = 1e-10     # Epsilon for numerical stability
    
    def __init__(self, sampling_rate: int = 1000):
        self.sampling_rate = sampling_rate
    
    def compute_spike_rate(self, signal: np.ndarray, threshold: float = None) -> np.ndarray:
        """
        Compute spike rate (threshold crossings per second)
        
        Args:
            signal: Neural signal array (time x channels)
            threshold: Spike detection threshold in standard deviations above mean.
                      If None, uses class default SPIKE_THRESHOLD.
        
        Returns:
            Array of spike rates (Hz) per channel
        """
        if threshold is None:
            threshold = self.SPIKE_THRESHOLD
        spikes = signal > threshold
        return spikes.sum(axis=0) / (signal.shape[0] / self.sampling_rate)
    
    def compute_phase_coherence(self, signal: np.ndarray) -> np.ndarray:
        """Compute phase coherence using Hilbert transform"""
        # Bandpass filter for theta (4-8 Hz)
        nyq = self.sampling_rate / 2
        low, high = 4 / nyq, 8 / nyq
        b, a = butter(4, [low, high], btype='band')
        
        coherence = []
        for ch in range(signal.shape[1]):
            filtered = filtfilt(b, a, signal[:, ch])
            analytic = hilbert(filtered)
            phase = np.angle(analytic)
            # Phase coherence as circular variance
            coh = 1 - np.var(np.exp(1j * phase))
            coherence.append(coh)
        
        return np.array(coherence)
    
    def compute_burst_duration(self, signal: np.ndarray, threshold: float = None) -> np.ndarray:
        """
        Average burst duration per channel
        
        Args:
            signal: Neural signal array (time x channels)
            threshold: Burst detection threshold. If None, uses class default.
        
        Returns:
            Array of average burst durations (seconds) per channel
        """
        if threshold is None:
            threshold = self.SPIKE_THRESHOLD
        durations = []
        for ch in range(signal.shape[1]):
            above = signal[:, ch] > threshold
            # Find consecutive runs
            diff = np.diff(np.concatenate([[0], above.astype(int), [0]]))
            starts = np.where(diff == 1)[0]
            ends = np.where(diff == -1)[0]
            if len(starts) > 0:
                avg_dur = np.mean(ends - starts) / self.sampling_rate
            else:
                avg_dur = 0.0
            durations.append(avg_dur)
        
        return np.array(durations)
    
    def extract_features(self, signal: np.ndarray, anomaly_events: List[int]) -> Dict:
        """Extract all glyph features"""
        logger.info("Extracting neural glyphs...")
        
        # Focus on anomaly windows
        if len(anomaly_events) == 0:
            # Use full signal if no anomalies detected
            signal_subset = signal
        else:
            # Extract windows around anomalies
            window_size = min(self.ANOMALY_WINDOW_SIZE, signal.shape[0] // 10)
            indices = []
            for idx in anomaly_events[:self.MAX_ANOMALIES]:
                start = max(0, idx - window_size // 2)
                end = min(signal.shape[0], idx + window_size // 2)
                indices.extend(range(start, end))
            signal_subset = signal[np.unique(indices), :]
        
        features = {
            'spike_rate': self.compute_spike_rate(signal_subset),
            'phase_coherence': self.compute_phase_coherence(signal_subset),
            'burst_duration': self.compute_burst_duration(signal_subset)
        }
        
        # Stack features into matrix
        feature_matrix = np.column_stack([
            features['spike_rate'],
            features['phase_coherence'],
            features['burst_duration']
        ])
        
        logger.info(f"Extracted glyph features: {feature_matrix.shape}")
        return {'features': feature_matrix, 'metadata': features}


class TRIG6Evaluator:
    """Evaluate codon mappings using TRIG6 metrics (Neuralink-infused)"""
    
    # Configurable parameters for TRIG6 evaluation
    SPIKE_RATE_DANGER_THRESHOLD = 0.15  # Max spike rate before danger
    
    def __init__(self, config: Dict):
        self.config = config
        self.eq_target = config.get('eq_target', 0.96)
        self.danger_limit = config.get('tan_danger_limit', 8.5)
    
    def compute_metrics(self, features: Dict, mapping: Dict) -> Dict:
        """Compute TRIG6 metrics from neural features"""
        # Extract feature stats
        spike_rate = features['metadata']['spike_rate']
        phase_coherence = features['metadata']['phase_coherence']
        burst_duration = features['metadata']['burst_duration']
        
        # Neural phase lock (for theta)
        neural_phase_lock = np.mean(phase_coherence)
        theta = 2 * np.pi * neural_phase_lock
        
        # Resonance (coherence + stochastic peak)
        coherence_mean = np.mean(phase_coherence)
        stochastic_peak = np.max(spike_rate) - np.mean(spike_rate)
        R = np.clip(0.6 * coherence_mean + 0.4 * stochastic_peak, 0.0, 1.0)
        
        # Drift (attention drift + bifurcation rate)
        attention_drift = np.std(phase_coherence)
        bifurcation_rate = np.sum(np.abs(np.diff(spike_rate)) > 0.5) / len(spike_rate)
        D = np.clip(0.7 * attention_drift + 0.3 * bifurcation_rate, 0.0, 1.0)
        
        # Noise (burst variance + sensory entropy)
        burst_variance = np.var(spike_rate)
        sensory_entropy = entropy(
            np.histogram(spike_rate, bins=NeuralGlyphExtractor.ENTROPY_BINS)[0] 
            + NeuralGlyphExtractor.ENTROPY_EPSILON
        )
        sensory_entropy_norm = sensory_entropy / np.log(NeuralGlyphExtractor.ENTROPY_BINS)  # Normalize
        N = np.clip(0.5 * burst_variance + 0.5 * sensory_entropy_norm, 0.0, 1.0)
        
        # Equilibrium (simplified KL divergence approximation)
        target_mean = self.eq_target
        neural_mean = coherence_mean
        kl_approx = abs(neural_mean - target_mean)
        eq = np.clip(1.0 - kl_approx, 0.0, 1.0)
        
        # Danger predicate
        danger = bool(
            abs(np.tan(theta)) > self.danger_limit 
            or np.mean(spike_rate) > self.SPIKE_RATE_DANGER_THRESHOLD
        )
        
        # Fitness
        fitness = float(R * (1.0 - D) * (1.0 - N) * eq)
        
        metrics = {
            'theta': float(theta),
            'resonance': float(R),
            'drift': float(D),
            'noise': float(N),
            'equilibrium': float(eq),
            'danger': danger,
            'fitness': fitness,
            'neural_phase_lock': float(neural_phase_lock),
            'coherence_mean': float(coherence_mean),
            'attention_drift': float(attention_drift),
            'burst_variance': float(burst_variance),
            'sensory_entropy': float(sensory_entropy_norm)
        }
        
        logger.info(f"TRIG6 Metrics: R={R:.3f} D={D:.3f} N={N:.3f} eq={eq:.3f} fit={fitness:.3f}")
        return metrics


class NeuralinkInfusionPipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.work_dir = Path(self.config['inputs']['work_dir'])
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Loaded pipeline config: {self.config['meta']['name']}")
    
    def run_stage_ingest(self) -> np.ndarray:
        """Stage 1: Neural Data Ingest"""
        logger.info("=" * 60)
        logger.info("STAGE 1: Neural Data Ingest")
        logger.info("=" * 60)
        
        stage = next(s for s in self.config['stages'] if s['id'] == 'ingest')
        params = stage['params']
        
        simulator = NeuralDataSimulator(
            channels=params['channels'],
            seed=self.config['inputs']['random_seed']
        )
        neural_data = simulator.simulate(duration_sec=params['sim_duration_sec'])
        
        # Save neural data
        output_path = self.work_dir / 'neural_data.npy'
        np.save(output_path, neural_data)
        logger.info(f"Saved neural data: {output_path}")
        
        return neural_data
    
    def run_stage_anomaly_detect(self, neural_data: np.ndarray) -> List[int]:
        """Stage 2: Neural Anomaly Detection"""
        logger.info("=" * 60)
        logger.info("STAGE 2: Neural Anomaly Detection")
        logger.info("=" * 60)
        
        stage = next(s for s in self.config['stages'] if s['id'] == 'anomaly_detect')
        params = stage['params']
        
        # Use mean activity per timepoint for anomaly detection
        mean_activity = neural_data.mean(axis=1).reshape(-1, 1)
        
        iso_forest = IsolationForest(
            contamination=params['contamination'],
            random_state=self.config['inputs']['random_seed']
        )
        predictions = iso_forest.fit_predict(mean_activity)
        
        anomaly_indices = np.where(predictions == -1)[0].tolist()
        logger.info(f"Detected {len(anomaly_indices)} anomalies")
        
        # Save anomalies
        output_path = self.work_dir / 'anomalies.json'
        with open(output_path, 'w') as f:
            json.dump({
                'count': len(anomaly_indices),
                'indices': anomaly_indices[:1000],  # Limit for JSON size
                'contamination': params['contamination']
            }, f, indent=2)
        logger.info(f"Saved anomalies: {output_path}")
        
        return anomaly_indices
    
    def run_stage_glyph_extract(self, neural_data: np.ndarray, anomalies: List[int]) -> Dict:
        """Stage 3: Neural Glyph Extraction"""
        logger.info("=" * 60)
        logger.info("STAGE 3: Neural Glyph Extraction")
        logger.info("=" * 60)
        
        extractor = NeuralGlyphExtractor()
        features = extractor.extract_features(neural_data, anomalies)
        
        # Save features
        glyphs_dir = self.work_dir / 'glyphs' / 'raw'
        glyphs_dir.mkdir(parents=True, exist_ok=True)
        
        np.save(glyphs_dir / 'features.npy', features['features'])
        
        metadata_path = self.work_dir / 'glyphs' / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump({
                'shape': features['features'].shape,
                'feature_names': ['spike_rate', 'phase_coherence', 'burst_duration']
            }, f, indent=2)
        logger.info(f"Saved glyph metadata: {metadata_path}")
        
        return features
    
    def run_stage_glyph_embed(self, features: Dict) -> np.ndarray:
        """Stage 4: Glyph Embedding (simplified - uses normalization)"""
        logger.info("=" * 60)
        logger.info("STAGE 4: Glyph Embedding")
        logger.info("=" * 60)
        
        # Simplified embedding: normalize features
        scaler = StandardScaler()
        embeddings = scaler.fit_transform(features['features'])
        
        # Save embeddings
        output_path = self.work_dir / 'glyphs' / 'embeddings.npy'
        np.save(output_path, embeddings)
        logger.info(f"Saved embeddings: {output_path} shape={embeddings.shape}")
        
        return embeddings
    
    def run_stage_glyph_cluster(self, embeddings: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """Stage 5: Glyph Clustering"""
        logger.info("=" * 60)
        logger.info("STAGE 5: Glyph Clustering")
        logger.info("=" * 60)
        
        stage = next(s for s in self.config['stages'] if s['id'] == 'glyph_cluster')
        n_clusters = self.config['inputs']['anomaly_target_count']
        
        kmeans = KMeans(
            n_clusters=n_clusters,
            max_iter=stage['params']['max_iter'],
            random_state=self.config['inputs']['random_seed']
        )
        labels = kmeans.fit_predict(embeddings)
        
        # Compute cluster stats
        stats = {
            'n_clusters': n_clusters,
            'cluster_sizes': {},
            'cluster_centers': kmeans.cluster_centers_.tolist()
        }
        
        for i in range(n_clusters):
            cluster_size = np.sum(labels == i)
            stats['cluster_sizes'][f'cluster_{i}'] = int(cluster_size)
        
        # Save results
        np.save(self.work_dir / 'glyphs' / 'cluster_labels.npy', labels)
        
        stats_path = self.work_dir / 'glyphs' / 'cluster_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Saved cluster stats: {stats_path}")
        
        return labels, stats
    
    def run_stage_symbol_assign(self, cluster_stats: Dict) -> Dict:
        """Stage 6: Symbol Assignment"""
        logger.info("=" * 60)
        logger.info("STAGE 6: Symbol Assignment")
        logger.info("=" * 60)
        
        # Assign neural symbols to clusters
        symbols = {}
        for i, (cluster_id, size) in enumerate(cluster_stats['cluster_sizes'].items()):
            symbol_id = f"NSYM_{i:03d}"
            symbols[cluster_id] = {
                'symbol_id': symbol_id,
                'size': size,
                'support': size / sum(cluster_stats['cluster_sizes'].values())
            }
        
        # Save symbol table
        symbol_dir = self.work_dir / 'symbols'
        symbol_dir.mkdir(parents=True, exist_ok=True)
        
        symbol_path = symbol_dir / 'symbol_table.json'
        with open(symbol_path, 'w') as f:
            json.dump(symbols, f, indent=2)
        logger.info(f"Saved symbol table: {symbol_path}")
        
        return symbols
    
    def run_stage_codon_mapping(self, symbols: Dict) -> Dict:
        """Stage 7: Initial Codon Mapping"""
        logger.info("=" * 60)
        logger.info("STAGE 7: Initial Codon Mapping")
        logger.info("=" * 60)
        
        # Load codon table
        codon_table_path = Path(self.config['stages'][6]['params']['codon_table'])
        with open(codon_table_path, 'r') as f:
            codon_table = json.load(f)
        
        # Map symbols to codons (simplified - round-robin assignment)
        codon_list = list(codon_table['codon_mappings'].keys())
        mapping = {}
        
        for i, (cluster_id, symbol_data) in enumerate(symbols.items()):
            codon_name = codon_list[i % len(codon_list)]
            mapping[symbol_data['symbol_id']] = {
                'codon': codon_name,
                'codon_data': codon_table['codon_mappings'][codon_name],
                'support': symbol_data['support']
            }
        
        # Save mapping
        binding_dir = self.work_dir / 'binding'
        binding_dir.mkdir(parents=True, exist_ok=True)
        
        mapping_path = binding_dir / 'symbol_to_codon_v0.json'
        with open(mapping_path, 'w') as f:
            json.dump(mapping, f, indent=2)
        logger.info(f"Saved codon mapping: {mapping_path}")
        
        return mapping
    
    def run_stage_trig6_eval(self, features: Dict, mapping: Dict) -> Dict:
        """Stage 8: TRIG6 Evaluation"""
        logger.info("=" * 60)
        logger.info("STAGE 8: TRIG6 Evaluation (Neuralink-Infused)")
        logger.info("=" * 60)
        
        evaluator = TRIG6Evaluator(self.config['meta'])
        metrics = evaluator.compute_metrics(features, mapping)
        
        # Save TRIG6 report
        binding_dir = self.work_dir / 'binding'
        
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'metrics': metrics,
            'config': self.config['stages'][7]['trig6']
        }
        
        report_path = binding_dir / 'trig6_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Saved TRIG6 report: {report_path}")
        
        # Save state history
        state_path = binding_dir / 'trig6_state_history.json'
        with open(state_path, 'w') as f:
            json.dump({'generations': [metrics]}, f, indent=2)
        
        return metrics
    
    def run_stage_evolution(self, metrics: Dict, mapping: Dict) -> Dict:
        """Stage 9: Evolution Loop (simplified)"""
        logger.info("=" * 60)
        logger.info("STAGE 9: Darwinian Augmentation Evolution")
        logger.info("=" * 60)
        
        # Simplified evolution: select champion based on fitness
        champion = {
            'mapping': mapping,
            'fitness': metrics['fitness'],
            'generation': 'champion',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Save champion
        binding_dir = self.work_dir / 'binding'
        champion_path = binding_dir / 'symbol_to_codon_champion.json'
        with open(champion_path, 'w') as f:
            json.dump(champion, f, indent=2)
        logger.info(f"Saved champion mapping: {champion_path}")
        
        # Evolution log
        log_path = binding_dir / 'evolution_log.json'
        with open(log_path, 'w') as f:
            json.dump({
                'generations': 1,
                'champion_fitness': metrics['fitness'],
                'note': 'Simplified evolution - single generation'
            }, f, indent=2)
        
        return champion
    
    def run_stage_codon_emit(self, champion: Dict):
        """Stage 10: Augmented Codon Emission"""
        logger.info("=" * 60)
        logger.info("STAGE 10: Augmented Codon Emission")
        logger.info("=" * 60)
        
        streams_dir = self.work_dir / 'binding' / 'codon_streams'
        streams_dir.mkdir(parents=True, exist_ok=True)
        
        # Emit codon stream
        stream_data = {
            'format': 'v1',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'champion': champion,
            'neuro_meta': {
                'pipeline': self.config['meta']['id'],
                'genome': self.config['genome_inheritance']['genes'],
                'fitness': champion['fitness']
            }
        }
        
        stream_path = streams_dir / 'neuro_aug_stream.json'
        with open(stream_path, 'w') as f:
            json.dump(stream_data, f, indent=2)
        logger.info(f"Emitted codon stream: {stream_path}")
    
    def run(self):
        """Execute complete pipeline"""
        logger.info("=" * 80)
        logger.info(f"Starting Neuralink Infusion Pipeline: {self.config['meta']['name']}")
        logger.info("=" * 80)
        
        start_time = datetime.now()
        
        # Run stages
        neural_data = self.run_stage_ingest()
        anomalies = self.run_stage_anomaly_detect(neural_data)
        features = self.run_stage_glyph_extract(neural_data, anomalies)
        embeddings = self.run_stage_glyph_embed(features)
        labels, cluster_stats = self.run_stage_glyph_cluster(embeddings)
        symbols = self.run_stage_symbol_assign(cluster_stats)
        mapping = self.run_stage_codon_mapping(symbols)
        metrics = self.run_stage_trig6_eval(features, mapping)
        champion = self.run_stage_evolution(metrics, mapping)
        self.run_stage_codon_emit(champion)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        logger.info("=" * 80)
        logger.info(f"Pipeline Complete! Duration: {duration:.2f}s")
        logger.info(f"Champion Fitness: {champion['fitness']:.4f}")
        logger.info(f"Artifacts: {self.work_dir}")
        logger.info("=" * 80)
        
        # Generate summary
        summary = {
            'status': 'SUCCESS',
            'duration_seconds': duration,
            'fitness': champion['fitness'],
            'metrics': metrics,
            'work_dir': str(self.work_dir),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        summary_path = self.work_dir / 'pipeline_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Summary: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Neuralink Infusion Pipeline - TRIG6 SAGCO-OS BCI Simulation'
    )
    parser.add_argument(
        '--config',
        default='neuralink_infusion_pipeline.yaml',
        help='Path to pipeline configuration YAML'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.config):
        logger.error(f"Config file not found: {args.config}")
        sys.exit(1)
    
    pipeline = NeuralinkInfusionPipeline(args.config)
    
    try:
        pipeline.run()
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
