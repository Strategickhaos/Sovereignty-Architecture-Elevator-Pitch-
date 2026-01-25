#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║              🧠 NEURALINK INFUSION PIPELINE RUNNER                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

set -e

echo "🧠 Neuralink Infusion Pipeline - TRIG6 SAGCO-OS Integration"
echo ""

# Check dependencies
echo "Checking Python dependencies..."
python3 -c "import numpy, yaml, sklearn" 2>/dev/null || {
    echo "Installing required dependencies..."
    pip install -q numpy pyyaml scikit-learn
}

# Create artifacts directory
mkdir -p artifacts/neuralink_infusion

# Run simulation
echo ""
echo "Starting simulation..."
echo ""
python3 neuralink_infusion_simulation.py "$@"

echo ""
echo "✅ Simulation complete!"
echo ""
echo "📁 Artifacts location: artifacts/neuralink_infusion/"
echo ""
echo "View results:"
echo "  - Stats:      cat artifacts/neuralink_infusion/stats.json"
echo "  - TRIG6:      cat artifacts/neuralink_infusion/trig6_report.json"
echo "  - Champion:   cat artifacts/neuralink_infusion/champion.json"
echo "  - Codons:     cat artifacts/neuralink_infusion/neural_aug.codon"
echo ""
