"""
midi_exporter.py — Exports MIDI files using only Python stdlib (no external libs).

Writes valid MIDI file bytes manually:
  - Header chunk: MThd
  - Track chunk: MTrk
  - Note on/off events with delta times
  - Multiple tracks (one per channel/instrument)
  - Tempo: 120 BPM default

MIDI note durations at 120 BPM, 480 ticks/beat:
  whole=1920, half=960, quarter=480, eighth=240, sixteenth=120
"""
import os
import struct
from collections import defaultdict

TICKS_PER_BEAT = 480

DURATION_TICKS = {
    "whole":     1920,
    "half":       960,
    "quarter":    480,
    "eighth":     240,
    "sixteenth":  120,
}


# ── Variable-length encoding (MIDI standard) ──────────────────────────────────

def _encode_varlen(value: int) -> bytes:
    """Encode an integer as a MIDI variable-length quantity."""
    result = []
    result.append(value & 0x7F)
    value >>= 7
    while value > 0:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.reverse()
    return bytes(result)


# ── MIDI event builders ───────────────────────────────────────────────────────

def _tempo_event(bpm: int) -> bytes:
    """Build a MIDI Set Tempo meta-event."""
    us_per_beat = 60_000_000 // bpm
    return (
        _encode_varlen(0) +           # delta time = 0
        b'\xff\x51\x03' +             # meta: set tempo, length 3
        struct.pack(">I", us_per_beat)[1:]  # 3 bytes (big-endian, drop leading byte)
    )


def _time_signature_event() -> bytes:
    """Build a 4/4 time signature meta-event."""
    return (
        _encode_varlen(0) +
        b'\xff\x58\x04'  # meta: time signature, length 4
        b'\x04\x02\x18\x08'  # 4/4, 24 MIDI clocks/click, 8 32nd notes/beat
    )


def _note_on(channel: int, pitch: int, velocity: int, delta: int = 0) -> bytes:
    channel = channel & 0x0F
    return (
        _encode_varlen(delta) +
        bytes([0x90 | channel, pitch & 0x7F, velocity & 0x7F])
    )


def _note_off(channel: int, pitch: int, delta: int) -> bytes:
    channel = channel & 0x0F
    return (
        _encode_varlen(delta) +
        bytes([0x80 | channel, pitch & 0x7F, 0x00])
    )


def _end_of_track() -> bytes:
    return _encode_varlen(0) + b'\xff\x2f\x00'


def _program_change(channel: int, program: int) -> bytes:
    """Set instrument program on a channel."""
    channel = channel & 0x0F
    return (
        _encode_varlen(0) +
        bytes([0xC0 | channel, program & 0x7F])
    )


# General MIDI program numbers per channel role
CHANNEL_PROGRAMS = {
    0: 0,    # Piano (Acoustic Grand Piano)
    1: 48,   # Strings (String Ensemble 1)
    2: 61,   # Brass (Brass Section)
    3: 73,   # Woodwind (Flute)
    4: 80,   # Synth (Lead 1 - square)
    9: 0,    # Percussion (channel 9 is always drums in GM)
}


def _build_track(notes_on_channel: list, channel: int, bpm: int) -> bytes:
    """Build a single MTrk chunk for one channel's notes."""
    events = bytearray()

    # Set tempo and time signature on track 0 (channel 0)
    if channel == 0:
        events += _tempo_event(bpm)
        events += _time_signature_event()

    # Program change
    prog = CHANNEL_PROGRAMS.get(channel, 0)
    if channel != 9:
        events += _program_change(channel, prog)

    # Emit notes sequentially (no polyphony; each note follows the previous)
    for note in notes_on_channel:
        ticks = DURATION_TICKS.get(note.duration, 480)
        pitch = max(0, min(127, note.pitch))
        vel = max(0, min(127, note.velocity))
        # Note on at delta=0 (immediately after previous note off)
        events += _note_on(channel, pitch, vel, delta=0)
        # Note off after duration ticks
        events += _note_off(channel, pitch, delta=ticks)

    events += _end_of_track()

    # Wrap in MTrk chunk
    chunk = b'MTrk' + struct.pack(">I", len(events)) + bytes(events)
    return chunk


def notes_to_midi_bytes(notes: list, bpm: int = 120) -> bytes:
    """Convert list of MusicNote objects to raw MIDI file bytes."""
    # Group notes by channel
    channels = defaultdict(list)
    for note in notes:
        channels[note.channel].append(note)

    # Sort channels so channel 0 (which carries tempo) comes first
    sorted_channels = sorted(channels.keys())
    num_tracks = len(sorted_channels)

    # MIDI header chunk
    # Format 1: multiple simultaneous tracks
    header = (
        b'MThd' +
        struct.pack(">I", 6) +           # chunk length always 6
        struct.pack(">H", 1) +           # format 1 (multiple tracks)
        struct.pack(">H", num_tracks) +  # number of tracks
        struct.pack(">H", TICKS_PER_BEAT)
    )

    tracks = bytearray()
    for ch in sorted_channels:
        tracks += _build_track(channels[ch], ch, bpm)

    return header + bytes(tracks)


def save_midi(notes: list, path: str, bpm: int = 120):
    """Save MIDI file to disk."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    data = notes_to_midi_bytes(notes, bpm=bpm)
    with open(path, "wb") as f:
        f.write(data)
    return path
