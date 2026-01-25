#!/bin/bash
#
# Quick Start Script for Loihi Neuromorphic Integration
# TRIG6 SAGCO-OS Neuralink Infusion Pipeline
#

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║          LOIHI NEUROMORPHIC INTEGRATION - QUICK START                    ║"
echo "║                  TRIG6 SAGCO-OS Neuralink Infusion                       ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Install dependencies (if needed)
echo ""
echo "Installing dependencies..."
pip install -q numpy scipy pyyaml 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "⚠ Warning: Some dependencies may already be installed"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "RUNNING INDIVIDUAL MODULES"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Module 1: EEG Processing
echo "1️⃣  Running EEG Processor..."
python3 loihi_eeg_processor.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ EEG data processed → data/processed/"
else
    echo "   ✗ Error processing EEG"
    exit 1
fi

# Module 2: Loihi SNN
echo "2️⃣  Running Loihi SNN Simulator..."
python3 loihi_snn_simulator.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Loihi SNN simulated → data/loihi/"
else
    echo "   ✗ Error running Loihi SNN"
    exit 1
fi

# Module 3: Genomics
echo "3️⃣  Running Genomics Reconstructor..."
python3 genomics_recon.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Genomics analyzed → data/genomics/"
else
    echo "   ✗ Error in genomics reconstruction"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "RUNNING FULL PIPELINE"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Full pipeline
echo "🚀 Running TRIG6 Integration Pipeline..."
echo ""
python3 trig6_runner.py

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo "SUCCESS! 🎉"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "📁 Output files generated:"
    echo ""
    find data -type f \( -name "*.json" -o -name "*.npy" -o -name "*.vcf" -o -name "*.txt" -o -name "*.py" \) 2>/dev/null | grep -v windows_dna | sort | sed 's/^/   /'
    echo ""
    echo "📚 Next Steps:"
    echo "   1. Read LOIHI_INTEGRATION.md for full documentation"
    echo "   2. Review TRIG6 metrics: data/trig6/eval_results.json"
    echo "   3. Check genomics report: data/genomics/neurogenetic_report.json"
    echo "   4. Examine pipeline results: data/pipeline_results.json"
    echo ""
    echo "🔬 To deploy to actual Loihi hardware:"
    echo "   - Apply to Intel INRC: https://intel.ly/neuromorphic"
    echo "   - Use generated Lava code: data/loihi/lava_eeg_network.py"
    echo ""
    echo "🧠🧬🔥 Bridging hardware brains to bio-code!"
else
    echo ""
    echo "✗ Pipeline failed. Check error messages above."
    exit 1
fi
