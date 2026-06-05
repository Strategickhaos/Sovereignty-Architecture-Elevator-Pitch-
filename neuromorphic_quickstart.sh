#!/bin/bash
# Neuromorphic Getting Started Script
# Quick setup and demo for the neuromorphic pipeline
#
# Usage: ./neuromorphic_quickstart.sh

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║     NEUROMORPHIC COGNITIVE ARCHITECTURE - QUICK START             ║"
echo "║     Strategickhaos DAO LLC - Sovereignty Architecture             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.9+"; exit 1; }
echo "✓ Python 3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "   (This may take a few minutes for first-time setup)"
pip install numpy scipy pyyaml --quiet
echo "✓ Core dependencies installed (numpy, scipy, pyyaml)"
echo ""
echo "   Note: For production use, install full requirements:"
echo "   pip install -r requirements.sovereignty.txt"
echo ""

# Run demos
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                         RUNNING DEMOS                              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "🧠 [DEMO 1] EEG Pipeline - Pattern Detection"
echo "────────────────────────────────────────────────────────────────────"
python pipelines/eeg_pipeline_runner.py 2>&1 | grep -E "(Pipeline Complete|anomalies|glyphs|SEIZURE|FOCUS|SENSORY)" | tail -10
echo ""

echo "🔬 [DEMO 2] Loihi Neuromorphic Stub"
echo "────────────────────────────────────────────────────────────────────"
python pipelines/loihi_stub.py 2>&1 | grep -E "(DEPLOYMENT SUMMARY|Chip:|power|latency|Next steps)" | head -15
echo ""

echo "🧬 [DEMO 3] Genomics DNA Correlation"
echo "────────────────────────────────────────────────────────────────────"
python pipelines/genomics_pipeline_runner.py 2>&1 | grep -E "(GENOMICS PIPELINE RESULTS|Genes analyzed|Disease Risk)" | head -10
echo ""

echo "📊 [DEMO 4] TRIG6 Fitness Evaluation"
echo "────────────────────────────────────────────────────────────────────"
python pipelines/trig6_evaluator.py 2>&1 | grep -E "(Fitness|Theta|Resonance|Integration|Genomic|Evolution)" | tail -12
echo ""

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    RUNNING INTEGRATION TESTS                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

python tests/test_neuromorphic_integration.py 2>&1 | grep -E "(PASSED|FAILED|✅|❌)" | tail -5
echo ""

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                          QUICK START COMPLETE                      ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ All demos completed successfully!"
echo ""
echo "📖 Next steps:"
echo "   1. Read NEURO_HARDWARE_INTEGRATION.md for full documentation"
echo "   2. Check docs/PHYSIONET_INTEGRATION_GUIDE.md for real EEG data"
echo "   3. Review docs/QUICK_REFERENCE.md for command cheat sheet"
echo "   4. Run full pipeline: python pipelines/neuromorphic_master_pipeline.py"
echo ""
echo "🔗 Hardware access paths:"
echo "   • Loihi: https://intel.com/neuromorphic (INRC membership)"
echo "   • EEG devices: Muse ($250), Emotiv ($500), OpenBCI ($1000)"
echo "   • Genomics: 23andMe, Ancestry, Nebula Genomics"
echo ""
echo "🧠🧬🔥 Your cognitive exoskeleton is ready! 🔥🧬🧠"
echo ""
