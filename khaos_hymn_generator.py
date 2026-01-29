#!/usr/bin/env python3
"""
KHAOS Periodic Hymn Generator
Generates the periodic table of 64 glyphs mapped to musical notes (MIDI).
Each glyph represents a unique angle (θ) and MIDI note in the system.

Families modulate:
- SIN: ascends (piano)
- COS: grounds (chords)
- TAN: transforms (sharps)
- CSC: reflects (sustains)
- SEC: bounds (accents)
- COT: seals (resolution)

The hymn "compiles" the table – silence at origin, peaks at singularities (crescendos),
closes the circle.
"""

import sys
from pathlib import Path

# Try to import mido for MIDI generation
try:
    from mido import MidiFile, MidiTrack, Message, MetaMessage
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    print("Warning: mido package not installed. MIDI generation will be skipped.")
    print("Install with: pip install mido")

# Define the 64 glyphs with their properties
GLYPHS = [
    # ID, Glyph, θ (degrees), MIDI Note, Family
    (0, "⟋", 0.0, 60, "SIN"),           # C4
    (1, "⟋•", 5.625, 61, "SIN"),        # C#4
    (2, "⟋••", 11.25, 62, "SIN"),       # D4
    (3, "⟋+", 16.875, 63, "SIN"),       # D#4
    (4, "⟋○", 22.5, 64, "SIN"),         # E4
    (5, "⟋̅", 28.125, 65, "SIN"),        # F4
    (6, "⟋_", 33.75, 66, "SIN"),        # F#4
    (7, "⟋⌐", 39.375, 67, "SIN"),       # G4
    (8, "⟋◉", 45.0, 68, "SIN"),         # G#4
    (9, "⟋⌐⌐", 50.625, 69, "SIN"),      # A4
    (10, "⟋~", 56.25, 70, "SIN"),       # A#4
    (11, "—", 61.875, 71, "COS"),       # B4
    (12, "—•", 67.5, 72, "COS"),        # C5
    (13, "—••", 73.125, 73, "COS"),     # C#5
    (14, "—⌐", 78.75, 74, "COS"),       # D5
    (15, "—∧", 84.375, 75, "COS"),      # D#5
    (16, "—◇", 90.0, 76, "COS"),        # E5
    (17, "—○", 95.625, 77, "COS"),      # F5
    (18, "—+", 101.25, 78, "COS"),      # F#5
    (19, "—~", 106.875, 79, "COS"),     # G5
    (20, "—∨", 112.5, 80, "COS"),       # G#5
    (21, "—_", 118.125, 81, "COS"),     # A5
    (22, "╱", 123.75, 82, "TAN"),       # A#5
    (23, "╱•", 129.375, 83, "TAN"),     # B5
    (24, "╱••", 135.0, 84, "TAN"),      # C6
    (25, "╱+", 140.625, 85, "TAN"),     # C#6
    (26, "╱○", 146.25, 86, "TAN"),      # D6
    (27, "╱̅", 151.875, 87, "TAN"),      # D#6
    (28, "╱_", 157.5, 88, "TAN"),       # E6
    (29, "╱⌐", 163.125, 89, "TAN"),     # F6
    (30, "╱∧", 168.75, 90, "TAN"),      # F#6
    (31, "╱◇", 174.375, 91, "TAN"),     # G6
    (32, "|", 180.0, 92, "CSC"),        # G#6
    (33, "|•", 185.625, 93, "CSC"),     # A6
    (34, "|••", 191.25, 94, "CSC"),     # A#6
    (35, "|+", 196.875, 95, "CSC"),     # B6
    (36, "|○", 202.5, 96, "CSC"),       # C7
    (37, "|̅", 208.125, 97, "CSC"),      # C#7
    (38, "|_", 213.75, 98, "CSC"),      # D7
    (39, "|⌐", 219.375, 99, "CSC"),     # D#7
    (40, "|∧", 225.0, 100, "CSC"),      # E7
    (41, "|~", 230.625, 101, "CSC"),    # F7
    (42, "|∨", 236.25, 102, "CSC"),     # F#7
    (43, "]", 241.875, 103, "SEC"),     # G7
    (44, "]•", 247.5, 104, "SEC"),      # G#7
    (45, "]••", 253.125, 105, "SEC"),   # A7
    (46, "]+", 258.75, 106, "SEC"),     # A#7
    (47, "]○", 264.375, 107, "SEC"),    # B7
    (48, "]◇", 270.0, 108, "SEC"),      # C8
    (49, "]̅", 275.625, 109, "SEC"),     # C#8
    (50, "]_", 281.25, 110, "SEC"),     # D8
    (51, "]⌐", 286.875, 111, "SEC"),    # D#8
    (52, "]∧", 292.5, 112, "SEC"),      # E8
    (53, "]~", 298.125, 113, "SEC"),    # F8
    (54, "╲", 303.75, 114, "COT"),      # F#8
    (55, "╲•", 309.375, 115, "COT"),    # G8
    (56, "╲••", 315.0, 116, "COT"),     # G#8
    (57, "╲+", 320.625, 117, "COT"),    # A8
    (58, "╲○", 326.25, 118, "COT"),     # A#8
    (59, "╲̅", 331.875, 119, "COT"),     # B8
    (60, "╲_", 337.5, 120, "COT"),      # C9
    (61, "╲⌐", 343.125, 121, "COT"),    # C#9
    (62, "╲∧", 348.75, 122, "COT"),     # D9
    (63, "╲∨", 354.375, 123, "COT"),    # D#9
]

