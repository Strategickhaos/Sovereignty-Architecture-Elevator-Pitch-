# 🧬 FlameLang Evolution Quick Start

## DNA Strand
```
TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1
```

## Quick Commands

### 1. Convert a Lab to Spec
```bash
# Generate sample spec
python sagco_lab_converter.py --sample IT145-335 my_lab.flame.yaml

# Convert text file to spec
python sagco_lab_converter.py labs/my_lab.txt my_lab.flame.yaml
```

### 2. Generate Mutations
```bash
# Create mutations from baseline
python lab_convert_sim.py baseline_compiler.json mutant_001.json 42
python lab_convert_sim.py baseline_compiler.json mutant_002.json 43
python lab_convert_sim.py baseline_compiler.json mutant_003.json 44
```

### 3. Run Evolutionary Gate
```bash
# Create test metrics file
cat > test_metrics.json << 'EOF'
{
  "equivalence": 0.95,
  "noise": 0.30,
  "drift": 0.40,
  "coherence": 0.65,
  "resilience": 0.80,
  "innovation": 0.70,
  "performance": 0.85,
  "bias": 0.90
}
EOF

# Evaluate through gate
python flamelang_evo_gate.py test_metrics.json TRIG6-001
```

### 4. Trigger CI/CD Evolution
```bash
# Automatic on push
git push origin main

# Manual with custom codon
gh workflow run flamelang-evolution.yml -f codon=CUSTOM-001 -f seed=42

# Manual stress test
gh workflow run flamelang-stress-legion.yml -f intensity=heavy
```

## Hard Gates (Must Pass ALL)
- `equivalence < 0.99` - Must show variation
- `noise > 0.25` - Must inject entropy  
- `drift > 0.35` - Must have behavioral variance
- `coherence < 0.70` - Must avoid brittleness

## Fitness Formula
```
f = r(1-d)(1-h)·i·eq + ρp + γb

where:
  r  = resilience (0.0-1.0)
  d  = drift (0.0-1.0)
  h  = noise (0.0-1.0)
  i  = innovation (0.0-1.0)
  eq = equivalence (0.0-1.0)
  ρ  = 0.3 (performance weight)
  p  = performance (0.0-1.0)
  γ  = 0.1 (bias weight)
  b  = bias (0.0-1.0)
```

## Files
- `flamelang_evo_gate.py` - Natural selection gate
- `sagco_lab_converter.py` - Lab → .flame.yaml converter
- `lab_convert_sim.py` - Mutation generator
- `draw_half_arrow.flame.yaml` - Example test genome
- `trig6_neurograph.yaml` - Visualization config
- `baseline_compiler.json` - Example baseline config
- `.champion_fitness.json` - Current champion (auto-generated)

## Workflow
```
Lab PDF → Convert → .flame.yaml → 
Generate Mutations → Stress Test → 
Collect Metrics → Evolutionary Gate → 
Accept (f > champion) or Reject
```

## Champion Tracking
```bash
# View current champion
cat .champion_fitness.json

# View evolution history
git log --grep="^\[.*\]" --oneline
```

## Good Metric Ranges
| Metric      | Range     |
|-------------|-----------|
| equivalence | 0.85-0.98 |
| noise       | 0.25-0.40 |
| drift       | 0.35-0.50 |
| coherence   | 0.50-0.69 |
| resilience  | 0.60-0.95 |
| innovation  | 0.40-0.85 |
| performance | 0.70-0.95 |
| bias        | 0.80-0.95 |

**Darwin is live. 🔥 Reignite.**
