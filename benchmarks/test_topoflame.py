#!/usr/bin/env python3
"""
TopoFlame INV-097 Tests
FlameLang Compiler - Möbius & Klein Topology Integration
Strategickhaos DAO LLC
"""

import pytest
import sys
import os
import json
import numpy as np
from pathlib import Path

# Add parent directory to path to import flamelang_compiler
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flamelang_compiler import (
    FlameLangCompiler,
    MobiusStripAlgorithm,
    KleinBottleAlgorithm,
    WavePacket,
    HEBREW_TOPOLOGY_ROOTS,
    DNA_NUCLEOTIDES
)


class TestMobiusStripAlgorithm:
    """Test Möbius strip topology algorithms"""
    
    def test_parametric_point_at_origin(self):
        """Test Möbius parametric point calculation at u=0, v=0"""
        x, y, z = MobiusStripAlgorithm.parametric_point(0, 0)
        
        # At u=0, v=0, the point should be at (radius, 0, 0)
        assert abs(x - 1.0) < 0.01, f"Expected x≈1.0, got {x}"
        assert abs(y) < 0.01, f"Expected y≈0, got {y}"
        assert abs(z) < 0.01, f"Expected z≈0, got {z}"
    
    def test_parametric_point_full_rotation(self):
        """Test Möbius parametric point at full rotation"""
        x1, y1, z1 = MobiusStripAlgorithm.parametric_point(0, 0.5)
        x2, y2, z2 = MobiusStripAlgorithm.parametric_point(2 * np.pi, 0.5)
        
        # After full rotation (2π), the Möbius strip exhibits its characteristic twist
        # The z-coordinate flips sign, demonstrating the non-orientable property
        assert abs(z1 + z2) < 0.1, "Möbius twist: z-coordinate should flip after full rotation"
    
    def test_compute_loop_cycle(self):
        """Test Möbius loop cycle transformation"""
        test_data = b"HELLO"
        iterations = 3
        
        states = MobiusStripAlgorithm.compute_loop_cycle(test_data, iterations)
        
        assert len(states) == iterations, f"Expected {iterations} states"
        
        for i, state in enumerate(states):
            assert state['iteration'] == i
            assert state['hebrew_root'] == 'SLH'
            assert state['topology'] == 'mobius'
            assert len(state['transformed_data']) == len(test_data)
            assert 0 <= state['u_parameter'] <= 2 * np.pi
    
    def test_wave_simulation(self):
        """Test wave simulation on Möbius strip"""
        frequency = 1.0
        time_steps = 100
        
        wave = MobiusStripAlgorithm.wave_simulation(frequency, time_steps)
        
        assert len(wave) == time_steps
        assert isinstance(wave, np.ndarray)
        
        # Wave should oscillate between -1 and 1 (approximately)
        assert wave.min() >= -1.5
        assert wave.max() <= 1.5


class TestKleinBottleAlgorithm:
    """Test Klein bottle topology algorithms"""
    
    def test_parametric_point_at_origin(self):
        """Test Klein bottle parametric point calculation"""
        x, y, z = KleinBottleAlgorithm.parametric_point(0, 0)
        
        # Should produce valid 3D coordinates
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(z, float)
    
    def test_parametric_point_symmetry(self):
        """Test Klein bottle symmetry properties"""
        # Test at phi=0 and phi=π
        x1, y1, z1 = KleinBottleAlgorithm.parametric_point(0, np.pi/2)
        x2, y2, z2 = KleinBottleAlgorithm.parametric_point(np.pi, np.pi/2)
        
        # Klein bottle should have certain symmetry properties
        assert abs(x1 + x2) < 0.1, "Klein bottle phi symmetry"
    
    def test_boundary_less_transform(self):
        """Test Klein bottle boundary-less transformation"""
        test_data = b"WORLD"
        
        result = KleinBottleAlgorithm.boundary_less_transform(test_data)
        
        assert 'transformed_data' in result
        assert 'enclosed_flow' in result
        assert 'hebrew_root' in result
        assert 'topology' in result
        assert 'boundary_property' in result
        
        assert result['hebrew_root'] == 'QLB'
        assert result['topology'] == 'klein'
        assert result['boundary_property'] == 'none'
        
        assert len(result['transformed_data']) == len(test_data)
        assert len(result['enclosed_flow']) == len(test_data)
        
        # Enclosed flow should be non-negative
        for flow in result['enclosed_flow']:
            assert flow >= 0
    
    def test_quantum_entanglement_sim(self):
        """Test quantum entanglement simulation"""
        state_a = WavePacket(
            amplitude=1.0,
            phase=0.0,
            frequency=1.0,
            klein_parameter=0.5
        )
        state_b = WavePacket(
            amplitude=1.0,
            phase=np.pi/2,
            frequency=1.0,
            klein_parameter=0.5
        )
        
        result = KleinBottleAlgorithm.quantum_entanglement_sim(state_a, state_b)
        
        assert 'correlation' in result
        assert 'entanglement_measure' in result
        assert 'phase_difference' in result
        assert 'topology' in result
        
        assert result['topology'] == 'klein_quantum'
        assert -1 <= result['correlation'] <= 1
        assert result['phase_difference'] >= 0


