#!/usr/bin/env python3
"""
example_complete_workflow.py

Complete workflow demonstration of SAGCO-OS components

This script demonstrates a realistic usage scenario combining:
- TRIG6 orchestration
- Neurograph visualization
- DNA evolution tracking
- Structured logging

Copyright (c) 2026 Strategickhaos DAO LLC
"""

import math
import numpy as np
from pathlib import Path

# Import SAGCO-OS components
from HybridWaveCoreState import HybridWaveCoreState, AgentRole
from neurograph_builder import NeurographBuilder
from dna_codon_registry import DNAStrand, CodonRegistry, Codon
from trig6_logger import TRIG6Logger

print("=" * 80)
print("SAGCO-OS Complete Workflow Demonstration")
print("=" * 80)
print()

# Step 1: Initialize DNA tracking
print("Step 1: Initializing DNA Evolution Tracking")
print("-" * 80)
strand = DNAStrand("SAGCO")
registry = CodonRegistry()

# Build initial DNA strand
initial_codons = ["FLM2", "MSMC2", "P16", "CMD27", "ISO103", "MESH5", 
                  "ORB1", "TRIG6", "WAVE1", "HYBRID1", "NEURO1", "OPS1"]

for codon_code in initial_codons:
    codon_def = registry.get_codon(codon_code)
    if codon_def:
        codon = Codon(
            code=codon_def.code,
            subsystem=codon_def.subsystem,
            version=codon_def.version,
            dependencies=codon_def.dependencies.copy()
        )
        strand.add_codon(codon, "Dom Garza", f"Initial {codon_def.subsystem}")

print(f"Initial DNA Strand: {strand}")
print(f"Codons: {len(strand.codons)}")
print()

# Step 2: Initialize TRIG6 orchestration
print("Step 2: Initializing TRIG6 Orchestration System")
print("-" * 80)
core = HybridWaveCoreState(initial_theta=math.pi / 4)
print(f"Initial theta: {math.degrees(core.theta):.2f}°")
print(f"Mode: {core.mode.value}")
print()

# Step 3: Initialize logger
print("Step 3: Initializing TRIG6 Logger")
print("-" * 80)
logger = TRIG6Logger(log_dir="/tmp/sagco_demo")
print(f"Log directory: /tmp/sagco_demo")
print()

# Step 4: Run orchestration scenario
print("Step 4: Running Multi-Task Orchestration Scenario")
print("-" * 80)

# Define task scenarios with different theta values
scenarios = [
    {"name": "Hypervisor Task", "theta": 0.1},
    {"name": "Compiler Task", "theta": math.pi / 6},
    {"name": "Security Task", "theta": math.pi / 4},
    {"name": "Academic Task", "theta": math.pi / 3},
    {"name": "Creative Task (Near Singularity)", "theta": math.pi / 2 - 0.05},
]

for i, scenario in enumerate(scenarios, 1):
    print(f"\nScenario {i}: {scenario['name']}")
    print(f"  Theta: {math.degrees(scenario['theta']):.2f}°")
    
    # Simulate agent outputs (in practice, these would come from actual AI agents)
    agent_outputs = np.random.rand(6)
    agent_outputs = agent_outputs / np.sum(agent_outputs)
    
    # Run orchestration
    weights, metrics = core.orchestrate(
        task_theta=scenario['theta'],
        agent_outputs=agent_outputs,
        target_theta=math.pi / 4,
        benchmark_resonance=0.85
    )
    
    print(f"  Mode: {core.mode.value}, Alpha: {core.alpha:.3f}")
    print(f"  Resonance: {metrics.resonance:.3f}, Drift: {metrics.drift:.3f}, Noise: {metrics.noise:.3f}")
    
    # Display top agents
    sorted_weights = sorted(weights.items(), key=lambda x: abs(x[1].weight), reverse=True)
    print(f"  Top Agents:")
    for agent, weight in sorted_weights[:3]:
        danger = " ⚠️" if weight.danger_zone else ""
        print(f"    {agent.name}: {weight.weight:.3f}{danger}")
    
    # Log to TRIG6 logger
    agent_weights = {agent.name: w.weight for agent, w in weights.items()}
    logger.log_orchestration(
        theta=scenario['theta'],
        mode=core.mode.value,
        alpha=core.alpha,
        agent_weights=agent_weights,
        metrics={
            "resonance": metrics.resonance,
            "drift": metrics.drift,
            "noise": metrics.noise
        }
    )
    
    # Check for danger zones
    danger_zones = core.detect_danger_zones(scenario['theta'])
    if danger_zones:
        print(f"  ⚠️  WARNING: {len(danger_zones)} danger zone(s) detected")
        logger.log_danger_zone(
            theta=scenario['theta'],
            agents=[a.name for a, w in weights.items() if w.danger_zone],
            singularities=[z.function_name for z in danger_zones]
        )

