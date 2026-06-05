# FlameLang Evolution Gate - Integration Guide

## Quick Integration Steps

### 1. Prerequisites

Ensure you have Python 3.12+ installed:
```bash
python3 --version
```

### 2. Directory Structure Verification

Your repo should now have:
```
repo_root/
├── src/emulator/wave_cores/trig6/evo_gate/
│   ├── __init__.py
│   ├── flamelang_evo_gate.py
│   └── README.md
├── logs/
│   └── trig_layer.jsonl
├── stress_results.json
├── docs/EVOLUTIONARY_GATE.md
└── .github/workflows/
    └── flamelang-evolution.yml
```

### 3. Manual Testing

Test the gate with the sample data:

```bash
cd /path/to/repo
python src/emulator/wave_cores/trig6/evo_gate/flamelang_evo_gate.py \
  --candidate main \
  --champion champion.json
```

Expected output:
```
✅ ACCEPTED - No existing champion, establishing baseline
🏆 New champion saved: main (f=0.8429)
```

### 4. Integrate with Your Metrics Collection

#### Option A: Replace Sample Files

When you have actual FlameBench and TRIG6 systems running:

1. **FlameBench output** → `stress_results.json`
   ```bash
   python your_flamebench_script.py > stress_results.json
   ```

2. **TRIG6 metrics** → `logs/trig_layer.jsonl`
   ```bash
   python your_trig6_collector.py >> logs/trig_layer.jsonl
   ```

#### Option B: Update Workflow

Edit `.github/workflows/flamelang-evolution.yml`:

Replace the placeholder sections with your actual commands:

```yaml
- name: Run FlameBench
  run: |
    # Replace this with your actual FlameBench execution
    python sagco-benchmark.py
    # Ensure it writes to stress_results.json

- name: Run TRIG6 metrics collection
  run: |
    # Replace this with your actual TRIG6 metrics collection
    python trig6_collect_metrics.py
    # Ensure it appends to logs/trig_layer.jsonl
```

### 5. Data Format Requirements

#### FlameBench Output (`stress_results.json`)

Must include at minimum:
```json
{
  "p_success": 0.85,      // Required: float 0.0-1.0
  "equivalence": 0.995    // Required: float 0.0-1.0
}
```

Optional fields (for reference):
```json
{
  "total_atoms": 42,
  "passed_atoms": 36,
  "failed_atoms": 6,
  "benchmark_type": "flamebench",
  "timestamp": "2026-01-25T03:51:00Z"
}
```

#### TRIG6 Metrics (`logs/trig_layer.jsonl`)

Each line should be a JSON object with:
```json
{
  "resonance": 0.75,         // Required: float 0.0-1.0
  "drift": 0.05,             // Required: float 0.0-1.0
  "noise_entropy": 0.08,     // Required: float 0.0-1.0
  "invention_density": 0.65, // Required: float 0.0-1.0
  "phase_coherence": 0.82    // Required: float 0.0-1.0
}
```

The gate reads the **last line** for most recent metrics.

### 6. CI/CD Integration

The workflow will automatically run on:
- Pushes to `main` or `develop` branches
- Pull requests targeting `main` or `develop`
- Only when files in `src/**` or `benchmarks/**` change

To trigger manually:
```bash
git commit --allow-empty -m "Test evolutionary gate"
git push
```

Check GitHub Actions → "FlameLang Evolution" workflow.

### 7. Understanding Results

#### Success (Exit Code 0)
- Candidate becomes new champion
- `champion.json` is updated
- Workflow continues

#### Rejection (Exit Code 1)
- One of these occurred:
  - `equivalence < 0.99` (hard gate failure)
  - `fitness <= champion_fitness` (no improvement)
- `champion.json` remains unchanged
- Workflow fails (expected behavior)

### 8. Tuning the Fitness Function

Adjust weights to prioritize different aspects:

```bash
# Emphasize phase coherence more
python flamelang_evo_gate.py --candidate SHA --rho 0.3 --gamma 0.2

# Emphasize FlameBench performance more
python flamelang_evo_gate.py --candidate SHA --rho 0.15 --gamma 0.4
```

Default weights:
- `ρ` (rho) = 0.2 - phase coherence weight
- `γ` (gamma) = 0.3 - FlameBench weight

### 9. Monitoring Evolution

Track fitness over time:
```bash
# View current champion
cat champion.json

# View fitness history (if you commit champion.json)
git log -p champion.json
```

### 10. Troubleshooting

#### Gate always rejects
```bash
# Reset champion to allow new baseline
rm champion.json
python flamelang_evo_gate.py --candidate new-baseline --champion champion.json
```

#### Missing files
```bash
# Gate will use defaults if files missing
# Check output for warnings:
⚠️  TRIG6 log not found at logs/trig_layer.jsonl
   Using default neutral values
```

#### Verify data format
```bash
# Check FlameBench output
python -m json.tool stress_results.json

# Check TRIG6 log (last line)
tail -1 logs/trig_layer.jsonl | python -m json.tool
```

## Next Steps

1. ✅ Test with sample data (you've completed this)
2. 📝 Integrate your actual FlameBench script
3. 📝 Integrate your actual TRIG6 metrics collector
4. 📝 Update GitHub Actions workflow with real commands
5. 📝 Run first evolution cycle on actual code change
6. 📈 Monitor fitness improvements over time

## Additional Resources

- Full documentation: `docs/EVOLUTIONARY_GATE.md`
- Package README: `src/emulator/wave_cores/trig6/evo_gate/README.md`
- FlameLang spec: `FLAMELANG_SPECIFICATION.md`

## Support

If you encounter issues:
1. Check the gate output for specific error messages
2. Verify data file formats match requirements
3. Review the comprehensive documentation
4. Check GitHub Actions logs for CI/CD issues

Happy evolving! 🔥
