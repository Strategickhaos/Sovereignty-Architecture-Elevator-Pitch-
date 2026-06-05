#!/usr/bin/env python3
"""
Test script for SAGCO SPM implementation
Validates all created files and their structure
"""
import os
import sys
import yaml

def test_file_exists(path, description):
    """Test if a file exists."""
    if os.path.exists(path):
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ MISSING {description}: {path}")
        return False

def test_directory_exists(path, description):
    """Test if a directory exists."""
    if os.path.isdir(path):
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ MISSING {description}: {path}")
        return False

def test_yaml_valid(path):
    """Test if YAML file is valid."""
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        print(f"✓ YAML is valid: {path}")
        return True, data
    except Exception as e:
        print(f"✗ YAML is INVALID: {path} - {e}")
        return False, None

def test_python_syntax(path):
    """Test if Python file has valid syntax."""
    try:
        with open(path, 'r') as f:
            compile(f.read(), path, 'exec')
        print(f"✓ Python syntax valid: {path}")
        return True
    except Exception as e:
        print(f"✗ Python syntax INVALID: {path} - {e}")
        return False

def test_executable(path):
    """Test if file is executable."""
    if os.access(path, os.X_OK):
        print(f"✓ File is executable: {path}")
        return True
    else:
        print(f"✗ File is NOT executable: {path}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("SAGCO SPM Implementation Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    # Test main script
    print("\n[1] Testing sagco-spm.py...")
    all_passed &= test_file_exists("sagco-spm.py", "Main runner script")
    all_passed &= test_python_syntax("sagco-spm.py")
    all_passed &= test_executable("sagco-spm.py")
    
    # Test YAML manifest
    print("\n[2] Testing spm.yml...")
    all_passed &= test_file_exists("spm.yml", "SPM manifest")
    yaml_valid, spm_data = test_yaml_valid("spm.yml")
    all_passed &= yaml_valid
    
    if yaml_valid and spm_data:
        print(f"  - SPM Version: {spm_data.get('spm_version', 'N/A')}")
        print(f"  - Identity: {spm_data.get('identity', {}).get('name', 'N/A')}")
        print(f"  - Codename: {spm_data.get('identity', {}).get('codename', 'N/A')}")
    
    # Test directories
    print("\n[3] Testing directory structure...")
    all_passed &= test_directory_exists("assets", "Assets directory")
    all_passed &= test_directory_exists("services", "Services directory")
    all_passed &= test_directory_exists("ui", "UI directory")
    all_passed &= test_directory_exists("ui/plymouth/sagco", "Plymouth theme directory")
    
    # Test asset files
    print("\n[4] Testing asset files...")
    all_passed &= test_file_exists("assets/banner.ascii", "ASCII banner")
    all_passed &= test_file_exists("assets/README.md", "Assets README")
    
    # Test service files
    print("\n[5] Testing systemd service files...")
    all_passed &= test_file_exists("services/sagco-banner.service", "Banner service")
    all_passed &= test_file_exists("services/sagco-runtime.service", "Runtime service")
    
    # Test UI files
    print("\n[6] Testing UI files...")
    all_passed &= test_file_exists("ui/motd", "MOTD file")
    all_passed &= test_file_exists("ui/issue", "Issue file")
    all_passed &= test_file_exists("ui/plymouth/sagco/sagco.plymouth", "Plymouth config")
    all_passed &= test_file_exists("ui/plymouth/sagco/script.script", "Plymouth script")
    
    # Test documentation
    print("\n[7] Testing documentation...")
    all_passed &= test_file_exists("SAGCO_SPM_README.md", "Main documentation")
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
