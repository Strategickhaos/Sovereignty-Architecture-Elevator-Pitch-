#!/usr/bin/env python3
"""
Unit tests for Sanskrit Canonicalization Module (P1)
"""

import unittest
import json
import tempfile
from pathlib import Path

from sanskrit_canonicalization import (
    SanskritCanonicalizer,
    stem_sanskrit,
    stable_hash,
    save_dhatu_db
)


class TestSanskritCanonicalizer(unittest.TestCase):
    """Test cases for Sanskrit canonicalization"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.canonicalizer = SanskritCanonicalizer()
    
    def test_unicode_normalization(self):
        """Test Unicode normalization removes ZWJ/ZWNJ"""
        text_with_zwj = "test\u200Dtext"
        text_with_zwnj = "test\u200Ctext"
        
        result1 = self.canonicalizer.normalize_unicode(text_with_zwj)
        result2 = self.canonicalizer.normalize_unicode(text_with_zwnj)
        
        self.assertEqual(result1, "testtext")
        self.assertEqual(result2, "testtext")
    
    def test_replacement_char_removal(self):
        """Test replacement character removal"""
        text_with_replacement = "test\uFFFDtext"
        result = self.canonicalizer.normalize_unicode(text_with_replacement)
        self.assertEqual(result, "testtext")
    
    def test_dhatu_lookup_exact_match(self):
        """Test exact match in dhatu database"""
        canonical, match_type, score = self.canonicalizer.lookup_dhatu("गुणगणविषय")
        
        self.assertEqual(canonical, "गुणगण")
        self.assertEqual(match_type, "exact")
        self.assertEqual(score, 1.0)
    
    def test_dhatu_lookup_no_match(self):
        """Test no match in dhatu database"""
        canonical, match_type, score = self.canonicalizer.lookup_dhatu("unknown")
        
        self.assertEqual(canonical, "unknown")
        self.assertEqual(match_type, "none")
        self.assertEqual(score, 0.0)
    
    def test_canonicalization_pipeline(self):
        """Test full canonicalization pipeline"""
        text = "गुणगणविषय गणगणविषय"
        result = self.canonicalizer.canonicalize(text)
        
        self.assertEqual(result["original"], text)
        self.assertEqual(result["canonical"], "गुणगण गुणगण")
        self.assertEqual(len(result["matches"]), 2)
        self.assertEqual(result["matches"][0]["match_type"], "exact")
        self.assertEqual(result["matches"][1]["match_type"], "exact")
    
    def test_multiple_word_canonicalization(self):
        """Test canonicalization with multiple words"""
        text = "धर्मस्य कर्मणि"
        result = self.canonicalizer.canonicalize(text)
        
        self.assertEqual(result["canonical"], "धर्म कर्मन्")
        self.assertEqual(len(result["matches"]), 2)
    
    def test_rewrite_log(self):
        """Test rewrite log tracks applied rewrites"""
        self.canonicalizer.rewrite_log.clear()
        self.canonicalizer.lookup_dhatu("गुणगणविषय")
        
        self.assertEqual(len(self.canonicalizer.rewrite_log), 1)
        self.assertIn("गुणगणविषय", self.canonicalizer.rewrite_log[0])
        self.assertIn("गुणगण", self.canonicalizer.rewrite_log[0])


class TestStemSanskrit(unittest.TestCase):
    """Test cases for stem_sanskrit function"""
    
    def test_stem_sanskrit_basic(self):
        """Test basic stem_sanskrit functionality"""
        result = stem_sanskrit("गुणगणविषय")
        
        self.assertIn("original", result)
        self.assertIn("canonical", result)
        self.assertIn("stable_hash", result)
        self.assertIn("matches", result)
    
    def test_stable_hash_deterministic(self):
        """Test stable hash is deterministic"""
        hash1 = stable_hash("test")
        hash2 = stable_hash("test")
        
        self.assertEqual(hash1, hash2)
    
    def test_stable_hash_different_inputs(self):
        """Test stable hash produces different results for different inputs"""
        hash1 = stable_hash("test1")
        hash2 = stable_hash("test2")
        
        self.assertNotEqual(hash1, hash2)
    
    def test_stem_sanskrit_with_custom_canonicalizer(self):
        """Test stem_sanskrit with custom canonicalizer"""
        custom_db = {"test": "canonical_test"}
        canonicalizer = SanskritCanonicalizer()
        canonicalizer.dhatu_db = custom_db
        
        result = stem_sanskrit("test", canonicalizer)
        self.assertEqual(result["canonical"], "canonical_test")


class TestDhatuDatabase(unittest.TestCase):
    """Test cases for dhatu database operations"""
    
    def test_load_dhatu_db(self):
        """Test loading dhatu database from file"""
        test_db = {"word1": "root1", "word2": "root2"}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_db, f)
            temp_path = f.name
        
        try:
            canonicalizer = SanskritCanonicalizer(temp_path)
            self.assertEqual(canonicalizer.dhatu_db, test_db)
        finally:
            Path(temp_path).unlink()
    
    def test_load_missing_dhatu_db(self):
        """Test loading missing dhatu database falls back to defaults"""
        canonicalizer = SanskritCanonicalizer("/nonexistent/path.json")
        
        # Should fall back to default DB
        self.assertIsNotNone(canonicalizer.dhatu_db)
        self.assertIn("गुणगणविषय", canonicalizer.dhatu_db)
    
    def test_save_dhatu_db(self):
        """Test saving dhatu database to file"""
        test_db = {"word1": "root1", "word2": "root2"}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            save_dhatu_db(test_db, temp_path)
            
            with open(temp_path, 'r') as f:
                loaded_db = json.load(f)
            
            self.assertEqual(loaded_db, test_db)
        finally:
            Path(temp_path).unlink()


class TestProvenanceMetadata(unittest.TestCase):
    """Test provenance and metadata tracking"""
    
    def test_match_metadata_present(self):
        """Test that match metadata is present in results"""
        result = stem_sanskrit("गुणगणविषय")
        
        self.assertTrue(len(result["matches"]) > 0)
        match = result["matches"][0]
        
        self.assertIn("original_surface", match)
        self.assertIn("canonical", match)
        self.assertIn("match_type", match)
        self.assertIn("match_score", match)
    
    def test_match_scores_valid(self):
        """Test match scores are in valid range"""
        result = stem_sanskrit("गुणगणविषय unknown")
        
        for match in result["matches"]:
            score = match["match_score"]
            self.assertTrue(0.0 <= score <= 1.0)


class TestCompressionScenarios(unittest.TestCase):
    """Test real-world compression scenarios"""
    
    def test_problem_statement_examples(self):
        """Test specific examples from problem statement"""
        canonicalizer = SanskritCanonicalizer()
        
        # Test case 1: गुणगणविषय → गुणगण
        result1 = canonicalizer.canonicalize("गुणगणविषय")
        self.assertEqual(result1["canonical"], "गुणगण")
        
        # Test case 2: गणगणविषय → गुणगण (drift case)
        result2 = canonicalizer.canonicalize("गणगणविषय")
        self.assertEqual(result2["canonical"], "गुणगण")
        
        # Verify both map to same canonical form
        hash1 = stable_hash(result1["canonical"])
        hash2 = stable_hash(result2["canonical"])
        self.assertEqual(hash1, hash2)
    
    def test_100_percent_hit_rate(self):
        """Test 100% hit rate on known roots"""
        known_roots = ["गुणगणविषय", "गणगणविषय", "धर्मस्य", "कर्मणि", "ब्रह्मणः"]
        canonicalizer = SanskritCanonicalizer()
        
        total_hits = 0
        total_attempts = 0
        
        for root in known_roots:
            result = canonicalizer.canonicalize(root)
            for match in result["matches"]:
                total_attempts += 1
                if match["match_type"] == "exact":
                    total_hits += 1
        
        hit_rate = total_hits / total_attempts if total_attempts > 0 else 0
        self.assertEqual(hit_rate, 1.0)  # 100% hit rate


if __name__ == "__main__":
    unittest.main()
