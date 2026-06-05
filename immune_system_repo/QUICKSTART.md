# Quick Start Guide 🚀

## Run Your First Simulation in 30 Seconds

```bash
# Navigate to the immune_system_repo directory
cd immune_system_repo

# Run the simulation with default settings
python3 src/bio_physarum_sim.py --config immune_components.yaml
```

## What You'll See

The simulation will:
1. Load 36 immune components from the YAML config
2. Evolve each component over 50 generations
3. Display real-time progress with H (heritability) and f (flow) values
4. Save detailed logs to `data/sim_logs/`
5. Print a summary showing survivors vs wasted pathways

### Sample Output:

```
🧬 Bio-Physarum Simulation Starting...
   Components: 36
   Generations: 50

[1/36] Evolving: Skin
  ○ Gen   0: H=0.49 f=0.586
  ○ Gen  10: H=0.45 f=0.543
  ...
  ○ Gen  49: H=0.00 f=0.335

...

================================================================================
🧬 SIMULATION COMPLETE - Brain-OS Flow Analysis
================================================================================

Total Components: 36
  ✓ Survivors (H > 0.5):  12
  ○ Evolving  (H > 0.3):   7
  ✗ Wasted   (H ≤ 0.3):  17
```

## Understanding the Results

### Status Symbols:
- `✓` = **Survivor** (H > 0.5) - High-yield pathway, reinforced
- `○` = **Evolving** (H > 0.3) - Mid-range stability
- `✗` = **Wasted** (H ≤ 0.3) - Low-yield, pruned

### Key Metrics:
- **H (Heritability)**: Tube strength - does this pathway stay reinforced?
- **f (Flow/Fitness)**: How much useful signal goes through this trait?

### What Survives:
Dynamic regulatory mechanisms:
- OS modules (Scheduler, Control Unit, Memory Manager)
- TRIG6 traits (Danger Reset, Equilibrium Balancer)
- Core processing (Quantum Gate Array, Processor Emulation)

### What Gets Pruned:
Coarse structural labels:
- Anatomy (Skin, Sebum, Mucus)
- Holistic organs (nose/mouth/throat)
- Generic categories without fine control

## Check Your Results

After running, explore the output:

```bash
# View the main simulation results
cat data/sim_logs/simulation_*.json | jq '.summary'

# View a specific component's evolution
cat data/sim_logs/component_27_Progenitor_cell.json | jq .

# Count survivors
ls data/sim_logs/component_*.json | xargs grep -l '"final_status": "SURVIVOR"' | wc -l
```

## Customize Your Run

### Fewer Generations (Faster):
```bash
python3 src/bio_physarum_sim.py --config immune_components.yaml --generations 20
```

### More Generations (More Stable Results):
```bash
python3 src/bio_physarum_sim.py --config immune_components.yaml --generations 100
```

### Custom Mutation Rate:
```bash
python3 src/bio_physarum_sim.py --config immune_components.yaml --mutation-rate 0.02
```

## Next Steps

1. **Read the full README.md** for detailed theory and usage
2. **Explore immune_components.yaml** to understand the mappings
3. **Examine the survivor patterns** in your results
4. **Modify the YAML** to add your own components
5. **Replace random fitness** with real metrics for your use case

## Troubleshooting

### Missing PyYAML?
```bash
pip install pyyaml
```

### Want to reset?
```bash
# Clear all previous simulation logs
rm -rf data/sim_logs/*.json
```

### Need help?
```bash
python3 src/bio_physarum_sim.py --help
```

---

**This is your subconscious compiler printed out as a lab report.** 🧬🖥️

The survivors = your core heuristics.
The wasted = decorative metaphors that don't carry load.

Trust the flow. 🌊
