# 🔥 FlameLang K8s Audit Log Transformation System

## Overview

The FlameLang K8s Audit Log Transformation System bridges Kubernetes operational events with FlameLang's behavioral DNA representation, enabling AI-driven analysis of controller patterns and anomaly detection.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                   FLAMELANG TRANSFORMATION SYSTEM                 │
├──────────────────────────────────────────────────────────────────┤
│  Layer 4: Interview Harness                                      │
│  ├── Test Cases & Scoring                                        │
│  ├── Candidate Evaluation                                        │
│  └── Challenge Generation                                        │
├──────────────────────────────────────────────────────────────────┤
│  Layer 3: Transformation Pipeline                                │
│  ├── CSV/JSON Parsers                                           │
│  ├── Batch Processing                                           │
│  └── Export (JSON/YAML/Text)                                    │
├──────────────────────────────────────────────────────────────────┤
│  Layer 2: DNA Extraction Engine                                 │
│  ├── Temporal Sequencing                                        │
│  ├── Gene Identification                                        │
│  ├── Pattern Recognition (heartbeat, mutation, scaling)         │
│  └── Anomaly Scoring                                            │
├──────────────────────────────────────────────────────────────────┤
│  Layer 1: Codon Mapping Schema                                  │
│  ├── K8s API Method → Genetic Codon Mapping                     │
│  ├── 20 Codon Definitions (UUA, GCU, AUG, etc.)                │
│  ├── 7 Behavioral Categories                                    │
│  └── Interview Question Mappings                                │
└──────────────────────────────────────────────────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Install dependencies (if needed)
pip install pyyaml  # Only external dependency

# Run tests
python3 tests/test_flamelang_system.py
```

## Quick Start

### 1. Transform Audit Logs

```python
from src.flamelang.transformation_pipeline import process_logs

# Process CSV or JSON audit logs
dna_profiles = process_logs(
    input_file="data/sample_gke_audit_logs.csv",
    output_dir="output",
    export_formats=['json', 'yaml', 'text']
)

# Access individual profiles
for principal, dna in dna_profiles.items():
    print(f"{principal}: {dna.total_events} events, {len(dna.genes)} genes")
```

### 2. Map K8s Operations to Codons

```python
from src.flamelang.codon_mapping import get_codon_for_method

# Map K8s methods to genetic codons
codon = get_codon_for_method("leases.update")
print(f"leases.update → {codon}")  # Output: UUA

codon = get_codon_for_method("configmaps.update")
print(f"configmaps.update → {codon}")  # Output: GCU

codon = get_codon_for_method("pods.create")
print(f"pods.create → {codon}")  # Output: AUG (START codon)
```

### 3. Extract Behavioral DNA

```python
from src.flamelang.dna_extraction import DNAExtractor, format_dna_profile

extractor = DNAExtractor(window_size=10, min_gene_length=3)

# Add events from parsed logs
extractor.add_events_from_dict(events)

# Extract DNA profile for a principal
dna = extractor.extract_dna_profile('controller@k8s.io')

# Print formatted profile
print(format_dna_profile(dna, verbose=True))
```

### 4. Run Interview Tests

```python
from src.flamelang.interview_harness import InterviewHarness

harness = InterviewHarness()

# Run all test cases
results = harness.run_all_tests()

# Print results
harness.print_results(results)

