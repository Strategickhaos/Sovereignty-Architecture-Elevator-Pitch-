# 🔥 FlameLang K8s Audit Log Transformation

**Transform Kubernetes audit logs into FlameLang behavioral DNA sequences for AI-driven analysis and candidate interviews.**

## What is This?

This system provides the **bridge between K8s operational data and FlameLang's behavioral DNA representation**, solving the problem stated:

> "You've got 10K+ row CSV with flattened GKE audit logs, JSON with structured K8s audit events, and 22M+ log entries. **How do you transform these logs into FlameLang codons for interview questions?**"

**Answer:** This system does exactly that.

## Quick Demo

```bash
# Run the live demonstration
python3 demo_flamelang_system.py

# Transform your audit logs
python3 src/flamelang/transformation_pipeline.py data/sample_gke_audit_logs.csv output/

# Run tests
python3 tests/test_flamelang_system.py
```

## The Bridge: Logs → FlameLang → Interview Questions

| Log Property | FlameLang Concept | Interview Question |
|--------------|-------------------|-------------------|
| Principal actions over time | Behavioral DNA sequences | Q7, Q17 (mutation engines) |
| RBAC authorization chains | Multi-AI ratification trails | Q3, Q21 (consensus mechanisms) |
| Cluster topology (red-team/jarvis) | Red/Blue/Purple team methodology | Q9, Q29 (adversarial defenses) |
| Lease coordination patterns | PID-RANCO control loops | Q2, Q16 (chaos-resilient models) |
| ConfigMap mutations | Echo ping anomaly detection | Q5, Q18 (anomaly vectorization) |

## System Components

### 1. Codon Mapping Schema (`src/flamelang/codon_mapping.py`)
Maps K8s audit events to genetic codons:
- `leases.update` → `UUA` (Leucine - stable heartbeat)
- `configmaps.update` → `GCU` (Alanine - flexible mutation)
- `pods.create` → `AUG` (Methionine - START codon)
- `pods.delete` → `UAA` (Ochre - STOP codon)
- **20 total codons** across 7 behavioral categories

### 2. DNA Extraction Engine (`src/flamelang/dna_extraction.py`)
Sequences principal actions into behavioral "genes":
- Temporal sequencing of operations
- Pattern recognition (heartbeat, mutation, scaling, control_loop, anomaly)
- Anomaly scoring (0.0-1.0 scale)
- Cluster topology analysis

### 3. Transformation Pipeline (`src/flamelang/transformation_pipeline.py`)
End-to-end processing:
- CSV/JSON parsers for K8s audit logs
- Batch processing of large log files
- Export to JSON, YAML, and text formats
- Integration with DNA extraction

### 4. Interview Test Harness (`src/flamelang/interview_harness.py`)
Candidate evaluation framework:
- 4 test cases (heartbeat, mutation, scaling, anomaly)
- Automated scoring (40% codon accuracy, 40% pattern recognition, 20% completeness)
- 70% passing threshold
- Challenge file generation

## Data Format Examples

### Input: K8s Audit Log CSV
```csv
timestamp,protoPayload.authenticationInfo.principalEmail,protoPayload.methodName,resource.labels.cluster_name
2024-01-15T08:00:00Z,system:kube-controller-manager@k8s.io,io.k8s.coordination.v1.leases.update,red-team
```

### Output: Behavioral DNA YAML
```yaml
principal: system:kube-controller-manager@k8s.io
clusters: [red-team]
total_events: 16
anomaly_score: 0.094
dominant_behaviors: [coordination, configuration]
codon_frequency:
  UUA: 10
  GCU: 4
genes:
- sequence: UUA-UUA-UUA-UUA-UUA-GCU-UUA-GGA-UUA-UUA
  pattern: heartbeat
  events: 10
```

## Usage

### Transform Logs
```python
from src.flamelang.transformation_pipeline import process_logs

dna_profiles = process_logs(
    input_file="your_audit_logs.csv",
    output_dir="output",
    export_formats=['json', 'yaml', 'text']
)
```

### Map Codons
```python
from src.flamelang.codon_mapping import get_codon_for_method

codon = get_codon_for_method("leases.update")  # Returns: "UUA"
```

