#!/usr/bin/env python3
"""
Tests for the canonical 64-node cyclic graph implementation.
"""

import unittest
import math
from canonical_64_node_graph import (
    N, THETA_STEP, theta, unit, increment, G,
    f_dna, i_dna, f_glyph, i_glyph, f_trig6, i_trig6,
    f_midi, i_midi, f_geo, i_geo, f_curve, f_rubik, i_rubik,
    verify_all_commutativity, get_node_labels,
    CODONS, GLYPHS
)


class TestBasicStructure(unittest.TestCase):
    """Test basic graph structure and constants."""
    
    def test_constants(self):
        """Verify graph constants."""
        assert N == 64
        assert THETA_STEP == 5.625
    
    def test_theta_function(self):
        """Test theta angle calculation."""
        assert theta(0) == 0.0
        assert theta(8) == 45.0
        assert theta(16) == 90.0
        assert theta(32) == 180.0
        assert theta(63) == 354.375
    
    def test_increment_function(self):
        """Test increment operator."""
        assert increment(0) == 1
        assert increment(31) == 32
        assert increment(63) == 0  # Wrap around
    
    def test_graph_structure(self):
        """Test graph G has all 64 nodes."""
        assert len(G) == N
        assert all(n in G for n in range(N))
        assert all(G[n] == (n + 1) % N for n in range(N))


class TestDNADomain(unittest.TestCase):
    """Test DNA codon mapping."""
    
    def test_codon_count(self):
        """Verify we have exactly 64 codons."""
        assert len(CODONS) == 64
    
    def test_f_dna(self):
        """Test DNA labeling function."""
        assert f_dna(0) == "UUU"
        assert f_dna(63) == "GGG"
    
    def test_i_dna(self):
        """Test DNA increment function."""
        assert i_dna("UUU") == "UUC"
        assert i_dna("GGG") == "UUU"  # Wrap around
    
    def test_dna_commutativity(self):
        """Test DNA domain commutativity at sample nodes."""
        for n in [0, 16, 32, 48, 63]:
            assert f_dna(increment(n)) == i_dna(f_dna(n))


class TestKHAOSGlyphs(unittest.TestCase):
    """Test KHAOS glyph mapping."""
    
    def test_glyph_count(self):
        """Verify we have exactly 64 glyphs."""
        assert len(GLYPHS) == 64
    
    def test_f_glyph(self):
        """Test glyph labeling function."""
        assert f_glyph(0) == "KHAOS_C1"
        assert "KHAOS_" in f_glyph(0)
        assert "Dual_" in f_glyph(50)
    
    def test_i_glyph(self):
        """Test glyph increment function."""
        glyph_0 = f_glyph(0)
        glyph_1 = f_glyph(1)
        assert i_glyph(glyph_0) == glyph_1
    
    def test_glyph_commutativity(self):
        """Test glyph domain commutativity at sample nodes."""
        for n in [0, 16, 32, 48, 63]:
            assert f_glyph(increment(n)) == i_glyph(f_glyph(n))


class TestTRIG6(unittest.TestCase):
    """Test TRIG6 angle mapping."""
    
    def test_f_trig6(self):
        """Test TRIG6 labeling function."""
        assert f_trig6(0) == 0.0
        assert f_trig6(16) == 90.0
        assert f_trig6(32) == 180.0
    
    def test_i_trig6(self):
        """Test TRIG6 increment function."""
        assert i_trig6(0.0) == 5.625
        assert abs(i_trig6(354.375) - 0.0) < 1e-9  # Wrap around
    
    def test_trig6_commutativity(self):
        """Test TRIG6 domain commutativity at sample nodes."""
        for n in [0, 16, 32, 48, 63]:
            f_then_i = f_trig6(increment(n))
            i_then_f = i_trig6(f_trig6(n))
            assert abs(f_then_i - i_then_f) < 1e-9


