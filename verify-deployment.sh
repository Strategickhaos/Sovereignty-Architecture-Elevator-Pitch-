#!/bin/bash
# SAGCO OS v0.1.0 - Deployment Verification Script
# Tests all deployment scenarios mentioned in the problem statement

set -e

echo "============================================================"
echo "SAGCO OS v0.1.0 - Deployment Verification"
echo "============================================================"
echo ""

# Test 1: Installation
echo "✓ Test 1: Installation"
echo "  Running: pip install -e \".[dev]\""
pip install -e ".[dev]" --quiet
echo "  ✓ Installation successful"
echo ""

# Test 2: Status Command
echo "✓ Test 2: Status Command"
echo "  Running: python -m src.core.sagco status"
python -m src.core.sagco status | head -10
echo "  ✓ Status command working"
echo ""

# Test 3: Version Command
echo "✓ Test 3: Version Command"
echo "  Running: python -m src.core.sagco version"
python -m src.core.sagco version
echo "  ✓ Version command working"
echo ""

# Test 4: Analysis Command
echo "✓ Test 4: Analysis Command"
echo "  Running: python -m src.core.sagco analyze \"explain create code\""
python -m src.core.sagco analyze "explain create code" | grep -A 10 "Activated Cognitive Layers"
echo "  ✓ Analysis working"
echo ""

# Test 5: JSON Output
echo "✓ Test 5: JSON Output"
echo "  Running: python -m src.core.sagco status --json"
python -m src.core.sagco status --json > /dev/null
echo "  ✓ JSON output working"
echo ""

# Test 6: Test Suite
echo "✓ Test 6: Test Suite"
echo "  Running: pytest tests/ -v"
pytest tests/ -q
echo "  ✓ All tests passing"
echo ""

echo "============================================================"
echo "✓ ALL DEPLOYMENT TESTS PASSED"
echo "============================================================"
echo ""
echo "SAGCO OS v0.1.0 is operational and ready for deployment!"
echo ""
echo "Next steps:"
echo "  1. GitHub Codespace: Push to GitHub and create a Codespace"
echo "  2. Local: Use 'python -m src.core.sagco' to run commands"
echo "  3. Tests: Use 'pytest tests/ -v' to run the test suite"
echo ""
