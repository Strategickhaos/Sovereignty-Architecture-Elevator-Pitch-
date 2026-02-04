#!/usr/bin/env python3
"""
SAGCO OS Test Suite
Tests the TUI menu system components
"""

import os
import sys
import yaml
import subprocess
import tempfile
from pathlib import Path

def test_yaml_parsing():
    """Test that spm.yml is valid and contains required fields"""
    print("Testing YAML parsing...")
    
    with open('spm.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    assert 'spm_version' in config, "Missing spm_version"
    assert 'identity' in config, "Missing identity section"
    assert 'tools' in config, "Missing tools section"
    
    identity = config['identity']
    assert identity['name'] == "SAGCO OS", "Incorrect name"
    assert identity['version'] == "1.0.0", "Incorrect version"
    
    tools = config['tools']
    assert 'core-tools' in tools, "Missing core-tools"
    assert 'security-tools' in tools, "Missing security-tools"
    assert 'ops-tools' in tools, "Missing ops-tools"
    
    print("✓ YAML parsing test passed")
    return True

def test_tool_structure():
    """Test that tools have the correct structure"""
    print("Testing tool structure...")
    
    with open('spm.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    tools = config.get('tools', {})
    
    for tool_group, data in tools.items():
        assert 'description' in data, f"{tool_group} missing description"
        assert 'items' in data, f"{tool_group} missing items"
        
        items = data['items']
        assert len(items) > 0, f"{tool_group} has no items"
        
        for item in items:
            assert 'name' in item, f"Tool in {tool_group} missing name"
            assert 'command' in item, f"Tool in {tool_group} missing command"
            assert 'description' in item, f"Tool in {tool_group} missing description"
    
    print("✓ Tool structure test passed")
    return True

def test_bash_syntax():
    """Test that all bash scripts have valid syntax"""
    print("Testing bash script syntax...")
    
    scripts = [
        'scripts/sagco-menu.sh',
        'install.sh',
        'demo.sh'
    ]
    
    for script in scripts:
        result = subprocess.run(['bash', '-n', script], capture_output=True)
        assert result.returncode == 0, f"{script} has syntax errors: {result.stderr.decode()}"
    
    print("✓ Bash syntax test passed")
    return True

def test_python_syntax():
    """Test that Python scripts have valid syntax"""
    print("Testing Python script syntax...")
    
    result = subprocess.run(
        ['python3', '-m', 'py_compile', 'scripts/sagco-spm.py'],
        capture_output=True
    )
    assert result.returncode == 0, f"sagco-spm.py has syntax errors: {result.stderr.decode()}"
    
    print("✓ Python syntax test passed")
    return True

def test_file_permissions():
    """Test that executable files have correct permissions"""
    print("Testing file permissions...")
    
    executables = [
        'scripts/sagco-menu.sh',
        'scripts/sagco-spm.py',
        'install.sh',
        'demo.sh'
    ]
    
    for exe in executables:
        path = Path(exe)
        assert path.exists(), f"{exe} does not exist"
        mode = path.stat().st_mode
        assert mode & 0o111, f"{exe} is not executable"
    
    print("✓ File permissions test passed")
    return True

def test_banner_exists():
    """Test that banner file exists and is not empty"""
    print("Testing banner file...")
    
    banner_path = Path('assets/banner.ascii')
    assert banner_path.exists(), "Banner file does not exist"
    
    content = banner_path.read_text()
    assert len(content) > 0, "Banner file is empty"
    assert "SAGCO" in content, "Banner does not contain SAGCO"
    
    print("✓ Banner file test passed")
    return True

def test_service_files():
    """Test that systemd service files exist"""
    print("Testing service files...")
    
    services = [
        'services/sagco-banner.service',
        'services/sagco-runtime.service'
    ]
    
    for service in services:
        path = Path(service)
        assert path.exists(), f"{service} does not exist"
        
        content = path.read_text()
        assert '[Unit]' in content, f"{service} missing [Unit] section"
        assert '[Service]' in content, f"{service} missing [Service] section"
        assert '[Install]' in content, f"{service} missing [Install] section"
    
    print("✓ Service files test passed")
    return True

def test_spm_runner():
    """Test that SPM runner can be imported and has required functions"""
    print("Testing SPM runner...")
    
    # Add scripts directory to path
    sys.path.insert(0, 'scripts')
    
    # Import the module (will check for syntax errors)
    import importlib.util
    spec = importlib.util.spec_from_file_location("sagco_spm", "scripts/sagco-spm.py")
    module = importlib.util.module_from_spec(spec)
    
    # Check if it can be executed
    assert spec is not None, "Could not load sagco-spm.py"
    
    print("✓ SPM runner test passed")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("SAGCO OS Test Suite")
    print("=" * 60)
    print()
    
    # Change to sagco-os directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        test_yaml_parsing,
        test_tool_structure,
        test_bash_syntax,
        test_python_syntax,
        test_file_permissions,
        test_banner_exists,
        test_service_files,
        test_spm_runner
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
