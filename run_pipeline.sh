#!/bin/bash
# Run the complete FlameBench → Guardian pipeline

set -e

echo "🔥 FlameLang Benchmark → Guardian Uncertainty Pipeline"
echo "========================================================"
echo ""

# Step 1: Run FlameBench
echo "📊 Step 1: Running FlameBench test harness..."
echo "------------------------------------------------------"
cd flamebench
python3 flamebench.py
cd ..
echo ""

# Step 2: Build Guardian (if not already built)
if [ ! -f "target/release/sagco-dom0d" ]; then
    echo "🔨 Building SAGCO Guardian (first time setup)..."
    echo "------------------------------------------------------"
    cargo build --release
    echo ""
fi

# Step 3: Run Guardian Analysis
echo "🛡️  Step 2: Running SAGCO Guardian analysis..."
echo "------------------------------------------------------"
./target/release/sagco-dom0d
echo ""

echo "✅ Pipeline complete!"
echo ""
echo "📝 Results:"
echo "   - Benchmark data: bench_cache/results.json"
echo "   - Guardian analysis: (printed above)"