### Extract DNA
```python
from src.flamelang.dna_extraction import DNAExtractor

extractor = DNAExtractor()
extractor.add_events_from_dict(events)
dna = extractor.extract_dna_profile('controller@k8s.io')
```

### Run Interview Tests
```python
from src.flamelang.interview_harness import InterviewHarness

harness = InterviewHarness()
results = harness.run_all_tests()
harness.print_results(results)
```

## Sample Data Provided

- **CSV**: `data/sample_gke_audit_logs.csv` (37 events from 9 principals)
- **JSON**: `data/sample_k8s_audit_events.json` (7 events with full structure)
- **Clusters**: red-team, jarvis-swarm-personal-001
- **Principals**: kube-controller-manager, kube-scheduler, jarvis-ai, chaos-monkey, admin, etc.

## Interview Questions Mapped

The system maps to these interview questions:

- **Q2**: PID-RANCO control loops (lease coordination)
- **Q3**: Multi-AI ratification (RBAC chains)
- **Q5**: Echo ping anomaly detection (ConfigMap mutations)
- **Q7**: Mutation engines (principal behavioral DNA)
- **Q9**: Red/Blue/Purple team (cluster topology)
- **Q16**: Chaos-resilient models (failure/recovery patterns)
- **Q17**: Evolutionary mutation tracking (change frequency)
- **Q18**: Anomaly vectorization (baseline deviations)
- **Q21**: Consensus mechanisms (leader election)
- **Q29**: Adversarial defenses (unauthorized access)

## Test Results

```
✅ Codon mapping: 3/3 tests passed
✅ DNA extraction: Genes extracted, anomaly scored
✅ Transformation pipeline: 9 principals processed from 37 events
✅ Interview harness: 3/4 tests passed, 75% average score
```

## Documentation

- **Quick Start**: This README
- **Comprehensive Guide**: `FLAMELANG_K8S_GUIDE.md`
- **FlameLang Spec**: `FLAMELANG_SPECIFICATION.md`
- **Code Documentation**: Inline docstrings in all modules

## File Structure

```
├── src/flamelang/
│   ├── codon_mapping.py          # K8s → Codon mappings
│   ├── dna_extraction.py         # Behavioral DNA extraction
│   ├── transformation_pipeline.py # End-to-end pipeline
│   └── interview_harness.py      # Test framework
├── data/
│   ├── sample_gke_audit_logs.csv
│   └── sample_k8s_audit_events.json
├── tests/
│   └── test_flamelang_system.py
├── demo_flamelang_system.py      # Live demonstration
├── FLAMELANG_K8S_GUIDE.md        # Detailed documentation
└── README_FLAMELANG.md           # This file
```

## Key Features

✅ **20 Genetic Codons** mapped to K8s operations  
✅ **5 Behavioral Patterns** recognized (heartbeat, mutation, scaling, control_loop, anomaly)  
✅ **7 Behavioral Categories** (Coordination, Configuration, Orchestration, Authorization, Discovery, Storage, Mutation)  
✅ **10 Interview Questions** mapped to log patterns  
✅ **Anomaly Scoring** (0.0-1.0) for security analysis  
✅ **Multi-format Export** (JSON, YAML, text)  
✅ **Automated Testing** framework for candidates  
✅ **CSV & JSON Support** for audit logs  

## Execution Path (As Requested)

1. **Log → Codon Mapping** — K8s audit events mapped to FlameLang codons (UUA, GCU, AUG, etc.)
2. **Behavioral DNA Extraction** — Principal actions sequenced into "genes" representing controller behavior
3. **Interview Test Harness** — Candidates receive raw logs + FlameLang spec, must produce working transformations

## What Makes This Unique

This is the **first system to bridge K8s operational data with genetic-inspired behavioral modeling**:

- Uses biological analogies (START/STOP codons, amino acids) for intuitive understanding
- Enables AI-driven pattern recognition on infrastructure behavior
- Provides automated candidate evaluation for deep K8s + FlameLang knowledge
- Supports anomaly detection through behavioral DNA analysis

## License

Part of the Strategickhaos Sovereignty Architecture.  
© 2024 Strategickhaos DAO LLC

---

🔥 **Trust nothing until it survives 100-angle crossfire.** 🔥
