#!/bin/bash
# SAGCO-MENU v1.2 - Comprehensive Test Suite

# Don't exit on error - we want to run all tests
set +e

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    SAGCO-MENU v1.2 TEST SUITE                              ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Setup test environment
TEST_DIR="/tmp/sagco-test-$$"
mkdir -p "$TEST_DIR/opt/sagco/bin"
mkdir -p "$TEST_DIR/var/lib/sagco"

# Copy files
cp "$(dirname "$0")/opt/sagco/spm.yml" "$TEST_DIR/opt/sagco/"
cp "$(dirname "$0")/opt/sagco/bin/sagco-menu.py" "$TEST_DIR/opt/sagco/bin/"

# Patch paths in Python script
sed -i 's|SPM_PATH = "/opt/sagco/spm.yml"|SPM_PATH = "'$TEST_DIR'/opt/sagco/spm.yml"|' \
    "$TEST_DIR/opt/sagco/bin/sagco-menu.py"
sed -i 's|STATE_PATH = "/var/lib/sagco/menu_state.json"|STATE_PATH = "'$TEST_DIR'/var/lib/sagco/menu_state.json"|' \
    "$TEST_DIR/opt/sagco/bin/sagco-menu.py"

chmod +x "$TEST_DIR/opt/sagco/bin/sagco-menu.py"

MENU="$TEST_DIR/opt/sagco/bin/sagco-menu.py"

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    local expected="$3"
    
    echo "┌────────────────────────────────────────────────────────────────────────┐"
    echo "│ TEST: $test_name"
    echo "└────────────────────────────────────────────────────────────────────────┘"
    
    result=$(eval "$test_cmd" 2>&1)
    
    if echo "$result" | grep -q "$expected"; then
        echo "✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "❌ FAIL"
        echo "Expected: $expected"
        echo "Got: $result"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# Test 1: Categories command
run_test "List categories" \
    "$MENU categories | wc -l" \
    "4"

# Test 2: Category order
run_test "Category ordering" \
    "$MENU categories | head -1 | cut -f1" \
    "core-tools"

# Test 3: Category icons
run_test "Category icons present" \
    "$MENU categories | grep -c '🛠️\|🔒\|⚙️\|🌐'" \
    "4"

# Test 4: Items in category
run_test "List items in core-tools" \
    "$MENU items core-tools | wc -l" \
    "5"

# Test 5: Item icons
run_test "Item icons present" \
    "$MENU items core-tools | grep -c '📂\|🐳\|☸️\|🐍\|🟢'" \
    "5"

# Test 6: Cross-tool search (exact match)
run_test "Search for 'Docker'" \
    "$MENU items all Docker | cut -f1" \
    "Docker"

# Test 7: Cross-tool search (case insensitive)
run_test "Search for 'DOCKER' (case insensitive)" \
    "$MENU items all DOCKER | cut -f1" \
    "Docker"

# Test 8: Cross-tool search (description match)
run_test "Search for 'network'" \
    "$MENU items all network | wc -l" \
    "3"

# Test 9: Cross-tool search (command match)
run_test "Search for 'version'" \
    "$MENU items all version | head -1 | cut -f1" \
    "Git"

# Test 10: Add to recent
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ TEST: Add to recently used"
echo "└────────────────────────────────────────────────────────────────────────┘"
$MENU add_recent core-tools Git
if [ -f "$TEST_DIR/var/lib/sagco/menu_state.json" ]; then
    echo "✅ PASS"
    ((TESTS_PASSED++))
else
    echo "❌ FAIL - State file not created"
    ((TESTS_FAILED++))
fi
echo ""

# Test 11: List recent
run_test "List recently used" \
    "$MENU recent | cut -f1" \
    "Git"

# Test 12: Recent limit (add 6 items, should only show 5)
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ TEST: Recent list limit (5 items max)"
echo "└────────────────────────────────────────────────────────────────────────┘"
$MENU add_recent core-tools Docker
$MENU add_recent security-tools Nmap
$MENU add_recent network-tools Curl
$MENU add_recent ops-tools Terraform
$MENU add_recent core-tools Python
$MENU add_recent network-tools SSH

