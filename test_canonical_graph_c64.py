#!/usr/bin/env python3
"""
Test Suite for Canonical 64-Node Cyclic Graph (C_64)
====================================================

Validates:
1. Graph structure properties (cycle, 64 nodes)
2. Each labeling is a valid graph homomorphism
3. Commutativity across all mappings
4. Invariant preservation
"""

import pytest
import math
from canonical_graph_c64 import (
    CanonicalGraph64,
    DNALabeling,
    TRIG6Labeling,
    MIDILabeling,
    GeometryLabeling,
    CurveLabeling,
    GlyphLabeling,
    CommutativityChecker,
    CanonicalGraphSystem,
    generate_commutative_diagram
)


class TestCanonicalGraph64:
    """Test the core graph structure."""
    
    def test_graph_has_64_nodes(self):
        """Verify the graph has exactly 64 nodes."""
        graph = CanonicalGraph64()
        assert len(graph.nodes()) == 64
        assert graph.N == 64
    
    def test_graph_is_cycle(self):
        """Verify the graph is a cycle (each node has one successor)."""
        graph = CanonicalGraph64()
        
        # Each node should have exactly one successor
        for n in range(64):
            succ = graph.successor(n)
            assert 0 <= succ < 64
            assert succ == (n + 1) % 64
    
    def test_graph_cycle_property(self):
        """Verify that following successors returns to start after 64 steps."""
        graph = CanonicalGraph64()
        
        start = 0
        current = start
        for _ in range(64):
            current = graph.successor(current)
        
        assert current == start, "Following 64 successors should return to start"
    
    def test_theta_invariant(self):
        """Verify θ(n) = n × 5.625° for all nodes."""
        graph = CanonicalGraph64()
        
        for n in range(64):
            expected = n * 5.625
            actual = graph.theta(n)
            assert abs(actual - expected) < 1e-10
    
    def test_theta_covers_full_circle(self):
        """Verify θ maps [0, 63] to [0°, 354.375°] covering the circle."""
        graph = CanonicalGraph64()
        
        assert graph.theta(0) == 0.0
        assert abs(graph.theta(63) - 354.375) < 1e-10
        
        # Node 64 wraps back to 0
        assert abs(graph.theta(64 % 64) - 0.0) < 1e-10
    
    def test_graph_distance(self):
        """Test graph distance calculation."""
        graph = CanonicalGraph64()
        
        # Distance from 0 to adjacent nodes
        assert graph.distance(0, 1) == 1
        assert graph.distance(0, 2) == 2
        
        # Distance respects symmetry
        assert graph.distance(10, 20) == graph.distance(20, 10)
        
        # Maximum distance on a 64-cycle is 32
        assert graph.distance(0, 32) == 32
        
        # Wrapping: 0 to 63 is distance 1 (backward)
        assert graph.distance(0, 63) == 1


class TestDNALabeling:
    """Test DNA codon labeling."""
    
    def test_has_64_codons(self):
        """Verify there are exactly 64 codons."""
        dna = DNALabeling()
        assert len(dna.CODONS) == 64
    
    def test_all_codons_unique(self):
        """Verify all codons are unique."""
        dna = DNALabeling()
        assert len(set(dna.CODONS)) == 64
    
    def test_codon_format(self):
        """Verify codons are valid RNA triplets."""
        dna = DNALabeling()
        valid_bases = {'U', 'C', 'A', 'G'}
        
        for codon in dna.CODONS:
            assert len(codon) == 3
            assert all(base in valid_bases for base in codon)
    
    def test_labeling_covers_all_nodes(self):
        """Verify labeling maps all 64 nodes to codons."""
        dna = DNALabeling()
        
        codons = [dna.label(n) for n in range(64)]
        assert len(codons) == 64
        assert len(set(codons)) == 64  # All unique
    
    def test_inverse_mapping(self):
        """Verify inverse mapping from codons to nodes."""
        dna = DNALabeling()
        
        for n in range(64):
            codon = dna.label(n)
            assert dna.inverse(codon) == n


class TestTRIG6Labeling:
    """Test TRIG6 angle labeling."""
    
    def test_angle_range(self):
        """Verify angles cover [0°, 360°)."""
        trig6 = TRIG6Labeling()
        
        angles = [trig6.label(n) for n in range(64)]
        assert min(angles) == 0.0
        assert max(angles) < 360.0
    
    def test_angle_step(self):
        """Verify consecutive nodes differ by 5.625°."""
        trig6 = TRIG6Labeling()
        
        for n in range(63):
            diff = trig6.label(n + 1) - trig6.label(n)
            assert abs(diff - 5.625) < 1e-10
    
    def test_radians_conversion(self):
        """Verify radian conversion is correct."""
        trig6 = TRIG6Labeling()
        
        for n in range(64):
            deg = trig6.label(n)
            rad = trig6.label_radians(n)
            expected = math.radians(deg)
            assert abs(rad - expected) < 1e-10


