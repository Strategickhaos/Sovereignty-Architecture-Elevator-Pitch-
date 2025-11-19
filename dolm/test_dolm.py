#!/usr/bin/env python3
"""
Test suite for Department of Living Memory (DoLM)
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from dolm_daemon import DoLMConfig, CodeAnalyzer, ObsidianVault


def test_config_initialization():
    """Test DoLM configuration initialization"""
    print("Testing DoLM configuration...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ['DOLM_VAULT_PATH'] = tmpdir
        config = DoLMConfig()
        
        assert config.vault_path == tmpdir
        assert len(config.watch_extensions) > 0
        assert '.py' in config.watch_extensions
        assert len(config.todo_patterns) > 0
        assert len(config.error_patterns) > 0
        
        # Check vault structure created
        vault = Path(tmpdir)
        assert (vault / 'errors').exists()
        assert (vault / 'todos').exists()
        assert (vault / 'daily').exists()
        assert (vault / '.obsidian').exists()
        assert (vault / '.obsidian' / 'config.json').exists()
        
    print("✓ Configuration test passed")


def test_code_analyzer():
    """Test code analysis functionality"""
    print("Testing code analyzer...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ['DOLM_VAULT_PATH'] = tmpdir
        config = DoLMConfig()
        analyzer = CodeAnalyzer(config)
        
        # Create a test file with TODOs and errors
        test_file = Path(tmpdir) / 'test.py'
        test_file.write_text("""
# TODO: Implement feature X
def main():
    # FIXME: This is broken
    pass

# HACK: Temporary workaround
# XXX: Critical issue here
""")
        
        results = analyzer.analyze_file(str(test_file))
        
        assert results['file'] == str(test_file)
        assert 'todos' in results
        assert 'errors' in results
        assert 'stats' in results
        assert len(results['todos']) >= 4  # Should find TODO, FIXME, HACK, XXX
        assert results['stats']['todo_count'] >= 4
        
    print("✓ Code analyzer test passed")


def test_obsidian_vault():
    """Test Obsidian vault note generation"""
    print("Testing Obsidian vault...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ['DOLM_VAULT_PATH'] = tmpdir
        config = DoLMConfig()
        vault = ObsidianVault(config)
        
        # Test TODO note creation
        todo_data = {
            'line': 42,
            'content': '# TODO: Test task',
            'type': 'TODO',
            'message': 'Test task'
        }
        vault.create_todo_note(todo_data, '/test/file.py')
        
        # Check note was created
        todo_files = list((Path(tmpdir) / 'todos').glob('*.md'))
        assert len(todo_files) > 0
        
        # Test error note creation
        error_data = {
            'line': 100,
            'content': 'Error: Something went wrong'
        }
        vault.create_error_note(error_data, '/test/file.py')
        
        # Check note was created
        error_files = list((Path(tmpdir) / 'errors').glob('*.md'))
        assert len(error_files) > 0
        
        # Test daily summary
        vault.create_daily_summary()
        daily_files = list((Path(tmpdir) / 'daily').glob('*.md'))
        assert len(daily_files) > 0
        
    print("✓ Obsidian vault test passed")


def test_end_to_end():
    """Test end-to-end workflow"""
    print("Testing end-to-end workflow...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ['DOLM_VAULT_PATH'] = tmpdir
        os.environ['DOLM_WATCH_PATH'] = tmpdir
        
        config = DoLMConfig()
        analyzer = CodeAnalyzer(config)
        vault = ObsidianVault(config)
        
        # Create test files
        test_file1 = Path(tmpdir) / 'test1.py'
        test_file1.write_text("""
# TODO: Add docstrings
def calculate(x, y):
    # FIXME: Handle division by zero
    return x / y
""")
        
        test_file2 = Path(tmpdir) / 'test2.js'
        test_file2.write_text("""
// TODO: Add error handling
function process() {
    // HACK: Quick fix for demo
    return null;
}
""")
        
        # Process files
        for test_file in [test_file1, test_file2]:
            results = analyzer.analyze_file(str(test_file))
            
            for todo in results['todos']:
                vault.create_todo_note(todo, str(test_file))
            
            for error in results['errors']:
                vault.create_error_note(error, str(test_file))
        
        # Generate summary
        vault.create_daily_summary()
        
        # Verify results
        todo_count = len(list((Path(tmpdir) / 'todos').glob('*.md')))
        daily_count = len(list((Path(tmpdir) / 'daily').glob('*.md')))
        
        assert todo_count >= 3  # Should have at least 3 TODOs
        assert daily_count == 1  # Should have 1 daily summary
        
    print("✓ End-to-end test passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Department of Living Memory (DoLM) - Test Suite")
    print("=" * 60)
    
    tests = [
        test_config_initialization,
        test_code_analyzer,
        test_obsidian_vault,
        test_end_to_end
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