# Generate challenge file for candidates
harness.generate_challenge_file("output/challenge.json")
```

## Codon Mapping Table

### Coordination Operations (Lease Management)
| Codon | K8s Method | Description | Frequency |
|-------|------------|-------------|-----------|
| UUA | leases.update | Leader election heartbeat | 2.0x |
| UUG | leases.get | Lease read operation | 1.0x |
| CUU | leases.create | Initial leader election | 1.0x |

### Configuration Operations (ConfigMap/Secret)
| Codon | K8s Method | Description | Frequency |
|-------|------------|-------------|-----------|
| GCU | configmaps.update | Configuration mutation | 1.5x |
| GCC | configmaps.get | Configuration read | 1.0x |
| GCA | configmaps.create | Configuration creation | 1.0x |
| UCU | secrets.get | Secret read | 1.0x |
| UCC | secrets.update | Secret rotation | 1.0x |

### Orchestration Operations (Pod/Deployment)
| Codon | K8s Method | Description | Frequency |
|-------|------------|-------------|-----------|
| AUG | pods.create | Pod initiation (START) | 1.8x |
| UAA | pods.delete | Pod termination (STOP) | 1.0x |
| CCU | pods.update | Pod state change | 1.0x |
| CCA | pods.patch | Pod modification | 1.0x |
| GAU | deployments.update | Deployment scaling | 1.0x |

### Authorization Operations (RBAC)
| Codon | K8s Method | Description | Frequency |
|-------|------------|-------------|-----------|
| CGU | authorization.k8s.io | RBAC check | 1.3x |
| CGC | rbac.allow | Access granted | 1.0x |
| CGA | rbac.deny | Access denied | 1.0x |

## Behavioral Patterns

The system recognizes the following behavioral patterns in gene sequences:

### 1. Heartbeat Pattern
**Characteristics:** Repeated coordination codons (UUA)
**Example:** `UUA-UUA-UUA-UUA`
**Meaning:** Controller maintaining leader election lease

### 2. Mutation Pattern
**Characteristics:** Configuration change codons (GCU, GCA, UCC)
**Example:** `GCC-GCU-GCU-UCC`
**Meaning:** Configuration or secret modifications

### 3. Scaling Pattern
**Characteristics:** Orchestration START/STOP codons (AUG, UAA)
**Example:** `AUG-CCU-CCU-UAA`
**Meaning:** Pod lifecycle operations (create → update → delete)

### 4. Control Loop Pattern
**Characteristics:** Mix of coordination and orchestration
**Example:** `UUA-CCU-UUA-GAU-UUA`
**Meaning:** Controller reconciliation loop

### 5. Unknown/Anomaly Pattern
**Characteristics:** Unusual or unexpected codon combinations
**Example:** `UCU-UCU-UCU-CGA-CGA`
**Meaning:** Potential security issue (repeated secret access denials)

## Interview Question Mappings

The system maps behavioral patterns to specific interview questions:

| Question | Topic | Log Pattern | Codon Categories |
|----------|-------|-------------|------------------|
| Q2 | PID-RANCO control loops | Lease coordination patterns | Coordination |
| Q3 | Multi-AI ratification | RBAC authorization chains | Authorization |
| Q5 | Echo ping anomaly detection | ConfigMap mutation patterns | Configuration |
| Q7 | Mutation engines | Principal actions over time | Mutation, Configuration |
| Q9 | Red/Blue/Purple team | Cluster topology | Authorization, Orchestration |
| Q16 | Chaos-resilient models | Failure/recovery patterns | Coordination, Orchestration |
| Q17 | Evolutionary mutation | Change frequency patterns | Mutation |
| Q18 | Anomaly vectorization | Deviation from baseline | Configuration, Mutation |
| Q21 | Consensus mechanisms | Leader election patterns | Coordination |
| Q29 | Adversarial defenses | Anomalous access attempts | Authorization |

## Data Format

### Input: K8s Audit Log CSV
```csv
timestamp,protoPayload.authenticationInfo.principalEmail,protoPayload.methodName,resource.labels.cluster_name,resource.type,labels.authorization.k8s.io/reason
2024-01-15T08:00:00Z,system:kube-controller-manager@k8s.io,io.k8s.coordination.v1.leases.update,red-team,k8s_lease,RBAC: allowed
```

### Input: K8s Audit Log JSON
```json
{
  "timestamp": "2024-01-15T08:00:00Z",
  "protoPayload": {
    "authenticationInfo": {
      "principalEmail": "system:kube-controller-manager@k8s.io"
    },
    "methodName": "io.k8s.coordination.v1.leases.update"
  },
  "resource": {
    "type": "k8s_lease",
    "labels": {
      "cluster_name": "red-team"
    }
  }
}
```

### Output: Behavioral DNA Profile
```yaml
flamelang_version: '1.0.0'
behavioral_dna:
- principal: system:kube-controller-manager@k8s.io
  clusters:
  - red-team
  total_events: 16
  anomaly_score: 0.094
  dominant_behaviors:
  - coordination
  - configuration
  codon_frequency:
    UUA: 10
    GCU: 4
    GGA: 2
  genes:
  - sequence: UUA-UUA-UUA-UUA-UUA-GCU-UUA-GGA-UUA-UUA
    pattern: heartbeat
    cluster: red-team
    events: 10