class TestMIDILabeling:
    """Test MIDI note labeling."""
    
    def test_midi_range(self):
        """Verify MIDI notes are in range [60, 123]."""
        midi = MIDILabeling()
        
        notes = [midi.label(n) for n in range(64)]
        assert min(notes) == 60  # Middle C
        assert max(notes) == 123  # B8
    
    def test_midi_consecutive(self):
        """Verify consecutive nodes map to consecutive MIDI notes."""
        midi = MIDILabeling()
        
        for n in range(63):
            assert midi.label(n + 1) == midi.label(n) + 1
    
    def test_note_names(self):
        """Verify note name generation."""
        midi = MIDILabeling()
        
        # Middle C should be C4
        assert midi.note_name(0) == "C4"
        
        # Node 12 should be one octave up (C5)
        assert midi.note_name(12) == "C5"


class TestGeometryLabeling:
    """Test unit circle embedding."""
    
    def test_unit_circle_magnitude(self):
        """Verify all points lie on the unit circle."""
        geom = GeometryLabeling()
        
        for n in range(64):
            z = geom.label(n)
            magnitude = abs(z)
            assert abs(magnitude - 1.0) < 1e-10
    
    def test_cartesian_coordinates(self):
        """Verify Cartesian coordinate conversion."""
        geom = GeometryLabeling()
        
        # Node 0 should be at (1, 0)
        x, y = geom.cartesian(0)
        assert abs(x - 1.0) < 1e-10
        assert abs(y - 0.0) < 1e-10
        
        # Node 16 (90°) should be at (0, 1)
        x, y = geom.cartesian(16)
        assert abs(x - 0.0) < 1e-10
        assert abs(y - 1.0) < 1e-10
    
    def test_polar_coordinates(self):
        """Verify polar coordinate representation."""
        geom = GeometryLabeling()
        
        for n in range(64):
            r, theta = geom.polar(n)
            assert abs(r - 1.0) < 1e-10
            assert 0 <= theta < 2 * math.pi


class TestCurveLabeling:
    """Test French curve interpolation."""
    
    def test_interpolation_endpoints(self):
        """Verify interpolation endpoints match node positions."""
        geom = GeometryLabeling()
        curve = CurveLabeling(geom)
        
        n_start, n_end = 0, 10
        
        # t=0 should give start position
        start_z = curve.interpolate(0.0, n_start, n_end)
        expected_start = geom.label(n_start)
        assert abs(start_z - expected_start) < 1e-10
        
        # t=1 should give end position
        end_z = curve.interpolate(1.0, n_start, n_end)
        expected_end = geom.label(n_end)
        assert abs(end_z - expected_end) < 1e-10
    
    def test_path_generation(self):
        """Verify path generation creates smooth curves."""
        geom = GeometryLabeling()
        curve = CurveLabeling(geom)
        
        path = curve.path(0, 10, steps=100)
        
        # Should have 101 points (0 to 100 inclusive)
        assert len(path) == 101
        
        # All points should be on or near the unit circle
        for z in path:
            assert abs(abs(z) - 1.0) < 0.01  # Tolerance for interpolation


class TestGlyphLabeling:
    """Test KHAOS glyph labeling."""
    
    def test_glyph_format(self):
        """Verify glyph identifiers follow K00-K63 format."""
        glyph = GlyphLabeling()
        
        for n in range(64):
            label = glyph.label(n)
            assert label.startswith('K')
            assert len(label) == 3
            assert label[1:].isdigit()
    
    def test_unique_glyphs(self):
        """Verify all glyphs are unique."""
        glyph = GlyphLabeling()
        
        glyphs = [glyph.label(n) for n in range(64)]
        assert len(set(glyphs)) == 64


class TestCommutativity:
    """Test that all labelings are graph homomorphisms."""
    
    def test_dna_homomorphism(self):
        """Verify DNA labeling preserves graph structure."""
        graph = CanonicalGraph64()
        checker = CommutativityChecker(graph)
        
        # Check all nodes
        for n in range(64):
            test = checker.check_dna_commutativity(n)
            assert test.commutes, f"DNA commutativity failed at node {n}"
    
    def test_trig6_homomorphism(self):
        """Verify TRIG6 labeling preserves graph structure."""
        graph = CanonicalGraph64()
        checker = CommutativityChecker(graph)
        
        for n in range(64):
            test = checker.check_trig6_commutativity(n)
            assert test.commutes, f"TRIG6 commutativity failed at node {n}"
    
    def test_midi_homomorphism(self):
        """Verify MIDI labeling preserves graph structure."""
        graph = CanonicalGraph64()
        checker = CommutativityChecker(graph)
        
        for n in range(64):
            test = checker.check_midi_commutativity(n)
            assert test.commutes, f"MIDI commutativity failed at node {n}"
    
    def test_geometry_homomorphism(self):
        """Verify geometry labeling preserves graph structure."""
        graph = CanonicalGraph64()
        checker = CommutativityChecker(graph)
        
        for n in range(64):
            test = checker.check_geometry_commutativity(n)
            assert test.commutes, f"Geometry commutativity failed at node {n}"
    
    def test_glyph_homomorphism(self):
        """Verify glyph labeling preserves graph structure."""
        graph = CanonicalGraph64()
        checker = CommutativityChecker(graph)
        
        for n in range(64):
            test = checker.check_glyph_commutativity(n)
            assert test.commutes, f"Glyph commutativity failed at node {n}"
    
    def test_all_labelings_commute(self):
        """Verify all labelings commute simultaneously."""
        graph = CanonicalGraph64()
        checker = CommutativityChecker(graph)
        
        results = checker.verify_all_nodes()
        
        # All tests should pass
        for labeling, tests in results.items():
            failures = [t for t in tests if not t.commutes]
            assert len(failures) == 0, f"{labeling} has {len(failures)} failures"


