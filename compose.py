#!/usr/bin/env python3
"""
TRIG6 COMPOSE — Geometry → Music Compiler
==========================================
Converts KHAOS periodic table glyphs into playable MIDI.

NOT a description. NOT a promise. An ARTIFACT.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
License: MIT

Usage:
    python compose.py --source khaos --outfile hymn.mid
    python compose.py --points "[(0, 1.0, 0.5), (45, 0.8, 0.3)]" --outfile custom.mid
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Tuple
import ast

# ═══════════════════════════════════════════════════════════════════════════════
# MIDI WRITER (Zero Dependencies - Pure Python)
# ═══════════════════════════════════════════════════════════════════════════════

class MidiWriter:
    """
    Minimal MIDI file writer. No external dependencies.
    Writes Format 0 (single track) MIDI files.
    """
    
    def __init__(self, tempo_bpm: int = 120, ticks_per_beat: int = 480):
        self.tempo_bpm = tempo_bpm
        self.ticks_per_beat = ticks_per_beat
        self.events = []  # (tick, event_bytes)
    
    def _var_length(self, value: int) -> bytes:
        """Encode variable-length quantity for MIDI"""
        result = []
        result.append(value & 0x7F)
        value >>= 7
        while value:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
        return bytes(reversed(result))
    
    def _int16(self, value: int) -> bytes:
        """Big-endian 16-bit integer"""
        return value.to_bytes(2, 'big')
    
    def _int32(self, value: int) -> bytes:
        """Big-endian 32-bit integer"""
        return value.to_bytes(4, 'big')
    
    def note_on(self, tick: int, channel: int, note: int, velocity: int):
        """Add note-on event"""
        self.events.append((tick, bytes([0x90 | (channel & 0x0F), note & 0x7F, velocity & 0x7F])))
    
    def note_off(self, tick: int, channel: int, note: int, velocity: int = 0):
        """Add note-off event"""
        self.events.append((tick, bytes([0x80 | (channel & 0x0F), note & 0x7F, velocity & 0x7F])))
    
    def add_note(self, start_tick: int, duration_ticks: int, channel: int, note: int, velocity: int):
        """Add a complete note (on + off)"""
        self.note_on(start_tick, channel, note, velocity)
        self.note_off(start_tick + duration_ticks, channel, note, 0)
    
    def write(self, filepath: str) -> int:
        """Write MIDI file. Returns bytes written."""
        # Sort events by tick
        self.events.sort(key=lambda x: x[0])
        
        # Build track data
        track_data = bytearray()
        
        # Tempo meta event (at tick 0)
        microseconds_per_beat = int(60_000_000 / self.tempo_bpm)
        tempo_bytes = microseconds_per_beat.to_bytes(3, 'big')
        track_data.extend(b'\x00')  # Delta time 0
        track_data.extend(b'\xFF\x51\x03')  # Tempo meta event
        track_data.extend(tempo_bytes)
        
        # Convert absolute ticks to delta times and write events
        last_tick = 0
        for tick, event_bytes in self.events:
            delta = tick - last_tick
            track_data.extend(self._var_length(delta))
            track_data.extend(event_bytes)
            last_tick = tick
        
        # End of track
        track_data.extend(b'\x00\xFF\x2F\x00')
        
        # Build file
        midi_data = bytearray()
        
        # Header chunk
        midi_data.extend(b'MThd')  # Chunk type
        midi_data.extend(self._int32(6))  # Chunk length
        midi_data.extend(self._int16(0))  # Format 0
        midi_data.extend(self._int16(1))  # 1 track
        midi_data.extend(self._int16(self.ticks_per_beat))  # Ticks per beat
        
        # Track chunk
        midi_data.extend(b'MTrk')  # Chunk type
        midi_data.extend(self._int32(len(track_data)))  # Chunk length
        midi_data.extend(track_data)
        
        # Write file
        Path(filepath).write_bytes(midi_data)
        return len(midi_data)


# ═══════════════════════════════════════════════════════════════════════════════
# KHAOS GLYPH REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

# 64 glyphs, 6 families, 5.625° per step
KHAOS_GLYPHS = [
    # SIN family (0-10): Rising, ascending
    {"id": 0,  "glyph": "⟋",    "family": "SIN", "theta": 0.0},
    {"id": 1,  "glyph": "⟋•",   "family": "SIN", "theta": 5.625},
    {"id": 2,  "glyph": "⟋••",  "family": "SIN", "theta": 11.25},
    {"id": 3,  "glyph": "⟋+",   "family": "SIN", "theta": 16.875},
    {"id": 4,  "glyph": "⟋○",   "family": "SIN", "theta": 22.5},
    {"id": 5,  "glyph": "⟋̅",    "family": "SIN", "theta": 28.125},
    {"id": 6,  "glyph": "⟋_",   "family": "SIN", "theta": 33.75},
    {"id": 7,  "glyph": "⟋⌐",   "family": "SIN", "theta": 39.375},
    {"id": 8,  "glyph": "⟋◉",   "family": "SIN", "theta": 45.0},
    {"id": 9,  "glyph": "⟋⌐⌐",  "family": "SIN", "theta": 50.625},
    {"id": 10, "glyph": "⟋~",   "family": "SIN", "theta": 56.25},
    
    # COS family (11-21): Grounded, horizontal
    {"id": 11, "glyph": "—",    "family": "COS", "theta": 61.875},
    {"id": 12, "glyph": "—•",   "family": "COS", "theta": 67.5},
    {"id": 13, "glyph": "—••",  "family": "COS", "theta": 73.125},
    {"id": 14, "glyph": "—⌐",   "family": "COS", "theta": 78.75},
    {"id": 15, "glyph": "—∧",   "family": "COS", "theta": 84.375},
    {"id": 16, "glyph": "—◇",   "family": "COS", "theta": 90.0},  # First singularity
    {"id": 17, "glyph": "—○",   "family": "COS", "theta": 95.625},
    {"id": 18, "glyph": "—+",   "family": "COS", "theta": 101.25},
    {"id": 19, "glyph": "—~",   "family": "COS", "theta": 106.875},
    {"id": 20, "glyph": "—∨",   "family": "COS", "theta": 112.5},
    {"id": 21, "glyph": "—_",   "family": "COS", "theta": 118.125},
    
    # TAN family (22-31): Transformation, sharps
    {"id": 22, "glyph": "╱",    "family": "TAN", "theta": 123.75},
    {"id": 23, "glyph": "╱•",   "family": "TAN", "theta": 129.375},
    {"id": 24, "glyph": "╱••",  "family": "TAN", "theta": 135.0},
    {"id": 25, "glyph": "╱+",   "family": "TAN", "theta": 140.625},
    {"id": 26, "glyph": "╱○",   "family": "TAN", "theta": 146.25},
    {"id": 27, "glyph": "╱̅",    "family": "TAN", "theta": 151.875},
    {"id": 28, "glyph": "╱_",   "family": "TAN", "theta": 157.5},
    {"id": 29, "glyph": "╱⌐",   "family": "TAN", "theta": 163.125},
    {"id": 30, "glyph": "╱∧",   "family": "TAN", "theta": 168.75},
    {"id": 31, "glyph": "╱◇",   "family": "TAN", "theta": 174.375},
    
    # CSC family (32-42): Reflection, sustains
    {"id": 32, "glyph": "|",    "family": "CSC", "theta": 180.0},  # Second singularity
    {"id": 33, "glyph": "|•",   "family": "CSC", "theta": 185.625},
    {"id": 34, "glyph": "|••",  "family": "CSC", "theta": 191.25},
    {"id": 35, "glyph": "|+",   "family": "CSC", "theta": 196.875},
    {"id": 36, "glyph": "|○",   "family": "CSC", "theta": 202.5},
    {"id": 37, "glyph": "|̅",    "family": "CSC", "theta": 208.125},
    {"id": 38, "glyph": "|_",   "family": "CSC", "theta": 213.75},
    {"id": 39, "glyph": "|⌐",   "family": "CSC", "theta": 219.375},
    {"id": 40, "glyph": "|∧",   "family": "CSC", "theta": 225.0},
    {"id": 41, "glyph": "|~",   "family": "CSC", "theta": 230.625},
    {"id": 42, "glyph": "|∨",   "family": "CSC", "theta": 236.25},
    
    # SEC family (43-52): Bounds, accents
    {"id": 43, "glyph": "]",    "family": "SEC", "theta": 241.875},
    {"id": 44, "glyph": "]•",   "family": "SEC", "theta": 247.5},
    {"id": 45, "glyph": "]••",  "family": "SEC", "theta": 253.125},
    {"id": 46, "glyph": "]+",   "family": "SEC", "theta": 258.75},
    {"id": 47, "glyph": "]○",   "family": "SEC", "theta": 264.375},
    {"id": 48, "glyph": "]◇",   "family": "SEC", "theta": 270.0},  # Third singularity
    {"id": 49, "glyph": "]̅",    "family": "SEC", "theta": 275.625},
    {"id": 50, "glyph": "]_",   "family": "SEC", "theta": 281.25},
    {"id": 51, "glyph": "]⌐",   "family": "SEC", "theta": 286.875},
    {"id": 52, "glyph": "]∧",   "family": "SEC", "theta": 292.5},
    
    # COT family (53-63): Resolution, seals
    {"id": 53, "glyph": "]~",   "family": "COT", "theta": 298.125},
    {"id": 54, "glyph": "╲",    "family": "COT", "theta": 303.75},
    {"id": 55, "glyph": "╲•",   "family": "COT", "theta": 309.375},
    {"id": 56, "glyph": "╲••",  "family": "COT", "theta": 315.0},
    {"id": 57, "glyph": "╲+",   "family": "COT", "theta": 320.625},
    {"id": 58, "glyph": "╲○",   "family": "COT", "theta": 326.25},
    {"id": 59, "glyph": "╲̅",    "family": "COT", "theta": 331.875},
    {"id": 60, "glyph": "╲_",   "family": "COT", "theta": 337.5},
    {"id": 61, "glyph": "╲⌐",   "family": "COT", "theta": 343.125},
    {"id": 62, "glyph": "╲∧",   "family": "COT", "theta": 348.75},
    {"id": 63, "glyph": "╲∨",   "family": "COT", "theta": 354.375},
]

# Family characteristics (affects musical expression)
FAMILY_PROFILES = {
    "SIN": {"base_velocity": 80, "duration_mult": 1.0, "channel": 0},   # Piano, ascending
    "COS": {"base_velocity": 70, "duration_mult": 1.5, "channel": 0},   # Piano, sustained
    "TAN": {"base_velocity": 90, "duration_mult": 0.75, "channel": 0},  # Piano, sharp
    "CSC": {"base_velocity": 75, "duration_mult": 1.25, "channel": 0},  # Piano, reflective
    "SEC": {"base_velocity": 85, "duration_mult": 0.5, "channel": 0},   # Piano, accented
    "COT": {"base_velocity": 65, "duration_mult": 2.0, "channel": 0},   # Piano, resolved
}

# Singularity indices (crescendo/peak moments)
SINGULARITIES = [16, 32, 48]  # 90°, 180°, 270°


# ═══════════════════════════════════════════════════════════════════════════════
# NOTE EVENT DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class NoteEvent:
    """A single note in the composition"""
    glyph_id: int
    glyph: str
    family: str
    theta: float
    midi_note: int
    velocity: int
    start_beat: float
    duration_beats: float
    
    def to_dict(self):
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════════
# COMPOSE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class KhaosComposer:
    """
    Compiles the KHAOS periodic table into a MIDI hymn.
    
    Mapping:
        - Pitch: glyph ID → MIDI note (C4 base, 2-octave range)
        - Timing: θ position → start time (full circle = 16 beats)
        - Duration: family profile → note length
        - Velocity: family profile + singularity boost
    """
    
    def __init__(self, tempo: int = 120, base_note: int = 60, beats_per_cycle: float = 16.0):
        self.tempo = tempo
        self.base_note = base_note  # C4 = 60
        self.beats_per_cycle = beats_per_cycle
        self.events: List[NoteEvent] = []
    
    def _theta_to_beat(self, theta: float) -> float:
        """Convert angular position to beat position"""
        return (theta / 360.0) * self.beats_per_cycle
    
    def _id_to_note(self, glyph_id: int) -> int:
        """Convert glyph ID to MIDI note (2-octave range, wrapping)"""
        return self.base_note + (glyph_id % 24)
    
    def _compute_velocity(self, glyph_id: int, family: str) -> int:
        """Compute note velocity with singularity boost"""
        base = FAMILY_PROFILES[family]["base_velocity"]
        
        # Boost at singularities (crescendo peaks)
        if glyph_id in SINGULARITIES:
            base = min(127, base + 30)
        
        # Slight variation based on position in family
        variation = (glyph_id % 11) - 5  # -5 to +5
        
        return max(1, min(127, base + variation))
    
    def _compute_duration(self, family: str) -> float:
        """Compute note duration based on family"""
        base_duration = 0.5  # Half beat default
        mult = FAMILY_PROFILES[family]["duration_mult"]
        return base_duration * mult
    
    def compile_periodic_table(self) -> List[NoteEvent]:
        """Compile all 64 glyphs into note events"""
        self.events = []
        
        for glyph_data in KHAOS_GLYPHS:
            glyph_id = glyph_data["id"]
            family = glyph_data["family"]
            theta = glyph_data["theta"]
            
            event = NoteEvent(
                glyph_id=glyph_id,
                glyph=glyph_data["glyph"],
                family=family,
                theta=theta,
                midi_note=self._id_to_note(glyph_id),
                velocity=self._compute_velocity(glyph_id, family),
                start_beat=self._theta_to_beat(theta),
                duration_beats=self._compute_duration(family),
            )
            self.events.append(event)
        
        return self.events
    
    def compile_custom_points(self, points: List[Tuple[float, float, float]]) -> List[NoteEvent]:
        """
        Compile custom geometry points into note events.
        
        Args:
            points: List of (theta_degrees, radius, diameter) tuples
                   - theta → pitch (via glyph ID)
                   - radius → duration
                   - diameter → velocity
        """
        self.events = []
        
        # Normalize radius/diameter for mapping
        if not points:
            return self.events
        
        radii = [p[1] for p in points]
        diameters = [p[2] for p in points]
        r_max = max(radii) if max(radii) > 0 else 1.0
        d_max = max(diameters) if max(diameters) > 0 else 1.0
        
        for i, (theta, radius, diameter) in enumerate(points):
            # Theta to glyph ID
            glyph_id = int(round(theta / 5.625)) % 64
            glyph_data = KHAOS_GLYPHS[glyph_id]
            
            # Radius to duration (0.25 to 2 beats)
            duration = 0.25 + 1.75 * (radius / r_max)
            
            # Diameter to velocity (40 to 127)
            velocity = int(40 + 87 * (diameter / d_max))
            velocity = max(1, min(127, velocity))
            
            event = NoteEvent(
                glyph_id=glyph_id,
                glyph=glyph_data["glyph"],
                family=glyph_data["family"],
                theta=theta,
                midi_note=self._id_to_note(glyph_id),
                velocity=velocity,
                start_beat=self._theta_to_beat(theta),
                duration_beats=duration,
            )
            self.events.append(event)
        
        return self.events
    
    def to_midi(self, filepath: str) -> dict:
        """
        Write composition to MIDI file.
        
        Returns:
            {
                "filepath": str,
                "bytes_written": int,
                "note_count": int,
                "duration_beats": float,
                "duration_seconds": float
            }
        """
        if not self.events:
            self.compile_periodic_table()
        
        midi = MidiWriter(tempo_bpm=self.tempo)
        ticks_per_beat = midi.ticks_per_beat
        
        for event in self.events:
            start_tick = int(event.start_beat * ticks_per_beat)
            duration_ticks = int(event.duration_beats * ticks_per_beat)
            channel = FAMILY_PROFILES[event.family]["channel"]
            
            midi.add_note(
                start_tick=start_tick,
                duration_ticks=duration_ticks,
                channel=channel,
                note=event.midi_note,
                velocity=event.velocity,
            )
        
        bytes_written = midi.write(filepath)
        
        # Calculate total duration
        if self.events:
            last_event = max(self.events, key=lambda e: e.start_beat + e.duration_beats)
            total_beats = last_event.start_beat + last_event.duration_beats
        else:
            total_beats = 0
        
        return {
            "filepath": filepath,
            "bytes_written": bytes_written,
            "note_count": len(self.events),
            "duration_beats": total_beats,
            "duration_seconds": (total_beats / self.tempo) * 60,
        }
    
    def to_json(self, filepath: str) -> int:
        """Write composition audit trail to JSON"""
        data = {
            "meta": {
                "tempo": self.tempo,
                "base_note": self.base_note,
                "beats_per_cycle": self.beats_per_cycle,
                "note_count": len(self.events),
            },
            "events": [e.to_dict() for e in self.events],
            "families": FAMILY_PROFILES,
            "singularities": SINGULARITIES,
        }
        
        Path(filepath).write_text(json.dumps(data, indent=2))
        return len(self.events)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="TRIG6 COMPOSE — Geometry to Music Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compile the full KHAOS periodic table to MIDI
  python compose.py --source khaos --outfile khaos_hymn.mid

  # Custom points from your drawing (theta, radius, diameter)
  python compose.py --points "[(45, 0.5, 0.125), (90, 0.75, 0.1875)]" --outfile custom.mid

  # Change tempo and base note
  python compose.py --source khaos --tempo 90 --base-note 48 --outfile slow_hymn.mid

Owner: Strategickhaos DAO LLC
        """
    )
    
    parser.add_argument("--source", choices=["khaos", "custom"], default="khaos",
                       help="Source: 'khaos' for periodic table, 'custom' for points")
    parser.add_argument("--points", type=str, default=None,
                       help="Custom points as Python list: [(theta, radius, diameter), ...]")
    parser.add_argument("--tempo", type=int, default=120,
                       help="Tempo in BPM (default: 120)")
    parser.add_argument("--base-note", type=int, default=60,
                       help="Base MIDI note (default: 60 = C4)")
    parser.add_argument("--outfile", type=str, default="khaos_hymn.mid",
                       help="Output MIDI filename")
    parser.add_argument("--json", action="store_true",
                       help="Also output JSON audit trail")
    
    args = parser.parse_args()
    
    # Create composer
    composer = KhaosComposer(
        tempo=args.tempo,
        base_note=args.base_note,
    )
    
    # Compile source
    if args.source == "khaos":
        print(f"🎵 Compiling KHAOS Periodic Table...")
        composer.compile_periodic_table()
    elif args.source == "custom":
        if not args.points:
            print("❌ Custom source requires --points argument")
            return 1
        print(f"🎵 Compiling custom geometry points...")
        try:
            points = ast.literal_eval(args.points)
            composer.compile_custom_points(points)
        except Exception as e:
            print(f"❌ Error parsing points: {e}")
            return 1
    else:
        print("❌ Invalid source option")
        return 1
    
    # Write MIDI
    result = composer.to_midi(args.outfile)
    
    print(f"")
    print(f"═══════════════════════════════════════════════════════")
    print(f"  TRIG6 COMPOSE — COMPLETE")
    print(f"═══════════════════════════════════════════════════════")
    print(f"  Output:    {result['filepath']}")
    print(f"  Size:      {result['bytes_written']} bytes")
    print(f"  Notes:     {result['note_count']}")
    print(f"  Duration:  {result['duration_beats']:.1f} beats ({result['duration_seconds']:.1f} sec)")
    print(f"  Tempo:     {args.tempo} BPM")
    print(f"═══════════════════════════════════════════════════════")
    print(f"")
    print(f"  ▶ Play with: vlc {args.outfile}")
    print(f"               timidity {args.outfile}")
    print(f"               open {args.outfile}  (macOS)")
    print(f"")
    
    # Optional JSON audit
    if args.json:
        outfile_path = Path(args.outfile)
        if outfile_path.suffix.lower() in [".mid", ".midi"]:
            json_file = str(outfile_path.with_suffix(".json"))
        else:
            json_file = str(outfile_path) + ".json"
        composer.to_json(json_file)
        print(f"  📋 Audit trail: {json_file}")
        print(f"")
    
    print(f"  Owner: Strategickhaos DAO LLC")
    print(f"  🎶 Stop describing the hymn. Start hearing it.")
    print(f"")
    
    return 0


if __name__ == "__main__":
    exit(main())
