# Audio Encoding System Documentation

## Overview

The Audio Encoding System implements a sophisticated multi-method approach to embed various types of data into audio files. This system is part of the Sovereignty Architecture and uses four distinct encoding methods to embed different data types into audio signals.

## Specification

The system implements the encoding specification version 1.0.0 as defined in `encoding_config.json`.

### Encoding Methods

#### 1. Frequency Micro Shift (DNA Strand)
- **Purpose**: Encode DNA sequence data
- **Method**: Each character is encoded as a subtle frequency shift within a specified range
- **Parameters**:
  - `samples_per_char`: `sample_rate * 0.1` (4,410 samples at 44.1kHz)
  - `range_hz`: [-1.0, 1.0] Hz frequency shift range
- **Data**: 88-character DNA sequence

#### 2. LR Phase Modulation (Source Hash)
- **Purpose**: Encode SHA256 hash values
- **Method**: Uses phase differences between left and right stereo channels
- **Parameters**:
  - `samples_per_char`: `sample_rate * 0.05` (2,205 samples at 44.1kHz)
  - `algorithm`: SHA256 (64 hexadecimal characters)
- **Data**: Source hash verification

#### 3. Ultrasonic Harmonic (Periodic Table)
- **Purpose**: Encode structured JSON data (periodic table information)
- **Method**: Binary encoding at ultrasonic frequencies (inaudible to humans)
- **Parameters**:
  - `frequency_hz`: 19,000 Hz (ultrasonic)
  - `samples_per_bit`: `sample_rate * 0.01` (441 samples at 44.1kHz)
  - `format`: JSON UTF-8 binary
- **Data**: Periodic table elements or other JSON structures

#### 4. Amplitude Watermark (Owner)
- **Purpose**: Embed owner information as a persistent watermark
- **Method**: Cyclic amplitude modulation based on owner name hash
- **Parameters**:
  - `cycle_seconds`: 2.0 seconds per cycle
  - `variation_percent`: 0.5 (50% amplitude variation)
- **Data**: Owner identification string

## Installation

### Prerequisites

```bash
# Python 3.8 or higher
python3 --version

# Install required dependencies
pip install numpy scipy pytest
```

Or using the project's requirements file:

```bash
pip install -r requirements.sovereignty.txt
```

### Dependencies

- **numpy** >= 1.24.0 - Numerical operations and signal processing
- **scipy** >= 1.10.0 - Audio file I/O (optional, will fallback to numpy)
- **pytest** - For running tests

## Usage

### Basic Usage

```python
from audio_encoder import AudioEncoder, EncodingConfig

# Load configuration
config = EncodingConfig.from_file("encoding_config.json")

# Create encoder
encoder = AudioEncoder(config, sample_rate=44100)

# Prepare your data
dna_sequence = "ACGT" * 22  # 88 characters
periodic_data = {
    "element": "Hydrogen",
    "symbol": "H",
    "atomic_number": 1
}
owner_name = "Strategickhaos DAO LLC"

# Encode all components
encoded_signals = encoder.encode_all(dna_sequence, periodic_data, owner_name)

# Combine into stereo audio
left_channel, right_channel = encoder.combine_signals(encoded_signals)

# Save to WAV file
encoder.save_wav(left_channel, right_channel, "output.wav")
```

### Running the Example

```bash
# Run the example script
python3 example_audio_encoding.py
```

This will:
1. Load the encoding configuration
2. Encode sample DNA, hash, periodic table, and owner data
3. Combine all signals into stereo audio
4. Save the result to `encoded_output.wav`

### Individual Encoding Methods

You can also use individual encoding methods:

```python
# Encode DNA strand only
dna_signal = encoder.encode_dna_strand("ACGT" * 22)

# Encode source hash only
left, right = encoder.encode_source_hash("a" * 64)

# Encode periodic table data only
periodic_signal = encoder.encode_periodic_table({"element": "H"})

# Encode owner watermark only
owner_signal = encoder.encode_owner("Owner Name", duration_seconds=10.0)
```

## Testing

The system includes comprehensive unit tests covering all encoding methods.

### Run All Tests

```bash
# Run all tests with verbose output
python3 -m pytest test_audio_encoder.py -v

# Run tests with coverage
python3 -m pytest test_audio_encoder.py --cov=audio_encoder
```

### Test Categories

1. **Configuration Tests**: Verify config loading and validation
2. **DNA Strand Encoding Tests**: Test frequency micro shift encoding
3. **Source Hash Encoding Tests**: Test LR phase modulation
4. **Periodic Table Encoding Tests**: Test ultrasonic harmonic encoding
5. **Owner Watermark Tests**: Test amplitude watermark
6. **Integration Tests**: Test complete encoding pipeline
7. **Audio Output Tests**: Test file saving functionality

### Expected Test Results