class TestHebrewTopologyRoots:
    """Test Hebrew topology root mappings"""
    
    def test_slh_root_properties(self):
        """Test SLH (Möbius) root properties"""
        slh = HEBREW_TOPOLOGY_ROOTS['SLH']
        
        assert slh['meaning'] == 'send/loop'
        assert slh['topology'] == 'mobius'
        assert slh['function'] == 'infinite_cycle'
        assert slh['gematria'] > 0
    
    def test_qlb_root_properties(self):
        """Test QLB (Klein) root properties"""
        qlb = HEBREW_TOPOLOGY_ROOTS['QLB']
        
        assert qlb['meaning'] == 'contain/bottle'
        assert qlb['topology'] == 'klein'
        assert qlb['function'] == 'boundary_less'
        assert qlb['gematria'] > 0


class TestFlameLangCompiler:
    """Test full FlameLang compilation pipeline"""
    
    @pytest.fixture
    def compiler(self):
        """Create a FlameLang compiler instance"""
        return FlameLangCompiler()
    
    def test_english_to_hebrew_mobius_keywords(self, compiler):
        """Test English to Hebrew conversion with Möbius keywords"""
        text = "loop cycle send"
        roots = compiler.english_to_hebrew(text)
        
        assert len(roots) > 0
        assert all(root == 'SLH' for root in roots)
    
    def test_english_to_hebrew_klein_keywords(self, compiler):
        """Test English to Hebrew conversion with Klein keywords"""
        text = "contain bottle enclose"
        roots = compiler.english_to_hebrew(text)
        
        assert len(roots) > 0
        assert all(root == 'QLB' for root in roots)
    
    def test_english_to_hebrew_mixed_keywords(self, compiler):
        """Test English to Hebrew conversion with mixed keywords"""
        text = "loop in bottle"
        roots = compiler.english_to_hebrew(text)
        
        assert len(roots) > 0
        assert 'SLH' in roots
        assert 'QLB' in roots
    
    def test_english_to_hebrew_default(self, compiler):
        """Test English to Hebrew conversion with no keywords"""
        text = "random words here"
        roots = compiler.english_to_hebrew(text)
        
        # Should default to balanced topology
        assert len(roots) == 2
        assert 'SLH' in roots
        assert 'QLB' in roots
    
    def test_hebrew_to_unicode(self, compiler):
        """Test Hebrew to Unicode conversion"""
        roots = ['SLH', 'QLB']
        unicode_points = compiler.hebrew_to_unicode(roots)
        
        assert len(unicode_points) > 0
        
        # Should contain gematria values
        assert 125 in unicode_points  # SLH gematria
        assert 132 in unicode_points  # QLB gematria
    
    def test_unicode_to_wave(self, compiler):
        """Test Unicode to Wave layer transformation"""
        unicode_points = [125, 83, 76, 72]
        wave_data = compiler.unicode_to_wave(unicode_points)
        
        assert 'mobius_transformations' in wave_data
        assert 'klein_transformation' in wave_data
        assert 'wave_simulation' in wave_data
        assert 'quantum_entanglement' in wave_data
        assert 'topology_type' in wave_data
        
        assert wave_data['topology_type'] == 'TopoFlame_INV-097'
        assert len(wave_data['mobius_transformations']) > 0
    
    def test_wave_to_dna(self, compiler):
        """Test Wave to DNA conversion"""
        unicode_points = [125, 83, 76, 72]
        wave_data = compiler.unicode_to_wave(unicode_points)
        dna_sequence = compiler.wave_to_dna(wave_data)
        
        assert len(dna_sequence) > 0
        
        # All characters should be valid DNA nucleotides
        for nucleotide in dna_sequence:
            assert nucleotide in DNA_NUCLEOTIDES
        
        # Identity cycle: should contain all A G C O
        for nucleotide in DNA_NUCLEOTIDES:
            assert nucleotide in dna_sequence, f"Missing nucleotide: {nucleotide}"
    
    def test_dna_to_llvm(self, compiler):
        """Test DNA to LLVM IR conversion"""
        dna_sequence = "AGCOAGCOAGCO"
        llvm_ir = compiler.dna_to_llvm(dna_sequence)
        
        assert len(llvm_ir) > 0
        assert "target datalayout" in llvm_ir
        assert "target triple" in llvm_ir
        assert "@dna_sequence" in llvm_ir
        assert "define i32 @mobius_transform" in llvm_ir
        assert "define i32 @klein_transform" in llvm_ir
        assert "define i32 @main()" in llvm_ir
    
    def test_full_compilation_pipeline(self, compiler):
        """Test full end-to-end compilation"""
        input_text = "infinite loop in enclosed bottle"
        result = compiler.compile(input_text)
        
        # Verify all pipeline stages
        assert result.input_text == input_text
        assert len(result.hebrew_roots) > 0
        assert len(result.unicode_points) > 0
        assert result.wave_simulation is not None
        assert len(result.dna_sequence) > 0
        assert len(result.llvm_ir) > 0
        assert result.topology_metadata is not None
        
        # Verify topology metadata
        assert result.topology_metadata['topology_type'] == 'TopoFlame_INV-097'
        assert result.topology_metadata['patent_status'] == 'NOVEL - No conflicts (math concepts, no language integrations)'
        assert result.topology_metadata['quantum_entangled'] is True
        
        # Verify DNA identity cycle
        for nucleotide in DNA_NUCLEOTIDES:
            assert nucleotide in result.dna_sequence
    
    def test_identity_cycle_verification(self, compiler):
        """Test DNA identity cycle verification"""
        # Valid sequence with all nucleotides
        valid_sequence = "AGCOAGCO"
        result = compiler._verify_identity_cycle(valid_sequence)
        assert "✅ PASS" in result
        
        # Invalid sequence missing nucleotides
        invalid_sequence = "AAAA"
        result = compiler._verify_identity_cycle(invalid_sequence)
        assert "❌ FAIL" in result
    
    def test_export_result(self, compiler, tmp_path):
        """Test result export to JSON"""
        input_text = "loop cycle"
        result = compiler.compile(input_text)
        
        output_file = tmp_path / "test_result.json"
        compiler.export_result(result, str(output_file))
        
        assert output_file.exists()
        
        # Verify JSON is valid
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert 'input_text' in data
        assert 'hebrew_roots' in data
        assert 'unicode_points' in data
        assert 'wave_simulation' in data
        assert 'dna_sequence' in data
        assert 'llvm_ir' in data
        assert 'topology_metadata' in data


