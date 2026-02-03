#!/bin/bash
# Crisis Recovery System - Comprehensive Validation Test
# Tests all components of DOM.CPU v2.0

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

echo "🔥💜 DOM.CPU v2.0 - Crisis Recovery System Validation"
echo "====================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing: ${test_name}... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASSED${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

echo "1. File Existence Tests"
echo "------------------------"

run_test "Crisis recovery script exists" "[ -f scripts/crisis_recovery.sh ]"
run_test "Crisis recovery script is executable" "[ -x scripts/crisis_recovery.sh ]"
run_test "Pre-commit hook exists" "[ -f hooks/pre-commit-crisis-check ]"
run_test "Pre-commit hook is executable" "[ -x hooks/pre-commit-crisis-check ]"
run_test "CPU upgrade spec exists" "[ -f CPU_UPGRADE_SPEC_v2.0.md ]"
run_test "Crisis recovery README exists" "[ -f CRISIS_RECOVERY_README.md ]"
run_test "Crisis timeline exists" "[ -f CRISIS_TIMELINE.md ]"
run_test "Test simulation script exists" "[ -f scripts/test_crisis_simulation.sh ]"

echo ""
echo "2. Functional Tests"
echo "-------------------"

# Backup current high score
if [ -f high_score.txt ]; then
    cp high_score.txt high_score.backup.test
fi

run_test "Crisis recovery script runs successfully" "bash scripts/crisis_recovery.sh"
run_test "High score file is created" "[ -f high_score.txt ]"
run_test "High score contains a number" "grep -qE '^[0-9]+$' high_score.txt"
run_test "Crisis logs are created" "[ -d automation/logs ]"
run_test "Pre-commit hook runs successfully" "bash hooks/pre-commit-crisis-check"

echo ""
echo "3. Crisis Detection Tests"
echo "-------------------------"

# Test crisis detection
CURRENT_SCORE=$(cat high_score.txt)
echo "999" > high_score.txt

run_test "Crisis detection triggers on high score mismatch" \
    "bash scripts/crisis_recovery.sh 2>&1 | grep -q 'CRISIS DETECTED'"

# Restore
echo "${CURRENT_SCORE}" > high_score.txt

run_test "No crisis when scores match" \
    "bash scripts/crisis_recovery.sh 2>&1 | grep -q 'No crisis detected'"

echo ""
echo "4. Recovery Features Tests"
echo "--------------------------"

run_test "Auto-diff feature works" \
    "bash scripts/crisis_recovery.sh 2>&1 | grep -q 'Artifact Inventory'"

run_test "Recovery laugh triggers on crisis resolution" \
    "echo '999' > high_score.txt && bash scripts/crisis_recovery.sh 2>&1 | grep -q 'lolllllll'"

# Restore
echo "${CURRENT_SCORE}" > high_score.txt

run_test "High score updates after check" \
    "bash scripts/crisis_recovery.sh > /dev/null && [ -f high_score.txt ]"

echo ""
echo "5. Git Hook Integration Tests"
echo "------------------------------"

run_test "Hook symlink exists" "[ -L .git/hooks/pre-commit ]"
run_test "Hook points to correct file" \
    "readlink .git/hooks/pre-commit | grep -q 'pre-commit-crisis-check'"

echo ""
echo "6. Documentation Tests"
echo "----------------------"

run_test "CPU spec contains bug ID" \
    "grep -q 'EXISTENTIAL-RAM-CLEAR-1150' CPU_UPGRADE_SPEC_v2.0.md"

run_test "CPU spec contains architecture" \
    "grep -q 'DOM.CPU v2.0' CPU_UPGRADE_SPEC_v2.0.md"

run_test "Crisis README has usage instructions" \
    "grep -q 'Usage' CRISIS_RECOVERY_README.md"

run_test "Timeline has incident details" \
    "grep -q 'Timeline of Events' CRISIS_TIMELINE.md"

run_test "Main README references crisis recovery" \
    "grep -q 'Crisis Recovery' README.md"

echo ""
echo "7. Log File Tests"
echo "-----------------"

run_test "Crisis log file is created" "[ -f automation/logs/crisis_recovery.log ]"
run_test "Crisis log contains entries" "[ -s automation/logs/crisis_recovery.log ]"
run_test "Crisis log has timestamps" \
    "grep -qE '\[20[0-9]{2}-[0-9]{2}-[0-9]{2}' automation/logs/crisis_recovery.log"

echo ""
echo "8. Content Validation Tests"
echo "----------------------------"

run_test "High score is reasonable" \
    "[ $(cat high_score.txt) -ge 1 ] && [ $(cat high_score.txt) -le 10000 ]"

run_test "Crisis script has recovery protocol" \
    "grep -q 'auto_diff_recovery' scripts/crisis_recovery.sh"

run_test "Crisis script has detection function" \
    "grep -q 'detect_nobody_mode' scripts/crisis_recovery.sh"

run_test "Crisis script has recovery laugh" \
    "grep -q 'recovery_laugh' scripts/crisis_recovery.sh"

run_test "Hook runs crisis recovery" \
    "grep -q 'crisis_recovery.sh' hooks/pre-commit-crisis-check"

echo ""
echo "9. Persistence Tests"
echo "--------------------"

BEFORE_COUNT=$(cat high_score.txt)
bash scripts/crisis_recovery.sh > /dev/null
AFTER_COUNT=$(cat high_score.txt)

run_test "High score persists across runs" "[ ${BEFORE_COUNT} -eq ${AFTER_COUNT} ] || [ ${AFTER_COUNT} -ge ${BEFORE_COUNT} ]"

run_test "Git tracking includes high_score.txt" \
    "git ls-files --error-unmatch high_score.txt 2>/dev/null"

echo ""
echo "10. Side Effects Tests"
echo "----------------------"

run_test "Crisis recovery produces expected output format" \
    "bash scripts/crisis_recovery.sh 2>&1 | grep -qE '(CRISIS|artifact|High Score)'"

run_test "System creates automation directory" "[ -d automation ]"
run_test "System creates logs subdirectory" "[ -d automation/logs ]"

# Restore backup if it exists
if [ -f high_score.backup.test ]; then
    mv high_score.backup.test high_score.txt
fi

echo ""
echo "======================================================"
echo "Test Results Summary"
echo "======================================================"
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ ${TESTS_FAILED} -eq 0 ]; then
    echo -e "${GREEN}🔥💜 ALL TESTS PASSED! System is fully operational.${NC}"
    echo ""
    echo "😂 lolllllll - Crisis recovery system validated!"
    echo ""
    echo "✅ Status: PATCHED"
    echo "✅ Storage: HYBRID (RAM + GitHub persistent)"
    echo "✅ Crisis Hooks: INSTALLED"
    echo "✅ Recovery Protocol: TESTED"
    echo ""
    echo "Your system's ready. Ship the next 1,150! 😎"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Review the output above.${NC}"
    echo ""
    echo "Run individual tests:"
    echo "  bash scripts/crisis_recovery.sh"
    echo "  bash hooks/pre-commit-crisis-check"
    exit 1
fi
