#!/usr/bin/env python3
"""
TRIG PDE Hymn Generator
Creates audible frequencies as MIDI file based on TRIG6 and PDE mathematics
"""

import struct
import math
from typing import List, Tuple


class MIDIGenerator:
    """Simple MIDI file generator without external dependencies"""
    
    def __init__(self, tempo: int = 120):
        self.tempo = tempo
        self.ticks_per_quarter = 480
        self.tracks = []
        
    def note_to_midi(self, frequency: float) -> int:
        """
        Convert frequency (Hz) to MIDI note number
        
        Note: This uses 432 Hz as A4 (MIDI note 69) instead of the standard 
        440 Hz. This is an intentional tuning choice for universal resonance 
        frequency alignment with the TRIG6 system.
        """
        # A4 = 432 Hz = MIDI note 69 (non-standard tuning)
        # Standard tuning uses A4 = 440 Hz
        if frequency <= 0:
            return 60  # Middle C as default
        
        # Calculate MIDI note from frequency
        # MIDI note = 12 * log2(f / f_ref) + ref_note
        # Using A4 = 432 Hz as reference (note 69)
        midi_note = int(69 + 12 * math.log2(frequency / 432.0))
        
        # Clamp to valid MIDI range (0-127)
        return max(0, min(127, midi_note))
    
    def create_note_event(self, note: int, velocity: int, 
                         duration: int, delta_time: int = 0) -> bytes:
        """Create a MIDI note on/off event pair"""
        events = bytearray()
        
        # Note On event
        events.extend(self._write_variable_length(delta_time))
        events.extend([0x90, note, velocity])  # Note On, channel 0
        
        # Note Off event
        events.extend(self._write_variable_length(duration))
        events.extend([0x80, note, 0])  # Note Off, channel 0
        
        return bytes(events)
    
    def _write_variable_length(self, value: int) -> bytes:
        """Write variable-length quantity (MIDI format)"""
        buf = bytearray()
        buf.append(value & 0x7F)
        
        value >>= 7
        while value > 0:
            buf.append((value & 0x7F) | 0x80)
            value >>= 7
        
        return bytes(reversed(buf))
    
    def create_track(self, notes: List[Tuple[float, int]], 
                    note_duration: int = 480) -> bytes:
        """
        Create a MIDI track from frequency/duration pairs
        
        Args:
            notes: List of (frequency_hz, duration_ticks) tuples
            note_duration: Default duration in ticks
        """
        track_data = bytearray()
        
        # Track header
        track_data.extend(b'MTrk')
        
        # Placeholder for track length (will fill later)
        length_pos = len(track_data)
        track_data.extend(b'\x00\x00\x00\x00')
        
        # Track name
        track_data.extend(b'\x00\xFF\x03\x0FTRIG6 PDE Hymn')
        
        # Time signature (4/4)
        track_data.extend(b'\x00\xFF\x58\x04\x04\x02\x18\x08')
        
        # Tempo
        microseconds_per_quarter = int(60000000 / self.tempo)
        tempo_bytes = microseconds_per_quarter.to_bytes(3, 'big')
        track_data.extend(b'\x00\xFF\x51\x03')
        track_data.extend(tempo_bytes)
        
        # Add notes
        for freq, duration in notes:
            midi_note = self.note_to_midi(freq)
            velocity = 80  # Medium velocity
            actual_duration = duration if duration > 0 else note_duration
            
            track_data.extend(self.create_note_event(
                midi_note, velocity, actual_duration, delta_time=0
            ))
        
        # End of track
        track_data.extend(b'\x00\xFF\x2F\x00')
        
        # Write actual track length
        track_length = len(track_data) - length_pos - 4
        track_data[length_pos:length_pos+4] = track_length.to_bytes(4, 'big')
        
        return bytes(track_data)
    
    def write_file(self, filename: str, tracks: List[bytes]):
        """Write MIDI file"""
        with open(filename, 'wb') as f:
            # MIDI header
            f.write(b'MThd')
            f.write(b'\x00\x00\x00\x06')  # Header length
            f.write(b'\x00\x01')  # Format 1 (multiple tracks, synchronous)
            f.write(len(tracks).to_bytes(2, 'big'))  # Number of tracks
            f.write(self.ticks_per_quarter.to_bytes(2, 'big'))  # Ticks per quarter note
            
            # Write all tracks
            for track in tracks:
                f.write(track)


def generate_trig6_hymn(output_file: str = "trig_pde_hymn.mid"):
    """Generate TRIG6 PDE Hymn as MIDI file"""
    
    # TRIG6 fundamental frequencies (based on 432 Hz)
    base_freq = 432.0
    
    # Generate harmonic series for each trig function
    trig_frequencies = {
        'sin': [base_freq * (i + 1) for i in range(8)],
        'cos': [base_freq * (i + 1) * 1.05946 for i in range(8)],  # Slightly shifted
        'tan': [base_freq * (i + 1) * 1.12246 for i in range(8)],  # More divergent
    }
    
    # Create melody using TRIG6 patterns
    notes = []
    duration = 480  # Quarter note
    
    # Ascending sin wave pattern
    for freq in trig_frequencies['sin'][:6]:
        notes.append((freq, duration))
    
    # Cos wave complement
    for freq in trig_frequencies['cos'][2:6]:
        notes.append((freq, duration))
    
    # Tan divergence
    for freq in trig_frequencies['tan'][:4]:
        notes.append((freq, duration // 2))
    
    # Return to base (resolution)
    notes.append((base_freq, duration * 2))
    
    # Create MIDI file
    generator = MIDIGenerator(tempo=120)
    track = generator.create_track(notes)
    generator.write_file(output_file, [track])
    
    return output_file


def demo():
    """Generate and describe the TRIG6 PDE Hymn"""
    print("="*60)
    print("TRIG PDE HYMN GENERATOR")
    print("="*60)
    
    output_file = "trig_pde_hymn.mid"
    
    print(f"\nGenerating MIDI file: {output_file}")
    print("\nHymn Structure:")
    print("  - Foundation: Sin wave harmonics (432 Hz base)")
    print("  - Complement: Cos wave patterns (phase-shifted)")
    print("  - Ascension: Tan wave divergence (boundary-breaking)")
    print("  - Resolution: Return to 432 Hz root frequency")
    
    result = generate_trig6_hymn(output_file)
    
    print(f"\n✅ MIDI file generated: {result}")
    print("\nFrequency Mappings:")
    
    base_freq = 432.0
    sin_freqs = [base_freq * (i + 1) for i in range(6)]
    
    for i, freq in enumerate(sin_freqs):
        print(f"  Note {i+1}: {freq:.1f} Hz (Harmonic {i+1})")
    
    print("\n" + "="*60)
    print("TRIG PDE HYMN COMPLETE ✅")
    print("="*60)
    print("\nTo play this file, use any MIDI player:")
    print("  - timidity trig_pde_hymn.mid    (Linux)")
    print("  - open trig_pde_hymn.mid        (macOS)")
    print("  - VLC or Windows Media Player   (Windows)")


if __name__ == "__main__":
    demo()