class TestPipelineIntegration:
    """Integration tests for complete pipeline"""
    
    def test_pipeline_mobius_emphasis(self):
        """Test pipeline with Möbius-heavy input"""
        compiler = FlameLangCompiler()
        result = compiler.compile("loop loop loop cycle send")
        
        # Should have more SLH roots
        slh_count = result.hebrew_roots.count('SLH')
        qlb_count = result.hebrew_roots.count('QLB')
        
        assert slh_count > qlb_count
    
    def test_pipeline_klein_emphasis(self):
        """Test pipeline with Klein-heavy input"""
        compiler = FlameLangCompiler()
        result = compiler.compile("contain bottle enclose")
        
        # Should have more QLB roots
        slh_count = result.hebrew_roots.count('SLH')
        qlb_count = result.hebrew_roots.count('QLB')
        
        assert qlb_count > slh_count
    
    def test_pipeline_balanced_topology(self):
        """Test pipeline with balanced topology"""
        compiler = FlameLangCompiler()
        result = compiler.compile("loop in bottle")
        
        # Should have both roots
        assert 'SLH' in result.hebrew_roots
        assert 'QLB' in result.hebrew_roots
    
    def test_multiple_compilations(self):
        """Test multiple independent compilations"""
        compiler = FlameLangCompiler()
        
        inputs = [
            "loop cycle",
            "contain bottle",
            "quantum entangled cycle"
        ]
        
        results = []
        for input_text in inputs:
            result = compiler.compile(input_text)
            results.append(result)
        
        # All should succeed
        assert len(results) == len(inputs)
        
        # Each should have valid DNA
        for result in results:
            for nucleotide in DNA_NUCLEOTIDES:
                assert nucleotide in result.dna_sequence


class TestTopoFlameInvariant:
    """Test TopoFlame invariant properties"""
    
    def test_topology_preservation(self):
        """Test that topology properties are preserved through pipeline"""
        compiler = FlameLangCompiler()
        result = compiler.compile("loop in bottle")
        
        # Verify Möbius properties in wave simulation
        assert 'mobius_transformations' in result.wave_simulation
        mobius_states = result.wave_simulation['mobius_transformations']
        
        for state in mobius_states:
            assert state['hebrew_root'] == 'SLH'
            assert state['topology'] == 'mobius'
        
        # Verify Klein properties in wave simulation
        assert 'klein_transformation' in result.wave_simulation
        klein_data = result.wave_simulation['klein_transformation']
        
        assert klein_data['hebrew_root'] == 'QLB'
        assert klein_data['topology'] == 'klein'
        assert klein_data['boundary_property'] == 'none'
    
    def test_dna_identity_cycle_invariant(self):
        """Test that DNA identity cycle is always maintained"""
        compiler = FlameLangCompiler()
        
        test_inputs = [
            "loop",
            "bottle",
            "cycle send",
            "contain enclose",
            "quantum loop"
        ]
        
        for input_text in test_inputs:
            result = compiler.compile(input_text)
            
            # Identity cycle must contain all A G C O
            for nucleotide in DNA_NUCLEOTIDES:
                assert nucleotide in result.dna_sequence, \
                    f"Missing {nucleotide} in DNA for input: {input_text}"


def run_tests():
    """Run all TopoFlame tests"""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == "__main__":
    run_tests()
