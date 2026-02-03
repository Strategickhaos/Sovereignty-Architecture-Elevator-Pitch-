#!/usr/bin/env python3
"""
Test suite for CPU Boot Digest system.
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cpu.boot_digest import BootDigest


def test_boot_digest_initialization():
    """Test that BootDigest can be initialized."""
    print("Testing BootDigest initialization...")
    boot = BootDigest()
    assert boot.repo_root is not None
    assert isinstance(boot.manifest, dict)
    print("✓ BootDigest initialized successfully")


def test_generate_digest():
    """Test that digest generation works."""
    print("Testing digest generation...")
    boot = BootDigest()
    digest = boot.generate_digest(fast_mode=True)
    
    assert "SAGCO BOOT DIGEST" in digest
    assert "STATUS:" in digest
    assert "Repo:" in digest
    assert "Commits:" in digest
    print("✓ Digest generated successfully")


def test_fast_mode():
    """Test fast mode digest."""
    print("Testing fast mode...")
    boot = BootDigest()
    digest_fast = boot.generate_digest(fast_mode=True)
    digest_full = boot.generate_digest(fast_mode=False)
    
    # Fast mode should be shorter
    assert len(digest_fast) < len(digest_full)
    print("✓ Fast mode working correctly")


def test_cli_doctor():
    """Test CLI doctor command."""
    print("Testing CLI doctor command...")
    result = subprocess.run(
        [sys.executable, "-m", "cpu", "doctor", "--no-report"],
        capture_output=True,
        text=True,
        timeout=15
    )
    
    assert result.returncode == 0
    assert "SAGCO BOOT DIGEST" in result.stdout
    print("✓ CLI doctor command works")


def test_cli_panic():
    """Test CLI panic command."""
    print("Testing CLI panic command...")
    result = subprocess.run(
        [sys.executable, "-m", "cpu", "panic"],
        capture_output=True,
        text=True,
        timeout=15
    )
    
    assert result.returncode == 0
    assert "SAGCO BOOT DIGEST" in result.stdout
    print("✓ CLI panic command works")


def test_boot_report_creation():
    """Test that BOOT_REPORT.md is created."""
    print("Testing BOOT_REPORT.md creation...")
    boot = BootDigest()
    digest = boot.generate_digest(fast_mode=False)
    report_path = boot.write_boot_report(digest)
    
    assert report_path.exists()
    content = report_path.read_text()
    assert "Boot Report" in content
    assert "SAGCO BOOT DIGEST" in content
    print("✓ BOOT_REPORT.md created successfully")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CPU Boot Digest Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        test_boot_digest_initialization,
        test_generate_digest,
        test_fast_mode,
        test_cli_doctor,
        test_cli_panic,
        test_boot_report_creation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except Exception as e:
            failed += 1
            print(f"✗ Test failed: {e}")
            print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
