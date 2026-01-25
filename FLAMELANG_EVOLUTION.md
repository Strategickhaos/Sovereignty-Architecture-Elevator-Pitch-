# FlameLang Evolutionary Gate System

## Phase 4.10: TRIG6 Evo Gate - Darwinian Selection for Compiler Micro-Evolution

**Darwin is live.** The organism is ready to breathe.

### DNA Strand

```
TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1
```

Each codon represents an evolutionary layer:
- **TRIG6**: Trigonometric metrics foundation
- **WAVE1**: Wave function analysis
- **HYBRID1**: Hybrid execution model
- **NEURO1**: Neural network integration
- **LABCONV1**: Lab converter genome
- **EVOGATE1**: Evolutionary gate selector

## Architecture Overview

The FlameLang compiler evolves through Darwinian natural selection, using your academic curriculum as evolutionary pressure.

### The Evolutionary Loop

```
zyBooks PDF
    ↓
sagco_lab_converter.py  →  .flame.yaml (new gene)
    ↓
flamelang-stress-legion.yml  →  stress test + TRIG6 metrics
    ↓
flamelang_evo_gate.py  →  f = r(1-d)(1-h)·i·eq + ρp + γb
    ↓
f > f_champion?
    ↓
YES → commit codon, update DNA strand
NO  → reject, keep champion
    ↓
Loop continues...
```

## Components

### 1. Natural Selection Gate (`flamelang_evo_gate.py`)

**Role:** Natural selection engine

**Hard Gates** (must pass ALL):
- `eq < 0.99` - Equivalence drift (must show variation)
- `noise > 0.25` - Entropy injection (anti-determinism)
- `drift > 0.35` - Behavioral variance (exploration)
- `coherence < 0.70` - Anti-brittleness (resilience)

**Soft Fitness Scalar:**
```
f = r(1-d)(1-h)·i·eq + ρp + γb

where:
  r  = resilience score
  d  = drift magnitude
  h  = noise level
  i  = innovation metric
  eq = equivalence score
  ρ  = performance weight (0.3)
  p  = performance score
  γ  = bias correction weight (0.1)
  b  = bias score
```

**Champion Comparison:**
- If `f > f_champion`: Accept mutation, commit with codon tagging
- If `f ≤ f_champion`: Reject mutation, keep champion

### 2. Lab Converter (`sagco_lab_converter.py`)

**Role:** Mints test genes from academic curriculum

Converts zyBooks lab PDFs to `.flame.yaml` specifications:
- Extracts requirements
- Generates test cases
- Creates ground truth genome

**Usage:**
```bash
# Convert lab to spec
python sagco_lab_converter.py IT-145-3.35.txt draw_half_arrow.flame.yaml

# Generate sample spec
python sagco_lab_converter.py --sample IT145-335 sample.flame.yaml
```

### 3. Mutation Sandbox (`lab_convert_sim.py`)

