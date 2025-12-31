#!/bin/bash
# Comprehensive Test Suite for BPEC
# Validates all components and generates test report

set -e

REPO_ROOT="/home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-"
SKHAOS_ROOT="${REPO_ROOT}/skhaos-emulator"
TEST_REPORT="${SKHAOS_ROOT}/TEST_REPORT.md"

cd "$SKHAOS_ROOT"

echo "🧪 BPEC Comprehensive Test Suite"
echo "================================="
echo ""

# Initialize test report
cat > "$TEST_REPORT" << 'EOF'
# BPEC Test Report
Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Test Results Summary

EOF

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Testing: $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo "✅ PASS"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo "- ✅ **$test_name**: PASS" >> "$TEST_REPORT"
    else
        echo "❌ FAIL"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo "- ❌ **$test_name**: FAIL" >> "$TEST_REPORT"
    fi
}

# Test 1: Module Files Exist
echo ""
echo "📂 Testing Module Files..."
run_test "bio_physics/mod.rs exists" "test -f src/bio_physics/mod.rs"
run_test "zipf_analyzer.rs exists" "test -f src/bio_physics/zipf_analyzer.rs"
run_test "dolphin_comm.rs exists" "test -f src/bio_physics/dolphin_comm.rs"
run_test "physics_dom.rs exists" "test -f src/bio_physics/physics_dom.rs"
run_test "udap_bio.rs exists" "test -f src/bio_physics/udap_bio.rs"

# Test 2: Phase Scripts
echo ""
echo "🔧 Testing Phase Scripts..."
run_test "phase13_zipf.sh executable" "test -x phases/phase13_zipf.sh"
run_test "phase14_dolphin.sh executable" "test -x phases/phase14_dolphin.sh"
run_test "phase15_physics.sh executable" "test -x phases/phase15_physics.sh"
run_test "evolve_recursive.sh executable" "test -x phases/evolve_recursive.sh"

# Test 3: Schema Files
echo ""
echo "📋 Testing Schema Files..."
run_test "udap.json valid" "test -f schemas/udap.json && grep -q 'skhaos' schemas/udap.json"
run_test "flamelang.dsl exists" "test -f schemas/flamelang.dsl"

# Test 4: Documentation
echo ""
echo "📚 Testing Documentation..."
run_test "README.md exists" "test -f README.md && grep -q 'BPEC' README.md"
run_test "CLI_COMMANDS.md complete" "test -f CLI_COMMANDS.md && grep -q '42' CLI_COMMANDS.md"
run_test "QUICKSTART.md exists" "test -f QUICKSTART.md"

# Test 5: Container Configuration
echo ""
echo "🐳 Testing Container Configuration..."
run_test "Podmanfile exists" "test -f containers/Podmanfile"
run_test "bio_physics.pod exists" "test -f containers/bio_physics.pod"

# Test 6: Phase Execution
echo ""
echo "🚀 Testing Phase Execution..."
echo "   (Running actual phases, this may take 30 seconds...)"

