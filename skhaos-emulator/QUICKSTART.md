# Quick Start Guide - SkhaOS BPEC

## Prerequisites
- Bash shell
- Basic utilities: bc, date

## Installation

```bash
# Clone repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-/skhaos-emulator
```

## Running the System

### Phase-by-Phase Deployment

```bash
# Phase 13: Deploy Zipf Analyzer
./phases/phase13_zipf.sh
# Output: Zipf distribution analysis, Menzerath validation, quantum priority mapping

# Phase 14: Deploy Dolphin Communication
./phases/phase14_dolphin.sh
# Output: Signature whistles, echolocation clicks, pod dialects

# Phase 15: Deploy Physics DOM
./phases/phase15_physics.sh
# Output: 4 physics laws enforced, bio-physics integration complete

# Recursive Evolution (5 generations)
./phases/evolve_recursive.sh
# Output: Bio-physics mutations with constraint enforcement
```

### Quick Test Run

```bash
# Run all phases in sequence
for phase in phases/phase*.sh; do
    echo "Running $phase..."
    $phase
    echo ""
done

# Then run evolution
./phases/evolve_recursive.sh
```

## Expected Outputs

### Sandbox Files
After running all phases, check `sandbox/` directory:
- `zipf_analysis.log` - Zipf distribution rankings
- `dolphin_signatures.log` - Signature whistle patterns
- `echolocation_analysis.log` - Click burst data
- `bio_physics_integration.log` - Cross-domain mappings
- `physics_constraints.log` - Law enforcement results
- `evolution_log.json` - Latest generation state
- `evolution_summary.json` - Final statistics
- `evolution_history.log` - Detailed mutation log

### Key Metrics to Observe

1. **Zipf Rankings**: Rank 1 should have highest occurrence
2. **Menzerath Validation**: High frequency → shorter duration
3. **Physics Violations**: Should always be 0
4. **Entropy**: Should increase across generations (1.0 → 3.5)
5. **Fitness**: Should increase (conservation + entropy balance)

## Understanding UDAP URIs

### Whale Zipf Pattern
```
skhaos://bio/zipf/unit/1?law=entropy&hz=20
         │    │    │    │  │          └─ Frequency in Hz
         │    │    │    │  └─ Physics law constraint
         │    │    │    └─ Zipf rank (1 = most frequent)
         │    │    └─ Pattern type (unit/phrase/moan)
         │    └─ Bio category (zipf/dolphin)
         └─ Domain (bio/physics/music)
```

### Dolphin Signature Whistle
```
skhaos://bio/dolphin/whistle?signature=true&pod=matrilineal_a&hz=10000
```

### Physics-Constrained Music
```
skhaos://physics/rondo/law=conservation&hz=10
```

## Interpreting Evolution Results

### Successful Generation
```
Generation 1/5
🐬 Step 1: Mutating dolphin dialects...
   Mutation rate: .1
   ✅ 2 signatures mutated

⚛️ Step 2: Enforcing physics constraints...
   Entropy: 1.0 → 1.5
   ✅ 2nd Law satisfied (entropy increased)
   ✅ Energy conserved

🎵 Step 3: Entangling with Mozart Rondo...
   ✅ Classical-bio entanglement active

📈 Step 5: Calculating evolutionary fitness...
   Fitness score: 2.500
```

**Good signs:**
- ✅ checkmarks on all constraints
- Entropy increasing (1.0 → 1.5)
- Energy delta < tolerance
- Fitness score positive and increasing

### Failed Generation (would appear as)
```
⚛️ Step 2: Enforcing physics constraints...
   Entropy: 2.0 → 1.5
   ❌ 2nd Law violated (entropy decreased)
   Reverting mutation...
```

**What this means:**
- Mutation violated 2nd law of thermodynamics
- System automatically reverts to previous state
- Evolution halts to prevent unstable mutations

## Customizing Evolution

Edit `phases/evolve_recursive.sh` to adjust:

### Number of Generations
```bash
MAX_GENERATIONS=10  # Default is 5
```

### Mutation Rate
```bash
MUTATION_RATE=$(echo "scale=3; 0.2 * $GENERATION" | bc)  # Increase from 0.1
```

### Energy Tolerance
```bash
if (( $(echo "$ENERGY_DELTA < 0.5" | bc -l) )); then  # Increase from 0.1
```

## Viewing Results

### Evolution Summary
```bash
cat sandbox/evolution_summary.json | jq '.'
```

### Latest Generation State
```bash
cat sandbox/evolution_log.json | jq '.mutations'
```

### Physics Constraint Log
```bash
grep "✅\|❌" sandbox/physics_constraints.log
```

### Zipf Distribution
```bash
cat sandbox/zipf_analysis.log | grep "Rank"
```

## Troubleshooting

### Scripts not executable
```bash
chmod +x phases/*.sh
```

### bc not found
```bash
# Ubuntu/Debian
sudo apt-get install bc

# Alpine
apk add bc
```

### Empty sandbox directory
The sandbox files are generated when you run the phase scripts. Run phase13, phase14, and phase15 first.

## Advanced: Container Deployment

```bash
# Build container
podman build -f containers/Podmanfile -t skhaos-bpec:latest .

# Run in isolated pod
podman play kube containers/bio_physics.pod

# Execute phases inside container
podman exec bio-physics-pod-bpec-simulator /workspace/phases/phase13_zipf.sh
```

## Next Steps

1. **Expand Species**: Add more whale types (pilot, beluga)
2. **Add Music Forms**: Implement fugue, sonata, variation
3. **MIDI Export**: Convert evolved patterns to playable music
4. **Visualization**: Plot Zipf distributions, entropy trajectories
5. **Scale Up**: Larger pod populations, more generations

## References

- `README.md` - Complete system overview
- `CLI_COMMANDS.md` - 42-command reference
- `schemas/udap.json` - URI specification
- `schemas/flamelang.dsl` - DSL syntax guide

---

**Need help?** Check the logs in `sandbox/` for detailed execution traces.
