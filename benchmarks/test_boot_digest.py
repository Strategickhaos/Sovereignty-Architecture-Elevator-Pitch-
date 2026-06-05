#!/usr/bin/env python3
"""
Boot Digest System Tests
Validates boot_digest.py functionality
"""

import os
import sys
import json
import tempfile
import shutil
import subprocess
from pathlib import Path

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from cpu import boot_digest

class BootDigestTests:
    def __init__(self):
        self.test_results = []
        
    def test_find_repo_root(self):
        """Test repository root detection"""
        print("Testing repo root detection...")
        try:
            repo_root = boot_digest.find_repo_root()
            assert repo_root is not None
            assert os.path.exists(os.path.join(repo_root, '.git'))
            print("✅ Repo root detection: PASSED")
            return True
        except Exception as e:
            print(f"❌ Repo root detection: FAILED - {e}")
            return False
    
    def test_get_git_stats(self):
        """Test git stats collection"""
        print("Testing git stats collection...")
        try:
            repo_root = boot_digest.find_repo_root()
            stats = boot_digest.get_git_stats(repo_root)
            assert 'commits' in stats
            assert 'last_commit' in stats
            assert 'open_prs_approx' in stats
            assert 'files_changed_7d' in stats
            assert isinstance(stats['commits'], int)
            print(f"✅ Git stats collection: PASSED (commits={stats['commits']})")
            return True
        except Exception as e:
            print(f"❌ Git stats collection: FAILED - {e}")
            return False
    
    def test_load_manifest(self):
        """Test manifest loading"""
        print("Testing manifest loading...")
        try:
            repo_root = boot_digest.find_repo_root()
            manifest_path = os.path.join(repo_root, boot_digest.MANIFEST_FILE)
            manifest = boot_digest.load_manifest(manifest_path)
            assert isinstance(manifest, dict)
            assert 'anchors' in manifest or manifest.get('anchors') is not None
            print(f"✅ Manifest loading: PASSED (anchors={len(manifest.get('anchors', []))})")
            return True
        except Exception as e:
            print(f"❌ Manifest loading: FAILED - {e}")
            return False
    
    def test_read_anchor(self):
        """Test anchor file reading"""
        print("Testing anchor file reading...")
        try:
            repo_root = boot_digest.find_repo_root()
            readme_path = os.path.join(repo_root, 'README.md')
            if os.path.exists(readme_path):
                content = boot_digest.read_anchor(readme_path)
                assert content is not None
                assert content != "FILE NOT FOUND"
                assert len(content) > 0
                print(f"✅ Anchor file reading: PASSED (length={len(content)})")
                return True
            else:
                print("⚠️ Anchor file reading: SKIPPED (README.md not found)")
                return True
        except Exception as e:
            print(f"❌ Anchor file reading: FAILED - {e}")
            return False
    
    def test_generate_digest_fast(self):
        """Test digest generation in fast mode"""
        print("Testing fast mode digest generation...")
        try:
            repo_root = boot_digest.find_repo_root()
            manifest = boot_digest.load_manifest(os.path.join(repo_root, boot_digest.MANIFEST_FILE))
            digest, stats = boot_digest.generate_digest(repo_root, manifest, fast_mode=True)
            assert digest is not None
            assert "# SAGCO BOOT DIGEST" in digest
            assert "Fast Mode: Stats Only" in digest
            assert "STATUS: CONFIDENCE_OK" in digest
            assert stats is not None
            assert 'commits' in stats
            print(f"✅ Fast mode digest: PASSED (length={len(digest)})")
            return True
        except Exception as e:
            print(f"❌ Fast mode digest: FAILED - {e}")
            return False
    
    def test_generate_digest_full(self):
        """Test digest generation in full mode"""
        print("Testing full mode digest generation...")
        try:
            repo_root = boot_digest.find_repo_root()
            manifest = boot_digest.load_manifest(os.path.join(repo_root, boot_digest.MANIFEST_FILE))
            digest, stats = boot_digest.generate_digest(repo_root, manifest, fast_mode=False)
            assert digest is not None
            assert "# SAGCO BOOT DIGEST" in digest
            assert "## Anchor Docs" in digest
            assert "STATUS: CONFIDENCE_OK" in digest
            assert stats is not None
            assert 'commits' in stats
            print(f"✅ Full mode digest: PASSED (length={len(digest)})")
            return True
        except Exception as e:
            print(f"❌ Full mode digest: FAILED - {e}")
            return False
    
    def test_cli_fast_mode(self):
        """Test CLI in fast mode"""
        print("Testing CLI fast mode...")
        try:
            repo_root = boot_digest.find_repo_root()
            script_path = os.path.join(repo_root, 'cpu', 'boot_digest.py')
            result = subprocess.run(
                ['python3', script_path, '--fast'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0
            assert "SAGCO BOOT DIGEST SUMMARY" in result.stdout
            assert "STATUS: CONFIDENCE_OK" in result.stdout
            print("✅ CLI fast mode: PASSED")
            return True
        except Exception as e:
            print(f"❌ CLI fast mode: FAILED - {e}")
            return False
    
    def run_all_tests(self):
        """Run all boot digest tests"""
        print("=" * 60)
        print("BOOT DIGEST SYSTEM VALIDATION")
        print("=" * 60)
        
        tests = [
            self.test_find_repo_root,
            self.test_get_git_stats,
            self.test_load_manifest,
            self.test_read_anchor,
            self.test_generate_digest_fast,
            self.test_generate_digest_full,
            self.test_cli_fast_mode,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            if test():
                passed += 1
            else:
                failed += 1
            print()
        
        print("=" * 60)
        print(f"RESULTS: {passed} passed, {failed} failed")
        print("=" * 60)
        
        return failed == 0

if __name__ == "__main__":
    tester = BootDigestTests()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
