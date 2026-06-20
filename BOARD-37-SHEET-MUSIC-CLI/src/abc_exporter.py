"""
abc_exporter.py — Exports ABC notation from MusicNote objects.

ABC notation format:
  X:1
  T:SAGCO Word Frequency Score
  M:4/4
  L:1/8
  K:C
  ... note sequence ...
  w: word1 word2 word3...
"""
import os

# Map MIDI pitch → ABC note name (in key of C)
def _pitch_to_abc(pitch: int) -> str:
    """Convert MIDI pitch to ABC notation note string."""
    NOTE_ABC = ["C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B"]
    octave = (pitch // 12) - 1  # MIDI octave (C4=60 → octave 4)
    name = NOTE_ABC[pitch % 12]

    # ABC notation: octave 4 = no modifier, 5 = lowercase, 3 = C,
    # lower octaves use commas, higher use apostrophes
    base_octave = 4
    diff = octave - base_octave
    if diff == 0:
        return name
    elif diff > 0:
        # Higher octaves: lowercase + apostrophes for each octave above 5
        if diff == 1:
            return name.lower()
        else:
            return name.lower() + "'" * (diff - 1)
    else:
        # Lower octaves: commas
        return name + "," * abs(diff)


def _duration_to_abc_len(duration: str) -> str:
    """Convert duration name to ABC length multiplier (base L:1/8).
    L:1/8 means 1 = eighth note.
      whole    = 16
      half     = 8
      quarter  = 4
      eighth   = 2  (wait — at L:1/8 base: eighth=1, but let's use L:1/4 base)
    Using L:1/4 base:
      whole    = 4
      half     = 2
      quarter  = 1 (no suffix)
      eighth   = /2
      sixteenth= /4
    """
    mapping = {
        "whole":      "4",
        "half":       "2",
        "quarter":    "",
        "eighth":     "/2",
        "sixteenth":  "/4",
    }
    return mapping.get(duration, "")


def to_abc(notes, title: str = "SAGCO Score") -> str:
    """Convert list of MusicNote to ABC notation string."""
    lines = [
        "X:1",
        f"T:{title}",
        "C:SAGCO Sovereign Architecture",
        "M:4/4",
        "L:1/4",
        "Q:1/4=120",
        "K:C",
    ]

    # Build note sequence, grouping into measures of 4 beats
    note_strs = []
    beat_counts = {
        "whole": 4, "half": 2, "quarter": 1, "eighth": 0.5, "sixteenth": 0.25
    }

    measure_notes = []
    measure_beats = 0.0
    measures = []

    for note in notes:
        abc_note = _pitch_to_abc(note.pitch) + _duration_to_abc_len(note.duration)
        beats = beat_counts.get(note.duration, 1.0)

        measure_notes.append(abc_note)
        measure_beats += beats

        if measure_beats >= 4.0:
            measures.append(" ".join(measure_notes) + " |")
            measure_notes = []
            measure_beats = 0.0

    if measure_notes:
        measures.append(" ".join(measure_notes) + " |]")

    # Split into lines of ~4 measures each
    for i in range(0, len(measures), 4):
        lines.append(" ".join(measures[i:i+4]))

    # Lyrics line
    lyrics = " ".join(n.lyric for n in notes)
    lines.append(f"w: {lyrics}")

    return "\n".join(lines) + "\n"


def save_abc(notes, path: str, title: str = "SAGCO Score"):
    """Save ABC notation to file."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    content = to_abc(notes, title=title)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
