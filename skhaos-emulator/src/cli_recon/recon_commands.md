# CLI Recon Commands - Avian-Cetacean Hybrid Group

This document defines the 3 new recon commands (43-45) for avian-cetacean hybrid bioacoustics.

## Command Table

| ID | Command Name          | Register Freq (Hz) | Bio Type | Pattern Analogy           | Physics Law | Example UDAP URI                                      |
|----|-----------------------|--------------------|----------|---------------------------|-------------|-------------------------------------------------------|
| 43 | crow_caw_probe        | 1000.00            | Crow     | Territorial caw hierarchy | Entropy     | skhaos://avian/crow/caw/1?law=entropy&hz=1000        |
| 44 | hybrid_dolphin_crow   | 50000.00           | Hybrid   | Whistle-caw entangle      | Uncertainty | skhaos://bio/hybrid/dolphin_crow?hz=50000             |
| 45 | orca_crow_evolve      | 13000.00           | Hybrid   | Dialect-caw mutation      | Conservation| skhaos://bio/hybrid/orca_crow?law=conservation&hz=13000|

## Command Descriptions

### 43. crow_caw_probe
- **Purpose**: Simulate crow territorial caw patterns with hierarchical structure
- **Frequency**: 1000 Hz (dominant crow frequency)
- **Pattern**: Territorial defense calls following Zipf distribution
- **Physics**: Entropy law increases diversity in flock coordination
- **Use Case**: Ground reconnaissance with low-frequency acoustic patterns

### 44. hybrid_dolphin_crow
- **Purpose**: Evolve hybrid patterns combining dolphin whistles with crow caws
- **Frequency**: 50000 Hz (dolphin-dominant hybrid)
- **Pattern**: Entanglement of high-frequency cetacean with low-frequency avian
- **Physics**: Uncertainty principle fuzzes Zipf ranks for robustness
- **Use Case**: Broadband reconnaissance spanning 0.5-50 kHz

### 45. orca_crow_evolve
- **Purpose**: Genetic evolution of orca dialects with crow learning patterns
- **Frequency**: 13000 Hz (orca-dominant hybrid)
- **Pattern**: Matrilineal orca calls mutated with crow social hierarchies
- **Physics**: Conservation law maintains energy across evolution
- **Use Case**: Mid-frequency swarm coordination with bio-mimetic efficiency

## Implementation

Each command is implemented through the following modules:

1. **avian_bio/zipf_sim.rs** - Generates Zipf distributions for species
2. **avian_bio/crow_pattern.rs** - Creates crow-specific patterns
3. **avian_bio/hybrid_evolve.rs** - Evolves hybrid patterns via genetic algorithm
4. **bio_physics/physics_dom.rs** - Applies physics law constraints

## Usage Examples

```bash
# Simulate crow territorial caws
./cli_recon crow_caw_probe --rank 1 --law entropy

# Generate dolphin-crow hybrid
./cli_recon hybrid_dolphin_crow --frequency 50000

# Evolve orca-crow dialect
./cli_recon orca_crow_evolve --law conservation --frequency 13000
```

## UDAP URI Examples

```
# Crow caw with entropy
skhaos://avian/crow/caw/1?law=entropy&hz=1000

# Dolphin-crow hybrid
skhaos://bio/hybrid/dolphin_crow?hz=50000

# Orca-crow with conservation
skhaos://bio/hybrid/orca_crow?law=conservation&hz=13000
```

## Technical Details

### Frequency Ranges
- **Crow**: 500-2000 Hz (0.5-2 kHz)
- **Orca**: 1000-25000 Hz (1-25 kHz)
- **Dolphin**: 25000-200000 Hz (25-200 kHz)
- **Hybrids**: Span multiple ranges for broadband coverage

### Zipf Law Adherence
All patterns follow Zipf's Law with slope approximately -1.0:
- High-rank (frequent) units have short durations
- Low-rank (rare) units have long durations
- Efficient communication following power law distribution

### Menzerath's Law
Longer sequences contain shorter elements:
- Dolphin: β ≈ -0.0001
- Orca: β ≈ -0.043
- Crow: β ≈ -0.2 to -0.5 (stronger in young/females)

### Physics Constraints
- **Entropy**: Increases hybrid diversity by factor 1.07
- **Uncertainty**: Adds ±10% fuzz to Zipf ranks
- **Conservation**: Maintains total acoustic energy
