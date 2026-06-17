# Synapse-Bus-Core

**Version 0.1.0-alpha (Event Horizon)**

A bio-mimetic, sovereign operating system core with GSCH physics engine integration.

## Architecture Overview

Synapse-Bus-Core implements the Master Architecture Manifest for the StrategicKhaos Sovereign OS, featuring:

- **Bio-Mimetic Design**: Systems mirror biological processes (cells, neurons, immune system)
- **GSCH Physics Engine**: Gradient-based homeostasis regulation
- **Sovereign Architecture**: Local-first dependencies, quarantined 3rd-party code
- **Legion of Minds Governance**: Multi-AI consensus (Claude, Grok, Gemini)
- **16 Purified Organs**: Autopsy-validated security tools with physics gates

## Directory Structure

```
synapse-bus-core/
├── src/
│   ├── claims/          # Patent timestamping (GSCH Claim 8, INV-088)
│   ├── primitives/      # Bio-digital interface (Membrane, Nucleus, Buffer, Clamp)
│   ├── homeostasis/     # Physics engine (Gradient, Feedback, Dissolve)
│   ├── nervous_system/  # Event processing (Spike, Dendrite, Reflex)
│   ├── council/         # AI governance (Ratification, Synthesis, Personalities)
│   ├── immune_system/   # Security teams (Red/Blue/Purple)
│   ├── organs/          # 16 purified tools (Vision, Touch, Speech, Immune)
│   ├── infra/           # Kubernetes integration (Nodes, Autopilot, SpotGambler)
│   └── ui/              # Event Horizon v0 (Holodeck, Narrative)
├── tests/
│   ├── sanity/          # Hallucination firewall tests
│   └── arena/           # Crossfire test harness
├── .github/workflows/   # CI/CD gates (Thermodynamics, Ripley, Crossfire)
├── deps/quarantine/     # Untrusted 3rd-party dependencies
├── knowledge/           # Memory palace (vector DB)
└── logs/                # Immunization records
```

## Core Concepts

### The Spike
Fundamental unit of neural communication between organs:
```rust
pub struct Spike {
    pub id: Uuid,
    pub timestamp: DateTime<Utc>,
    pub origin: OrganType,
    pub vector: PhysicsVector,  // GSCH data
    pub payload: CryptoCell<Vec<u8>>,
    pub risk_score: f32,
}
```

### Physics Vector (GSCH)
```rust
pub struct PhysicsVector {
    pub heat: f32,      // System entropy (0.0 - 1.0)
    pub gravity: f32,   // Attraction/repulsion force
}
```

### The 16 Organs

**Vision (Reconnaissance)**:
- Retina (f.k.a. Nmap) - Topology mapping
- Cochlea (f.k.a. Wireshark) - Packet analysis
- Sonar (f.k.a. Masscan) - Port enumeration
- Arachnid (f.k.a. Burp Suite) - HTTP interception

**Touch (Exploitation)**:
- Osteon (f.k.a. Metasploit) - Exploit delivery
- SynapseFire (f.k.a. Hydra) - Credential testing
- Erosion (f.k.a. SQLMap) - DB integrity testing
- PhaseShift (f.k.a. ProxyChains) - Traffic routing

**Speech (C2 & Social)**:
- Larynx (f.k.a. SET) - Phishing simulation
- Doppelganger (f.k.a. Responder) - LLMNR detection

**Immune (Defense & Forensics)**:
- Leukocyte (f.k.a. Snort) - Intrusion detection
- Hippocampus (f.k.a. Volatility) - Memory analysis
- Scalpel (f.k.a. Foremost) - File carving
- Enzyme (f.k.a. John the Ripper) - Hash analysis
- Faraday (f.k.a. Aircrack) - Wireless analysis
- Chronos (f.k.a. Git/Autopsy) - Timeline forensics

## Building

```bash
# Build the project
cargo build --release

# Run tests
cargo test

# Run the daemon
cargo run
```

## Python Interop

```bash
# Install Python bindings
pip install -e .

# Use from Python
import synapse_bus_core
```

## CI/CD Gates

Three automated gatekeepers protect code quality:

1. **Thermodynamics Gate**: Rejects PRs with high cyclomatic complexity
2. **Ripley Gates**: Seven alchemical stages of code transformation
3. **Crossfire Arena**: 100-angle adversarial attack generation

## Axioms

1. **Sovereignty**: All 3rd party dependencies live in quarantine until purified
2. **True First**: Patent timestamping ensures proof of invention
3. **Bio-Mimetic**: Systems mirror biological processes for resilience

## License

MIT

## Version History

- **v0.1.0-alpha (Event Horizon)**: Initial alpha release
  - Core nervous system implementation
  - 16 organ stubs
  - GSCH physics engine
  - Legion of Minds governance framework
  - Immune system (Red/Blue/Purple teams)

---

**⚠️ Alpha Release**: Use in production at your own risk. This is a research and development project implementing novel architectures.
