#!/bin/bash
# SAGCO Menu System Test Suite v1.2
# Tests all core functionality of the menu system

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Setup test environment
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export SPM_PATH="$REPO_ROOT/opt/sagco/spm.yml"
export SAGCO_STATE_DIR="/tmp/sagco_test_$$"
export SAGCO_BIN="$REPO_ROOT/opt/sagco/bin"
MENU_PY="$REPO_ROOT/opt/sagco/bin/sagco-menu.py"

mkdir -p "$SAGCO_STATE_DIR"

# Test helper functions
test_pass() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

test_fail() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

test_section() {
    echo ""
    echo -e "${YELLOW}=== $1 ===${NC}"
}

# Test 1: File existence
test_section "File Existence Tests"

if [[ -f "$SPM_PATH" ]]; then
    test_pass "spm.yml exists"
else
    test_fail "spm.yml missing"
fi

if [[ -x "$MENU_PY" ]]; then
    test_pass "sagco-menu.py is executable"
else
    test_fail "sagco-menu.py not executable"
fi

# Test 2: Python syntax
test_section "Syntax Validation Tests"

if python3 -m py_compile "$MENU_PY" 2>/dev/null; then
    test_pass "Python syntax valid"
else
    test_fail "Python syntax error"
fi

if python3 -c "import yaml; yaml.safe_load(open('$SPM_PATH'))" 2>/dev/null; then
    test_pass "YAML syntax valid"
else
    test_fail "YAML syntax error"
fi

# Test 3: Categories listing
test_section "Categories Listing Tests"

CATEGORIES_OUTPUT=$(python3 "$MENU_PY" categories 2>&1)
if echo "$CATEGORIES_OUTPUT" | grep -q "security-tools"; then
    test_pass "Categories include security-tools"
else
    test_fail "Categories missing security-tools"
fi

if echo "$CATEGORIES_OUTPUT" | grep -q "🔒"; then
    test_pass "Categories include icons"
else
    test_fail "Categories missing icons"
fi

CATEGORY_COUNT=$(echo "$CATEGORIES_OUTPUT" | wc -l)
if [[ $CATEGORY_COUNT -ge 4 ]]; then
    test_pass "Categories count is $CATEGORY_COUNT (expected >= 4)"
else
    test_fail "Categories count is $CATEGORY_COUNT (expected >= 4)"
fi

# Test 4: Items listing
test_section "Items Listing Tests"

ITEMS_OUTPUT=$(python3 "$MENU_PY" items security-tools 2>&1)
if echo "$ITEMS_OUTPUT" | grep -q "Nmap"; then
    test_pass "Security tools include Nmap"
else
    test_fail "Security tools missing Nmap"
fi

ITEMS_COUNT=$(echo "$ITEMS_OUTPUT" | wc -l)
if [[ $ITEMS_COUNT -ge 3 ]]; then
    test_pass "Security tools count is $ITEMS_COUNT (expected >= 3)"
else
    test_fail "Security tools count is $ITEMS_COUNT (expected >= 3)"
fi

# Test 5: Global search
test_section "Global Search Tests"

# Test exact substring match
SEARCH_NMAP=$(python3 "$MENU_PY" items all "nmap" 2>&1)
if echo "$SEARCH_NMAP" | grep -q "Nmap"; then
    test_pass "Search for 'nmap' finds Nmap"
else
    test_fail "Search for 'nmap' doesn't find Nmap"
fi

# Test broader search
SEARCH_NETWORK=$(python3 "$MENU_PY" items all "network" 2>&1)
NETWORK_COUNT=$(echo "$SEARCH_NETWORK" | wc -l)
if [[ $NETWORK_COUNT -ge 5 ]]; then
    test_pass "Search for 'network' finds $NETWORK_COUNT tools (expected >= 5)"
else
    test_fail "Search for 'network' finds $NETWORK_COUNT tools (expected >= 5)"
fi

# Test no results
SEARCH_NONE=$(python3 "$MENU_PY" items all "xyznonexistent" 2>&1)
if [[ -z "$SEARCH_NONE" ]]; then
    test_pass "Search for nonexistent term returns empty"
else
    test_fail "Search for nonexistent term should return empty"
fi

# Test 6: Recent items
test_section "Recent Items Tests"