```

## CLI Usage

### Transform Logs
```bash
# Process CSV file
python3 src/flamelang/transformation_pipeline.py data/sample_gke_audit_logs.csv output/

# Process JSON file
python3 src/flamelang/transformation_pipeline.py data/sample_k8s_audit_events.json output/
```

### View Codon Mapping
```bash
python3 src/flamelang/codon_mapping.py
```

### Run Tests
```bash
# Run all system tests
python3 tests/test_flamelang_system.py

# Run interview harness
python3 -c "from src.flamelang.interview_harness import InterviewHarness; h = InterviewHarness(); h.print_results(h.run_all_tests())"
```

## Example Output

### DNA Profile Text Output
```
================================================================================
🧬 BEHAVIORAL DNA PROFILE: system:kube-controller-manager@k8s.io
================================================================================

Clusters: red-team
Total Events: 16
Time Span: 2024-01-15T08:00:00+00:00 to 2024-01-15T08:09:00+00:00
Anomaly Score: 0.094

Dominant Behavior Categories:
  1. coordination
  2. configuration
  3. discovery

Codon Frequency (Top 10):
  UUA:   10 (62.50%)
  GCU:    4 (25.00%)
  GGA:    2 ( 6.25%)
  ACU:    1 ( 6.25%)

Genes Extracted: 2

Pattern Distribution:
  heartbeat: 2

================================================================================
```

## Testing

The system includes comprehensive tests:

1. **Codon Mapping Tests** - Verify K8s method → codon mappings
2. **DNA Extraction Tests** - Validate behavioral pattern recognition
3. **Pipeline Tests** - End-to-end transformation testing
4. **Interview Harness Tests** - Candidate evaluation framework

Run all tests:
```bash
python3 tests/test_flamelang_system.py
```

## Interview Challenge

Candidates receive:
1. Raw K8s audit logs (CSV/JSON)
2. FlameLang specification
3. Expected output format

They must:
1. Map K8s operations to FlameLang codons
2. Extract behavioral DNA sequences
3. Identify patterns (heartbeat, mutation, scaling, etc.)
4. Calculate anomaly scores

Scoring:
- Codon mapping accuracy: 40%
- Pattern recognition: 40%
- DNA extraction completeness: 20%
- Passing score: 70%

## Directory Structure

```
.
├── src/flamelang/
│   ├── __init__.py                    # Package exports
│   ├── codon_mapping.py               # K8s → Codon mapping schema
│   ├── dna_extraction.py              # Behavioral DNA extraction
│   ├── transformation_pipeline.py     # End-to-end pipeline
│   └── interview_harness.py           # Test framework
├── data/
│   ├── sample_gke_audit_logs.csv     # Sample CSV data
│   └── sample_k8s_audit_events.json  # Sample JSON data
├── tests/
│   └── test_flamelang_system.py      # System tests
├── output/                            # Generated output files
└── FLAMELANG_K8S_GUIDE.md            # This file
```

## License

Part of the Strategickhaos Sovereignty Architecture.
© 2024 Strategickhaos DAO LLC

## Contributing

This system is designed for interview and evaluation purposes. For enhancements or bug reports, contact the Strategickhaos team.

---

🔥 **Trust nothing until it survives 100-angle crossfire.** 🔥
