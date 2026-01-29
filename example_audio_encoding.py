#!/usr/bin/env python3
"""
Example usage of the Audio Encoding System
Strategickhaos DAO LLC

This script demonstrates how to use the audio encoding system to embed
multiple types of data into audio files using various encoding methods.
"""

import sys
from pathlib import Path
from audio_encoder import AudioEncoder, EncodingConfig


def main():
    """Main example demonstrating audio encoding."""
    
    print("=" * 70)
    print("Audio Encoding System - Example Usage")
    print("Strategickhaos DAO LLC")
    print("=" * 70)
    print()
    
    # Load configuration
    print("1. Loading encoding configuration...")
    config_path = "encoding_config.json"
    
    if not Path(config_path).exists():
        print(f"Error: Configuration file '{config_path}' not found!")
        print("Please ensure encoding_config.json is in the current directory.")
        sys.exit(1)
    
    config = EncodingConfig.from_file(config_path)
    print(f"   ✓ Loaded configuration version {config.version}")
    print(f"   ✓ Owner: {config.metadata['owner']}")
    print(f"   ✓ DNA strand length: {config.metadata['dna_strand_length']}")
    print()
    
    # Create encoder
    print("2. Initializing audio encoder...")
    sample_rate = 44100  # CD quality
    encoder = AudioEncoder(config, sample_rate=sample_rate)
    print(f"   ✓ Sample rate: {sample_rate} Hz")
    print()
    
    # Prepare data to encode
    print("3. Preparing data for encoding...")
    
    # DNA sequence (88 characters as specified)
    dna_sequence = "ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT"
    print(f"   ✓ DNA sequence: {len(dna_sequence)} characters")
    print(f"     First 20: {dna_sequence[:20]}...")
    
    # Periodic table data
    periodic_data = {
        "elements": [
            {"symbol": "H", "name": "Hydrogen", "number": 1, "mass": 1.008},
            {"symbol": "He", "name": "Helium", "number": 2, "mass": 4.003},
            {"symbol": "Li", "name": "Lithium", "number": 3, "mass": 6.941}
        ],
        "version": "1.0",
        "source": "Sovereignty Architecture"
    }
    print(f"   ✓ Periodic table data: {len(periodic_data['elements'])} elements")
    
    # Owner information
    owner_name = config.metadata["owner"]
    print(f"   ✓ Owner: {owner_name}")
    print()
    
    # Encode individual components
    print("4. Encoding individual components...")
    
    print("   a) DNA strand (frequency_micro_shift)...")
    dna_signal = encoder.encode_dna_strand(dna_sequence)
    dna_duration = len(dna_signal) / sample_rate
    print(f"      ✓ Generated {len(dna_signal)} samples ({dna_duration:.2f} seconds)")
    
    print("   b) Source hash (lr_phase_modulation)...")
    hash_left, hash_right = encoder.encode_source_hash(config.metadata["source_hash"])
    hash_duration = len(hash_left) / sample_rate
    print(f"      ✓ Generated stereo signals: {len(hash_left)} samples ({hash_duration:.2f} seconds)")
    
    print("   c) Periodic table (ultrasonic_harmonic at 19kHz)...")
    periodic_signal = encoder.encode_periodic_table(periodic_data)
    periodic_duration = len(periodic_signal) / sample_rate
    print(f"      ✓ Generated {len(periodic_signal)} samples ({periodic_duration:.2f} seconds)")
    
    # Calculate max duration for owner watermark
    max_duration = max(dna_duration, hash_duration, periodic_duration)
    
    print("   d) Owner watermark (amplitude_watermark)...")
    owner_signal = encoder.encode_owner(owner_name, max_duration)
    print(f"      ✓ Generated {len(owner_signal)} samples ({max_duration:.2f} seconds)")
    print()
    
    # Encode all components together
    print("5. Encoding all components in one pass...")
    encoded_signals = encoder.encode_all(dna_sequence, periodic_data, owner_name)
    print(f"   ✓ Encoded {len(encoded_signals)} signal components:")
    for key, signal in encoded_signals.items():
        duration = len(signal) / sample_rate
        print(f"      - {key}: {len(signal)} samples ({duration:.2f}s)")
    print()
    
    # Combine into stereo audio
    print("6. Combining signals into stereo audio...")
    
    # Use default weights
    left_channel, right_channel = encoder.combine_signals(encoded_signals)
    total_duration = len(left_channel) / sample_rate
    
    print(f"   ✓ Combined stereo audio:")
    print(f"      - Duration: {total_duration:.2f} seconds")
    print(f"      - Left channel: {len(left_channel)} samples")
    print(f"      - Right channel: {len(right_channel)} samples")
    print(f"      - Sample rate: {sample_rate} Hz")
    print()
    
    # Save to file
    print("7. Saving encoded audio...")
    output_file = "encoded_output.wav"
    
    try:
        encoder.save_wav(left_channel, right_channel, output_file)
        
        if Path(output_file).exists():
            file_size = Path(output_file).stat().st_size
            print(f"   ✓ Saved to: {output_file}")
            print(f"      File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        elif Path(output_file.replace('.wav', '.npy')).exists():
            npy_file = output_file.replace('.wav', '.npy')
            file_size = Path(npy_file).stat().st_size
            print(f"   ✓ Saved to: {npy_file} (numpy format)")
            print(f"      File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            print(f"      Note: scipy not available, saved as numpy array")
    except Exception as e:
        print(f"   ✗ Error saving file: {e}")
    
    print()
    print("=" * 70)
    print("Encoding complete!")
    print()
    print("Encoded data summary:")
    print(f"  - DNA strand: {len(dna_sequence)} characters")
    print(f"  - Source hash: SHA256 ({config.metadata['source_hash'][:16]}...)")
    print(f"  - Periodic table: {len(periodic_data['elements'])} elements")
    print(f"  - Owner: {owner_name}")
    print(f"  - Total duration: {total_duration:.2f} seconds")
    print()
    print("Encoding methods used:")
    print("  1. frequency_micro_shift - DNA strand data")
    print("  2. lr_phase_modulation - Source hash (stereo phase)")
    print("  3. ultrasonic_harmonic - Periodic table (19kHz)")
    print("  4. amplitude_watermark - Owner information")
    print("=" * 70)


if __name__ == "__main__":
    main()