print()

# Step 5: Generate neurograph visualization
print("\nStep 5: Generating Neurograph Visualization")
print("-" * 80)

builder = NeurographBuilder()
builder.build_complete_neurograph(
    theta=core.theta,
    agent_weights={agent.name: w.weight for agent, w in weights.items()},
    alpha=core.alpha,
    drift=metrics.drift,
    resonance=metrics.resonance,
    noise=metrics.noise
)

# Export neurograph
neurograph_dir = Path("/tmp/sagco_demo/neurographs")
neurograph_dir.mkdir(parents=True, exist_ok=True)

dot_file = neurograph_dir / "final_neurograph.dot"
json_file = neurograph_dir / "final_neurograph.json"

with open(dot_file, 'w') as f:
    f.write(builder.to_dot())

with open(json_file, 'w') as f:
    f.write(builder.to_json())

print(f"Neurograph exported to:")
print(f"  DOT: {dot_file}")
print(f"  JSON: {json_file}")

summary = builder.get_summary()
print(f"  Nodes: {summary['nodes']} (Active: {summary['active_nodes']}, Danger: {summary['danger_nodes']})")
print(f"  Edges: {summary['edges']}")
print()

# Step 6: Simulate evolution - increment TRIG6 version
print("Step 6: Simulating Software Evolution")
print("-" * 80)
strand.increment_version(
    "TRIG6",
    "v6.1",
    author="Dom Garza",
    justification="Added enhanced singularity detection and danger zone warnings"
)
print(f"Updated DNA Strand: {strand}")
print(f"Mutations: {len(strand.mutation_history)}")
print()

# Step 7: Export DNA evolution
dna_file = Path("/tmp/sagco_demo") / "dna_evolution.json"
with open(dna_file, 'w') as f:
    f.write(strand.export_json())
print(f"DNA evolution exported to: {dna_file}")
print()

# Step 8: Generate summary report
print("\nStep 8: Generating Summary Report")
print("-" * 80)
summary_report = logger.export_summary()
print(summary_report)

summary_file = Path("/tmp/sagco_demo") / "trig6_summary.txt"
with open(summary_file, 'w') as f:
    f.write(summary_report)
print(f"\nSummary exported to: {summary_file}")

# Final status
print("\n" + "=" * 80)
print("SAGCO-OS Workflow Complete!")
print("=" * 80)
print("\nOutput files:")
print(f"  - DNA Evolution: {dna_file}")
print(f"  - Neurograph DOT: {dot_file}")
print(f"  - Neurograph JSON: {json_file}")
print(f"  - TRIG6 Summary: {summary_file}")
print(f"  - TRIG6 Logs: /tmp/sagco_demo/trig6_*.log")
print("\nTo visualize neurograph (if graphviz installed):")
print(f"  dot -Tpng {dot_file} -o /tmp/sagco_demo/neurographs/neurograph.png")
print()
