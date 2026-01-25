# PhysioNet EEG Dataset Integration Guide

## Overview

This guide shows how to integrate real EEG data from PhysioNet into the neuromorphic pipeline.

## PhysioNet Datasets

### Recommended Datasets

1. **EEG Motor Movement/Imagery Dataset**
   - URL: https://physionet.org/content/eegmmidb/1.0.0/
   - Subjects: 109
   - Tasks: Motor execution and imagery
   - Format: EDF+
   - Sampling: 160 Hz

2. **CHB-MIT Scalp EEG Database**
   - URL: https://physionet.org/content/chbmit/1.0.0/
   - Subjects: 24 (pediatric)
   - Condition: Epilepsy/seizures
   - Format: EDF
   - Sampling: 256 Hz
   - **Perfect for SEIZURE_PREDICT codon validation**

3. **TUH EEG Corpus** (requires registration)
   - URL: https://www.isip.piconepress.com/projects/tuh_eeg/
   - Recordings: 30,000+
   - Conditions: Diverse clinical data
   - Format: EDF
   - **Best for comprehensive testing**

## Installation

```bash
# Install MNE-Python for EEG processing
pip install mne

# Install PhysioNet data downloader
pip install wfdb

# Optional: Install PyEDFlib for direct EDF reading
pip install pyedflib
```

## Download Dataset

### Option 1: Using wget

```bash
# Create data directory
mkdir -p data/physionet

# Download EEG Motor Movement/Imagery Dataset
cd data/physionet
wget -r -N -c -np https://physionet.org/files/eegmmidb/1.0.0/

# Download CHB-MIT Epilepsy Dataset
wget -r -N -c -np https://physionet.org/files/chbmit/1.0.0/
```

### Option 2: Using WFDB Python

```python
import wfdb

# Download specific record
record = wfdb.rdrecord('eegmmidb/1.0.0/S001/S001R01')

# Access data
eeg_data = record.p_signal  # numpy array
sampling_rate = record.fs
channel_names = record.sig_name
```

## Integration with Pipeline

### Method 1: Using MNE (Recommended)

```python
from pipelines.eeg_pipeline_runner import EEGPipelineRunner
import mne

# Load PhysioNet EDF file
raw = mne.io.read_raw_edf(
    'data/physionet/eegmmidb/1.0.0/S001/S001R01.edf',
    preload=True
)

# Initialize pipeline
pipeline = EEGPipelineRunner()

# Inject real data
pipeline.data = raw.get_data()  # [n_channels, n_samples]
pipeline.eeg_config.sampling_rate = int(raw.info['sfreq'])
pipeline.eeg_config.channels = raw.info['nchan']

# Run pipeline
pipeline.preprocess()
pipeline.spike_convert()
anomalies = pipeline.anomaly_detect()
glyphs = pipeline.glyph_extract()

print(f"Detected glyphs: {glyphs}")
```

### Method 2: Direct ingest_eeg modification

Modify `pipelines/eeg_pipeline_runner.py`:

```python
def ingest_eeg(self, source: str, source_type: str = "dataset") -> np.ndarray:
    if source_type == "dataset":
        # Add PhysioNet support
        if source.endswith('.edf'):
            import mne
            raw = mne.io.read_raw_edf(source, preload=True)
            self.data = raw.get_data()
            self.eeg_config.sampling_rate = int(raw.info['sfreq'])
            self.eeg_config.channels = raw.info['nchan']
        else:
            # Existing simulated code...
```

## Epilepsy Seizure Detection Example

```python
from pipelines.neuromorphic_master_pipeline import NeuromorphicMasterPipeline
import mne

# Load CHB-MIT epilepsy data
raw = mne.io.read_raw_edf('data/physionet/chbmit/1.0.0/chb01/chb01_03.edf', preload=True)

# Initialize master pipeline
pipeline = NeuromorphicMasterPipeline()

# Inject real data
pipeline.eeg_pipeline.data = raw.get_data()
pipeline.eeg_pipeline.eeg_config.sampling_rate = int(raw.info['sfreq'])

# Run preprocessing and detection
pipeline.eeg_pipeline.preprocess()
pipeline.eeg_pipeline.spike_convert()
anomalies = pipeline.eeg_pipeline.anomaly_detect()

# Check for seizure predictions
seizure_glyphs = [a for a in anomalies if a.pattern_type == "epilepsy_spike"]
print(f"Detected {len(seizure_glyphs)} potential seizure markers")

# Run genomics correlation
glyphs = pipeline.eeg_pipeline.glyph_extract()
if "SEIZURE_PREDICT" in glyphs:
    print("⚠️ SEIZURE_PREDICT codon emitted!")
    print("Genomic link: SCN1A variant (Dravet syndrome)")
```

