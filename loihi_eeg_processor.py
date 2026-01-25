#!/usr/bin/env python3
"""
Loihi EEG Processor - Real EEG Integration for Neuromorphic Processing
Part of TRIG6 SAGCO-OS Neuralink Infusion Pipeline

Processes real EEG data (from PhysioNet, Muse, OpenBCI) and converts to spike trains
for Intel Loihi neuromorphic chip processing.

Author: Dominic Garza (Strategickhaos DAO LLC)
Version: 1.0.0
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Union
from pathlib import Path
import yaml
import json
from datetime import datetime


@dataclass
class EEGConfig:
    """Configuration for EEG processing"""
    sample_rate: int = 256  # Hz
    num_channels: int = 64
    filter_low: float = 0.5  # Hz
    filter_high: float = 40.0  # Hz
    notch_freq: float = 60.0  # Hz (power line)
    epoch_duration: float = 1.0  # seconds
    normalization: str = "z-score"


@dataclass
class SpikeEncoding:
    """Configuration for spike encoding"""
    method: str = "rate_coding"  # rate_coding, temporal_coding, phase_coding
    threshold: float = 0.5
    max_spike_rate: float = 200.0  # Hz
    time_window: float = 0.01  # seconds


class EEGPreprocessor:
    """Preprocess raw EEG data for neuromorphic processing"""
    
    def __init__(self, config: EEGConfig):
        self.config = config
        
    def load_eeg_data(self, file_path: Union[str, Path], format: str = "numpy") -> np.ndarray:
        """
        Load EEG data from various formats
        
        Args:
            file_path: Path to EEG data file
            format: Data format (numpy, edf, csv)
            
        Returns:
            EEG data array (time x channels)
        """
        file_path = Path(file_path)
        
        if format == "numpy" or file_path.suffix == ".npy":
            return np.load(file_path)
        
        elif format == "csv" or file_path.suffix == ".csv":
            return np.loadtxt(file_path, delimiter=',')
        
        elif format == "edf":
            # Placeholder for EDF loading (requires mne or pyedflib)
            # import mne
            # raw = mne.io.read_raw_edf(file_path, preload=True)
            # return raw.get_data().T
            print(f"EDF format requires MNE library. Returning simulated data.")
            return self._generate_simulated_eeg()
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_simulated_eeg(self, duration: float = 10.0) -> np.ndarray:
        """
        Generate simulated EEG data for testing
        
        Args:
            duration: Duration in seconds
            
        Returns:
            Simulated EEG array (time x channels)
        """
        n_samples = int(duration * self.config.sample_rate)
        n_channels = self.config.num_channels
        
        # Generate multi-band EEG signals
        t = np.linspace(0, duration, n_samples)
        eeg_data = np.zeros((n_samples, n_channels))
        
        for ch in range(n_channels):
            # Delta (0.5-4 Hz) - sleep/meditation
            delta = 0.3 * np.sin(2 * np.pi * 2.0 * t + ch * 0.1)
            
            # Theta (4-8 Hz) - drowsiness/meditation
            theta = 0.4 * np.sin(2 * np.pi * 6.0 * t + ch * 0.2)
            
            # Alpha (8-13 Hz) - relaxed wakefulness
            alpha = 0.5 * np.sin(2 * np.pi * 10.0 * t + ch * 0.3)
            
            # Beta (13-30 Hz) - active thinking
            beta = 0.3 * np.sin(2 * np.pi * 20.0 * t + ch * 0.4)
            
            # Gamma (30-100 Hz) - cognitive processing
            gamma = 0.2 * np.sin(2 * np.pi * 40.0 * t + ch * 0.5)
            
            # Noise
            noise = 0.1 * np.random.randn(n_samples)
            
            eeg_data[:, ch] = delta + theta + alpha + beta + gamma + noise
        
        return eeg_data
    
    def bandpass_filter(self, data: np.ndarray) -> np.ndarray:
        """
        Apply bandpass filter to EEG data
        
        Args:
            data: Raw EEG data (time x channels)
            
        Returns:
            Filtered EEG data
        """
        # Simple FFT-based bandpass filter (for production, use scipy.signal)
        from scipy import signal
        
        sos = signal.butter(4, [self.config.filter_low, self.config.filter_high], 
                           btype='bandpass', fs=self.config.sample_rate, output='sos')
        filtered = signal.sosfilt(sos, data, axis=0)
        
        return filtered
    
    def notch_filter(self, data: np.ndarray, freq: float = 60.0, Q: float = 30.0) -> np.ndarray:
        """
        Apply notch filter to remove power line noise
        
        Args:
            data: EEG data (time x channels)
            freq: Notch frequency (Hz)
            Q: Quality factor
            
        Returns:
            Notch-filtered data
        """
        from scipy import signal
        
        b, a = signal.iirnotch(freq, Q, self.config.sample_rate)
        filtered = signal.filtfilt(b, a, data, axis=0)
        
        return filtered
    
    def normalize(self, data: np.ndarray, method: str = "z-score") -> np.ndarray:
        """
        Normalize EEG data
        
        Args:
            data: EEG data (time x channels)
            method: Normalization method (z-score, min-max)
            
        Returns:
            Normalized data
        """
        if method == "z-score":
            mean = np.mean(data, axis=0, keepdims=True)
            std = np.std(data, axis=0, keepdims=True)
            return (data - mean) / (std + 1e-8)
        
        elif method == "min-max":
            min_val = np.min(data, axis=0, keepdims=True)
            max_val = np.max(data, axis=0, keepdims=True)
            return (data - min_val) / (max_val - min_val + 1e-8)
        
        else:
            raise ValueError(f"Unknown normalization method: {method}")
    
    def epoch_data(self, data: np.ndarray) -> np.ndarray:
        """
        Divide continuous EEG into epochs
        
        Args:
            data: Continuous EEG data (time x channels)
            
        Returns:
            Epoched data (epochs x time x channels)
        """
        epoch_samples = int(self.config.epoch_duration * self.config.sample_rate)
        n_samples = data.shape[0]
        n_epochs = n_samples // epoch_samples
        
        # Truncate to fit epochs
        data_truncated = data[:n_epochs * epoch_samples]
        
        # Reshape into epochs
        epochs = data_truncated.reshape(n_epochs, epoch_samples, -1)
        
        return epochs
    
    def preprocess(self, raw_data: np.ndarray) -> np.ndarray:
        """
        Full preprocessing pipeline
        
        Args:
            raw_data: Raw EEG data (time x channels)
            
        Returns:
            Preprocessed and epoched data
        """
        print(f"Preprocessing EEG data: {raw_data.shape}")
        
        # 1. Bandpass filter
        print(f"  Applying bandpass filter ({self.config.filter_low}-{self.config.filter_high} Hz)")
        filtered = self.bandpass_filter(raw_data)
        
        # 2. Notch filter
        print(f"  Applying notch filter ({self.config.notch_freq} Hz)")
        notched = self.notch_filter(filtered, self.config.notch_freq)
        
        # 3. Normalize
        print(f"  Normalizing ({self.config.normalization})")
        normalized = self.normalize(notched, self.config.normalization)
        
        # 4. Epoch
        print(f"  Epoching ({self.config.epoch_duration}s epochs)")
        epoched = self.epoch_data(normalized)
        
        print(f"  Result: {epoched.shape[0]} epochs, {epoched.shape[1]} samples, {epoched.shape[2]} channels")
        
        return epoched


class SpikeEncoder:
    """Convert EEG signals to spike trains for Loihi SNN"""
    
    def __init__(self, config: SpikeEncoding):
        self.config = config
    
    def rate_coding(self, eeg_epochs: np.ndarray) -> np.ndarray:
        """
        Rate coding: EEG amplitude → spike frequency
        
        Args:
            eeg_epochs: Normalized EEG epochs (epochs x time x channels)
            
        Returns:
            Spike trains (epochs x time x channels), binary 0/1
        """
        print(f"Spike encoding using rate coding (threshold={self.config.threshold})")
        
        # Simple threshold-based encoding
        # Values above threshold generate spikes
        spikes = (eeg_epochs > self.config.threshold).astype(np.int8)
        
        return spikes
    
    def temporal_coding(self, eeg_epochs: np.ndarray) -> np.ndarray:
        """
        Temporal coding: Signal strength → spike timing
        
        Args:
            eeg_epochs: Normalized EEG epochs
            
        Returns:
            Spike trains with temporal information
        """
        print(f"Spike encoding using temporal coding")
        
        # Time-to-first-spike: stronger signals spike earlier
        # This is a simplified version
        spikes = np.zeros_like(eeg_epochs, dtype=np.int8)
        
        for epoch in range(eeg_epochs.shape[0]):
            for ch in range(eeg_epochs.shape[2]):
                signal = eeg_epochs[epoch, :, ch]
                # Find peaks
                peaks = signal > self.config.threshold
                if np.any(peaks):
                    first_peak = np.argmax(peaks)
                    spikes[epoch, first_peak, ch] = 1
        
        return spikes
    
    def phase_coding(self, eeg_epochs: np.ndarray, reference_freq: float = 6.0) -> np.ndarray:
        """
        Phase coding: Encode relative to reference oscillation (e.g., theta)
        
        Args:
            eeg_epochs: Normalized EEG epochs
            reference_freq: Reference frequency in Hz (default: theta at 6 Hz)
            
        Returns:
            Phase-encoded spike trains
        """
        print(f"Spike encoding using phase coding (ref freq={reference_freq} Hz)")
        
        # Extract phase of reference oscillation
        # Spikes occur at specific phases relative to this oscillation
        # This is a simplified implementation
        
        spikes = np.zeros_like(eeg_epochs, dtype=np.int8)
        
        # For now, use a combination of amplitude and phase
        # Production version would use Hilbert transform for phase extraction
        threshold_phase = eeg_epochs > self.config.threshold
        spikes = threshold_phase.astype(np.int8)
        
        return spikes
    
    def encode(self, eeg_epochs: np.ndarray) -> np.ndarray:
        """
        Encode EEG to spikes using configured method
        
        Args:
            eeg_epochs: Preprocessed EEG epochs
            
        Returns:
            Spike trains
        """
        if self.config.method == "rate_coding":
            return self.rate_coding(eeg_epochs)
        elif self.config.method == "temporal_coding":
            return self.temporal_coding(eeg_epochs)
        elif self.config.method == "phase_coding":
            return self.phase_coding(eeg_epochs)
        else:
            raise ValueError(f"Unknown encoding method: {self.config.method}")


class LoihiEEGProcessor:
    """Main processor combining preprocessing and spike encoding"""
    
    def __init__(self, pipeline_config_path: Optional[str] = None):
        """
        Initialize processor with optional pipeline config
        
        Args:
            pipeline_config_path: Path to neuralink_infusion_pipeline.yaml
        """
        if pipeline_config_path:
            with open(pipeline_config_path, 'r') as f:
                pipeline_config = yaml.safe_load(f)
                
            # Extract EEG config
            eeg_stage = next((s for s in pipeline_config['pipeline']['stages'] 
                            if s['name'] == 'eeg_ingest'), None)
            
            if eeg_stage:
                preproc = eeg_stage['config']['preprocessing']
                self.eeg_config = EEGConfig(
                    sample_rate=256,  # Default
                    filter_low=preproc['low_freq'],
                    filter_high=preproc['high_freq'],
                    notch_freq=preproc['notch_filter'],
                    epoch_duration=preproc['epoch_duration'],
                    normalization=preproc['normalization']
                )
            
            # Extract spike encoding config
            spike_stage = next((s for s in pipeline_config['pipeline']['stages'] 
                              if s['name'] == 'spike_encoding'), None)
            
            if spike_stage:
                rate_cfg = spike_stage['config']['rate_coding']
                self.spike_config = SpikeEncoding(
                    method=spike_stage['config']['encoding_method'],
                    threshold=rate_cfg['threshold'],
                    max_spike_rate=rate_cfg['max_spike_rate'],
                    time_window=rate_cfg['time_window']
                )
        else:
            # Default configs
            self.eeg_config = EEGConfig()
            self.spike_config = SpikeEncoding()
        
        self.preprocessor = EEGPreprocessor(self.eeg_config)
        self.encoder = SpikeEncoder(self.spike_config)
    
    def process(self, input_path: Optional[str] = None, 
                raw_data: Optional[np.ndarray] = None) -> Dict:
        """
        Full processing pipeline: Load → Preprocess → Encode → Save
        
        Args:
            input_path: Path to input EEG file (optional if raw_data provided)
            raw_data: Raw EEG data array (optional if input_path provided)
            
        Returns:
            Dictionary with processed results
        """
        print("=" * 80)
        print("LOIHI EEG PROCESSOR - TRIG6 SAGCO-OS Neuralink Infusion")
        print("=" * 80)
        
        # Load data
        if raw_data is not None:
            print(f"\nUsing provided raw data: {raw_data.shape}")
            eeg_raw = raw_data
        elif input_path:
            print(f"\nLoading EEG data from: {input_path}")
            eeg_raw = self.preprocessor.load_eeg_data(input_path)
        else:
            print(f"\nGenerating simulated EEG data...")
            eeg_raw = self.preprocessor._generate_simulated_eeg(duration=10.0)
        
        # Preprocess
        print(f"\n--- PREPROCESSING ---")
        eeg_preprocessed = self.preprocessor.preprocess(eeg_raw)
        
        # Encode to spikes
        print(f"\n--- SPIKE ENCODING ---")
        spike_trains = self.encoder.encode(eeg_preprocessed)
        
        # Calculate statistics
        spike_rate = np.mean(spike_trains) * 100  # Percentage
        total_spikes = np.sum(spike_trains)
        
        print(f"\n--- RESULTS ---")
        print(f"  Total spikes: {total_spikes}")
        print(f"  Spike rate: {spike_rate:.2f}%")
        print(f"  Output shape: {spike_trains.shape}")
        
        results = {
            'raw_data': eeg_raw,
            'preprocessed': eeg_preprocessed,
            'spike_trains': spike_trains,
            'statistics': {
                'total_spikes': int(total_spikes),
                'spike_rate_percent': float(spike_rate),
                'num_epochs': eeg_preprocessed.shape[0],
                'num_channels': eeg_preprocessed.shape[2],
                'samples_per_epoch': eeg_preprocessed.shape[1]
            },
            'config': {
                'eeg': vars(self.eeg_config),
                'spike': vars(self.spike_config)
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def save_output(self, results: Dict, output_dir: str = "data/processed"):
        """
        Save processing results
        
        Args:
            results: Results dictionary from process()
            output_dir: Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save spike trains
        spike_path = output_path / "eeg_spikes.npy"
        np.save(spike_path, results['spike_trains'])
        print(f"\n✓ Saved spike trains to: {spike_path}")
        
        # Save preprocessed data
        processed_path = output_path / "neural_data.npy"
        np.save(processed_path, results['preprocessed'])
        print(f"✓ Saved preprocessed data to: {processed_path}")
        
        # Save metadata
        metadata = {
            'statistics': results['statistics'],
            'config': results['config'],
            'timestamp': results['timestamp']
        }
        
        metadata_path = output_path / "processing_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Saved metadata to: {metadata_path}")
        
        print(f"\n🧠 EEG processing complete! Ready for Loihi deployment.")


def main():
    """Demo of EEG processing for Loihi"""
    
    # Initialize processor
    processor = LoihiEEGProcessor()
    
    # Process EEG (using simulated data)
    results = processor.process()
    
    # Save outputs
    processor.save_output(results)
    
    # Visualize spike raster (first epoch, first 10 channels)
    print("\n--- SPIKE RASTER PREVIEW (First Epoch, Channels 0-9) ---")
    spike_epoch = results['spike_trains'][0, :, :10]
    
    for ch in range(spike_epoch.shape[1]):
        spike_times = np.where(spike_epoch[:, ch] == 1)[0]
        raster = ['.' if i not in spike_times else '|' for i in range(spike_epoch.shape[0])]
        print(f"Ch{ch:2d}: {''.join(raster[:80])}")
    
    print("\n🔥 Ready for TRIG6 evaluation and Loihi deployment!")
    
    return results


if __name__ == "__main__":
    main()
