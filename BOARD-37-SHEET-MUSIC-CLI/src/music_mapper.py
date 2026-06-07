"""
music_mapper.py — Core mapping engine for SAGCO Sheet Music CLI.
Converts word frequency data into MusicNote objects following sovereign mapping laws.
"""
from dataclasses import dataclass


# ── Sovereign instrument map ──────────────────────────────────────────────────
INSTRUMENT_MAP = {
    "noun":        ("Piano",     0),
    "verb":        ("Strings",   1),
    "adjective":   ("Brass",     2),
    "adverb":      ("Woodwind",  3),
    "conjunction": ("Percussion", 9),
    "preposition": ("Percussion", 9),
}

DURATION_TICKS = {
    "whole":      1920,
    "half":        960,
    "quarter":     480,
    "eighth":      240,
    "sixteenth":   120,
}

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


@dataclass
class MusicNote:
    word: str
    rank: int
    occurrence: int
    pct: float
    pos: str
    pitch: int       # MIDI 0-127
    duration: str    # "whole","half","quarter","eighth","sixteenth"
    velocity: int    # MIDI 0-127
    channel: int     # instrument channel
    lyric: str       # the word itself

    @property
    def instrument(self) -> str:
        pos_key = self.pos.lower()
        if pos_key in INSTRUMENT_MAP:
            return INSTRUMENT_MAP[pos_key][0]
        return "Synth"

    @property
    def note_name(self) -> str:
        """Return human-readable note name e.g. 'E4'."""
        octave = (self.pitch // 12) - 1
        name = NOTE_NAMES[self.pitch % 12]
        return f"{name}{octave}"

    @property
    def ticks(self) -> int:
        return DURATION_TICKS.get(self.duration, 480)


def rank_to_pitch(rank: int, total_ranks: int) -> int:
    """Map rank linearly across 2 octaves: C3-C5 (MIDI 48-72).
    Rank 1 → lowest pitch (48), rank N → highest pitch (72).
    """
    if total_ranks <= 1:
        return 48
    # Linear interpolation: rank 1 → 48, rank total_ranks → 72
    pitch = 48 + int((rank - 1) / (total_ranks - 1) * 24)
    return max(48, min(72, pitch))


def occurrence_to_duration(occ: int, max_occ: int) -> str:
    """High occurrence → longer note. Maps to whole/half/quarter/eighth/sixteenth."""
    if max_occ <= 0:
        return "quarter"
    ratio = occ / max_occ
    if ratio >= 0.80:
        return "whole"
    elif ratio >= 0.60:
        return "half"
    elif ratio >= 0.35:
        return "quarter"
    elif ratio >= 0.15:
        return "eighth"
    else:
        return "sixteenth"


def pct_to_velocity(pct: float) -> int:
    """Map pct% to MIDI velocity in range 40-127.
    pct is expected as a decimal (e.g. 0.63 for 0.63%).
    We treat 0-5% as the realistic max range for any single word.
    """
    # Clamp to 0-5 range, then scale to 40-127
    clamped = max(0.0, min(5.0, pct))
    velocity = int(40 + (clamped / 5.0) * 87)
    return max(40, min(127, velocity))


def pos_to_channel(pos_tag: str) -> int:
    """Map POS tag string to MIDI channel."""
    key = pos_tag.lower().strip()
    if key in INSTRUMENT_MAP:
        return INSTRUMENT_MAP[key][1]
    # Partial matches
    for k, (_, ch) in INSTRUMENT_MAP.items():
        if key.startswith(k):
            return ch
    return 4  # Synth


def map_word_to_note(rank: int, word: str, occurrence: int, pct: float,
                     pos: str, total_ranks: int = 100, max_occ: int = 100) -> MusicNote:
    """Full mapping: word frequency row → MusicNote."""
    pitch = rank_to_pitch(rank, total_ranks)
    duration = occurrence_to_duration(occurrence, max_occ)
    velocity = pct_to_velocity(pct)
    channel = pos_to_channel(pos)

    return MusicNote(
        word=word,
        rank=rank,
        occurrence=occurrence,
        pct=pct,
        pos=pos,
        pitch=pitch,
        duration=duration,
        velocity=velocity,
        channel=channel,
        lyric=word,
    )


def map_rows_to_notes(rows: list) -> list:
    """Convert list of row dicts (from xlsx_parser) into MusicNote objects."""
    if not rows:
        return []
    total_ranks = len(rows)
    max_occ = max((r.get("occurrence", 0) for r in rows), default=1)
    notes = []
    for row in rows:
        note = map_word_to_note(
            rank=row.get("rank", 1),
            word=row.get("word", "?"),
            occurrence=row.get("occurrence", 1),
            pct=row.get("pct", 0.0),
            pos=row.get("pos", "other"),
            total_ranks=total_ranks,
            max_occ=max_occ,
        )
        notes.append(note)
    return notes