class TestCanonicalGraphSystem:
    """Test the complete integrated system."""
    
    def test_system_initialization(self):
        """Verify system initializes all components."""
        system = CanonicalGraphSystem()
        
        assert system.graph is not None
        assert system.dna is not None
        assert system.trig6 is not None
        assert system.midi is not None
        assert system.geometry is not None
        assert system.curve is not None
        assert system.glyph is not None
        assert system.checker is not None
    
    def test_get_all_labels(self):
        """Verify get_all_labels returns complete labeling."""
        system = CanonicalGraphSystem()
        
        labels = system.get_all_labels(0)
        
        # Check all required fields are present
        assert 'node' in labels
        assert 'dna' in labels
        assert 'angle_deg' in labels
        assert 'angle_rad' in labels
        assert 'midi' in labels
        assert 'midi_note' in labels
        assert 'geometry_complex' in labels
        assert 'geometry_xy' in labels
        assert 'geometry_polar' in labels
        assert 'glyph' in labels
    
    def test_verify_commutativity(self):
        """Verify system-wide commutativity check."""
        system = CanonicalGraphSystem()
        
        summary = system.verify_commutativity()
        
        # Should test all nodes × all labelings
        assert summary['total_tests'] == 320  # 64 nodes × 5 labelings
        assert summary['passed'] == 320
        assert summary['failed'] == 0
        assert summary['overall_pass_rate'] == 1.0
        
        # Each labeling should pass all tests
        for labeling, details in summary['details'].items():
            assert details['passed'] == 64
            assert details['failed'] == 0
            assert details['pass_rate'] == 1.0
    
    def test_export_graph_data(self):
        """Verify graph data export."""
        system = CanonicalGraphSystem()
        
        data = system.export_graph_data()
        
        assert data['graph_type'] == "C_64 (64-node cycle graph)"
        assert data['node_count'] == 64
        assert data['edge_count'] == 64
        assert len(data['nodes']) == 64
        assert 'commutative_diagram' in data
        assert 'novelty_statement' in data


class TestCommutativeDiagram:
    """Test commutative diagram generation."""
    
    def test_diagram_generation(self):
        """Verify diagram can be generated."""
        diagram = generate_commutative_diagram()
        
        assert isinstance(diagram, str)
        assert len(diagram) > 0
        assert "C_64" in diagram
        assert "commute" in diagram.lower()
    
    def test_diagram_contains_labelings(self):
        """Verify diagram mentions all labelings."""
        diagram = generate_commutative_diagram()
        
        # Should mention key labelings
        assert "DNA" in diagram
        assert "TRIG6" in diagram or "angle" in diagram
        assert "MIDI" in diagram


class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_full_cycle_traversal(self):
        """Test traversing the full graph cycle with all labelings."""
        system = CanonicalGraphSystem()
        
        visited = set()
        current = 0
        
        for step in range(64):
            visited.add(current)
            
            # Get all labels for current node
            labels = system.get_all_labels(current)
            assert labels['node'] == current
            
            # Move to next node
            current = system.graph.successor(current)
        
        # Should have visited all 64 nodes exactly once
        assert len(visited) == 64
        assert current == 0  # Back to start
    
    def test_labeling_consistency(self):
        """Test that all labelings are consistent across operations."""
        system = CanonicalGraphSystem()
        
        for n in range(64):
            labels = system.get_all_labels(n)
            
            # DNA codon should match direct labeling
            assert labels['dna'] == system.dna.label(n)
            
            # Angle should match
            assert labels['angle_deg'] == system.trig6.label(n)
            
            # MIDI should match
            assert labels['midi'] == system.midi.label(n)
            
            # Geometry should match
            assert labels['geometry_complex'] == system.geometry.label(n)
            
            # Glyph should match
            assert labels['glyph'] == system.glyph.label(n)


# ============================================================================
# Pytest Configuration
# ============================================================================

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
