#!/bin/bash
# Example: Run the Neuralink Infusion Pipeline
# Demonstrates complete TRIG6 SAGCO-OS BCI simulation workflow

set -e  # Exit on error

echo "=========================================="
echo "Neuralink Infusion Pipeline Demo"
echo "TRIG6 SAGCO-OS Brain-Computer Interface"
echo "=========================================="
echo ""

# Check dependencies
echo "[1/4] Checking dependencies..."
if ! python3 -c "import numpy, scipy, sklearn, yaml" 2>/dev/null; then
    echo "Installing required Python packages..."
    pip3 install numpy scipy scikit-learn pyyaml
else
    echo "✓ All dependencies installed"
fi
echo ""

# Run the pipeline
echo "[2/4] Running Neuralink infusion pipeline..."
python3 neuralink_runner.py --config neuralink_infusion_pipeline.yaml
echo ""

# Display results
echo "[3/4] Pipeline Results:"
echo "----------------------------------------"

if [ -f "artifacts/neuralink_infusion/pipeline_summary.json" ]; then
    echo "✓ Pipeline completed successfully!"
    echo ""
    
    # Extract key metrics using Python
    python3 << 'EOF'
import json
with open('artifacts/neuralink_infusion/pipeline_summary.json', 'r') as f:
    summary = json.load(f)
    
print(f"Status: {summary['status']}")
print(f"Duration: {summary['duration_seconds']:.2f} seconds")
print(f"Fitness: {summary['fitness']:.4f}")
print("")
print("TRIG6 Metrics:")
print(f"  Resonance (R): {summary['metrics']['resonance']:.3f}")
print(f"  Drift (D):     {summary['metrics']['drift']:.3f}")
print(f"  Noise (N):     {summary['metrics']['noise']:.3f}")
print(f"  Equilibrium:   {summary['metrics']['equilibrium']:.3f}")
print(f"  Danger:        {summary['metrics']['danger']}")
print("")
print("Neural Characteristics:")
print(f"  Phase Lock:    {summary['metrics']['neural_phase_lock']:.4f}")
print(f"  Coherence:     {summary['metrics']['coherence_mean']:.4f}")
print(f"  Att. Drift:    {summary['metrics']['attention_drift']:.4f}")
print(f"  Burst Var:     {summary['metrics']['burst_variance']:.1f}")
EOF
else
    echo "✗ Pipeline failed - check logs"
    exit 1
fi

echo ""
echo "[4/4] Generated Artifacts:"
echo "----------------------------------------"
echo "Neural Data:     artifacts/neuralink_infusion/neural_data.npy"
echo "Anomalies:       artifacts/neuralink_infusion/anomalies.json"
echo "Glyphs:          artifacts/neuralink_infusion/glyphs/"
echo "Symbols:         artifacts/neuralink_infusion/symbols/"
echo "TRIG6 Report:    artifacts/neuralink_infusion/binding/trig6_report.json"
echo "Champion Map:    artifacts/neuralink_infusion/binding/symbol_to_codon_champion.json"
echo "Codon Streams:   artifacts/neuralink_infusion/binding/codon_streams/"
echo ""

echo "=========================================="
echo "Demo Complete! 🧬🧠🔥"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Review TRIG6 metrics in artifacts/neuralink_infusion/binding/trig6_report.json"
echo "2. Examine codon mappings in symbol_to_codon_champion.json"
echo "3. Explore neural augmentation codons in spec/codon_table_neuro_aug_v1.json"
echo "4. Read NEURALINK_INFUSION_README.md for full documentation"
echo ""
echo "For Dom - weaponize those bursts! 🔥🔥🔥"