class TestMIDI(unittest.TestCase):
    """Test MIDI note mapping."""
    
    def test_f_midi(self):
        """Test MIDI labeling function."""
        assert f_midi(0) == 60  # C4
        assert f_midi(1) == 61
        assert f_midi(63) == 123
    
    def test_i_midi(self):
        """Test MIDI increment function."""
        assert i_midi(60) == 61
        assert i_midi(123) == 60  # Wrap around
    
    def test_midi_commutativity(self):
        """Test MIDI domain commutativity at sample nodes."""
        for n in [0, 16, 32, 48, 63]:
            assert f_midi(increment(n)) == i_midi(f_midi(n))


class TestGeometry(unittest.TestCase):
    """Test geometric unit circle mapping."""
    
    def test_f_geo(self):
        """Test geometry labeling function."""
        # Test cardinal points
        x, y = f_geo(0)
        assert abs(x - 1.0) < 1e-5
        assert abs(y - 0.0) < 1e-5
        
        x, y = f_geo(16)
        assert abs(x - 0.0) < 1e-5
        assert abs(y - 1.0) < 1e-5
    
    def test_i_geo(self):
        """Test geometry increment function."""
        p0 = f_geo(0)
        p1 = f_geo(1)
        i_p0 = i_geo(p0)
        assert abs(i_p0[0] - p1[0]) < 1e-5
        assert abs(i_p0[1] - p1[1]) < 1e-5
    
    def test_geo_commutativity(self):
        """Test geometry domain commutativity at sample nodes."""
        for n in [0, 8, 16, 32, 48]:
            f_then_i = f_geo(increment(n))
            i_then_f = i_geo(f_geo(n))
            assert abs(f_then_i[0] - i_then_f[0]) < 1e-5
            assert abs(f_then_i[1] - i_then_f[1]) < 1e-5


class TestCurves(unittest.TestCase):
    """Test French curve mapping."""
    
    def test_f_curve(self):
        """Test curve labeling function."""
        curve = f_curve(0)
        assert "start" in curve
        assert "end" in curve
        assert "arc_degrees" in curve
        assert "arc_radians" in curve
        assert curve["arc_degrees"] == THETA_STEP


class TestRubik(unittest.TestCase):
    """Test Rubik-derived phase mapping."""
    
    def test_f_rubik(self):
        """Test Rubik labeling function."""
        phase = f_rubik(0)
        assert "Phase 0" in phase
        assert "0.000°" in phase
    
    def test_i_rubik(self):
        """Test Rubik increment function."""
        phase_0 = f_rubik(0)
        phase_1 = f_rubik(1)
        assert "Phase 1" in i_rubik(phase_0)


class TestCommutativity(unittest.TestCase):
    """Test overall commutativity verification."""
    
    def test_verify_all_commutativity(self):
        """Test that all domains pass commutativity verification."""
        results = verify_all_commutativity()
        
        # Check all domains are present
        assert "DNA" in results
        assert "Glyph" in results
        assert "TRIG6" in results
        assert "MIDI" in results
        assert "Geometry" in results
        
        # Check all domains pass
        for domain, data in results.items():
            assert data["passed"] == 64, f"{domain} should have 64 passed tests"
            assert data["failed"] == 0, f"{domain} should have 0 failed tests"
            assert len(data["failures"]) == 0, f"{domain} should have no failures"


class TestNodeLabels(unittest.TestCase):
    """Test comprehensive node label generation."""
    
    def test_get_node_labels(self):
        """Test get_node_labels returns all expected fields."""
        labels = get_node_labels(0)
        
        assert "node" in labels
        assert "theta_deg" in labels
        assert "DNA" in labels
        assert "Glyph" in labels
        assert "TRIG6" in labels
        assert "MIDI" in labels
        assert "Geometry" in labels
        assert "Curve" in labels
        assert "Rubik" in labels
        
        assert labels["node"] == 0
        assert labels["DNA"] == "UUU"
    
    def test_sample_nodes(self):
        """Test labels for sample nodes."""
        sample_nodes = [0, 8, 16, 32, 48, 63]
        for n in sample_nodes:
            labels = get_node_labels(n)
            assert labels["node"] == n
            assert labels["theta_deg"] == theta(n)


if __name__ == "__main__":
    unittest.main()