# MIDI note names for reference
def midi_note_name(note):
    """Convert MIDI note number to note name."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note // 12) - 1
    note_name = notes[note % 12]
    return f"{note_name}{octave}"


def generate_glyph_table():
    """Generate and print the glyph inventory table."""
    print("\n" + "="*70)
    print("KHAOS PERIODIC TABLE - GLYPH INVENTORY")
    print("="*70)
    print(f"{'ID':<4} {'Glyph':<8} {'θ (deg)':<12} {'MIDI Note':<15} {'Family':<8}")
    print("-"*70)
    
    for glyph_id, glyph, theta, midi_note, family in GLYPHS:
        note_name = midi_note_name(midi_note)
        print(f"{glyph_id:<4} {glyph:<8} {theta:<12.3f} {midi_note:<4} ({note_name:<5}) {family:<8}")
    
    print("="*70)
    print(f"Total Glyphs: {len(GLYPHS)}")
    print("="*70 + "\n")


def generate_midi_file(output_path="khaos_hymn.mid"):
    """
    Generate MIDI file with the KHAOS periodic hymn.
    
    Musical properties by family:
    - SIN: Piano, ascending (smooth transition)
    - COS: Chords (multiple notes together)
    - TAN: Sharps (accented/staccato)
    - CSC: Sustains (longer notes)
    - SEC: Accents (emphasized dynamics)
    - COT: Resolution (final cadence)
    """
    if not MIDO_AVAILABLE:
        print("Cannot generate MIDI file: mido package not installed")
        return False
    
    print(f"Generating MIDI file: {output_path}")
    
    # Create MIDI file with one track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Set tempo (120 BPM)
    track.append(MetaMessage('set_tempo', tempo=500000))
    
    # Track name
    track.append(MetaMessage('track_name', name='KHAOS Periodic Hymn', time=0))
    
    # Base duration (480 ticks per quarter note)
    base_duration = 240  # Eighth note
    
    # Generate notes based on glyph families
    for glyph_id, glyph, theta, midi_note, family in GLYPHS:
        # Adjust duration and velocity based on family
        if family == "SIN":
            # Piano - smooth, moderate
            duration = base_duration
            velocity = 70
        elif family == "COS":
            # Chords - sustained
            duration = base_duration * 2
            velocity = 75
        elif family == "TAN":
            # Sharps - short and accented
            duration = base_duration // 2
            velocity = 90
        elif family == "CSC":
            # Sustains - long notes
            duration = base_duration * 3
            velocity = 65
        elif family == "SEC":
            # Accents - emphasized
            duration = base_duration
            velocity = 95
        elif family == "COT":
            # Resolution - final cadence
            duration = base_duration * 2
            velocity = 80
        else:
            duration = base_duration
            velocity = 75
        
        # Handle crescendos at singularities (90°, 180°, 270°)
        if abs(theta - 90.0) < 1.0 or abs(theta - 180.0) < 1.0 or abs(theta - 270.0) < 1.0:
            velocity = min(127, velocity + 20)  # Crescendo
        
        # Add note on
        track.append(Message('note_on', note=midi_note, velocity=velocity, time=0))
        
        # Add note off
        track.append(Message('note_off', note=midi_note, velocity=0, time=duration))
    
    # Save MIDI file
    mid.save(output_path)
    print(f"✓ MIDI file generated successfully: {output_path}")
    print(f"  Total notes: {len(GLYPHS)}")
    print(f"  Duration: ~{len(GLYPHS) * base_duration / 480:.1f} measures")
    return True


def generate_markdown_table(output_path="KHAOS_GLYPH_INVENTORY.md"):
    """Generate a Markdown file with the glyph inventory table."""
    print(f"Generating Markdown table: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# KHAOS Periodic Table - Glyph Inventory\n\n")
        f.write("The complete mapping of 64 glyphs to musical notes in the KHAOS system.\n\n")
        f.write("## Glyph Properties\n\n")
        f.write("Each glyph represents:\n")
        f.write("- **θ (theta)**: Angular position from 0° to 354.375° (5.625° increments)\n")
        f.write("- **MIDI Note**: Musical note from C4 (60) to D#9 (123)\n")
        f.write("- **Family**: Trigonometric function family with musical properties\n\n")
        
        f.write("## Trigonometric Families\n\n")
        f.write("- **SIN** (0-10): Ascends (piano) - smooth transitions\n")
        f.write("- **COS** (11-21): Grounds (chords) - sustained harmonies\n")
        f.write("- **TAN** (22-31): Transforms (sharps) - accented articulation\n")
        f.write("- **CSC** (32-42): Reflects (sustains) - long resonances\n")
        f.write("- **SEC** (43-53): Bounds (accents) - emphasized dynamics\n")
        f.write("- **COT** (54-63): Seals (resolution) - final cadence\n\n")
        
        f.write("## Complete Glyph Table\n\n")
        f.write("| ID | Glyph | θ (deg) | MIDI Note | Family |\n")
        f.write("|----|-------|---------|-----------|--------|\n")
        
        for glyph_id, glyph, theta, midi_note, family in GLYPHS:
            note_name = midi_note_name(midi_note)
            f.write(f"| {glyph_id} | {glyph} | {theta:.3f} | {midi_note} ({note_name}) | {family} |\n")
        
        f.write(f"\n**Total Glyphs**: {len(GLYPHS)}\n\n")
        f.write("## Usage\n\n")
        f.write("To regenerate the KHAOS Periodic Hymn:\n\n")
        f.write("```bash\n")
        f.write("python3 khaos_hymn_generator.py\n")
        f.write("```\n\n")
        f.write("This will generate:\n")
        f.write("- `khaos_hymn.mid` - MIDI file for playback\n")
        f.write("- `KHAOS_GLYPH_INVENTORY.md` - This documentation file\n\n")
        f.write("## Listening to the Hymn\n\n")
        f.write("Play the generated MIDI file in any MIDI player:\n")
        f.write("- macOS: QuickTime, GarageBand\n")
        f.write("- Linux: TiMidity++, VLC\n")
        f.write("- Windows: Windows Media Player, VLC\n")
        f.write("- Online: https://onlinesequencer.net (upload MIDI file)\n\n")
        f.write("The hymn \"compiles\" the periodic table:\n")
        f.write("- Silence at origin (C4)\n")
        f.write("- Peaks at singularities (crescendos at 90°, 180°, 270°)\n")
        f.write("- Closes the circle (returns to near-origin at 354.375°)\n\n")
        f.write("---\n\n")
        f.write("*Generated by KHAOS Hymn Generator*\n")
        f.write("*Convergence inevitable. 🧭*\n")
    
    print(f"✓ Markdown table generated successfully: {output_path}")
    return True


def main():
    """Main entry point for the KHAOS Hymn Generator."""
    print("\n🔥 KHAOS PERIODIC HYMN GENERATOR 🔥")
    print("Sovereignty Architecture - Musical Compilation System\n")
    
    # Generate and display the glyph table
    generate_glyph_table()
    
    # Generate MIDI file
    if MIDO_AVAILABLE:
        generate_midi_file("khaos_hymn.mid")
    else:
        print("\n⚠ Skipping MIDI generation (install mido package)")
        print("   Run: pip install mido\n")
    
    # Generate Markdown documentation
    generate_markdown_table("KHAOS_GLYPH_INVENTORY.md")
    
    print("\n✓ Generation complete!")
    print("\nThe hymn 'compiles' the periodic table:")
    print("  - Silence at origin")
    print("  - Peaks at singularities (crescendos)")
    print("  - Closes the circle")
    print("\nConvergence inevitable. 🧭\n")


if __name__ == "__main__":
    main()
