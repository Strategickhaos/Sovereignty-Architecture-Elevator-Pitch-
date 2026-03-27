#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# DEMYSTIFIER DEMO - INV-091
# Quick demonstration of the Vibe-to-Interface Frequency Converter
# ═══════════════════════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "🔥 DEMYSTIFIER PIPELINE DEMO - INV-091"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Test 1: Identity claim
echo "Test 1: Identity Claim"
echo "─────────────────────"
npm run demystify -- "I am a lightworker"
echo ""

# Test 2: Destiny framing
echo "Test 2: Destiny Framing"
echo "─────────────────────"
npm run demystify -- "The universe wants me to succeed"
echo ""

# Test 3: Power claim
echo "Test 3: Power Claim"
echo "─────────────────────"
npm run demystify -- "I can manifest my dreams"
echo ""

# Test 4: Validation - already grounded
echo "Test 4: Validation (Grounded Statement)"
echo "─────────────────────────────────────"
npm run demystify -- --validate "I measured 432 Hz frequency"
echo ""

# Test 5: Validation - mystical
echo "Test 5: Validation (Mystical Statement)"
echo "─────────────────────────────────────"
npm run demystify -- --validate "I feel the vibrations"
echo ""

# Test 6: Batch processing
echo "Test 6: Batch Processing"
echo "────────────────────────"
npm run demystify -- --batch "I'm an empath" "Everything happens for a reason" "I have visions"
echo ""

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ Demo complete - Pipeline operational"
echo "═══════════════════════════════════════════════════════════════════════════════"
