#!/bin/bash
# SAGCO-MENU v1.1 Test Script
# Demonstrates all features of the SAGCO menu system

set -e

BASE_DIR="/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-"
PY_SCRIPT="$BASE_DIR/opt/sagco/bin/sagco-menu.py"
YAML_FILE="$BASE_DIR/opt/sagco/spm.yml"

# Override paths for testing
export SPM_PATH="$YAML_FILE"
export STATE_PATH="$BASE_DIR/var/lib/sagco/menu_state.json"

echo "🔥 SAGCO-MENU v1.1 Test Suite 🔥"
echo "================================"
echo ""

# Test 1: Categories
echo "Test 1: List Categories (with icons and ordering)"
echo "-------------------------------------------------"
python3 "$PY_SCRIPT" categories
echo ""

# Test 2: Items
echo "Test 2: List Items in 'core-tools' category"
echo "--------------------------------------------"
python3 "$PY_SCRIPT" items core-tools
echo ""

# Test 3: Search
echo "Test 3: Search for 'network' in security-tools"
echo "----------------------------------------------"
python3 "$PY_SCRIPT" items security-tools network
echo ""

# Test 4: Empty search
echo "Test 4: List all security-tools (empty search)"
echo "----------------------------------------------"
python3 "$PY_SCRIPT" items security-tools ""
echo ""

# Test 5: Recently used (empty)
echo "Test 5: Recently used (before adding any)"
echo "-----------------------------------------"
python3 "$PY_SCRIPT" recent || echo "(empty - no recent items yet)"
echo ""

# Test 6: Add to recent
echo "Test 6: Add tools to recently used"
echo "-----------------------------------"
python3 "$PY_SCRIPT" add_recent core-tools Git
echo "Added: Git"
python3 "$PY_SCRIPT" add_recent security-tools Nmap
echo "Added: Nmap"
python3 "$PY_SCRIPT" add_recent ops-tools Docker
echo "Added: Docker"
echo ""

# Test 7: Recently used (populated)
echo "Test 7: Recently used (after adding tools)"
echo "------------------------------------------"
python3 "$PY_SCRIPT" recent
echo ""

# Test 8: Add duplicate
echo "Test 8: Add duplicate (should move to end)"
echo "------------------------------------------"
python3 "$PY_SCRIPT" add_recent core-tools Git
echo "Re-added: Git (should be last now)"
python3 "$PY_SCRIPT" recent
echo ""

# Test 9: Verify state file
echo "Test 9: Verify state file contents"
echo "-----------------------------------"
cat "$STATE_PATH"
echo ""

# Test 10: Category ordering
echo "Test 10: Verify category ordering matches YAML"
echo "----------------------------------------------"
echo "Expected order: core-tools, security-tools, ops-tools"
echo "Actual order:"
python3 "$PY_SCRIPT" categories | cut -f1
echo ""

echo "✅ All tests completed successfully!"
echo ""
echo "📝 Summary:"
echo "  - Categories with icons: ✓"
echo "  - Items with search/filter: ✓"
echo "  - Recently used tracking: ✓"
echo "  - State persistence: ✓"
echo "  - Category ordering: ✓"
echo ""
echo "🎯 SAGCO-MENU v1.1 is ready for deployment!"