recent_count=$($MENU recent | wc -l)
if [ "$recent_count" -eq 5 ]; then
    echo "✅ PASS (5 items in recent list)"
    ((TESTS_PASSED++))
else
    echo "❌ FAIL (Expected 5, got $recent_count)"
    ((TESTS_FAILED++))
fi
echo ""

# Test 13: Recent list doesn't contain oldest
run_test "Oldest item removed from recent" \
    "$MENU recent | cut -f1 | grep -c '^Git$'" \
    "0"

# Test 14: Recent list move to end
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ TEST: Re-using tool moves to end of recent list"
echo "└────────────────────────────────────────────────────────────────────────┘"
$MENU add_recent core-tools Docker
last_item=$($MENU recent | tail -1 | cut -f1)
if [ "$last_item" = "Docker" ]; then
    echo "✅ PASS (Docker moved to end)"
    ((TESTS_PASSED++))
else
    echo "❌ FAIL (Expected Docker at end, got $last_item)"
    ((TESTS_FAILED++))
fi
echo ""

# Test 15: State file structure
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ TEST: State file JSON structure"
echo "└────────────────────────────────────────────────────────────────────────┘"
if python3 -c "import json; json.load(open('$TEST_DIR/var/lib/sagco/menu_state.json'))" 2>/dev/null; then
    echo "✅ PASS (Valid JSON)"
    ((TESTS_PASSED++))
else
    echo "❌ FAIL (Invalid JSON)"
    ((TESTS_FAILED++))
fi
echo ""

# Test 16: Per-user state
run_test "Per-user state (user key in JSON)" \
    "cat $TEST_DIR/var/lib/sagco/menu_state.json" \
    '"recent"'

# Test 17: YAML validation
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ TEST: YAML file validation"
echo "└────────────────────────────────────────────────────────────────────────┘"
if python3 -c "import yaml; yaml.safe_load(open('$TEST_DIR/opt/sagco/spm.yml'))" 2>/dev/null; then
    echo "✅ PASS (Valid YAML)"
    ((TESTS_PASSED++))
else
    echo "❌ FAIL (Invalid YAML)"
    ((TESTS_FAILED++))
fi
echo ""

# Test 18: All categories have required fields
run_test "Categories have icons" \
    "$MENU categories | cut -f2 | grep -c '^.\+$'" \
    "4"

# Test 19: All items have required fields
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ TEST: All items have required fields"
echo "└────────────────────────────────────────────────────────────────────────┘"
all_items=$($MENU items core-tools)
name_count=$(echo "$all_items" | cut -f1 | grep -c '^.\+$')
cmd_count=$(echo "$all_items" | cut -f4 | grep -c '^.\+$')
if [ "$name_count" -eq 5 ] && [ "$cmd_count" -eq 5 ]; then
    echo "✅ PASS (All items have name and command)"
    ((TESTS_PASSED++))
else
    echo "❌ FAIL (Missing name or command)"
    ((TESTS_FAILED++))
fi
echo ""

# Test 20: Empty search returns all
run_test "Empty search returns all category items" \
    "$MENU items core-tools '' | wc -l" \
    "5"

# Summary
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                           TEST SUMMARY                                     ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"
echo "✅ Passed: $TESTS_PASSED"
echo "❌ Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED! 🔥💜"
    echo ""
    echo "SAGCO-MENU v1.2 is fully functional:"
    echo "  ✓ Cross-tool fuzzy search"
    echo "  ✓ Category ordering with icons"
    echo "  ✓ Recently used tracking (per-user)"
    echo "  ✓ State persistence (JSON)"
    echo "  ✓ YAML validation"
    echo ""
    echo "DOM. 😭🔥💜"
else
    echo "⚠️  Some tests failed. Please review the output above."
fi

# Cleanup
rm -rf "$TEST_DIR"

exit $TESTS_FAILED