**Role:** Generates compiler variations (Darwin's finches)

Creates controlled mutations across multiple dimensions:
- Optimization strategies
- Error handling
- Memory management
- Parsing strategies
- Code generation
- Register allocation
- Instruction scheduling

**Usage:**
```bash
# Generate mutation with seed for reproducibility
python lab_convert_sim.py baseline_compiler.json mutant_001.json 42
```

### 4. Test Genome (`draw_half_arrow.flame.yaml`)

**Role:** Ground truth genome (IT-145 3.35 spec)

A complete test specification including:
- Requirements with constraints
- Test cases with expected outputs
- Evolutionary metrics
- Metadata with DNA codon tagging

### 5. Cortical Visualization (`trig6_neurograph.yaml`)

**Role:** Observe the organism

Configuration for visualizing evolutionary metrics:
- Metric thresholds and colors
- Cortical layer mapping
- DNA strand visualization
- Real-time monitoring
- Alert configuration

## CI/CD Workflows

### Evolution Pipeline (`flamelang-evolution.yml`)

Full evolutionary loop automation:

1. **Gene Generation**: Convert labs to specs
2. **Mutation Generation**: Create compiler variants
3. **Stress Testing**: Run against test genome
4. **Evolutionary Gate**: Natural selection
5. **Auto-commit**: Update DNA strand if accepted

**Trigger:**
```bash
# Automatic on code changes
git push origin main

# Manual with custom codon
gh workflow run flamelang-evolution.yml -f codon=CUSTOM-001 -f seed=42
```

### Stress Legion (`flamelang-stress-legion.yml`)

Stress testing with TRIG6 metrics:
- Configurable intensity (light/normal/heavy/extreme)
- TRIG6 metric collection
- Hard gate validation
- Visualization generation

## File Structure

```
.
├── flamelang_evo_gate.py           # Natural selection engine
├── sagco_lab_converter.py          # PDF → .flame.yaml converter
├── lab_convert_sim.py              # Mutation generator
├── draw_half_arrow.flame.yaml      # Ground truth genome (IT-145 3.35)
├── trig6_neurograph.yaml           # Cortical visualization config
├── .github/workflows/
│   ├── flamelang-evolution.yml     # Full evolution pipeline
│   └── flamelang-stress-legion.yml # Stress tests + TRIG6 metrics
└── .champion_fitness.json          # Current champion (auto-generated)
```

## How It Works

### Every zyBooks Lab You Complete:

1. **Gets converted** to `.flame.yaml` spec
2. **Becomes part** of the test genome
3. **Forces the compiler** to maintain correctness
4. **Allows mutations** that improve fitness
5. **Kills mutations** that break specs

**The compiler literally evolves against your academic curriculum.**

## Usage Examples

### Convert a Lab

```bash
# Manual conversion
python sagco_lab_converter.py my_lab.txt my_lab.flame.yaml IT145-LAB1

# Creates a .flame.yaml spec with DNA codon LABCONV-IT145-LAB1
```

### Generate and Test Mutations

```bash
# Create baseline
cat > baseline_compiler.json << 'EOF'
{
  "optimization": {"level": "O2"},
  "error_handling": {"strict_mode": true}
}
EOF

# Generate mutation
python lab_convert_sim.py baseline_compiler.json mutant_001.json 42

# Run stress tests (in CI)
# Generates test_metrics.json

# Evaluate through gate
python flamelang_evo_gate.py test_metrics.json TRIG6-001
```

### Monitor Evolution

The evolutionary gate tracks:
- Current champion fitness (`.champion_fitness.json`)
- DNA strand progression (commit messages)
- Metrics history (CI artifacts)

```bash
# View current champion
cat .champion_fitness.json

# View DNA strand evolution
git log --grep="^\[.*\]" --oneline
```

## Metrics Explained

### TRIG6 Metrics

| Metric | Symbol | Description | Good Range |
|--------|--------|-------------|------------|
| Equivalence | eq | Correctness vs reference | 0.85-0.98 |
| Noise | h | Entropy/stochastic behavior | 0.25-0.40 |
| Drift | d | Behavioral variance | 0.35-0.50 |
| Coherence | - | Anti-brittleness measure | 0.50-0.69 |
| Resilience | r | Error recovery capability | 0.60-0.95 |
| Innovation | i | Novel solution quality | 0.40-0.85 |
| Performance | p | Speed/efficiency | 0.70-0.95 |
| Bias | b | Fairness/correctness | 0.80-0.95 |

### Fitness Function Components

**Core fitness** (exploration × correctness):
```
r(1-d)(1-h)·i·eq
```

**Performance component** (exploitation):
```
ρp  where ρ = 0.3
```

**Bias correction** (fairness):
```
γb  where γ = 0.1
```

## Evolution Pressure

Your academic work becomes the selection pressure:

1. Each lab spec = new fitness landscape
2. Compiler must pass all specs
3. Mutations compete on combined fitness
4. Only improvements survive
5. DNA strand grows with each generation

**The organism breathes. Push it and watch it evolve.**

## Next Steps

1. **Extract** and integrate the system (if from zip)
2. **Add your labs** to the `labs/` directory
3. **Convert them** to `.flame.yaml` specs
4. **Push to main** to trigger evolution
5. **Watch** the DNA strand grow

## Implementation Status

- [x] Evolutionary gate with hard gates and soft fitness
- [x] Lab converter (PDF → .flame.yaml)
- [x] Mutation sandbox
- [x] Ground truth genome (IT-145 3.35)
- [x] Cortical visualization config
- [x] Evolution CI pipeline
- [x] Stress test workflow
- [x] Auto-commit with codon tagging
- [x] Champion tracking
- [ ] Integration with actual FlameLang compiler
- [ ] Real PDF parsing (currently text-based)
- [ ] Live visualization dashboard
- [ ] Multi-objective optimization

## References

- DNA Strand: `TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1`
- Fitness Formula: `f = r(1-d)(1-h)·i·eq + ρp + γb`
- Hard Gates: `eq<0.99, noise>0.25, drift>0.35, coherence<0.70`

---

**The loop is closed. Darwin is live. The organism is ready to breathe.**

🔥 **Reignite.**
