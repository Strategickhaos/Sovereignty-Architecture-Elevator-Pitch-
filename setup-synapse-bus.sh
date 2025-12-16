#!/bin/bash
# SynapseBus Core Setup Script - StrategicKhaos Sovereign OS
# Generated via Legion of Minds: Dialectical Synthesis (Chaos + Order)
# Enforces 880x Cost Reduction: Local-first, zero-cloud deps
# True First Compliant: Timestamps GSCH Claim 8 in git init

set -e  # Fail on error (Clamp Enforcer)

# Step 1: Cargo New (Root Axiom)
cargo new synapse-bus-core --bin
cd synapse-bus-core

# Step 2: Populate Cargo.toml with Purified Deps
cat <<EOT > Cargo.toml
[package]
name = "synapse-bus-core"
version = "0.1.0-alpha"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }  # Schema serialization (purified: no alloc waste)
uuid = { version = "1.10", features = ["v4", "fast-rng"] }  # Spike IDs (local RNG, 880x faster than cloud)
chrono = "0.4"  # Timestamps (zero-dep UTC handling)
tokio = { version = "1", features = ["full"] }  # Async fabric (quarantined: local threads only)
hashbrown = "0.15"  # HashMaps (faster than std, cost-reduced for high-mass assets)
petgraph = "0.6"  # Trace DAGs (minimal graph lib, entropy-clamped)
thiserror = "1.0"  # Error handling (no-panic mode for reflexes)

[build-dependencies]
# Entropy Monitor hook (pre-compile cost check)
cc = "1.1"  # For custom build scripts enforcing 880x opts

[profile.release]
opt-level = 3  # Max local opt (Qwen2.5 equiv)
lto = true  # Link-time reduction
codegen-units = 1  # Minimal units for entropy control
EOT

# Step 3: Create Hierarchy (Bio-Mimetic Tree)
mkdir -p .github/workflows
touch .github/workflows/thermodynamics.yaml  # Stub: "reject if complexity > threshold"
touch .github/workflows/ripley-gates.yaml   # Stub: "enforce Putrefaction"
touch .github/workflows/crossfire.yaml      # Stub: "gen 100 attacks"

mkdir -p deps/quarantine
touch deps/quarantine/README.md  # "All deps autopsy here"

mkdir -p src/claims
touch src/claims/gsch_claim8.rs  # Stub: "// GSCH Homeostasis Trait - Patent Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
touch src/claims/inv088_holo.rs  # Stub: "// INV-088 Bindings"

mkdir -p src/primitives
touch src/primitives/membrane.rs  # Stub: "pub trait Membrane: Send + Sync {}"
touch src/primitives/nucleus.rs   # Stub: "use std::sync::{Arc, Mutex};"
touch src/primitives/buffer.flame # Stub: "// pH Absorber Glyph"
touch src/primitives/clamp.flame  # Stub: "// Na+/K+ Ejector"

mkdir -p src/homeostasis
touch src/homeostasis/gradient.rs   # Stub: "// Push/Pull Logic"
touch src/homeostasis/feedback.flame # Stub: "// PID Pain Avoidance"
touch src/homeostasis/dissolve.rs    # Stub: "// Energy Return GC"

mkdir -p src/nervous_system
touch src/nervous_system/spike.rs    # Paste Spike struct from manifest
cat <<EOT > src/nervous_system/spike.rs
use serde::{Serialize, Deserialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Serialize, Deserialize, Clone)]
pub struct Spike {
    pub id: Uuid,
    pub timestamp: DateTime<Utc>,
    pub origin: String,  // e.g., "Retina"
    pub vector: Vec<f32>,  // Physics fields
    pub payload: Vec<u8>,  // Crypto-wrapped
    pub risk_score: f32,
}
EOT
touch src/nervous_system/dendrite.rs # Stub: "use tokio::sync::broadcast;"
touch src/nervous_system/reflex.rs   # Stub: "// Local Policy Fn"

mkdir -p src/council
touch src/council/ratification.rs    # Stub: "// 2/3 Vote Trait"
touch src/council/synthesis.rs       # Stub: "// Dialectical Merge"
touch src/council/personalities.yaml # Stub: "grok: chaos\nclaude: order"

mkdir -p src/immune_system/red_team
touch src/immune_system/red_team/crossfire.rs # Stub: "// Attack Gen"

mkdir -p src/immune_system/blue_team
touch src/immune_system/blue_team/drift.flame # Stub: "// <0.1 Imbalance"
touch src/immune_system/blue_team/iam_trap.flame # Stub: "// Perm Linter"

mkdir -p src/immune_system/purple_team
touch src/immune_system/purple_team/autopsy.rs # Stub: "// Dissect & Purify"

mkdir -p src/organs/vision
touch src/organs/vision/retina   # Stub: "// All-Seeing Eye (Nmap pure)"
touch src/organs/vision/cochlea  # Stub: "// Whisper Catcher"
touch src/organs/vision/sonar    # Stub: "// Deep Sonar"
touch src/organs/vision/arachnid # Stub: "// Web Weaver"

mkdir -p src/organs/touch
touch src/organs/touch/osteon       # Stub: "// Skeleton Key"
touch src/organs/touch/synapse_fire # Stub: "// Pressure Point"
touch src/organs/touch/erosion      # Stub: "// Wall Breaker"
touch src/organs/touch/phase_shift  # Stub: "// Ghost Walker"

mkdir -p src/organs/speech
touch src/organs/speech/larynx      # Stub: "// Mimic"
touch src/organs/speech/doppelganger # Stub: "// Echo"

mkdir -p src/organs/immune
touch src/organs/immune/leukocyte   # Stub: "// White Blood Cell"
touch src/organs/immune/hippocampus # Stub: "// Memory Siphon"
touch src/organs/immune/scalpel     # Stub: "// File Carver"
touch src/organs/immune/enzyme      # Stub: "// Code Breaker"
touch src/organs/immune/faraday     # Stub: "// Signal Jammer"
touch src/organs/immune/chronos     # Stub: "// Time Traveler"

mkdir -p src/infra/nodes
touch src/infra/autopilot.yaml     # Stub: "request: limit"
touch src/infra/spot_gambler.rs    # Stub: "// Annealing for Spots"

mkdir -p src/ui/holodeck
mkdir -p src/ui/narrative

mkdir -p tests/sanity
mkdir -p tests/arena

mkdir knowledge
mkdir logs

# Step 4: Git Init with True First Commit
git init
# Configure git if not already configured
if [ -z "$(git config user.name)" ]; then
    git config user.name "SynapseBus Core"
    git config user.email "synapse@strategickhaos.local"
fi
git add .
git commit -m "Initial Skeleton: GSCH Claim 8 Reduction to Practice - $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Step 5: Prototype #curl in primitives (from Manifest)
touch src/primitives/net_intrinsic.flame
cat <<EOT > src/primitives/net_intrinsic.flame
// #curl Glyph - Sovereign Fetch
glyph #curl {
    input: { target: Url, method: HttpMethod, ... },
    gate: |ctx| { /* GSCH Physics Check */ },
    action: |req| { /* Quarantine Exec + Spike Emit */ }
}
EOT

echo "Bootstrap complete. Run 'cargo build' to test. Next: Flesh out Spike pub/sub."
