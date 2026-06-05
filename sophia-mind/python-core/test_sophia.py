#!/usr/bin/env python3
"""
Test suite for SOPHIA MIND Brain Visualizer
"""

import tempfile
import json
from pathlib import Path
import sophia_parser
import sophia_sync


def test_parser():
    """Test the markdown parser"""
    print("🧪 Testing SOPHIA Parser...")
    
    # Create temporary vault
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = Path(tmpdir)
        
        # Create test markdown files
        (vault / "test1.md").write_text("""---
title: "Test Node 1"
glyph: FL1
frequency: 528
tags: [test, code]
---

# Test Node 1

This is a test node with a link to [[test2]].
""")
        
        (vault / "test2.md").write_text("""---
title: "Test Node 2"
glyph: AT1
---

# Test Node 2

Connected to [[test1]] and [[test3]].
""")
        
        (vault / "test3.md").write_text("""# Test Node 3

Simple node with #[RC1] glyph in body.
""")
        
        # Parse vault
        parser = sophia_parser.SophiaParser(str(vault))
        result = parser.parse_vault()
        
        # Verify results
        assert result['node_count'] == 3, f"Expected 3 nodes, got {result['node_count']}"
        assert 'test1' in parser.nodes, "test1 node not found"
        assert 'test2' in parser.nodes, "test2 node not found"
        assert 'test3' in parser.nodes, "test3 node not found"
        
        # Check node properties
        test1 = parser.nodes['test1']
        assert test1['frequency'] == 528, f"Expected frequency 528, got {test1['frequency']}"
        assert 'FL1' in test1['glyphs'], "FL1 glyph not found in test1"
        assert 'test2' in test1['connections'], "Connection to test2 not found"
        
        test3 = parser.nodes['test3']
        assert 'RC1' in test3['glyphs'], "RC1 glyph not found in test3"
        
        # Test export
        output = vault / "graph.json"
        parser.export_to_unity(str(output))
        
        # Verify export
        assert output.exists(), "Export file not created"
        
        with open(output) as f:
            data = json.load(f)
            assert 'nodes' in data, "nodes missing from export"
            assert 'edges' in data, "edges missing from export"
            assert len(data['nodes']) == 3, "Wrong number of nodes in export"
        
        # Test statistics
        stats = parser.get_statistics()
        assert stats['total_nodes'] == 3, "Wrong total nodes in stats"
        
        print("✅ Parser tests passed!")
        return True


def test_sync():
    """Test the sync engine"""
    print("🧪 Testing SOPHIA Sync Engine...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = Path(tmpdir) / "vault"
        vault.mkdir()
        
        proton = Path(tmpdir) / "proton"
        proton.mkdir()
        
        # Create test file
        (vault / "test.md").write_text("# Test\n\nTest content")
        
        # Initialize sync
        sync = sophia_sync.SophiaSync(str(vault), {
            'proton': str(proton)
        })
        
        # Detect changes
        changes = sync.detect_changes()
        assert len(changes['added']) == 1, "Should detect 1 added file"
        assert 'test.md' in changes['added'], "test.md not in added files"
        
        # Sync to proton
        sync.sync_to_proton(changes)
        
        # Verify file was copied
        proton_file = proton / "test.md"
        assert proton_file.exists(), "File not synced to proton"
        assert proton_file.read_text() == vault.joinpath("test.md").read_text(), "File content mismatch"
        
        # Test modification detection
        (vault / "test.md").write_text("# Test\n\nModified content")
        changes = sync.detect_changes()
        assert len(changes['modified']) == 1, "Should detect 1 modified file"
        
        # Test deletion detection
        (vault / "test.md").unlink()
        changes = sync.detect_changes()
        assert len(changes['deleted']) == 1, "Should detect 1 deleted file"
        
        print("✅ Sync engine tests passed!")
        return True


def test_glyph_mapping():
    """Test FlameLang glyph to frequency mapping"""
    print("🧪 Testing FlameLang Glyph Mapping...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = Path(tmpdir)
        parser = sophia_parser.SophiaParser(str(vault))
        
        # Test various glyphs
        test_cases = {
            'AE1': 432,   # Aegis Engine - Coherence
            'FL1': 528,   # FlameLang - Transformation
            'RC1': 639,   # Recon - Connection
            'FB1': 741,   # Flamebearer - Expression
            'LY1': 852,   # Lyra - Intuition
            'AT1': 963,   # Athena - Oneness
            'GR1': 999,   # Genesis - Creation
        }
        
        for glyph, expected_freq in test_cases.items():
            freq = parser.glyph_to_frequency([glyph])
            assert freq == expected_freq, f"Glyph {glyph}: expected {expected_freq}Hz, got {freq}Hz"
        
        # Test default frequency
        default_freq = parser.glyph_to_frequency(['UNKNOWN'])
        assert default_freq == 432, f"Default frequency should be 432Hz, got {default_freq}Hz"
        
        print("✅ Glyph mapping tests passed!")
        return True


def main():
    """Run all tests"""
    print("🧠 SOPHIA MIND Test Suite")
    print("=" * 50)
    
    try:
        test_parser()
        test_sync()
        test_glyph_mapping()
        
        print("\n" + "=" * 50)
        print("✨ All tests passed! SOPHIA MIND is ready!")
        print("=" * 50)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
