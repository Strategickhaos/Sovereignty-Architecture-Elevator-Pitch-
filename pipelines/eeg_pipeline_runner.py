#!/usr/bin/env python3
"""
EEG Pipeline Runner - Neuromorphic Cognitive Architecture
Handles EEG data ingestion, preprocessing, spike conversion, anomaly detection, and glyph extraction

Version: 1.0.0
Date: 2026-01-25
Operator: Dominic Garza (DOM_010101)
Entity: Strategickhaos DAO LLC
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging
from pathlib import Path
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EEGConfig:
    """Configuration for EEG pipeline"""
    sampling_rate: int = 256  # Hz
    channels: int = 4
    bandpass_low: float = 0.5  # Hz
    bandpass_high: float = 50.0  # Hz
    notch_freq: float = 60.0  # Hz (US) or 50.0 (EU)
    epoch_duration: float = 2.0  # seconds
    

@dataclass
class SpikeConfig:
    """Configuration for spike conversion"""
    encoding: str = "rate_code"  # or "time_to_first_spike", "phase_code"
    max_firing_rate: int = 100  # Hz
    refractory_period: float = 0.002  # seconds
    

@dataclass
class AnomalyPattern:
    """Detected anomaly pattern"""
    pattern_type: str
    confidence: float
    timestamp: float
    features: Dict[str, float]
    glyph: Optional[str] = None


class EEGPipelineRunner:
    """
    EEG Pipeline Runner for Neuromorphic Integration
    
    Stages:
        1. ingest_eeg: Load EEG data from hardware or datasets
        2. preprocess: Filter, epoch, and normalize signals
        3. spike_convert: Convert to spike trains for Loihi
        4. anomaly_detect: Detect ADHD/autism/epilepsy patterns
        5. glyph_extract: Map patterns to FlameLang glyphs
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize pipeline with configuration"""
        self.eeg_config = EEGConfig()
        self.spike_config = SpikeConfig()
        self.data = None
        self.preprocessed_data = None
        self.spike_trains = None
        self.anomalies: List[AnomalyPattern] = []
        self.glyphs: List[str] = []
        
        if config_path:
            self.load_config(config_path)
            
        logger.info("EEG Pipeline Runner initialized")
    
    def load_config(self, config_path: str):
        """Load pipeline configuration from YAML"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Update configurations from YAML
            if 'eeg' in config:
                for key, value in config['eeg'].items():
                    if hasattr(self.eeg_config, key):
                        setattr(self.eeg_config, key, value)
                        
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def ingest_eeg(self, source: str, source_type: str = "dataset") -> np.ndarray:
        """
        Stage 1: Ingest EEG data from hardware or datasets
        
        Args:
            source: Path to dataset file or hardware device identifier
            source_type: "dataset" or "hardware"
            
        Returns:
            Raw EEG data as numpy array [n_channels, n_samples]
        """
        logger.info(f"Ingesting EEG data from {source_type}: {source}")
        
        if source_type == "dataset":
            # Simulate loading from PhysioNet, TUH, or BCI Competition datasets
            # In production, use MNE's read_raw_edf, read_raw_brainvision, etc.
            logger.info(f"Loading dataset from: {source}")
            
            # Simulated data for demonstration
            # In production, use MNE-Python for real data:
            #   import mne
            #   raw = mne.io.read_raw_edf(source, preload=True)
            #   self.data = raw.get_data()
            #   self.eeg_config.sampling_rate = int(raw.info['sfreq'])
            #   self.eeg_config.channels = raw.info['nchan']
            
            duration_seconds = 60
            n_samples = int(self.eeg_config.sampling_rate * duration_seconds)
            
            # Simulate realistic EEG data with noise
            self.data = np.random.randn(self.eeg_config.channels, n_samples) * 50  # μV scale
            
            # Add some simulated patterns
            self._add_simulated_patterns()
            
        elif source_type == "hardware":
            # Placeholder for hardware integration (Muse, Emotiv, OpenBCI)
            logger.info(f"Connecting to hardware device: {source}")
            # In production, use device-specific SDKs
            raise NotImplementedError("Hardware integration requires device-specific SDK")
        
        else:
            raise ValueError(f"Unknown source_type: {source_type}")
        
        logger.info(f"Ingested data shape: {self.data.shape}")
        return self.data
    
    def _add_simulated_patterns(self):
        """Add simulated EEG patterns for demonstration"""
        # Add epilepsy-like spike-wave complex at random times
        n_spikes = 3
        spike_duration = int(0.5 * self.eeg_config.sampling_rate)  # 500ms
        
        for _ in range(n_spikes):
            spike_start = np.random.randint(0, self.data.shape[1] - spike_duration)
            spike_signal = 200 * np.sin(2 * np.pi * 3 * np.arange(spike_duration) / self.eeg_config.sampling_rate)
            self.data[0, spike_start:spike_start+spike_duration] += spike_signal
        
        # Add ADHD-like theta/beta ratio anomaly
        theta_band = np.sin(2 * np.pi * 5 * np.arange(self.data.shape[1]) / self.eeg_config.sampling_rate)
        self.data[1, :] += 30 * theta_band
    
    def preprocess(self) -> np.ndarray:
        """
        Stage 2: Preprocess EEG signals
        
        Operations:
            - Bandpass filter (0.5-50 Hz)
            - Notch filter (50/60 Hz line noise)
            - Artifact removal (simplified ICA)
            - Epoch extraction
            - Normalization (z-score)
            
        Returns:
            Preprocessed EEG data [n_epochs, n_channels, n_samples_per_epoch]
        """
        logger.info("Preprocessing EEG data")
        
        if self.data is None:
            raise ValueError("No data to preprocess. Run ingest_eeg first.")
        
        # 1. Bandpass filter (simplified implementation)
        # In production, use: mne.filter.filter_data()
        filtered_data = self._bandpass_filter(
            self.data, 
            self.eeg_config.bandpass_low, 
            self.eeg_config.bandpass_high
        )
        
        # 2. Notch filter for line noise
        filtered_data = self._notch_filter(filtered_data, self.eeg_config.notch_freq)
        
        # 3. Artifact removal (simplified - just remove extreme values)
        # In production, use: mne.preprocessing.ICA
        filtered_data = self._remove_artifacts(filtered_data)
        
        # 4. Epoch extraction
        epoch_samples = int(self.eeg_config.epoch_duration * self.eeg_config.sampling_rate)
        n_epochs = filtered_data.shape[1] // epoch_samples
        
        epochs = np.array([
            filtered_data[:, i*epoch_samples:(i+1)*epoch_samples]
            for i in range(n_epochs)
        ])
        
        # 5. Normalization (z-score per channel)
        self.preprocessed_data = self._normalize(epochs)
        
        logger.info(f"Preprocessed data shape: {self.preprocessed_data.shape}")
        return self.preprocessed_data
    
    def _bandpass_filter(self, data: np.ndarray, low: float, high: float) -> np.ndarray:
        """Apply bandpass filter (simplified FFT-based)"""
        from scipy import signal
        
        nyquist = self.eeg_config.sampling_rate / 2
        low_norm = low / nyquist
        high_norm = high / nyquist
        
        b, a = signal.butter(4, [low_norm, high_norm], btype='band')
        
        filtered = np.zeros_like(data)
        for ch in range(data.shape[0]):
            filtered[ch] = signal.filtfilt(b, a, data[ch])
        
        return filtered
    
    def _notch_filter(self, data: np.ndarray, freq: float) -> np.ndarray:
        """Apply notch filter for line noise"""
        from scipy import signal
        
        nyquist = self.eeg_config.sampling_rate / 2
        freq_norm = freq / nyquist
        
        b, a = signal.iirnotch(freq_norm, Q=30)
        
        filtered = np.zeros_like(data)
        for ch in range(data.shape[0]):
            filtered[ch] = signal.filtfilt(b, a, data[ch])
        
        return filtered
    
    def _remove_artifacts(self, data: np.ndarray, threshold: float = 200.0) -> np.ndarray:
        """Remove extreme artifacts (simplified)"""
        # Clip extreme values
        return np.clip(data, -threshold, threshold)
    
    def _normalize(self, data: np.ndarray) -> np.ndarray:
        """Z-score normalization per channel"""
        normalized = np.zeros_like(data)
        
        for epoch_idx in range(data.shape[0]):
            for ch in range(data.shape[1]):
                channel_data = data[epoch_idx, ch, :]
                mean = np.mean(channel_data)
                std = np.std(channel_data)
                
                if std > 0:
                    normalized[epoch_idx, ch, :] = (channel_data - mean) / std
                else:
                    normalized[epoch_idx, ch, :] = channel_data - mean
        
        return normalized
    
    def spike_convert(self, encoding: Optional[str] = None) -> List[np.ndarray]:
        """
        Stage 3: Convert EEG signals to spike trains for Loihi
        
        Args:
            encoding: Spike encoding method ("rate_code", "time_to_first_spike", "phase_code")
            
        Returns:
            List of spike trains (one per epoch)
        """
        if encoding:
            self.spike_config.encoding = encoding
        
        logger.info(f"Converting to spike trains using {self.spike_config.encoding} encoding")
        
        if self.preprocessed_data is None:
            raise ValueError("No preprocessed data. Run preprocess first.")
        
        self.spike_trains = []
        
        for epoch in self.preprocessed_data:
            if self.spike_config.encoding == "rate_code":
                spikes = self._rate_code_encoding(epoch)
            elif self.spike_config.encoding == "time_to_first_spike":
                spikes = self._ttfs_encoding(epoch)
            elif self.spike_config.encoding == "phase_code":
                spikes = self._phase_encoding(epoch)
            else:
                raise ValueError(f"Unknown encoding: {self.spike_config.encoding}")
            
            self.spike_trains.append(spikes)
        
        logger.info(f"Generated {len(self.spike_trains)} spike train epochs")
        return self.spike_trains
    
    def _rate_code_encoding(self, epoch: np.ndarray) -> np.ndarray:
        """Rate coding: firing rate proportional to signal amplitude"""
        # Convert normalized amplitude to firing rate
        # Positive values → higher firing rate
        
        n_channels, n_samples = epoch.shape
        spikes = np.zeros_like(epoch, dtype=np.int8)
        
        for ch in range(n_channels):
            signal = epoch[ch, :]
            
            # Map amplitude to firing probability
            # Normalized signal is ~N(0,1), so map [0, 2] → [0, max_firing_rate]
            firing_prob = (signal + 2) / 4 * (self.spike_config.max_firing_rate / self.eeg_config.sampling_rate)
            firing_prob = np.clip(firing_prob, 0, 1)
            
            # Generate spikes probabilistically
            spikes[ch, :] = (np.random.rand(n_samples) < firing_prob).astype(np.int8)
        
        return spikes
    
    def _ttfs_encoding(self, epoch: np.ndarray) -> np.ndarray:
        """Time-to-first-spike: latency encoding"""
        # Higher amplitude → earlier spike
        n_channels, n_samples = epoch.shape
        spikes = np.zeros_like(epoch, dtype=np.int8)
        
        for ch in range(n_channels):
            signal = epoch[ch, :]
            
            # Find first threshold crossing per window
            window_size = 50  # samples
            for i in range(0, n_samples, window_size):
                window = signal[i:i+window_size]
                
                if len(window) > 0 and window.max() > 0.5:  # threshold
                    first_spike = np.argmax(window > 0.5)
                    spikes[ch, i + first_spike] = 1
        
        return spikes
    
    def _phase_encoding(self, epoch: np.ndarray) -> np.ndarray:
        """Phase coding: spike timing relative to oscillation phase"""
        # Simplified: spike at phase peaks
        n_channels, n_samples = epoch.shape
        spikes = np.zeros_like(epoch, dtype=np.int8)
        
        for ch in range(n_channels):
            signal = epoch[ch, :]
            
            # Find local maxima (simplified phase detection)
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(signal, distance=10)
            
            spikes[ch, peaks] = 1
        
        return spikes
    
    def anomaly_detect(self) -> List[AnomalyPattern]:
        """
        Stage 4: Detect ADHD/autism/epilepsy patterns
        
        Returns:
            List of detected anomaly patterns
        """
        logger.info("Detecting anomaly patterns")
        
        if self.preprocessed_data is None:
            raise ValueError("No preprocessed data. Run preprocess first.")
        
        self.anomalies = []
        
        for epoch_idx, epoch in enumerate(self.preprocessed_data):
            timestamp = epoch_idx * self.eeg_config.epoch_duration
            
            # Detect epilepsy patterns (spike-wave complexes, HFOs)
            epilepsy_anomalies = self._detect_epilepsy(epoch, timestamp)
            self.anomalies.extend(epilepsy_anomalies)
            
            # Detect ADHD patterns (theta/beta ratio, bursts)
            adhd_anomalies = self._detect_adhd(epoch, timestamp)
            self.anomalies.extend(adhd_anomalies)
            
            # Detect autism patterns (entropy, coherence)
            autism_anomalies = self._detect_autism(epoch, timestamp)
            self.anomalies.extend(autism_anomalies)
            
            # Detect memory patterns
            memory_anomalies = self._detect_memory_gaps(epoch, timestamp)
            self.anomalies.extend(memory_anomalies)
        
        logger.info(f"Detected {len(self.anomalies)} anomaly patterns")
        return self.anomalies
    
    def _detect_epilepsy(self, epoch: np.ndarray, timestamp: float) -> List[AnomalyPattern]:
        """Detect epilepsy-related patterns"""
        anomalies = []
        
        # Detect high amplitude spikes (simplified)
        max_amplitude = np.max(np.abs(epoch))
        
        if max_amplitude > 3.0:  # 3 standard deviations
            anomalies.append(AnomalyPattern(
                pattern_type="epilepsy_spike",
                confidence=min(max_amplitude / 5.0, 1.0),
                timestamp=timestamp,
                features={
                    "max_amplitude": float(max_amplitude),
                    "channel": int(np.argmax(np.max(np.abs(epoch), axis=1)))
                }
            ))
        
        # Detect high-frequency oscillations (80-500 Hz)
        # Simplified: check for rapid oscillations
        for ch in range(epoch.shape[0]):
            signal = epoch[ch, :]
            zero_crossings = np.sum(np.diff(np.sign(signal)) != 0)
            crossing_rate = zero_crossings / len(signal) * self.eeg_config.sampling_rate
            
            if crossing_rate > 80:  # HFO threshold
                anomalies.append(AnomalyPattern(
                    pattern_type="high_frequency_oscillation",
                    confidence=0.85,
                    timestamp=timestamp,
                    features={
                        "crossing_rate": float(crossing_rate),
                        "channel": ch
                    }
                ))
        
        return anomalies
    
    def _detect_adhd(self, epoch: np.ndarray, timestamp: float) -> List[AnomalyPattern]:
        """Detect ADHD-related patterns"""
        anomalies = []
        
        # Calculate theta/beta ratio (simplified)
        # Theta: 4-8 Hz, Beta: 13-30 Hz
        for ch in range(epoch.shape[0]):
            signal = epoch[ch, :]
            
            # Use FFT to estimate power in frequency bands
            from scipy import signal as scipy_signal
            freqs, psd = scipy_signal.welch(signal, fs=self.eeg_config.sampling_rate)
            
            theta_power = np.mean(psd[(freqs >= 4) & (freqs <= 8)])
            beta_power = np.mean(psd[(freqs >= 13) & (freqs <= 30)])
            
            if beta_power > 0:
                theta_beta_ratio = theta_power / beta_power
                
                if theta_beta_ratio > 2.5:  # ADHD threshold
                    anomalies.append(AnomalyPattern(
                        pattern_type="adhd_burst",
                        confidence=0.75,
                        timestamp=timestamp,
                        features={
                            "theta_beta_ratio": float(theta_beta_ratio),
                            "channel": ch
                        }
                    ))
        
        # Detect attention drift (high variance)
        variance = np.var(epoch)
        if variance > 2.0:
            anomalies.append(AnomalyPattern(
                pattern_type="attention_drift",
                confidence=0.70,
                timestamp=timestamp,
                features={"variance": float(variance)}
            ))
        
        return anomalies
    
    def _detect_autism(self, epoch: np.ndarray, timestamp: float) -> List[AnomalyPattern]:
        """Detect autism-related patterns"""
        anomalies = []
        
        # Calculate entropy (simplified measure of signal complexity)
        from scipy.stats import entropy
        
        for ch in range(epoch.shape[0]):
            signal = epoch[ch, :]
            
            # Discretize signal for entropy calculation
            hist, _ = np.histogram(signal, bins=20)
            signal_entropy = entropy(hist + 1)  # add 1 to avoid log(0)
            
            if signal_entropy > 2.5:  # High entropy threshold
                anomalies.append(AnomalyPattern(
                    pattern_type="autism_entropy",
                    confidence=0.72,
                    timestamp=timestamp,
                    features={
                        "entropy": float(signal_entropy),
                        "channel": ch
                    }
                ))
        
        # Detect reduced alpha coherence (simplified)
        # Would require multi-channel coherence analysis in production
        
        return anomalies
    
    def _detect_memory_gaps(self, epoch: np.ndarray, timestamp: float) -> List[AnomalyPattern]:
        """Detect memory-related patterns"""
        anomalies = []
        
        # Detect theta phase reset (simplified)
        for ch in range(epoch.shape[0]):
            signal = epoch[ch, :]
            
            # Check for theta band power
            from scipy import signal as scipy_signal
            freqs, psd = scipy_signal.welch(signal, fs=self.eeg_config.sampling_rate)
            
            theta_power = np.mean(psd[(freqs >= 4) & (freqs <= 8)])
            
            if theta_power > 1.5:
                anomalies.append(AnomalyPattern(
                    pattern_type="memory_gap",
                    confidence=0.68,
                    timestamp=timestamp,
                    features={
                        "theta_power": float(theta_power),
                        "channel": ch
                    }
                ))
        
        return anomalies
    
    def glyph_extract(self) -> List[str]:
        """
        Stage 5: Extract FlameLang glyphs from detected patterns
        
        Returns:
            List of glyph names
        """
        logger.info("Extracting glyphs from anomaly patterns")
        
        if not self.anomalies:
            logger.warning("No anomalies detected. Run anomaly_detect first.")
            return []
        
        # Map pattern types to glyphs (from codon_table.yaml)
        pattern_to_glyph = {
            "epilepsy_spike": "SEIZURE_PREDICT",
            "high_frequency_oscillation": "HFO_DETECT",
            "adhd_burst": "FOCUS_BOOST",
            "attention_drift": "STABILIZE_LOOP",
            "autism_entropy": "SENSORY_GATE",
            "memory_gap": "MEMORY_EXPORT"
        }
        
        self.glyphs = []
        
        for anomaly in self.anomalies:
            glyph = pattern_to_glyph.get(anomaly.pattern_type)
            
            if glyph and anomaly.confidence > 0.7:  # Confidence threshold
                anomaly.glyph = glyph
                self.glyphs.append(glyph)
                logger.info(f"  {anomaly.pattern_type} → {glyph} (confidence: {anomaly.confidence:.2f})")
        
        # Remove duplicates while preserving order
        unique_glyphs = list(dict.fromkeys(self.glyphs))
        
        logger.info(f"Extracted {len(unique_glyphs)} unique glyphs: {unique_glyphs}")
        return unique_glyphs
    
    def run_full_pipeline(self, source: str, source_type: str = "dataset") -> Dict:
        """
        Run the complete EEG pipeline
        
        Args:
            source: Data source path or device
            source_type: "dataset" or "hardware"
            
        Returns:
            Dictionary with pipeline results
        """
        logger.info("="*60)
        logger.info("Starting Full EEG Pipeline")
        logger.info("="*60)
        
        # Stage 1: Ingest
        self.ingest_eeg(source, source_type)
        
        # Stage 2: Preprocess
        self.preprocess()
        
        # Stage 3: Spike conversion
        self.spike_convert()
        
        # Stage 4: Anomaly detection
        self.anomaly_detect()
        
        # Stage 5: Glyph extraction
        self.glyph_extract()
        
        # Compile results
        results = {
            "data_shape": self.data.shape,
            "preprocessed_shape": self.preprocessed_data.shape,
            "n_spike_trains": len(self.spike_trains),
            "n_anomalies": len(self.anomalies),
            "anomalies": [
                {
                    "type": a.pattern_type,
                    "confidence": a.confidence,
                    "timestamp": a.timestamp,
                    "glyph": a.glyph
                }
                for a in self.anomalies
            ],
            "glyphs": list(dict.fromkeys(self.glyphs))  # unique glyphs
        }
        
        logger.info("="*60)
        logger.info("Pipeline Complete!")
        logger.info(f"Detected {results['n_anomalies']} anomalies")
        logger.info(f"Extracted {len(results['glyphs'])} unique glyphs")
        logger.info("="*60)
        
        return results


def main():
    """Example usage of EEG Pipeline Runner"""
    # Initialize pipeline
    pipeline = EEGPipelineRunner()
    
    # Run full pipeline with simulated data
    results = pipeline.run_full_pipeline(
        source="simulated_eeg_data",
        source_type="dataset"
    )
    
    # Print results
    print("\n" + "="*60)
    print("PIPELINE RESULTS")
    print("="*60)
    print(f"Data shape: {results['data_shape']}")
    print(f"Anomalies detected: {results['n_anomalies']}")
    print(f"\nExtracted glyphs:")
    for glyph in results['glyphs']:
        print(f"  • {glyph}")
    print("="*60)


if __name__ == "__main__":
    main()
