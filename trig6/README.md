# TRIG6 Sovereign Compute Engine

**A domain OS with a proof pipeline for deterministic computation and sovereignty verification.**

## License

MIT License - Copyright (c) 2025 Strategickhaos

All files in this module are licensed under the MIT License. See the LICENSE file in the repository root for full details.

## Architecture

TRIG6 is a sovereign compute engine with:

- **Core compute**: Zero external dependencies
- **Optional modules**: Music/visuals require extra packages (midiutil, matplotlib, mido)
- **Canonical registry**: Compiled from canonical 64-glyph registry (IDs 0–63)
- **No external lookup**: Intrinsic resolution from a versioned local registry

## Quick Start

### Run Doctor Check

```bash
python3 trig6.py doctor
```

### Generate Proof Bundle

```bash
python3 proof.py --all --bundle --output ./proof_bundle
```

### Docker Build

```bash
docker build -t trig6:latest .
docker run trig6:latest doctor
```

## File Structure

```
trig6/
├── trig6.py       # Core compute engine
├── proof.py       # Sovereignty proof generator
├── Dockerfile     # Container definition
├── install.sh     # Installation script
├── core/          # Core computation modules
├── domains/       # Domain-specific extensions
├── packs/         # Functionality bundles
├── games/         # Game implementations
└── sagco/         # SAGCO OS integration
```

## Core Features

### 1. Deterministic Validation

The `doctor` command provides deterministic validation:

```bash
python3 trig6.py doctor
```

Output:
```
=== TRIG6 Sovereign Compute Engine ===
Version: 1.0.0
Registry Size: 64 glyphs
Registry Hash: [deterministic hash]
[PASS] Registry integrity verified
[PASS] All systems operational
```

### 2. Proof Bundle Generation

Generate cryptographic proof bundles with environment capture:

```bash
python3 proof.py --all --bundle
```

The proof generator:
- Records git commit hash
- Captures Python version
- Captures system information (uname -a)
- Lists pip packages
- Computes SHA256 hashes of all source files
- Generates bundle hash for verification
- Scans: `trig6.py`, `proof.py`, `core/`, `domains/`, `packs/`, `games/`, `sagco/`

### 3. Docker Deployment

The Dockerfile includes:
- Health checks using `doctor` command
- Non-root execution (trig6 user)
- All required directories
- MIT license metadata

## Installation

### System-wide Installation

```bash
cd trig6/
chmod +x install.sh
./install.sh install
```

This installs to `~/.khaos/trig6/` with automatic Python interpreter detection.

### Manual Installation

```bash
# Copy to desired location
mkdir -p ~/.khaos/trig6
cp -r trig6/ ~/.khaos/trig6/

# Run directly
python3 ~/.khaos/trig6/trig6.py doctor
```

## Commands

### trig6.py

- `doctor` - Run system diagnostics and validation
- `info` - Display system information
- `list` - List all glyphs in the canonical registry

### proof.py

- `--all` - Scan all directories
- `--bundle` - Generate proof bundle
- `--output <dir>` - Specify output directory (default: ./proof_bundle)

## Registry

TRIG6 uses a canonical 64-glyph registry (IDs 0–63) organized as:

- **0-15**: Core trigonometric functions (sin, cos, tan, etc.)
- **16-31**: Extended operations (add, sub, mul, div, etc.)
- **32-47**: Logical and bitwise operations
- **48-63**: Advanced mathematical functions

View the full registry:

```bash
python3 trig6.py list
```

## Dependencies

### Core Engine

The core compute engine has **zero external dependencies** - it uses only Python standard library.

### Optional Modules

Optional functionality requires additional packages:

- Music generation: `midiutil`, `mido`
- Visualizations: `matplotlib`

Install optional dependencies:

```bash
pip install midiutil mido matplotlib
```

## Docker Usage

### Build

```bash
docker build -t trig6:latest .
```

### Run

```bash
# Run doctor check
docker run trig6:latest doctor

# Run with custom command
docker run trig6:latest list

# Generate proof bundle
docker run -v $(pwd)/proofs:/proofs trig6:latest proof.py --all --bundle --output /proofs
```

### Health Check

The container includes a health check that runs `doctor` every 30 seconds:

```bash
docker ps  # Check HEALTH status
```

## Proof Pipeline

The sovereignty proof pipeline ensures:

1. **Deterministic execution**: `trig6.py doctor` produces consistent results
2. **Cryptographic verification**: `proof.py` generates SHA256 hashes of all sources
3. **Environment capture**: Records Python version, system info, dependencies
4. **Commit tracking**: Includes git commit hash in all proofs
5. **Bundle integrity**: Computes hash of entire proof bundle

Example proof workflow:

```bash
# 1. Validate system
python3 trig6.py doctor

# 2. Generate proof bundle
python3 proof.py --all --bundle

# 3. Verify proof bundle
cat proof_bundle/proof_summary.txt

# 4. Get bundle hash for external verification
grep "Bundle Hash" proof_bundle/proof_summary.txt
```

## Terminology

Following audit-proof terminology:

- ✅ **"Core compute is zero external dependencies"** - Accurate for trig6.py
- ✅ **"Optional modules require extra packages"** - Clear about music/visual deps
- ✅ **"No external lookup; intrinsic resolution from a versioned local registry"** - Registry is compiled into source
- ✅ **"Compiled from canonical 64-glyph registry (IDs 0–63)"** - No mention of "padding"

## Contributing

This is part of the Strategickhaos Sovereignty Architecture. Contributions should:

1. Maintain zero dependencies for core compute
2. Use MIT license
3. Include proof generation for all changes
4. Pass `doctor` validation

## Support

- Repository: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- Issues: File via GitHub Issues
- License: MIT (see LICENSE file in repository root)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**
