# SAGCO OS Quick Start Guide

## Prerequisites

- Rust toolchain (1.70+): `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- Python 3.8+: Pre-installed on most systems
- PyYAML: `pip install pyyaml`

## 5-Minute Setup

### 1. Build All Components

```bash
# From repository root
cargo build --release --workspace
```

This builds:
- `sagco-guardian` library + `sagco-oracle` binary
- `sagco-kernel` library
- `sagco-dna` binary

### 2. Create Example Guardian Export

```bash
# Create a test Guardian export file
cp benchmarks/guardian-uncertainty.example.json guardian-uncertainty.json

# Or create one with good metrics for testing mutation:
cat > guardian-uncertainty.json << 'EOF'
{
  "source": "flamebench",
  "dna_strand": "FLM2-CMD4-MESH5-ORB1",
  "uncertainties": [
    {
      "tag": "if-else",
      "p_correct": 0.96,
      "entropy": 0.25,
      "alpha": 48.0,
      "beta": 2.0,
      "sample_size": 50
    }
  ],
  "overall": {
    "p_success": 0.96,
    "entropy": 0.25
  }
}
EOF
```

### 3. Run sagco-mesh

```bash
python3 tools/sagco-mesh.py
```

Expected output:
```
SAGCO-MESH v1.0.0 - Network Discovery & Health Monitor
======================================================================
Scanning 5 host(s)...

NAME         IP               ROLE           STATE  SERVICES       
======================================================================
ATHENA       192.168.2.26     subconscious   DOWN   -              
LYRA         192.168.1.50     right_hemi     DOWN   -              
...
======================================================================
Mesh Health: 0/5 nodes online (0%)
```

(Nodes will be DOWN unless you're actually running them on those IPs)

### 4. Run sagco-oracle

```bash
# Analyze text input
echo "Test hallucination detection" | ./target/release/sagco-oracle
```

Expected output:
```
╔════════════════════════════════════════╗
║  SAGCO-ORACLE v1.0                     ║
║  Guardian Layer Analysis               ║
╚════════════════════════════════════════╝

FLM2 Compiler Health Report:
  Source: flamebench
  DNA Strand: FLM2-CMD4-MESH5-ORB1
  Overall Success: 96.0%
  Entropy: 0.250

Analyzing input: "Test hallucination detection"

[... geometry and safety classification ...]
```

### 5. Run sagco-dna

```bash
./target/release/sagco-dna
```

Expected output:
```
╔════════════════════════════════════════╗
║  SAGCO-DNA v1.0                        ║
║  DNA Strand Evolution Manager          ║
╚════════════════════════════════════════╝

Loading Guardian metrics from: guardian-uncertainty.json

Current DNA Strand: FLM2-CMD4-MESH5-ORB1
FLM2 Compiler Health:
  p_success = 0.960
  entropy   = 0.250

✓ Mutation suggested: FLM2-CMD4-MESH5-ORB1 → FLM2.1-CMD4-MESH5-ORB1
  Reason: p_success >= 0.95 and entropy < 0.3

Updating sagco_unified_spec.yaml...
✓ DNA strand updated successfully!
```

### 6. Verify DNA Mutation

```bash
grep "DNA Strand:" sagco_unified_spec.yaml
```

Should show:
```
DNA Strand: FLM2.1-CMD4-MESH5-ORB1
```

## Testing the Complete Pipeline

### Test 1: Oracle with Low Confidence Text

```bash
echo "a" | ./target/release/sagco-oracle
```

This should show low p_correct and higher risk level.

### Test 2: Oracle with High Confidence Text

```bash
echo "This is a comprehensive test of the SAGCO OS Guardian layer with detailed analysis of uncertainty metrics and safety classification for production deployment in hypervisor environments" | ./target/release/sagco-oracle
```

This should show higher p_correct and lower risk level.

### Test 3: DNA Mutation with Failing Metrics

Create a failing Guardian export:

```bash
cat > guardian-uncertainty.json << 'EOF'
{
  "source": "flamebench",
  "dna_strand": "FLM2-CMD4-MESH5-ORB1",
  "uncertainties": [],
  "overall": {
    "p_success": 0.85,
    "entropy": 0.45
  }
}
EOF

./target/release/sagco-dna
```

Should output:
```
✗ No mutation suggested
  Thresholds not met:
    - p_success: 0.850 (need >= 0.95)
    - entropy: 0.450 (need < 0.30)
```

### Test 4: Custom Mesh Node

Add a new node:

```bash
cat > mesh/hosts/testnode.yaml << 'EOF'
name: TESTNODE
role: experimental
ip: 127.0.0.1
os: "Linux"
cpu: "Test"
ram_gb: 1
tags: ["test"]
EOF

python3 tools/sagco-mesh.py
```

Should now show 6 nodes.

## Running Tests

### Unit Tests

```bash
# Test kernel module
cargo test -p sagco-kernel

# Test guardian module
cargo test -p sagco-guardian
```

All tests should pass:
```
running 5 tests
test dna_mutation::tests::test_parse_dna_components ... ok
test dna_mutation::tests::test_suggest_flm_mutation ... ok
test dna_mutation::tests::test_suggest_flm_mutation_incremental ... ok
test dna_mutation::tests::test_suggest_mesh_mutation ... ok
test dna_mutation::tests::test_suggest_orbit_mutation ... ok

test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

## Common Issues

### Issue: "PyYAML not installed"

**Solution:**
```bash
pip install pyyaml
# or
pip3 install pyyaml
```

### Issue: "Guardian uncertainty export not found"

**Solution:**
Create a test file in one of these locations:
- `./guardian-uncertainty.json` (current directory)
- `E:\FlameBench\guardian-uncertainty.json` (Windows)
- `/opt/flamebench/guardian-uncertainty.json` (Linux)

### Issue: "sagco_unified_spec.yaml not found"

**Solution:**
Run from repository root, or update paths in the code.

### Issue: Mesh nodes all show DOWN

**Solution:**
This is expected if nodes aren't actually running at those IPs. To test with localhost:

```bash
cat > mesh/hosts/localhost.yaml << 'EOF'
name: LOCALHOST
role: test
ip: 127.0.0.1
os: "Current System"
cpu: "Local"
ram_gb: 16
tags: ["local", "test"]
EOF

# Start SSH server if not running
sudo systemctl start sshd  # Linux
# or configure SSH on Windows

python3 tools/sagco-mesh.py
```

## Next Steps

1. **Read the Architecture**: See `HYPERVISOR_FLOW.md` for detailed flow
2. **Read the Pipeline Guide**: See `SAGCO_PIPELINE_README.md` for complete documentation
3. **Integrate FlameBench**: Set up actual compilation tests
4. **Deploy to Mesh**: Configure real nodes in `mesh/hosts/`
5. **Automate**: Set up cron jobs for nightly DNA evolution

## Production Deployment Checklist

- [ ] Build with `--release` for performance
- [ ] Set up proper file paths (E:\ on Windows, /opt/ on Linux)
- [ ] Configure mesh nodes with real IPs
- [ ] Implement FlameBench with actual FLM2 compiler
- [ ] Set up systemd timers or cron jobs
- [ ] Configure logging (`/var/log/sagco/`)
- [ ] Implement backup for `sagco_unified_spec.yaml`
- [ ] Add authentication for mesh node scanning
- [ ] Set up monitoring and alerts
- [ ] Document rollback procedures

---

**Quick Start Complete** ✓  
**All Components Tested** ✓  
**Ready for Integration** ✓