All 25 tests should pass:
- Configuration tests: 3 tests
- DNA encoding tests: 4 tests
- Hash encoding tests: 4 tests
- Periodic table tests: 4 tests
- Owner watermark tests: 4 tests
- Integration tests: 4 tests
- Output tests: 1 test
- End-to-end test: 1 test

## Configuration

### Configuration File Format

The `encoding_config.json` file follows this structure:

```json
{
  "version": "1.0.0",
  "encoding": {
    "dna_strand": { ... },
    "source_hash": { ... },
    "periodic_table": { ... },
    "owner": { ... }
  },
  "metadata": {
    "dna_strand_length": 88,
    "source_hash": "sha256_hash_here",
    "timestamp": "2026-01-29T23:03:16.426254Z",
    "owner": "Strategickhaos DAO LLC"
  }
}
```

### Customizing Encoding Parameters

You can modify the encoding parameters in `encoding_config.json`:

- **Sample rates**: Adjust `samples_per_char` or `samples_per_bit`
- **Frequency ranges**: Modify `range_hz` or `frequency_hz`
- **Watermark properties**: Change `cycle_seconds` or `variation_percent`

## Architecture

### Class Structure

```
EncodingConfig
├── version: str
├── encoding: Dict
└── metadata: Dict

AudioEncoder
├── __init__(config, sample_rate)
├── encode_dna_strand(sequence) → ndarray
├── encode_source_hash(hash) → (left, right)
├── encode_periodic_table(data) → ndarray
├── encode_owner(name, duration) → ndarray
├── encode_all(dna, data, owner) → Dict
├── combine_signals(encoded) → (left, right)
└── save_wav(left, right, filepath)
```

### Signal Processing Pipeline

```
Input Data → Individual Encoders → Separate Signals → Combiner → Stereo Audio → WAV File
                                                                                    
DNA Strand ──────────→ Frequency Micro Shift
Source Hash ─────────→ LR Phase Modulation
Periodic Table ──────→ Ultrasonic Harmonic     → Signal Mixer → Left/Right → Output
Owner Info ──────────→ Amplitude Watermark                      Channels
```

## Technical Details

### Audio Specifications

- **Sample Rate**: 44,100 Hz (CD quality)
- **Bit Depth**: 16-bit PCM
- **Channels**: Stereo (2 channels)
- **Format**: WAV (RIFF WAVE)

### Signal Mixing

Signals are combined with these default weights:
- DNA strand: 30%
- Source hash: 20%
- Periodic table: 10% (lower due to ultrasonic frequency)
- Owner watermark: 40%

The combined signal is normalized to prevent clipping (max amplitude = 0.95).

### Frequency Allocations

- **DNA Strand**: ~1000 Hz carrier ± 1 Hz modulation
- **Source Hash**: ~2000 Hz carrier with phase modulation
- **Periodic Table**: 19,000 Hz ultrasonic (inaudible)
- **Owner Watermark**: 440 Hz carrier (A4 note) with amplitude modulation

## Security Considerations

1. **Hash Verification**: The SHA256 hash provides cryptographic verification of source data
2. **Ultrasonic Encoding**: Data at 19kHz is inaudible but can be decoded with proper tools
3. **Watermarking**: Owner information is persistently embedded and survives audio transformations
4. **Steganography**: Multiple encoding methods provide layered data embedding

## Limitations

1. **Audible Artifacts**: DNA and hash encoding may produce audible tones
2. **Compression Sensitivity**: MP3/lossy compression may damage ultrasonic data
3. **Sample Rate Dependency**: Ultrasonic encoding requires ≥40kHz sample rate (Nyquist)
4. **Data Capacity**: Limited by audio duration and encoding density

## Future Enhancements

1. **Decoding Functions**: Implement signal extraction and decoding
2. **Error Correction**: Add Reed-Solomon or similar error correction codes
3. **Compression Resilience**: Implement redundancy for lossy compression survival
4. **Additional Methods**: Add spread spectrum or OFDM encoding options
5. **Real-time Processing**: Support streaming audio encoding

## Troubleshooting

### Issue: scipy not found
**Solution**: The system will automatically fall back to saving as `.npy` files if scipy is not available. Install scipy for WAV support:
```bash
pip install scipy
```

### Issue: Audio sounds distorted
**Solution**: Reduce the mixing weights or adjust the normalization factor in `combine_signals()`.

### Issue: Invalid DNA sequence length
**Solution**: Ensure your DNA sequence is exactly 88 characters as specified in the configuration.

### Issue: Invalid hash length
**Solution**: Provide a valid 64-character hexadecimal SHA256 hash.

## References

- Audio steganography techniques
- Digital watermarking standards
- Ultrasonic data transmission
- Phase modulation in stereo audio

## License

Part of the Sovereignty Architecture project by Strategickhaos DAO LLC.

## Contact

For questions or issues, please refer to the main project documentation.

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-29  
**Author**: Strategickhaos DAO LLC
