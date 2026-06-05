#!/usr/bin/env python3
"""
Test script for compose.py
Tests the TRIG6 COMPOSE functionality
"""

import sys
import os
from pathlib import Path
import tempfile

# Import compose module
import compose


def test_midi_writer():
    """Test basic MIDI writer functionality"""
    print("Testing MIDI writer...")
    
    midi = compose.MidiWriter(tempo_bpm=120, ticks_per_beat=480)
    
    # Add a simple note (C4 for 1 beat)
    midi.add_note(start_tick=0, duration_ticks=480, channel=0, note=60, velocity=80)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
        temp_path = f.name
    
    bytes_written = midi.write(temp_path)
    
    # Verify file exists and has content
    assert Path(temp_path).exists(), "MIDI file not created"
    assert bytes_written > 0, "MIDI file is empty"
    
    # Read file to verify it's valid MIDI
    with open(temp_path, 'rb') as f:
        header = f.read(4)
        assert header == b'MThd', f"Invalid MIDI header: {header}"
    
    # Cleanup
    os.unlink(temp_path)
    print("✓ MIDI writer test passed")


def test_khaos_glyphs():
    """Test KHAOS glyph registry"""
    print("Testing KHAOS glyph registry...")
    
    assert len(compose.KHAOS_GLYPHS) == 64, "Should have 64 glyphs"
    
    # Check family distribution
    families = {}
    for glyph in compose.KHAOS_GLYPHS:
        family = glyph['family']
        families[family] = families.get(family, 0) + 1
    
    assert len(families) == 6, f"Should have 6 families, got {len(families)}"
    print(f"✓ KHAOS glyph registry test passed (6 families, 64 glyphs)")


def test_periodic_table_compilation():
    """Test compiling the full periodic table"""
    print("Testing periodic table compilation...")
    
    composer = compose.KhaosComposer(tempo=120, base_note=60)
    events = composer.compile_periodic_table()
    
    assert len(events) == 64, f"Should generate 64 events, got {len(events)}"
    
    # Verify all events have required properties
    for event in events:
        assert hasattr(event, 'glyph_id'), "Event missing glyph_id"
        assert hasattr(event, 'midi_note'), "Event missing midi_note"
        assert hasattr(event, 'velocity'), "Event missing velocity"
        assert 0 <= event.velocity <= 127, f"Invalid velocity: {event.velocity}"
        assert 0 <= event.midi_note <= 127, f"Invalid MIDI note: {event.midi_note}"
    
    print("✓ Periodic table compilation test passed")


def test_midi_generation():
    """Test MIDI file generation from periodic table"""
    print("Testing MIDI file generation...")
    
    composer = compose.KhaosComposer(tempo=120, base_note=60)
    composer.compile_periodic_table()
    
    with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as f:
        temp_path = f.name
    
    result = composer.to_midi(temp_path)
    
    assert result['note_count'] == 64, f"Should have 64 notes, got {result['note_count']}"
    assert result['bytes_written'] > 0, "MIDI file should have content"
    assert Path(temp_path).exists(), "MIDI file not created"
    
    # Verify MIDI file structure
    with open(temp_path, 'rb') as f:
        data = f.read()
        assert data[:4] == b'MThd', "Invalid MIDI header"
        assert b'MTrk' in data, "Missing track chunk"
    
    # Cleanup
    os.unlink(temp_path)
    print("✓ MIDI file generation test passed")


def test_custom_points():
    """Test custom points compilation"""
    print("Testing custom points compilation...")
    
    composer = compose.KhaosComposer(tempo=120, base_note=60)
    
    # Test with some custom points
    points = [
        (0, 1.0, 0.5),    # theta, radius, diameter
        (45, 0.8, 0.3),
        (90, 0.6, 0.4),
        (180, 0.9, 0.6),
    ]
    
    events = composer.compile_custom_points(points)
    
    assert len(events) == 4, f"Should generate 4 events, got {len(events)}"
    
    # Verify all events are valid
    for event in events:
        assert 0 <= event.velocity <= 127, f"Invalid velocity: {event.velocity}"
        assert 0 <= event.midi_note <= 127, f"Invalid MIDI note: {event.midi_note}"
        assert event.duration_beats > 0, "Duration should be positive"
    
    print("✓ Custom points compilation test passed")


def test_json_export():
    """Test JSON audit trail export"""
    print("Testing JSON export...")
    
    composer = compose.KhaosComposer(tempo=90, base_note=48)
    composer.compile_periodic_table()
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_path = f.name
    
    count = composer.to_json(temp_path)
    
    assert count == 64, f"Should export 64 events, got {count}"
    assert Path(temp_path).exists(), "JSON file not created"
    
    # Verify JSON is valid
    import json
    with open(temp_path, 'r') as f:
        data = json.load(f)
        assert 'meta' in data, "JSON missing meta section"
        assert 'events' in data, "JSON missing events section"
        assert len(data['events']) == 64, "JSON should have 64 events"
    
    # Cleanup
    os.unlink(temp_path)
    print("✓ JSON export test passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("TRIG6 COMPOSE TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        test_midi_writer,
        test_khaos_glyphs,
        test_periodic_table_compilation,
        test_midi_generation,
        test_custom_points,
        test_json_export,
    ]
    
    failed = []
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed.append((test.__name__, e))
        print()
    
    print("=" * 60)
    if not failed:
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return 0
    else:
        print(f"FAILED: {len(failed)} test(s)")
        for name, error in failed:
            print(f"  - {name}: {error}")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