# Add first item
python3 "$MENU_PY" add_recent security-tools Nmap 2>&1 >/dev/null
RECENT_OUTPUT=$(python3 "$MENU_PY" recent 2>&1)
if echo "$RECENT_OUTPUT" | grep -q "Nmap"; then
    test_pass "Recent items include added tool"
else
    test_fail "Recent items missing added tool"
fi

# Add more items
python3 "$MENU_PY" add_recent networking Ping 2>&1 >/dev/null
python3 "$MENU_PY" add_recent development "Python Shell" 2>&1 >/dev/null
python3 "$MENU_PY" add_recent system-admin "Disk Usage" 2>&1 >/dev/null
RECENT_COUNT=$(python3 "$MENU_PY" recent 2>&1 | wc -l)
if [[ $RECENT_COUNT -eq 4 ]]; then
    test_pass "Recent items count is $RECENT_COUNT (expected 4)"
else
    test_fail "Recent items count is $RECENT_COUNT (expected 4)"
fi

# Test 7: Recent items cap
test_section "Recent Items Cap Tests"

# Add 3 more items (total 7, should cap at 5)
python3 "$MENU_PY" add_recent networking Traceroute 2>&1 >/dev/null
python3 "$MENU_PY" add_recent security-tools Wireshark 2>&1 >/dev/null
python3 "$MENU_PY" add_recent networking Netstat 2>&1 >/dev/null

RECENT_CAP_COUNT=$(python3 "$MENU_PY" recent 2>&1 | wc -l)
if [[ $RECENT_CAP_COUNT -eq 5 ]]; then
    test_pass "Recent items capped at 5"
else
    test_fail "Recent items not capped (got $RECENT_CAP_COUNT, expected 5)"
fi

# Verify first item was removed
if ! python3 "$MENU_PY" recent 2>&1 | grep -q "Nmap"; then
    test_pass "Oldest item (Nmap) removed after cap"
else
    test_fail "Oldest item (Nmap) still present after cap"
fi

# Test 8: Deduplication
test_section "Deduplication Tests"

# Add duplicate
python3 "$MENU_PY" add_recent networking Netstat 2>&1 >/dev/null
NETSTAT_COUNT=$(python3 "$MENU_PY" recent 2>&1 | grep -c "Netstat")
if [[ $NETSTAT_COUNT -eq 1 ]]; then
    test_pass "Duplicate item deduplicated"
else
    test_fail "Duplicate item not deduplicated (found $NETSTAT_COUNT times)"
fi

# Verify it's at the end (most recent)
LAST_ITEM=$(python3 "$MENU_PY" recent 2>&1 | tail -1)
if echo "$LAST_ITEM" | grep -q "Netstat"; then
    test_pass "Deduplicated item moved to end"
else
    test_fail "Deduplicated item not moved to end"
fi

# Test 9: State file format
test_section "State File Tests"

STATE_FILE="$SAGCO_STATE_DIR/menu_state_$USER.json"
if [[ -f "$STATE_FILE" ]]; then
    test_pass "State file created"
else
    test_fail "State file not created"
fi

if python3 -c "import json; json.load(open('$STATE_FILE'))" 2>/dev/null; then
    test_pass "State file is valid JSON"
else
    test_fail "State file is not valid JSON"
fi

if grep -q '"recent"' "$STATE_FILE"; then
    test_pass "State file contains 'recent' key"
else
    test_fail "State file missing 'recent' key"
fi

# Test 10: Environment variables
test_section "Environment Variable Tests"

CUSTOM_SPM="/tmp/custom_spm_$$.yml"
cp "$SPM_PATH" "$CUSTOM_SPM"
export SPM_PATH="$CUSTOM_SPM"

if python3 "$MENU_PY" categories 2>&1 | grep -q "security-tools"; then
    test_pass "Custom SPM_PATH works"
else
    test_fail "Custom SPM_PATH not working"
fi

rm "$CUSTOM_SPM"
export SPM_PATH="$REPO_ROOT/opt/sagco/spm.yml"

# Test 11: Per-user state
test_section "Per-User State Tests"

STATE_FILE_CHECK="$SAGCO_STATE_DIR/menu_state_$USER.json"
if [[ -f "$STATE_FILE_CHECK" ]]; then
    test_pass "Per-user state file uses \$USER variable"
else
    test_fail "Per-user state file not using \$USER variable"
fi

# Cleanup
rm -rf "$SAGCO_STATE_DIR"

# Summary
test_section "Test Summary"
TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
echo ""
echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
