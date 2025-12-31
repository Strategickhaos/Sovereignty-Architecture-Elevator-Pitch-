# 42 Recon Commands - Bio-Physics Mappings
# Complete CLI reference for Bio-Physics Entanglement Compiler

## Command Table

| ID | Command Name         | Register Hz | Bio Type      | Pattern Analogy                    | Physics Law Mapping          | Example UDAP URI |
|----|---------------------|-------------|---------------|------------------------------------|------------------------------|------------------|
| **Zipf Whale Group (Humpback Units/Phrases, 20-4kHz, 1/f Rank)** |
| 1  | wave_probe          | 20.00       | Humpback Zipf | High-rank short unit               | Entropy minimization         | skhaos://bio/zipf/unit/1?law=entropy&hz=20 |
| 2  | entangle_scan       | 500.00      | Humpback Zipf | Phrase distribution                | Uncertainty branching        | skhaos://bio/zipf/phrase/rank?hz=500 |
| 3  | packet_oscillate    | 1000.00     | Humpback Zipf | Menzerath brevity                  | Conservation of energy       | skhaos://bio/zipf/moan?brevity=true&hz=1000 |
| 4  | frequency_sweep     | 50.00       | Humpback Zipf | Low-frequency moan                 | Entropy gradient descent     | skhaos://bio/zipf/unit/2?hz=50 |
| 5  | harmonic_analyze    | 100.00      | Humpback Zipf | Groan harmonic structure           | Uncertainty superposition    | skhaos://bio/zipf/groan?hz=100 |
| 6  | theme_extract       | 200.00      | Humpback Zipf | Recurring theme identification     | Conservation of motifs       | skhaos://bio/zipf/theme?rank=1&hz=200 |
| 7  | phrase_cluster      | 300.00      | Humpback Zipf | Phrase grouping by similarity      | Entropy clustering           | skhaos://bio/zipf/cluster?hz=300 |
| 8  | cultural_trace      | 400.00      | Humpback Zipf | Cultural evolution tracking        | Relativity timeframe shift   | skhaos://bio/zipf/evolution?hz=400 |
| 9  | unit_decompose      | 600.00      | Humpback Zipf | Break phrases into units           | Conservation decomposition   | skhaos://bio/zipf/decompose?hz=600 |
| 10 | zipf_rank_calc      | 800.00      | Humpback Zipf | Calculate Zipf coefficient         | Entropy distribution fit     | skhaos://bio/zipf/coefficient?hz=800 |
| 11 | brevity_check       | 1500.00     | Humpback Zipf | Verify Menzerath's law             | Conservation brevity         | skhaos://bio/zipf/brevity?hz=1500 |
| 12 | song_evolve         | 2000.00     | Humpback Zipf | Evolve song over generations       | Entropy increase trajectory  | skhaos://bio/zipf/evolve?hz=2000 |
| 13 | frequency_map       | 3000.00     | Humpback Zipf | Map frequency spectrum             | Relativity frequency shift   | skhaos://bio/zipf/map?hz=3000 |
| 14 | unit_hierarchy      | 4000.00     | Humpback Zipf | Hierarchical unit structure        | Uncertainty tree branching   | skhaos://bio/zipf/hierarchy?hz=4000 |
| **Dolphin Group (Whistles/Clicks, 1-200kHz, Signature Dialects)** |
| 15 | signature_gen       | 5.00        | Dolphin       | Generate unique signature          | Relativity ID persistence    | skhaos://bio/dolphin/signature?gen=true&hz=5 |
| 16 | whistle_match       | 8.00        | Dolphin       | Match whistle to dolphin           | Conservation ID stability    | skhaos://bio/dolphin/match?hz=8 |
| 17 | pod_identify        | 10.00       | Dolphin       | Identify pod by dialect            | Relativity observer frame    | skhaos://bio/dolphin/pod?identify=true&hz=10 |
| 18 | dialect_learn       | 12.00       | Dolphin       | Learn new dialect pattern          | Entropy learning increase    | skhaos://bio/dolphin/learn?hz=12 |
| 19 | dolphin_whistle     | 10.00       | Dolphin       | Signature name whistle             | Relativity ID persistence    | skhaos://bio/dolphin/whistle?signature=true&hz=10 |
| 20 | echo_burst          | 120.00      | Dolphin       | Echolocation click burst           | Quantum measurement collapse | skhaos://bio/dolphin/click?burst=200&hz=120 |
| 21 | dialect_dialogue    | 200.00      | Dolphin       | Pod-specific chirp/scream          | Entropy in learning          | skhaos://bio/dolphin/dialect?pod=alpha&hz=200 |
| 22 | click_analyze       | 150.00      | Dolphin       | Analyze echolocation pattern       | Quantum probe wavefunction   | skhaos://bio/dolphin/analyze?hz=150 |
| 23 | burst_frequency     | 180.00      | Dolphin       | Burst repetition rate              | Conservation pulse timing    | skhaos://bio/dolphin/frequency?hz=180 |
| 24 | matrilineal_trace   | 15.00       | Dolphin       | Track matrilineal learning         | Relativity generational time | skhaos://bio/dolphin/matrilineal?hz=15 |
| 25 | whistle_entangle    | 18.00       | Dolphin       | Entangle whistle with whale unit   | Uncertainty superposition    | skhaos://bio/dolphin/entangle?hz=18 |
| 26 | pod_exchange        | 14.00       | Dolphin       | Simulate pod communication         | Conservation info exchange   | skhaos://bio/dolphin/exchange?pod=alpha,beta&hz=14 |
| 27 | dialect_evolve      | 16.00       | Dolphin       | Evolve dialect over time           | Entropy cultural drift       | skhaos://bio/dolphin/evolve?hz=16 |
| **Hybrid Whale-Dolphin Group (Entangled Patterns)** |
| 28 | bio_entangle        | 25.00       | Hybrid        | Entangle whale and dolphin         | Uncertainty superposition    | skhaos://bio/hybrid/entangle?hz=25 |
| 29 | cetacean_unify      | 30.00       | Hybrid        | Unified cetacean pattern           | Conservation total energy    | skhaos://bio/hybrid/unify?hz=30 |
| 30 | cross_species       | 35.00       | Hybrid        | Cross-species communication        | Relativity species frame     | skhaos://bio/hybrid/cross?hz=35 |
| 31 | bio_compiler        | 40.00       | Hybrid        | Compile bio patterns to ops        | All laws composite           | skhaos://bio/hybrid/compile?hz=40 |
| **Musical Integration Group (Classical + Bio)** |
| 32 | motif_rank          | 5.00        | Music         | Rank musical motifs by Zipf        | Entropy motif distribution   | skhaos://bio/music/motif?rank=true&hz=5 |
| 33 | theme_zipf          | 10.00       | Music         | Apply Zipf to theme analysis       | Conservation theme energy    | skhaos://bio/music/theme?zipf=true&hz=10 |
| 34 | canon_delay         | 33.00       | Music         | Canon form with replication        | Thermodynamic replication    | skhaos://bio/music/canon?law=entropy&hz=33 |
| 35 | fugue_thread        | 28.00       | Music         | Fugue voices as parallel threads   | Relativity spacetime sync    | skhaos://bio/music/fugue?law=relativity&hz=28 |
| 36 | variation_form      | 37.00       | Music         | Variation form with mutations      | Conservation energy balance  | skhaos://bio/music/variation?law=conservation&hz=37 |
| **Physics DOM Group (Law Constraints, Variable Hz)** |
| 37 | rondo_cycle         | 10.00       | Physics       | ABACA with entropy reset           | Conservation loop            | skhaos://bio/physics/rondo?law=conservation&hz=10 |
| 38 | sonata_transform    | 22.00       | Physics       | Development with uncertainty       | Heisenberg branching         | skhaos://bio/physics/sonata?law=uncertainty&hz=22 |
| 39 | fugue_parallel      | 28.00       | Physics       | Threads with relativity sync       | Spacetime coordination       | skhaos://bio/physics/fugue?law=relativity&hz=28 |
| 40 | canon_delay         | 33.00       | Physics       | Replica with entropy decay         | Thermodynamic replication    | skhaos://bio/physics/canon?law=entropy&hz=33 |
| 41 | variation_mutate    | 37.00       | Physics       | Mutations with conservation        | Energy-balanced evolution    | skhaos://bio/physics/variation?law=conservation&hz=37 |
| 42 | coda_terminate      | 40.00       | Physics       | Collapse with uncertainty peak     | Quantum final state          | skhaos://bio/physics/coda?law=uncertainty&hz=40 |

## Total: 42 Commands
- Zipf Whale: 14 commands (IDs 1-14)
- Dolphin: 13 commands (IDs 15-27)
- Hybrid: 4 commands (IDs 28-31)
- Musical: 5 commands (IDs 32-36)
- Physics: 6 commands (IDs 37-42)

## Overall Evolvability: Ecosystem-Complete
- Bio-communications (Zipf + Dolphin)
- Physics constraints (All 4 laws)
- Musical patterns (Classical forms)
- Swarm evolution with recursive mutations
