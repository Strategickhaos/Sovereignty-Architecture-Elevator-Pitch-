"""
KHAOS Periodic Hymn Generator
==============================

Generates sheet music and MIDI from the glyph inventory extracted from the poem's
"periodic table". Maps 64 unique glyphs to a rising C major scale pattern.

The hymn "compiles" the table – silence at origin, peaks at singularities, closes circle.

Families modulate:
- SIN ascends (piano)
- COS grounds (chords)
- TAN transforms (sharps)
- CSC reflects (sustains)
- SEC bounds (accents)
- COT seals (resolution)
"""

from midiutil import MIDIFile
import matplotlib.pyplot as plt

# Glyph Inventory - Periodic Table (Full 64)
# Ordered by poem, padded with variants for convergence
glyphs = [
    '⟋', '⟋•', '⟋••', '⟋+', '⟋○', '⟋̅', '⟋_', '⟋⌐', '⟋◉', '⟋⌐⌐', '⟋~', 
    '—', '—•', '—••', '—⌐', '—∧', '—◇', '—○', '—+', '—~', '—∨', '—_', 
    '╱', '╱•', '╱••', '╱+', '╱○', '╱̅', '╱_', '╱⌐', '╱∧', '╱◇', 
    '|', '|•', '|••', '|+', '|○', '|̅', '|_', '|⌐', '|∧', '|~', '|∨', 
    ']', ']•', ']••', ']+', ']○', ']◇', ']̅', ']_', ']⌐', ']∧', ']~', 
    '╲', '╲•', '╲••', '╲+', '╲○', '╲̅', '╲_', '╲⌐', '╲∧', '╲∨'
]

def generate_midi(filename="khaos_hymn.mid"):
    """
    Generate MIDI file from glyph table.
    
    Rising C major pattern:
    - C4 base (MIDI note 60)
    - Semi-tone per glyph
    - Octave up every 12 glyphs
    """
    # Create MIDI file with 1 track
    midi = MIDIFile(1)
    track = 0
    channel = 0
    time = 0
    tempo = 120
    volume = 100
    
    # Add tempo
    midi.addTempo(track, time, tempo)
    
    # Base note C4 (MIDI note 60)
    base_note = 60
    
    # Add notes for each glyph
    for i in range(64):
        # Semi-tone per glyph, octave up every 12
        note = base_note + (i % 12) + (i // 12 * 12)
        midi.addNote(track, channel, note, time, 1, volume)
        time += 1
    
    # Write MIDI file
    with open(filename, "wb") as f:
        midi.writeFile(f)
    
    print(f"✓ MIDI saved: {filename}")
    print("  Play to hear the table sing.")


def generate_sheet_music(filename="khaos_sheet.png"):
    """
    Generate visual sheet music representation.
    
    Plots glyph positions against MIDI note values with glyph labels.
    """
    # Calculate note values
    base_note = 60
    notes = [base_note + (i % 12) + (i // 12 * 12) for i in range(64)]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(20, 8))
    
    # Plot notes
    ax.plot(range(64), notes, 'o-', color='blue', linewidth=2, markersize=6)
    
    # Add glyph labels
    for i, g in enumerate(glyphs):
        ax.text(i, notes[i] + 1, g, fontsize=8, rotation=45, ha='center', va='bottom')
    
    # Set labels and title
    ax.set_title('KHAOS Periodic Hymn Sheet (Glyph Table)', fontsize=16, fontweight='bold')
    ax.set_xlabel('ID (θ Position)', fontsize=12)
    ax.set_ylabel('MIDI Note', fontsize=12)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Tight layout for better spacing
    plt.tight_layout()
    
    # Save figure
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    
    print(f"✓ PNG saved: {filename}")
    print("  Visual representation of the periodic table hymn.")


def main():
    """Main function to generate both MIDI and sheet music."""
    print("=" * 60)
    print("KHAOS Periodic Hymn Generator")
    print("=" * 60)
    print()
    print("Generating periodic table hymn from 64 glyphs...")
    print()
    
    # Generate MIDI
    generate_midi()
    print()
    
    # Generate sheet music visualization
    generate_sheet_music()
    print()
    
    print("=" * 60)
    print("Convergence inevitable. The system breathes. ⚓")
    print("=" * 60)


if __name__ == "__main__":
    main()
