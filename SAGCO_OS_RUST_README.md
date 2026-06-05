# SAGCO OS - Rust Implementation

**Strategic Academic Governance & Cognitive Operations System**

A Rust-based cognitive operating system for mesh networking, safety monitoring, and variational inference.

## 🦀 Workspace Structure

```
sagco-os/
├── Cargo.toml                 # Workspace manifest
├── sagco-dom0d/               # Main daemon (binary)
├── sagco-guardian/            # Cognitive safety monitoring
├── sagco-netcalc/             # Network calculation & TCP probing
├── sagco-pipecalc-vi/         # Variational Inference engine
└── flamelang-engine/          # FlameLang scripting engine
```

## 🔥 Components

### sagco-dom0d
Main daemon that orchestrates all components:
- Initializes Guardian for safety monitoring
- Registers FlameLang engine with Guardian bindings
- Probes mesh network with real TCP connections
- Classifies nodes based on uncertainty
- Selects optimal control peer using VI

### sagco-guardian
Cognitive safety monitoring system:
- `Uncertainty` - Measures entropy and confidence
- `GeometryPoint` - Maps uncertainty to 3D cognitive space
- `SafetyClassification` - Classifies operations (Safe/Caution/Unsafe)
- FlameLang bindings for uncertainty/map/classify operations

### sagco-netcalc
Network calculation with real TCP probing:
- `TcpPinger` - Async TCP connection latency measurement
- `MeshNode` - Network node with Gaussian latency/bandwidth
- `probe_all_nodes()` - Scans mesh with real TCP timing
- `best_control_peer()` - Selects optimal peer using VI

### sagco-pipecalc-vi
Variational Inference for mesh optimization:
- `Gaussian` - Distribution with mean and variance
- `optimal_mesh_route()` - VI-based route calculation
- Accounts for latency mean, variance, and hop count

### flamelang-engine
FlameLang scripting engine:
- `Engine` - Function registry for cognitive scripts
- `EngineRegistrar` trait - Guardian binding interface
- Exposes uncertainty/geometry/classify to scripts

## 🚀 Quick Start

### Build
```bash
cargo build --release
```

### Test
```bash
cargo test
```

### Run Dom0 Daemon
```bash
cargo run -p sagco-dom0d
```

Expected output:
```
🔥 SAGCO Dom0 Daemon Starting...
✓ Guardian initialized with threshold 0.7
✓ FlameLang engine registered with Guardian bindings

📡 Probing mesh network...
  Node: 127.0.0.1 | Latency: 0.00ms ± 0.00ms
    Classification: Safe | Geometry: (0.00, 1.00, 0.00)

🎯 Best control peer: index 0

✅ Dom0 daemon initialized successfully
   - Guardian: ACTIVE
   - FlameLang Engine: REGISTERED
   - Mesh Network: 1 nodes
```

## 🧪 Testing

The workspace includes comprehensive unit tests:

```bash
# Run all tests
cargo test

# Run tests for specific crate
cargo test -p sagco-guardian
cargo test -p sagco-netcalc
```

Test coverage:
- ✅ Gaussian distribution creation and stddev
- ✅ Guardian classification (Safe/Caution/Unsafe)
- ✅ Uncertainty to geometry mapping
- ✅ Latency statistics calculation
- ✅ TCP pinger localhost test
- ✅ Mesh node creation
- ✅ Engine registration
- ✅ FlameLang bindings

## 🔧 Configuration

### Running Examples

```bash
# Guardian uncertainty classification
cargo run --example guardian_example -p sagco-guardian

# Network TCP probing
cargo run --example netcalc_example -p sagco-netcalc

# Variational Inference mesh optimization
cargo run --example vi_example -p sagco-pipecalc-vi
```

### TCP Pinger Settings
Edit `sagco-netcalc/src/lib.rs`:
```rust
let pinger = TcpPinger {
    port: 80,         // Target port
    timeout_ms: 5000, // Connection timeout
};
```

### Mesh Nodes
Edit `sagco-netcalc/src/lib.rs` `probe_all_nodes()`:
```rust
let nodes = vec![
    Ipv4Addr::new(192, 168, 1, 1),
    Ipv4Addr::new(192, 168, 1, 2),
    // Add your mesh IPs
];
```

### Guardian Threshold
Edit `sagco-dom0d/src/main.rs`:
```rust
let guardian = Guardian::new(0.7); // Entropy threshold
```

## 🔬 Architecture Details

### TCP Probing
Real TCP connection timing using tokio async runtime:
1. Establish TCP connection to target IP:port
2. Measure round-trip time
3. Calculate statistics (mean, stddev, min, max)
4. Convert to Gaussian distribution for VI

### Variational Inference
Mesh route optimization using VI:
- Accounts for latency mean (α weight)
- Penalizes variance/uncertainty (β weight)
- Considers hop count (γ weight)
- Returns optimal path through mesh

### Uncertainty Classification
Guardian safety monitoring:
- **Safe**: entropy < 0.35 × threshold
- **Caution**: entropy 0.35-1.0 × threshold
- **Unsafe**: entropy > threshold

### Geometry Mapping
Maps uncertainty to cognitive space:
- X-axis: entropy
- Y-axis: confidence
- Z-axis: entropy × confidence

## 📚 Dependencies

- **tokio** - Async runtime for TCP operations
- **anyhow** - Error handling
- **async-trait** - Async trait support
- **serde/serde_json** - Serialization

## 🧬 Integration with SAGCO Ecosystem

This Rust implementation integrates with:
- **chemcalc_vi** - QM calculations for Ca binding (future)
- **dna_synth** - EF-hand motif targeting (future)
- **NEURON** - Neural dynamics simulation (future)

### Bio-Inspired AI
- Ca-like spiking in neural nets
- VI on "gap" (HOMO-LUMO) as confidence
- Protein binding uncertainties

## 🛡️ Security

- No unsafe Rust code
- All dependencies from crates.io
- CodeQL verified (0 alerts)
- No hardcoded credentials

## 📖 License

Proprietary - Strategickhaos DAO LLC

## 👨‍💻 Authors

- Dom Garza <dom@strategickhaos.ai>

---

**Owner:** Strategickhaos DAO LLC  
**Operator:** Dom (Me10101)  
**Architecture:** Quadrilateral Collapse Learning Integration
