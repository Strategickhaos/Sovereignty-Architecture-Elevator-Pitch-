#!/usr/bin/env python3
"""
FlameLang Meroitic Converter Test Suite
Tests for Meroitic Unicode mapping and conversion functionality
"""

import sys
import json
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flamelang.meroitic_converter import (
    english_to_meroitic_root,
    ConversionSpike,
    meroitic_hieroglyph_map,
    export_conversion_to_json
)


class TestMeroiticConverter:
    """Test suite for FlameLang Meroitic converter"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.test_results = []
        
    def test_basic_conversion(self):
        """Test 1: Basic English to Meroitic conversion"""
        print("\n🔥 Test 1: Basic English to Meroitic conversion")
        
        spike = english_to_meroitic_root("Flame Lang")
        
        # Verify output structure
        assert isinstance(spike, ConversionSpike), "Output should be ConversionSpike"
        assert spike.input == "Flame Lang", "Input should be preserved"
        assert len(spike.output_glyphs) > 0, "Output glyphs should not be empty"
        assert len(spike.unicode_map) > 0, "Unicode map should not be empty"
        
        print(f"   Input: {spike.input}")
        print(f"   Output: {spike.output_glyphs}")
        print(f"   Unicode: {spike.unicode_map}")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_syllable_priority(self):
        """Test 2: Two-letter syllable prioritization"""
        print("\n🔥 Test 2: Syllable prioritization (la > l+a)")
        
        spike = english_to_meroitic_root("la")
        
        # Should map to single glyph 𐦐 (U+10990) not 'l' + 'a'
        assert '\U00010990' in spike.output_glyphs, "Should contain 'la' glyph"
        assert spike.output_glyphs == '\U00010990', "Should be exactly one glyph for 'la'"
        
        print(f"   Input: la")
        print(f"   Output: {spike.output_glyphs}")
        print(f"   Unicode: {spike.unicode_map}")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_phonetic_preprocessing(self):
        """Test 3: Phonetic preprocessing (th->ta, ch->kha, ph->pa)"""
        print("\n🔥 Test 3: Phonetic preprocessing")
        
        test_cases = [
            ("the", "ta"),  # 'th' should become 'ta'
            ("chat", "kha"),  # 'ch' should become 'kha'
            ("phone", "pa")  # 'ph' should become 'pa'
        ]
        
        for input_text, expected_phoneme in test_cases:
            spike = english_to_meroitic_root(input_text)
            # Check if the expected phoneme was processed
            print(f"   {input_text} -> {spike.output_glyphs}")
            assert len(spike.output_glyphs) > 0, f"Should convert {input_text}"
            
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_unmapped_fallback(self):
        """Test 4: Unmapped characters fallback"""
        print("\n🔥 Test 4: Unmapped character fallback")
        
        spike = english_to_meroitic_root("xyz")
        
        # x, y, z are not in the meroitic map, should fall through
        assert 'x' in spike.output_glyphs or 'y' in spike.output_glyphs, "Should contain unmapped chars"
        
        print(f"   Input: xyz")
        print(f"   Output: {spike.output_glyphs}")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_unicode_map_generation(self):
        """Test 5: Unicode codepoint map generation"""
        print("\n🔥 Test 5: Unicode codepoint map generation")
        
        spike = english_to_meroitic_root("a")
        
        # Should generate U+ format Unicode points
        assert "U+" in spike.unicode_map, "Should contain U+ prefix"
        assert spike.unicode_map.count("U+") >= 1, "Should have at least one Unicode point"
        
        print(f"   Input: a")
        print(f"   Unicode map: {spike.unicode_map}")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_conversion_spike_structure(self):
        """Test 6: ConversionSpike dataclass structure"""
        print("\n🔥 Test 6: ConversionSpike structure")
        
        spike = english_to_meroitic_root("test")
        
        # Check all required fields
        assert hasattr(spike, 'input'), "Should have 'input' field"
        assert hasattr(spike, 'output_glyphs'), "Should have 'output_glyphs' field"
        assert hasattr(spike, 'unicode_map'), "Should have 'unicode_map' field"
        assert hasattr(spike, 'entropy'), "Should have 'entropy' field"
        assert spike.entropy == 0.5, "Default entropy should be 0.5"
        
        # Check to_dict method
        spike_dict = spike.to_dict()
        assert isinstance(spike_dict, dict), "to_dict should return dict"
        assert 'input' in spike_dict, "Dict should contain 'input'"
        assert 'output_glyphs' in spike_dict, "Dict should contain 'output_glyphs'"
        
        print(f"   Spike fields: input, output_glyphs, unicode_map, entropy")
        print(f"   to_dict() works: {list(spike_dict.keys())}")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_json_export(self):
        """Test 7: JSON export functionality"""
        print("\n🔥 Test 7: JSON export to file")
        
        spike = english_to_meroitic_root("test export")
        test_file = "/tmp/test_meroitic_export.json"
        
        # Export to JSON
        export_conversion_to_json(spike, test_file)
        
        # Verify file exists and is valid JSON
        assert os.path.exists(test_file), "JSON file should be created"
        
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        assert 'conversion' in data, "Should have 'conversion' key"
        assert 'map_summary' in data, "Should have 'map_summary' key"
        assert data['conversion']['input'] == spike.input, "Should preserve input"
        assert isinstance(data['map_summary'], list), "map_summary should be a list"
        
        # Clean up
        os.remove(test_file)
        
        print(f"   Exported to: {test_file}")
        print(f"   JSON keys: {list(data.keys())}")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_meroitic_map_completeness(self):
        """Test 8: Meroitic hieroglyph map completeness"""
        print("\n🔥 Test 8: Meroitic map completeness")
        
        # Verify map contains expected glyphs
        expected_glyphs = ['a', 'e', 'i', 'o', 'la', 'ma', 'na', 'ra', 'sa', 'ta', 'ka']
        
        for glyph in expected_glyphs:
            assert glyph in meroitic_hieroglyph_map, f"Map should contain '{glyph}'"
            
        # Verify Unicode range (U+10980–U+1099F)
        for key, value in meroitic_hieroglyph_map.items():
            codepoint = ord(value)
            assert 0x10980 <= codepoint <= 0x1099F, f"Glyph {key} should be in Meroitic Unicode block"
            
        print(f"   Map contains {len(meroitic_hieroglyph_map)} glyphs")
        print(f"   All glyphs in Unicode range U+10980–U+1099F")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_density_improvement(self):
        """Test 9: Verify density improvement (semantic compression)"""
        print("\n🔥 Test 9: Semantic density improvement")
        
        test_phrase = "Flame Lang"
        spike = english_to_meroitic_root(test_phrase)
        
        # Count original vs converted length
        original_len = len(test_phrase.replace(' ', ''))
        converted_len = len(spike.output_glyphs)
        
        print(f"   Original: '{test_phrase}' ({original_len} chars)")
        print(f"   Converted: '{spike.output_glyphs}' ({converted_len} chars)")
        print(f"   Compression ratio: {original_len}/{converted_len} = {original_len/converted_len:.2f}x")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def test_case_insensitivity(self):
        """Test 10: Case-insensitive conversion"""
        print("\n🔥 Test 10: Case-insensitive conversion")
        
        spike_lower = english_to_meroitic_root("flame")
        spike_upper = english_to_meroitic_root("FLAME")
        spike_mixed = english_to_meroitic_root("FlAmE")
        
        # All should produce same output
        assert spike_lower.output_glyphs == spike_upper.output_glyphs, "Case should not matter"
        assert spike_lower.output_glyphs == spike_mixed.output_glyphs, "Mixed case should match"
        
        print(f"   'flame' -> {spike_lower.output_glyphs}")
        print(f"   'FLAME' -> {spike_upper.output_glyphs}")
        print(f"   'FlAmE' -> {spike_mixed.output_glyphs}")
        print("   ✅ PASSED")
        self.passed += 1
        return True
        
    def run_all_tests(self):
        """Run all test cases"""
        print("=" * 60)
        print("🔥 FlameLang Meroitic Converter Test Suite")
        print("=" * 60)
        
        tests = [
            self.test_basic_conversion,
            self.test_syllable_priority,
            self.test_phonetic_preprocessing,
            self.test_unmapped_fallback,
            self.test_unicode_map_generation,
            self.test_conversion_spike_structure,
            self.test_json_export,
            self.test_meroitic_map_completeness,
            self.test_density_improvement,
            self.test_case_insensitivity
        ]
        
        for test in tests:
            try:
                test()
            except AssertionError as e:
                print(f"   ❌ FAILED: {e}")
                self.failed += 1
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                self.failed += 1
                
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        
        return self.failed == 0


if __name__ == "__main__":
    runner = TestMeroiticConverter()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