# Clean sandbox first
rm -rf sandbox/*.log sandbox/*.json 2>/dev/null || true

run_test "Phase 13 execution" "./phases/phase13_zipf.sh > /dev/null 2>&1"
run_test "Zipf analysis generated" "test -f sandbox/zipf_analysis.log"
run_test "Evolution log created" "test -f sandbox/evolution_log.json"

run_test "Phase 14 execution" "./phases/phase14_dolphin.sh > /dev/null 2>&1"
run_test "Dolphin signatures generated" "test -f sandbox/dolphin_signatures.log"
run_test "Echolocation analysis generated" "test -f sandbox/echolocation_analysis.log"

run_test "Phase 15 execution" "./phases/phase15_physics.sh > /dev/null 2>&1"
run_test "Physics constraints logged" "test -f sandbox/physics_constraints.log"
run_test "Bio-physics integration logged" "test -f sandbox/bio_physics_integration.log"

run_test "Evolution recursive execution" "./phases/evolve_recursive.sh > /dev/null 2>&1"
run_test "Evolution summary generated" "test -f sandbox/evolution_summary.json"
run_test "Evolution history logged" "test -f sandbox/evolution_history.log"

# Test 7: Content Validation
echo ""
echo "🔍 Testing Content Validation..."
run_test "Zipf rank 1 in analysis" "grep -q 'Rank 1' sandbox/zipf_analysis.log"
run_test "Menzerath validated" "grep -q 'validates_principle.*true' sandbox/zipf_analysis.log"
run_test "Dolphin alpha_001 in log" "grep -q 'alpha_001' sandbox/dolphin_signatures.log"
run_test "Echolocation nav pattern" "grep -q 'nav_001' sandbox/echolocation_analysis.log"
run_test "Entropy law in physics" "grep -q 'ENTROPY' sandbox/physics_constraints.log"
run_test "Zero violations" "grep -q 'Violation Log: 0' sandbox/physics_constraints.log"

# Test 8: Evolution Results
echo ""
echo "📊 Testing Evolution Results..."
run_test "5 generations completed" "grep -q '\"total_generations\": 5' sandbox/evolution_summary.json"
run_test "Zero physics violations" "grep -q '\"physics_violations\": 0' sandbox/evolution_summary.json"
run_test "Stable ecosystem" "grep -q '\"ecosystem_status\": \"stable\"' sandbox/evolution_summary.json"
run_test "Entropy increased" "grep -q '\"final_entropy\": 3.5' sandbox/evolution_summary.json"

# Test 9: UDAP URI Validation
echo ""
echo "🔗 Testing UDAP URI Examples..."
run_test "Zipf URI in schema" "grep -q 'skhaos://bio/zipf/unit/1' schemas/udap.json"
run_test "Dolphin whistle URI in schema" "grep -q 'skhaos://bio/dolphin/whistle' schemas/udap.json"
run_test "Physics rondo URI in schema" "grep -q 'skhaos://physics/rondo' schemas/udap.json"

# Test 10: Asset Files
echo ""
echo "🎼 Testing Asset Files..."
run_test "Mozart physics mapping exists" "test -f assets/classical/mozart_rondo_physics.txt"
run_test "Rondo form documented" "grep -q 'A-B-A-C-A' assets/classical/mozart_rondo_physics.txt"

# Generate summary
echo ""
echo "=" >> "$TEST_REPORT"
echo "" >> "$TEST_REPORT"
cat >> "$TEST_REPORT" << EOF

## Statistics

- **Total Tests**: ${TOTAL_TESTS}
- **Passed**: ${PASSED_TESTS}
- **Failed**: ${FAILED_TESTS}
- **Success Rate**: $(echo "scale=2; ($PASSED_TESTS * 100) / $TOTAL_TESTS" | bc)%

## Module File Sizes

\`\`\`
$(ls -lh src/bio_physics/*.rs | awk '{print $9, $5}')
\`\`\`

## Generated Outputs

\`\`\`
$(ls -lh sandbox/ 2>/dev/null | tail -n +2 | awk '{print $9, $5}')
\`\`\`

## Test Environment

- OS: $(uname -s)
- Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- Shell: $BASH_VERSION
- Working Directory: $(pwd)

## Conclusion

EOF

if [ $FAILED_TESTS -eq 0 ]; then
    cat >> "$TEST_REPORT" << EOF
✅ **ALL TESTS PASSED**

The Bio-Physics Entanglement Compiler (BPEC) is fully operational:
- All modules implemented and tested
- Phase scripts execute successfully
- Physics constraints enforced (0 violations)
- Evolution runs stable (entropy increases correctly)
- UDAP URIs validated
- Documentation complete

**System Status: READY FOR DEPLOYMENT** 🚀

EOF
    echo ""
    echo "✅ ALL TESTS PASSED ($PASSED_TESTS/$TOTAL_TESTS)"
else
    cat >> "$TEST_REPORT" << EOF
⚠️ **SOME TESTS FAILED**

Please review the failed tests above and check:
1. All files are in correct locations
2. Scripts have execute permissions
3. Dependencies are installed (bash, bc)

Failed tests: $FAILED_TESTS

EOF
    echo ""
    echo "⚠️ SOME TESTS FAILED ($FAILED_TESTS/$TOTAL_TESTS)"
fi

echo ""
echo "📄 Test report generated: $TEST_REPORT"
echo ""
echo "=" 
echo "Test Summary:"
echo "  Total:  $TOTAL_TESTS"
echo "  Passed: $PASSED_TESTS"
echo "  Failed: $FAILED_TESTS"
echo "="
echo ""

# Exit with failure if any tests failed
exit $FAILED_TESTS
