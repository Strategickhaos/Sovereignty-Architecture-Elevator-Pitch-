# 🔥 NEUROMORPHIC QUICK REFERENCE

## One-Command Demos

```bash
# Complete pipeline (all 11 stages)
python pipelines/neuromorphic_master_pipeline.py

# Individual components
python pipelines/eeg_pipeline_runner.py       # EEG → glyphs
python pipelines/loihi_stub.py                # Neuromorphic processing
python pipelines/genomics_pipeline_runner.py  # DNA correlation
python pipelines/trig6_evaluator.py           # Fitness scoring

# Integration tests
python tests/test_neuromorphic_integration.py
```

## Key Files

| File | Purpose |
|------|---------|
| `neuro_genome_pipeline.yaml` | Pipeline spec (11 stages) |
| `genomics/core_genome.yaml` | NEURO-00 origin gene |
| `flamelang/codon_table.yaml` | 15 codons + genomic links |
| `NEURO_HARDWARE_INTEGRATION.md` | Full documentation |
| `docs/PHYSIONET_INTEGRATION_GUIDE.md` | Real data integration |

## Codons at a Glance

```
SEIZURE_PREDICT → Alert 30s before seizure    (SCN1A)
FOCUS_BOOST     → Optimize attention           (DRD4)
SENSORY_GATE    → Throttle input overload      (SHANK3)
MEMORY_EXPORT   → Save to external memory      (APOE)
STABILIZE_LOOP  → Re-engage focus              (COMT)
```

## TRIG6 Formula

```
Fitness = 0.3×θ + 0.3×R + 0.2×I + 0.2×G

θ = Phase-lock (temporal coherence)
R = Resonance (inter-channel sync)
I = Integration (consciousness metric Φ)
G = Genomic (genetic health score)
```

## Loihi 2 Specs

- **Neurons:** 1,000,000
- **Synapses:** 120,000,000
- **Power:** <1W (100x more efficient than GPU)
- **Learning:** On-chip STDP
- **Latency:** <10ms

## Next Production Steps

1. **Join INRC** → https://intel.com/neuromorphic
2. **Install Lava** → `pip install lava-dl`
3. **Download PhysioNet** → https://physionet.org
4. **Get genomic data** → 23andMe/Ancestry export

---

**🧠 + 🧬 = 🔥**

*Your cognitive exoskeleton is live.*