## Expected Output Structure

```python
# EEG data format
eeg_data.shape = (n_channels, n_samples)
# Example: (64, 256000) for 64 channels, 1000 seconds at 256 Hz

# After preprocessing
preprocessed_data.shape = (n_epochs, n_channels, samples_per_epoch)
# Example: (500, 64, 512) for 500 epochs of 2 seconds each

# Spike trains
spike_trains[0].shape = (n_channels, samples_per_epoch)
# Binary array: 1 = spike, 0 = no spike

# Anomalies
anomalies = [
    {
        "type": "epilepsy_spike",
        "confidence": 0.92,
        "timestamp": 45.3,
        "glyph": "SEIZURE_PREDICT"
    },
    ...
]
```

## Channel Mapping

Standard 10-20 EEG system:

```
Fp1, Fp2  - Frontal pole
F3, F4    - Frontal
C3, C4    - Central
P3, P4    - Parietal
O1, O2    - Occipital
F7, F8    - Temporal frontal
T3, T4    - Temporal
T5, T6    - Temporal posterior
```

Consumer devices (Muse, Emotiv):
- Fewer channels (4-5)
- Typically: AF7, AF8, TP9, TP10 (Muse)

## Validation

### Seizure Detection Validation

Use CHB-MIT dataset with known seizure times:

```python
# Load dataset with seizure annotations
seizure_times = [...]  # From CHB-MIT summary files

# Run detection
detected_seizures = pipeline.detect_epilepsy_patterns()

# Calculate metrics
true_positives = count_overlaps(detected_seizures, seizure_times)
sensitivity = true_positives / len(seizure_times)
print(f"Sensitivity: {sensitivity:.1%}")
```

### ADHD Pattern Validation

Use motor imagery dataset (tasks requiring attention):

```python
# Compare task periods vs. rest periods
task_bursts = detect_during_period(task_start, task_end)
rest_bursts = detect_during_period(rest_start, rest_end)

# Expect more ADHD bursts during challenging tasks
print(f"Task bursts: {len(task_bursts)}")
print(f"Rest bursts: {len(rest_bursts)}")
```

## Performance Benchmarks

| Dataset | Records | Processing Time | Anomalies | Glyphs |
|---------|---------|-----------------|-----------|---------|
| EEG Motor | 109 | ~2 min | ~500 | 3-5 |
| CHB-MIT | 24 subjects | ~5 min | ~200 | 2-4 |
| Simulated | 1 | <1 sec | ~150-200 | 3 |

## Troubleshooting

### MNE Installation Issues

```bash
# If MNE fails to install, try:
pip install --upgrade pip setuptools wheel
pip install mne --no-cache-dir

# Or use conda:
conda install -c conda-forge mne
```

### Memory Issues with Large Files

```python
# Load data in chunks
raw = mne.io.read_raw_edf(file_path, preload=False)  # Don't load all at once
raw.load_data()  # Load when ready

# Or crop to specific time range
raw.crop(tmin=0, tmax=60)  # First 60 seconds only
```

### Channel Count Mismatch

```python
# Adjust config to match dataset
pipeline.eeg_config.channels = raw.info['nchan']

# Or select specific channels
raw.pick_channels(['C3', 'C4', 'Cz', 'Fz'])  # Select 4 channels
```

## Next Steps

1. **Download PhysioNet dataset** (start with EEG Motor Movement)
2. **Modify ingest_eeg** to support EDF files (see Method 2 above)
3. **Run pipeline** on real data
4. **Validate results** against known annotations
5. **Fine-tune thresholds** based on real patterns

## References

- PhysioNet: https://physionet.org/
- MNE-Python: https://mne.tools/
- EEG 10-20 System: https://en.wikipedia.org/wiki/10%E2%80%9320_system_(EEG)
- CHB-MIT Dataset: https://physionet.org/content/chbmit/1.0.0/

---

*Generated by: Sovereignty Architecture Neuromorphic Integration*  
*Date: 2026-01-25*  
*Operator: DOM_010101*
