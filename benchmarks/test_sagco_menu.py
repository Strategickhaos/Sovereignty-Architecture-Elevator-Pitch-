#!/usr/bin/env python3
"""
SAGCO Menu System Tests
Test YAML-driven tool catalog with search, ordering, icons, and recently used functionality
"""

import sys
import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add opt/sagco/bin to Python path for importing sagco-menu
sys.path.insert(0, str(Path(__file__).parent.parent / "opt" / "sagco" / "bin"))


class SAGCOMenuTests:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.sagco_menu_py = self.repo_root / "opt" / "sagco" / "bin" / "sagco-menu.py"
        self.spm_yml = self.repo_root / "opt" / "sagco" / "spm.yml"
        self.test_results = []
        
    def run_command(self, args):
        """Run sagco-menu.py command and return output."""
        cmd = ["python3", str(self.sagco_menu_py)] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.repo_root))
        return result.returncode, result.stdout, result.stderr
    
    def test_01_yaml_structure_valid(self):
        """Test 1: Verify YAML structure is valid and contains required keys."""
        result = {"test_id": 1, "name": "YAML Structure Validation", "status": "PASS"}
        
        try:
            import yaml
            with open(self.spm_yml, 'r') as f:
                spm = yaml.safe_load(f)
            
            # Check required keys
            assert "tools" in spm, "Missing 'tools' key in YAML"
            tools = spm["tools"]
            
            # Check order key exists
            assert "order" in tools, "Missing 'order' key in tools"
            result["categories_in_order"] = tools["order"]
            
            # Check categories exist
            for category in tools["order"]:
                assert category in tools, f"Category '{category}' in order but not defined"
                cat_data = tools[category]
                assert "description" in cat_data, f"Missing description in {category}"
                assert "items" in cat_data, f"Missing items in {category}"
                
            result["categories_found"] = len(tools["order"])
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def test_02_categories_listing(self):
        """Test 2: List categories and verify ordering."""
        result = {"test_id": 2, "name": "Categories Listing", "status": "PASS"}
        
        try:
            returncode, stdout, stderr = self.run_command(["categories"])
            
            assert returncode == 0, f"Command failed with exit code {returncode}"
            
            lines = [l for l in stdout.strip().split('\n') if l]
            result["categories_count"] = len(lines)
            
            # Parse categories
            categories = []
            for line in lines:
                parts = line.split('\t')
                assert len(parts) >= 3, f"Invalid category line format: {line}"
                categories.append({
                    "key": parts[0],
                    "icon": parts[1],
                    "description": parts[2]
                })
            
            result["categories"] = categories
            
            # Verify expected categories exist
            expected_keys = ["core-tools", "security-tools", "ops-tools"]
            found_keys = [c["key"] for c in categories]
            
            for expected in expected_keys:
                assert expected in found_keys, f"Expected category '{expected}' not found"
            
            # Verify ordering
            assert found_keys == expected_keys, f"Category ordering incorrect: {found_keys}"
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def test_03_items_listing(self):
        """Test 3: List items in categories with icons."""
        result = {"test_id": 3, "name": "Items Listing", "status": "PASS"}
        
        try:
            # Test core-tools
            returncode, stdout, stderr = self.run_command(["items", "core-tools"])
            assert returncode == 0, "Command failed"
            
            lines = [l for l in stdout.strip().split('\n') if l]
            result["core_tools_count"] = len(lines)
            
            # Parse items
            items = []
            for line in lines:
                parts = line.split('\t')
                assert len(parts) == 4, f"Invalid item line format: {line}"
                items.append({
                    "name": parts[0],
                    "icon": parts[1],
                    "description": parts[2],
                    "command": parts[3]
                })
            
            result["core_tools_items"] = items
            
            # Verify expected items
            item_names = [i["name"] for i in items]
            assert "Git" in item_names, "Git not found in core-tools"
            assert "TMUX" in item_names, "TMUX not found in core-tools"
            
            # Verify icons present
            for item in items:
                assert item["icon"], f"Missing icon for {item['name']}"
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def test_04_search_functionality(self):
        """Test 4: Search/filter items by name and description."""
        result = {"test_id": 4, "name": "Search Functionality", "status": "PASS"}
        
        try:
            # Search for "nmap" in security-tools
            returncode, stdout, stderr = self.run_command(["items", "security-tools", "nmap"])
            assert returncode == 0, "Command failed"
            
            lines = [l for l in stdout.strip().split('\n') if l]
            result["nmap_search_results"] = len(lines)
            
            # Should find Nmap
            assert len(lines) == 1, f"Expected 1 result for 'nmap', got {len(lines)}"
            assert "Nmap" in lines[0], "Nmap not found in search results"
            
            # Search for "network" (should match by description)
            returncode, stdout, stderr = self.run_command(["items", "security-tools", "network"])
            lines = [l for l in stdout.strip().split('\n') if l]
            result["network_search_results"] = len(lines)
            
            assert len(lines) >= 1, "Network search should find at least one result"
            
            # Search for non-existent term
            returncode, stdout, stderr = self.run_command(["items", "security-tools", "nonexistent"])
            lines = [l for l in stdout.strip().split('\n') if l]
            result["empty_search_results"] = len(lines)
            
            assert len(lines) == 0, "Non-existent search should return no results"
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def test_05_recently_used_tracking(self):
        """Test 5: Recently used items tracking and retrieval."""
        result = {"test_id": 5, "name": "Recently Used Tracking", "status": "PASS"}
        
        try:
            # Clear state by removing any existing state file
            state_file = self.repo_root / "opt" / "sagco" / "menu_state.json"
            if state_file.exists():
                state_file.unlink()
            
            # Initially should be empty
            returncode, stdout, stderr = self.run_command(["recent"])
            assert returncode == 0, "Recent command failed"
            lines = [l for l in stdout.strip().split('\n') if l]
            assert len(lines) == 0, f"Recently used should be empty initially, got {len(lines)} items"
            
            # Add items to recent
            self.run_command(["add_recent", "core-tools", "Git"])
            self.run_command(["add_recent", "security-tools", "Nmap"])
            self.run_command(["add_recent", "ops-tools", "Docker"])
            
            # Check recent
            returncode, stdout, stderr = self.run_command(["recent"])
            assert returncode == 0, "Recent command failed after adding items"
            
            lines = [l for l in stdout.strip().split('\n') if l]
            result["recent_count"] = len(lines)
            
            assert len(lines) == 3, f"Expected 3 recent items, got {len(lines)}"
            
            # Verify items are in correct order (Git, Nmap, Docker)
            assert "Git" in lines[0], "First recent item should be Git"
            assert "Nmap" in lines[1], "Second recent item should be Nmap"
            assert "Docker" in lines[2], "Third recent item should be Docker"
            
            # Test duplicate handling (adding Git again should move it to end)
            self.run_command(["add_recent", "core-tools", "Git"])
            returncode, stdout, stderr = self.run_command(["recent"])
            lines = [l for l in stdout.strip().split('\n') if l]
            
            assert len(lines) == 3, "Duplicate should not increase count"
            assert "Git" in lines[2], "Duplicate Git should move to end"
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def test_06_icon_presence(self):
        """Test 6: Verify icons are present for categories and items."""
        result = {"test_id": 6, "name": "Icon Presence", "status": "PASS"}
        
        try:
            # Check category icons
            returncode, stdout, stderr = self.run_command(["categories"])
            lines = [l for l in stdout.strip().split('\n') if l]
            
            icons_found = 0
            for line in lines:
                parts = line.split('\t')
                if len(parts) >= 2 and parts[1].strip():
                    icons_found += 1
            
            result["category_icons_found"] = icons_found
            result["total_categories"] = len(lines)
            
            assert icons_found == len(lines), f"Not all categories have icons: {icons_found}/{len(lines)}"
            
            # Check item icons
            returncode, stdout, stderr = self.run_command(["items", "core-tools"])
            lines = [l for l in stdout.strip().split('\n') if l]
            
            item_icons_found = 0
            for line in lines:
                parts = line.split('\t')
                if len(parts) >= 2 and parts[1].strip():
                    item_icons_found += 1
            
            result["item_icons_found"] = item_icons_found
            result["total_items"] = len(lines)
            
            assert item_icons_found == len(lines), f"Not all items have icons: {item_icons_found}/{len(lines)}"
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def test_07_bash_script_exists(self):
        """Test 7: Verify bash script exists and is executable."""
        result = {"test_id": 7, "name": "Bash Script Validation", "status": "PASS"}
        
        try:
            bash_script = self.repo_root / "opt" / "sagco" / "bin" / "sagco-menu.sh"
            
            assert bash_script.exists(), "sagco-menu.sh does not exist"
            result["script_exists"] = True
            
            # Check if executable
            is_executable = os.access(bash_script, os.X_OK)
            result["is_executable"] = is_executable
            
            assert is_executable, "sagco-menu.sh is not executable"
            
            # Check shebang
            with open(bash_script, 'r') as f:
                first_line = f.readline().strip()
                result["shebang"] = first_line
                assert first_line == "#!/bin/bash", f"Invalid shebang: {first_line}"
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def test_08_profile_integration(self):
        """Test 8: Verify profile.d integration script exists."""
        result = {"test_id": 8, "name": "Profile.d Integration", "status": "PASS"}
        
        try:
            profile_script = self.repo_root / "etc" / "profile.d" / "sagco-menu.sh"
            
            assert profile_script.exists(), "profile.d/sagco-menu.sh does not exist"
            result["profile_script_exists"] = True
            
            # Check if executable
            is_executable = os.access(profile_script, os.X_OK)
            result["is_executable"] = is_executable
            
            # Check it references the correct path
            with open(profile_script, 'r') as f:
                content = f.read()
                assert "sagco-menu.sh" in content, "Profile script does not reference sagco-menu.sh"
            
        except Exception as e:
            result["status"] = "FAIL"
            result["error"] = str(e)
        
        return result
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        print("=" * 80)
        print("SAGCO Menu System Tests")
        print("=" * 80)
        
        tests = [
            self.test_01_yaml_structure_valid,
            self.test_02_categories_listing,
            self.test_03_items_listing,
            self.test_04_search_functionality,
            self.test_05_recently_used_tracking,
            self.test_06_icon_presence,
            self.test_07_bash_script_exists,
            self.test_08_profile_integration,
        ]
        
        for test_func in tests:
            result = test_func()
            self.test_results.append(result)
            
            status_symbol = "✓" if result["status"] == "PASS" else "✗"
            print(f"{status_symbol} Test {result['test_id']}: {result['name']} - {result['status']}")
            
            if result["status"] == "FAIL":
                print(f"  Error: {result.get('error', 'Unknown')}")
        
        # Summary
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        total = len(self.test_results)
        
        print("=" * 80)
        print(f"Tests Passed: {passed}/{total}")
        print("=" * 80)
        
        # Save detailed results
        reports_dir = self.repo_root / "benchmarks" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        with open(reports_dir / "sagco_menu_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\nDetailed results saved to: {reports_dir / 'sagco_menu_results.json'}")
        
        return passed == total


if __name__ == "__main__":
    tester = SAGCOMenuTests()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
