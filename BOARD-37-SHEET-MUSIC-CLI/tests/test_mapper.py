"""
test_mapper.py — Unit tests for BOARD-37 Sheet Music CLI.
"""
import sys
import os
import unittest

# Add src to path
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")
sys.path.insert(0, SRC)

from music_mapper import (
    rank_to_pitch, occurrence_to_duration, pct_to_velocity,
    pos_to_channel, map_word_to_note, map_rows_to_notes, MusicNote,
)
from abc_exporter import to_abc
from midi_exporter import notes_to_midi_bytes


class TestRankToPitch(unittest.TestCase):
    def test_rank1_is_C3(self):
        """Rank 1 should map to MIDI 48 (C3)."""
        self.assertEqual(rank_to_pitch(1, 20), 48)

    def test_rankN_is_C5(self):
        """Rank N (last) should map to MIDI 72 (C5)."""
        self.assertEqual(rank_to_pitch(20, 20), 72)

    def test_middle_rank_is_between(self):
        pitch = rank_to_pitch(10, 20)
        self.assertGreater(pitch, 48)
        self.assertLess(pitch, 72)

    def test_single_rank(self):
        """With only one rank, should return 48."""
        self.assertEqual(rank_to_pitch(1, 1), 48)

    def test_ascending_order(self):
        """Higher rank → higher pitch."""
        pitches = [rank_to_pitch(i, 10) for i in range(1, 11)]
        self.assertEqual(pitches, sorted(pitches))


class TestOccurrenceToDuration(unittest.TestCase):
    def test_high_occurrence_whole(self):
        self.assertEqual(occurrence_to_duration(100, 100), "whole")

    def test_low_occurrence_sixteenth(self):
        self.assertEqual(occurrence_to_duration(1, 100), "sixteenth")

    def test_medium_occurrence_quarter(self):
        dur = occurrence_to_duration(50, 100)
        self.assertIn(dur, ("quarter", "half"))

    def test_high_is_longer_than_low(self):
        durations = ["whole", "half", "quarter", "eighth", "sixteenth"]
        d_high = occurrence_to_duration(80, 100)
        d_low  = occurrence_to_duration(5, 100)
        self.assertLess(durations.index(d_high), durations.index(d_low))


class TestPctToVelocity(unittest.TestCase):
    def test_range_40_to_127(self):
        for pct in [0.0, 0.5, 1.0, 2.5, 5.0, 10.0]:
            v = pct_to_velocity(pct)
            self.assertGreaterEqual(v, 40)
            self.assertLessEqual(v, 127)

    def test_zero_pct_minimum_velocity(self):
        self.assertEqual(pct_to_velocity(0.0), 40)

    def test_high_pct_high_velocity(self):
        self.assertGreater(pct_to_velocity(5.0), pct_to_velocity(0.5))


class TestPosToChannel(unittest.TestCase):
    def test_noun_piano(self):
        self.assertEqual(pos_to_channel("Noun"), 0)

    def test_verb_strings(self):
        self.assertEqual(pos_to_channel("Verb"), 1)

    def test_adjective_brass(self):
        self.assertEqual(pos_to_channel("Adjective"), 2)

    def test_adverb_woodwind(self):
        self.assertEqual(pos_to_channel("Adverb"), 3)

    def test_conjunction_percussion(self):
        self.assertEqual(pos_to_channel("Conjunction"), 9)

    def test_preposition_percussion(self):
        self.assertEqual(pos_to_channel("Preposition"), 9)

    def test_other_synth(self):
        self.assertEqual(pos_to_channel("Other"), 4)
        self.assertEqual(pos_to_channel("Unknown"), 4)
        self.assertEqual(pos_to_channel("xyz"), 4)


class TestFullPipeline(unittest.TestCase):
    def _sample_rows(self):
        return [
            {"rank": 1,  "word": "registry", "lemma": "registry", "pos": "Noun",   "pct": 1.89, "occurrence": 72},
            {"rank": 2,  "word": "sagco",    "lemma": "sagco",    "pos": "Verb",   "pct": 1.74, "occurrence": 66},
            {"rank": 3,  "word": "compiler", "lemma": "compiler", "pos": "Noun",   "pct": 1.10, "occurrence": 38},
            {"rank": 4,  "word": "guard",    "lemma": "guard",    "pos": "Adjective","pct": 0.89,"occurrence": 34},
            {"rank": 5,  "word": "tokens",   "lemma": "token",    "pos": "Conjunction","pct": 0.05,"occurrence": 2},
        ]

    def test_csv_to_notes(self):
        rows = self._sample_rows()
        notes = map_rows_to_notes(rows)
        self.assertEqual(len(notes), 5)
        self.assertIsInstance(notes[0], MusicNote)

    def test_abc_contains_headers(self):
        rows = self._sample_rows()
        notes = map_rows_to_notes(rows)
        abc = to_abc(notes, title="Test Score")
        self.assertIn("X:1", abc)
        self.assertIn("T:Test Score", abc)
        self.assertIn("M:4/4", abc)
        self.assertIn("K:C", abc)
        self.assertIn("w:", abc)

    def test_abc_contains_lyrics(self):
        rows = self._sample_rows()
        notes = map_rows_to_notes(rows)
        abc = to_abc(notes)
        self.assertIn("registry", abc)
        self.assertIn("sagco", abc)

    def test_all_channels_assigned(self):
        rows = self._sample_rows()
        notes = map_rows_to_notes(rows)
        channels = {n.channel for n in notes}
        # At least Piano (0) and Strings (1) should appear
        self.assertIn(0, channels)
        self.assertIn(1, channels)


class TestMidiBytes(unittest.TestCase):
    def _make_notes(self):
        rows = [
            {"rank": 1, "word": "registry", "lemma": "registry", "pos": "Noun", "pct": 1.0, "occurrence": 10},
            {"rank": 2, "word": "sagco",    "lemma": "sagco",    "pos": "Verb", "pct": 0.8, "occurrence": 8},
        ]
        return map_rows_to_notes(rows)

    def test_midi_starts_with_MThd(self):
        notes = self._make_notes()
        data = notes_to_midi_bytes(notes)
        self.assertTrue(data.startswith(b'MThd'), "MIDI file must start with MThd magic bytes")

    def test_midi_contains_MTrk(self):
        notes = self._make_notes()
        data = notes_to_midi_bytes(notes)
        self.assertIn(b'MTrk', data)

    def test_midi_length_nonzero(self):
        notes = self._make_notes()
        data = notes_to_midi_bytes(notes)
        self.assertGreater(len(data), 14)  # At least header size


if __name__ == "__main__":
    unittest.main(verbosity=2)
