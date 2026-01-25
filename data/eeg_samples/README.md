# Data Directory Structure

This directory contains input data for the neuromorphic blood-neuro integration pipeline.

## Directory Layout

```
data/
├── eeg_samples/           # EEG/iEEG data for seizure detection
│   ├── raw_ieeg.npy      # Raw intracranial EEG (NumPy format)
│   ├── scalp_eeg.edf     # Scalp EEG (EDF format)
│   └── README.md         # This file
│
└── blood_samples/         # Blood science data
    ├── cell_images/       # Microscopy images of blood cells
    ├── fasta.npy          # DNA/RNA sequences (NumPy encoded)
    ├── variants.vcf       # Genetic variants (VCF format)
    └── README.md
```

## EEG Data Format

### raw_ieeg.npy
- **Format**: NumPy array (.npy)
- **Dimensions**: [channels, timepoints]
- **Sample Rate**: 1000 Hz
- **Channels**: Typically 16-256 intracranial electrodes
- **Purpose**: High-resolution seizure detection

### scalp_eeg.edf
- **Format**: European Data Format (EDF)
- **Sample Rate**: 256 Hz
- **Channels**: 10-20 system (19-21 electrodes)
- **Purpose**: Non-invasive wearable applications

## Expected Data Properties

### EEG Features to Extract
- Spike bursts (high-amplitude transients)
- HFO ripples (80-500 Hz oscillations)
- Chirp patterns (progressive frequency changes)
- Theta phase (4-8 Hz baseline)

### Blood Features to Extract
- Cell morphology (shape variance)
- Hemoglobin structure
- Genetic variants (SNPs, indels)
- Coagulation markers

## Data Acquisition

### Clinical EEG Sources
- Epilepsy monitoring units (EMU)
- Wearable EEG devices
- Research databases (with appropriate permissions)

### Blood Sample Sources
- Clinical blood draws
- Microscopy imaging
- Whole-genome/exome sequencing
- Reference databases (ClinVar, gnomAD)

## Privacy & Ethics

**IMPORTANT**: All data must be:
- De-identified (HIPAA compliant)
- Obtained with informed consent
- Used in accordance with IRB approval
- Stored securely with encryption

## Sample Data

For testing purposes, synthetic data can be generated using:
```python
import numpy as np

# Generate synthetic EEG (16 channels, 10 seconds at 1000 Hz)
eeg_data = np.random.randn(16, 10000) * 50  # microvolts
np.save('raw_ieeg.npy', eeg_data)
```

## References

- EEG data standards: [BIDS-EEG specification](https://bids-specification.readthedocs.io/)
- VCF format: [VCF 4.2 specification](https://samtools.github.io/hts-specs/VCFv4.2.pdf)
- FASTA format: [NCBI FASTA specification](https://www.ncbi.nlm.nih.gov/genbank/fastaformat/)

## Contact

For data sharing or collaboration inquiries, contact Strategickhaos DAO LLC.
