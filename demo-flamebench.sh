#!/bin/bash
# FlameBench Demo - Complete workflow demonstration
# DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1

set -e

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    FLAMEBENCH DEMO WORKFLOW                                   ║"
echo "║  DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1                 ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
RESULTS_DIR="results"
SEED=42

echo "📋 Configuration:"
echo "   Results Directory: $RESULTS_DIR"
echo "   Random Seed: $SEED"
echo ""

# Step 1: Run Python benchmark
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "STEP 1: Running FlameBench Python Benchmark"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

if [ ! -f "flamebench.py" ]; then
    echo "❌ Error: flamebench.py not found"
    exit 1
fi

python3 flamebench.py --output-dir "$RESULTS_DIR" --seed "$SEED"

echo ""
echo "✅ Benchmark complete"
echo ""

# Step 2: Check output files
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "STEP 2: Verifying Output Files"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

if [ -f "$RESULTS_DIR/flamebench-results.json" ]; then
    echo "✅ flamebench-results.json exists"
    SIZE=$(stat -f%z "$RESULTS_DIR/flamebench-results.json" 2>/dev/null || stat -c%s "$RESULTS_DIR/flamebench-results.json" 2>/dev/null)
    echo "   Size: $SIZE bytes"
else
    echo "❌ flamebench-results.json not found"
    exit 1
fi

if [ -f "$RESULTS_DIR/guardian-uncertainty.json" ]; then
    echo "✅ guardian-uncertainty.json exists"
    SIZE=$(stat -f%z "$RESULTS_DIR/guardian-uncertainty.json" 2>/dev/null || stat -c%s "$RESULTS_DIR/guardian-uncertainty.json" 2>/dev/null)
    echo "   Size: $SIZE bytes"
else
    echo "❌ guardian-uncertainty.json not found"
    exit 1
fi

echo ""

# Step 3: Build Rust loader (if not already built)
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "STEP 3: Building Rust Loader"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

if [ ! -d "flamebench_loader" ]; then
    echo "❌ Error: flamebench_loader directory not found"
    exit 1
fi

cd flamebench_loader

if [ ! -f "target/release/flamebench_loader" ]; then
    echo "🔨 Building Rust loader..."
    cargo build --release
    echo "✅ Build complete"
else
    echo "✅ Rust loader already built"
fi

cd ..
echo ""

# Step 4: Run Rust loader
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "STEP 4: Running Rust Uncertainty Loader"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

./flamebench_loader/target/release/flamebench_loader "$RESULTS_DIR"

echo ""

# Step 5: Show sample data
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "STEP 5: Sample Output Data"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

echo "📊 Overall Metrics (from flamebench-results.json):"
if command -v jq &> /dev/null; then
    jq '.overall' "$RESULTS_DIR/flamebench-results.json"
else
    echo "   (install jq for pretty printing)"
    grep -A 3 '"overall"' "$RESULTS_DIR/flamebench-results.json" | head -4
fi

echo ""
echo "📊 Top 3 Concepts (from guardian-uncertainty.json):"
if command -v jq &> /dev/null; then
    jq '.uncertainties[:3] | .[] | {tag: .tag, p_correct: .p_correct, entropy: .entropy}' "$RESULTS_DIR/guardian-uncertainty.json"
else
    echo "   (install jq for pretty printing)"
    head -30 "$RESULTS_DIR/guardian-uncertainty.json"
fi

echo ""

# Summary
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "DEMO COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "✅ All steps completed successfully"
echo ""
echo "📁 Output files:"
echo "   - $RESULTS_DIR/flamebench-results.json"
echo "   - $RESULTS_DIR/guardian-uncertainty.json"
echo ""
echo "🔥 Next Steps:"
echo "   1. Review results in $RESULTS_DIR/"
echo "   2. Integrate guardian-uncertainty.json with your guardian system"
echo "   3. Use fitness scores for DNA mutation decisions"
echo "   4. Add more capsules via GitHub gists or embedded code"
echo ""
echo "🧬 DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1"
echo ""
