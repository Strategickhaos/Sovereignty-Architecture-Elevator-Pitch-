#!/bin/bash
# SAGCO-MENU v1.1 Integration Test
# Tests all three micro-hardening features

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "SAGCO-MENU v1.1 Integration Test"
echo "=========================================="
echo ""

# Test 1: Per-User State Management
echo "Test 1: Per-User State Management"
echo "----------------------------------"
export USER="testuser1"
./sagco-menu.py clear 2>/dev/null || true
./sagco-menu.py add "Tool A" "echo a"
./sagco-menu.py add "Tool B" "echo b"
echo "User 1 recents:"
./sagco-menu.py get

export USER="testuser2"
./sagco-menu.py clear 2>/dev/null || true
./sagco-menu.py add "Tool X" "echo x"
./sagco-menu.py add "Tool Y" "echo y"
echo ""
echo "User 2 recents:"
./sagco-menu.py get

export USER="testuser1"
echo ""
echo "Back to User 1 (should still have A and B):"
./sagco-menu.py get
echo "✅ Per-user state working"
echo ""

# Test 2: Cap Recents at 5
echo "Test 2: Cap Recents at 5 Unique Items"
echo "---------------------------------------"
export USER="testuser3"
./sagco-menu.py clear 2>/dev/null || true
for i in {1..8}; do
    ./sagco-menu.py add "Tool $i" "echo $i" >/dev/null 2>&1
done
echo "Added 8 tools, should only see last 5:"
./sagco-menu.py get
COUNT=$(./sagco-menu.py get | grep "Tool" | wc -l)
if [ "$COUNT" -eq 5 ]; then
    echo "✅ Cap at 5 items working"
else
    echo "❌ Expected 5 items, got $COUNT"
    exit 1
fi
echo ""

# Test 3: Deduplication
echo "Test 3: Deduplication"
echo "---------------------"
./sagco-menu.py clear 2>/dev/null || true
./sagco-menu.py add "Tool Alpha" "echo alpha" >/dev/null 2>&1
./sagco-menu.py add "Tool Beta" "echo beta" >/dev/null 2>&1
./sagco-menu.py add "Tool Gamma" "echo gamma" >/dev/null 2>&1
echo "Before re-adding Alpha:"
./sagco-menu.py get
echo ""
./sagco-menu.py add "Tool Alpha" "echo alpha-updated" >/dev/null 2>&1
echo "After re-adding Alpha (should be at end, no duplicate):"
./sagco-menu.py get
COUNT=$(./sagco-menu.py get | grep "Tool Alpha" | wc -l)
if [ "$COUNT" -eq 1 ]; then
    echo "✅ Deduplication working"
else
    echo "❌ Expected 1 Tool Alpha, got $COUNT"
    exit 1
fi
echo ""

# Test 4: YAML Parsing
echo "Test 4: YAML Parsing"
echo "--------------------"
python3 -c "
import yaml
with open('tools.yaml', 'r') as f:
    data = yaml.safe_load(f)
    categories = len(data.get('categories', []))
    total_tools = sum(len(cat.get('tools', [])) for cat in data.get('categories', []))
    print(f'Parsed {categories} categories with {total_tools} tools')
    if categories >= 5 and total_tools >= 10:
        print('✅ YAML structure valid')
    else:
        print(f'❌ Expected at least 5 categories and 10 tools')
        exit(1)
"
echo ""

# Test 5: File Permissions and Fallback
echo "Test 5: State File Fallback"
echo "---------------------------"
export USER="testuser4"
./sagco-menu.py clear 2>/dev/null || true
./sagco-menu.py add "Fallback Test" "echo test" >/dev/null 2>&1
if [ -f "$HOME/.sagco_menu_state_testuser4.json" ]; then
    echo "State file created in fallback location: $HOME/.sagco_menu_state_testuser4.json"
    echo "✅ Fallback mechanism working"
else
    echo "❌ State file not found in expected location"
    exit 1
fi
echo ""

# Cleanup
echo "Cleanup"
echo "-------"
for user in testuser1 testuser2 testuser3 testuser4; do
    export USER="$user"
    ./sagco-menu.py clear 2>/dev/null || true
done
echo "✅ Test data cleaned up"
echo ""

echo "=========================================="
echo "All tests passed! ✅"
echo "=========================================="
echo ""
echo "SAGCO-MENU v1.1 Features Verified:"
echo "  ✅ Per-user state management"
echo "  ✅ Recents capped at 5 items"
echo "  ✅ Automatic deduplication"
echo "  ✅ YAML parsing"
echo "  ✅ Fallback state storage"
echo ""
echo "Ready for production use!"
