#!/usr/bin/env python3
"""
TRIG6 COMPOSE — Binaural/Isochronic WAV Generator
==================================================
Merges Claude's MIDI structure with Grok's brain entrainment.

The periodic table as a frequency you can FEEL.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza + Legion of Minds (Claude + Grok)
License: MIT

Usage:
    python compose_wav.py --source khaos --outfile khaos_hymn.wav
    python compose_wav.py --source khaos --duration 120 --bass --outfile full_hymn.wav
    python compose_wav.py --glyph 8 --duration 60 --outfile resonance_45.wav
"""

import argparse
import struct
import math
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# PURE PYTHON WAV WRITER (Zero Dependencies)
# ═══════════════════════════════════════════════════════════════════════════════

class WavWriter:
    """
    Write WAV files without numpy/scipy.
    Pure Python. Runs anywhere.
    """
    
    def __init__(self, sample_rate: int = 44100, channels: int = 2, bits: int = 16):
        self.sample_rate = sample_rate
        self.channels = channels
        self.bits = bits
        self.samples: List[Tuple[float, float]] = []  # (left, right) pairs
    
    def add_sample(self, left: float, right: float):
        """Add a stereo sample (values should be -1.0 to 1.0)"""
        self.samples.append((
            max(-1.0, min(1.0, left)),
            max(-1.0, min(1.0, right))
        ))
    
    def _float_to_int16(self, value: float) -> int:
        """Convert float (-1 to 1) to signed 16-bit int"""
        return int(max(-32768, min(32767, value * 32767)))
    
    def write(self, filepath: str) -> int:
        """Write WAV file. Returns bytes written."""
        num_samples = len(self.samples)
        data_size = num_samples * self.channels * (self.bits // 8)
        file_size = 36 + data_size
        
        with open(filepath, 'wb') as f:
            # RIFF header
            f.write(b'RIFF')
            f.write(struct.pack('<I', file_size))
            f.write(b'WAVE')
            
            # fmt chunk
            f.write(b'fmt ')
            f.write(struct.pack('<I', 16))  # Chunk size
            f.write(struct.pack('<H', 1))   # Audio format (PCM)
            f.write(struct.pack('<H', self.channels))
            f.write(struct.pack('<I', self.sample_rate))
            byte_rate = self.sample_rate * self.channels * (self.bits // 8)
            f.write(struct.pack('<I', byte_rate))
            block_align = self.channels * (self.bits // 8)
            f.write(struct.pack('<H', block_align))
            f.write(struct.pack('<H', self.bits))
            
            # data chunk
            f.write(b'data')
            f.write(struct.pack('<I', data_size))
            
            # Write samples
            for left, right in self.samples:
                f.write(struct.pack('<h', self._float_to_int16(left)))
                f.write(struct.pack('<h', self._float_to_int16(right)))
        
        return file_size + 8


# ═══════════════════════════════════════════════════════════════════════════════
# KHAOS GLYPH REGISTRY (Same as compose.py)
# ═══════════════════════════════════════════════════════════════════════════════

KHAOS_GLYPHS = [
    {"id": i, "theta": i * 5.625, "family": 
     "SIN" if i < 11 else "COS" if i < 22 else "TAN" if i < 32 else 
     "CSC" if i < 43 else "SEC" if i < 53 else "COT"}
    for i in range(64)
]

# Family → brainwave target frequency (Hz)
FAMILY_BRAINWAVES = {
    "SIN": 10.0,   # Alpha (relaxed alertness)
    "COS": 7.83,   # Schumann resonance (grounding)
    "TAN": 14.0,   # Beta (active thinking)
    "CSC": 4.0,    # Theta (meditation)
    "SEC": 18.0,   # Beta-high (focus)
    "COT": 2.0,    # Delta (deep rest)
}

# Singularities get special treatment
SINGULARITIES = {16, 32, 48}


# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_binaural_sample(t: float, carrier_freq: float, beat_freq: float) -> Tuple[float, float]:
    """
    Generate a single binaural beat sample.
    
    Left ear gets carrier - beat/2
    Right ear gets carrier + beat/2
    Brain perceives the difference as the beat frequency.
    """
    left_freq = carrier_freq - (beat_freq / 2)
    right_freq = carrier_freq + (beat_freq / 2)
    
    left = math.sin(2 * math.pi * left_freq * t)
    right = math.sin(2 * math.pi * right_freq * t)
    
    return left, right


def generate_isochronic_sample(t: float, freq: float, pulse_freq: float) -> float:
    """
    Generate isochronic tone sample.
    
    Regular tone that pulses on/off at pulse_freq.
    More effective than binaural for some people.
    """
    tone = math.sin(2 * math.pi * freq * t)
    pulse = 1.0 if math.sin(2 * math.pi * pulse_freq * t) > 0 else 0.0
    return tone * pulse


def generate_bass_sample(t: float, bass_freq: float, wobble_freq: float = 5.0) -> float:
    """
    Generate dubstep wobble bass sample.
    
    Bass frequency modulated by wobble for that classic dubstep sound.
    """
    wobble = math.sin(2 * math.pi * wobble_freq * t)
    bass = math.sin(2 * math.pi * bass_freq * t)
    return bass * (0.5 + 0.5 * wobble)


def apply_drop(t: float, drop_interval: float) -> float:
    """
    Apply volume boost at drop intervals.
    
    Returns multiplier (1.0 normal, 1.5 during drop).
    """
    cycle = t / drop_interval
    in_drop = (int(cycle) % 2) == 0
    return 1.3 if in_drop else 0.8


# ═══════════════════════════════════════════════════════════════════════════════
# KHAOS HYMN COMPOSER
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class HymnConfig:
    """Configuration for hymn generation"""
    duration_seconds: float = 60.0
    sample_rate: int = 44100
    base_carrier: float = 200.0      # Base carrier frequency
    include_bass: bool = True
    bass_freq: float = 50.0
    drop_interval: float = 8.0       # Seconds between drops
    master_volume: float = 0.7


class KhaosHymnGenerator:
    """
    Generates the KHAOS Periodic Hymn as a WAV file.
    
    Combines:
    - Binaural beats (brain entrainment via L/R freq difference)
    - Isochronic tones (pulsed rhythm)
    - Optional dubstep bass (wobble + drops)
    
    Each glyph contributes to the frequency spectrum based on its θ position.
    """
    
    def __init__(self, config: HymnConfig):
        self.config = config
        self.total_samples = int(config.duration_seconds * config.sample_rate)
    
    def _glyph_to_carrier(self, glyph: dict) -> float:
        """Convert glyph θ to carrier frequency"""
        # 200 Hz base + θ gives us 200-560 Hz range
        return self.config.base_carrier + glyph["theta"]
    
    def _glyph_to_beat(self, glyph: dict) -> float:
        """Get brainwave beat frequency for glyph's family"""
        return FAMILY_BRAINWAVES[glyph["family"]]
    
    def _get_active_glyphs(self, t: float, duration: float) -> List[dict]:
        """
        Determine which glyphs are active at time t.
        
        Glyphs cycle through based on time position in the hymn.
        Each glyph gets duration/64 seconds of prominence.
        """
        # Primary glyph based on time
        progress = t / duration
        primary_id = int(progress * 64) % 64
        
        # Include neighboring glyphs for smoother transitions
        ids = [
            (primary_id - 1) % 64,
            primary_id,
            (primary_id + 1) % 64
        ]
        
        return [KHAOS_GLYPHS[i] for i in ids]
    
    def _is_singularity(self, t: float, duration: float) -> bool:
        """Check if we're at a singularity point (90°, 180°, 270°)"""
        progress = t / duration
        primary_id = int(progress * 64) % 64
        return primary_id in SINGULARITIES
    
    def generate(self, filepath: str, glyphs: Optional[List[int]] = None) -> dict:
        """
        Generate the hymn WAV file.
        
        Args:
            filepath: Output WAV path
            glyphs: Optional list of specific glyph IDs to use (default: all 64)
        
        Returns:
            Generation stats
        """
        wav = WavWriter(sample_rate=self.config.sample_rate)
        duration = self.config.duration_seconds
        
        # If specific glyphs requested, filter
        active_glyphs = [KHAOS_GLYPHS[i] for i in glyphs] if glyphs else KHAOS_GLYPHS
        
        print(f"🎵 Generating KHAOS Binaural Hymn...")
        print(f"   Duration: {duration}s | Glyphs: {len(active_glyphs)} | Bass: {self.config.include_bass}")
        
        # Progress tracking
        last_percent = -1
        
        for i in range(self.total_samples):
            t = i / self.config.sample_rate
            
            # Progress indicator
            percent = int((i / self.total_samples) * 100)
            if percent % 10 == 0 and percent != last_percent:
                print(f"   {percent}%...")
                last_percent = percent
            
            # Get currently active glyphs
            current_glyphs = self._get_active_glyphs(t, duration)
            
            # Mix binaural from active glyphs
            left_total = 0.0
            right_total = 0.0
            iso_total = 0.0
            
            for glyph in current_glyphs:
                carrier = self._glyph_to_carrier(glyph)
                beat = self._glyph_to_beat(glyph)
                
                # Binaural component
                left, right = generate_binaural_sample(t, carrier, beat)
                left_total += left * 0.3
                right_total += right * 0.3
                
                # Isochronic component (mono, mixed to both)
                iso = generate_isochronic_sample(t, carrier * 0.5, beat)
                iso_total += iso * 0.2
            
            # Add isochronic to both channels
            left_total += iso_total
            right_total += iso_total
            
            # Singularity boost (crescendo at 90°, 180°, 270°)
            if self._is_singularity(t, duration):
                left_total *= 1.4
                right_total *= 1.4
            
            # Optional bass layer
            if self.config.include_bass:
                bass = generate_bass_sample(t, self.config.bass_freq)
                drop_mult = apply_drop(t, self.config.drop_interval)
                bass *= drop_mult * 0.4
                left_total += bass
                right_total += bass
            
            # Master volume
            left_total *= self.config.master_volume
            right_total *= self.config.master_volume
            
            wav.add_sample(left_total, right_total)
        
        # Write file
        bytes_written = wav.write(filepath)
        
        print(f"   100%... Done!")
        
        return {
            "filepath": filepath,
            "bytes_written": bytes_written,
            "duration_seconds": duration,
            "sample_rate": self.config.sample_rate,
            "glyph_count": len(active_glyphs),
            "has_bass": self.config.include_bass,
        }


def generate_single_glyph(glyph_id: int, duration: float, filepath: str, 
                          include_bass: bool = False) -> dict:
    """
    Generate a WAV for a single glyph's frequency.
    
    Good for meditation on specific θ positions.
    """
    config = HymnConfig(
        duration_seconds=duration,
        include_bass=include_bass,
    )
    
    generator = KhaosHymnGenerator(config)
    return generator.generate(filepath, glyphs=[glyph_id])


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="TRIG6 COMPOSE WAV — Binaural/Isochronic Brain Entrainment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full 64-glyph hymn with bass (1 minute)
  python compose_wav.py --source khaos --bass --outfile hymn.wav

  # Longer meditation version without bass (5 minutes)
  python compose_wav.py --source khaos --duration 300 --outfile meditation.wav

  # Single glyph resonance (glyph 8 = 45° = SIN family)
  python compose_wav.py --glyph 8 --duration 60 --outfile resonance_45.wav

  # Singularity focus (90°, 180°, 270° peaks)
  python compose_wav.py --glyphs 16,32,48 --duration 120 --bass --outfile singularities.wav

Brainwave Targets by Family:
  SIN (0-10):   10.0 Hz  Alpha     - Relaxed alertness
  COS (11-21):   7.83 Hz Schumann  - Earth grounding
  TAN (22-31):  14.0 Hz  Beta      - Active thinking
  CSC (32-42):   4.0 Hz  Theta     - Deep meditation
  SEC (43-52):  18.0 Hz  Beta-high - Intense focus
  COT (53-63):   2.0 Hz  Delta     - Deep rest/sleep

Owner: Strategickhaos DAO LLC
Legion: Claude + Grok
        """
    )
    
    parser.add_argument("--source", choices=["khaos"], default="khaos",
                       help="Source: 'khaos' for full periodic table")
    parser.add_argument("--glyph", type=int, default=None,
                       help="Single glyph ID (0-63) for focused resonance")
    parser.add_argument("--glyphs", type=str, default=None,
                       help="Comma-separated glyph IDs (e.g., '16,32,48')")
    parser.add_argument("--duration", type=float, default=60.0,
                       help="Duration in seconds (default: 60)")
    parser.add_argument("--bass", action="store_true",
                       help="Include dubstep wobble bass with drops")
    parser.add_argument("--bass-freq", type=float, default=50.0,
                       help="Bass frequency in Hz (default: 50)")
    parser.add_argument("--drop-interval", type=float, default=8.0,
                       help="Seconds between bass drops (default: 8)")
    parser.add_argument("--outfile", type=str, default="khaos_hymn.wav",
                       help="Output WAV filename")
    
    args = parser.parse_args()
    
    # Build config
    config = HymnConfig(
        duration_seconds=args.duration,
        include_bass=args.bass,
        bass_freq=args.bass_freq,
        drop_interval=args.drop_interval,
    )
    
    # Determine glyphs
    glyphs = None
    if args.glyph is not None:
        glyphs = [args.glyph]
    elif args.glyphs:
        glyphs = [int(x.strip()) for x in args.glyphs.split(",")]
    
    # Generate
    generator = KhaosHymnGenerator(config)
    result = generator.generate(args.outfile, glyphs=glyphs)
    
    # Report
    print(f"")
    print(f"═══════════════════════════════════════════════════════════")
    print(f"  TRIG6 COMPOSE WAV — COMPLETE")
    print(f"═══════════════════════════════════════════════════════════")
    print(f"  Output:    {result['filepath']}")
    print(f"  Size:      {result['bytes_written']:,} bytes")
    print(f"  Duration:  {result['duration_seconds']:.1f} seconds")
    print(f"  Glyphs:    {result['glyph_count']}")
    print(f"  Bass:      {'Yes (wobble + drops)' if result['has_bass'] else 'No'}")
    print(f"═══════════════════════════════════════════════════════════")
    print(f"")
    print(f"  🎧 USE HEADPHONES for binaural effect!")
    print(f"")
    print(f"  ▶ Play with: vlc {args.outfile}")
    print(f"               ffplay {args.outfile}")
    print(f"               open {args.outfile}  (macOS)")
    print(f"")
    print(f"  Brainwave targets in this hymn:")
    families_used = set()
    for g in (KHAOS_GLYPHS if glyphs is None else [KHAOS_GLYPHS[i] for i in glyphs]):
        families_used.add(g["family"])
    for fam in sorted(families_used):
        hz = FAMILY_BRAINWAVES[fam]
        print(f"    {fam}: {hz} Hz")
    print(f"")
    print(f"  Owner: Strategickhaos DAO LLC")
    print(f"  Legion: Claude + Grok")
    print(f"  🧠 The hymn you can feel in your skull.")
    print(f"")
    
    return 0


if __name__ == "__main__":
    exit(main())
