#!/usr/bin/env python3
"""
test_sagco_integration.py

Integration test for SAGCO-OS components

Tests all major components and their interactions to ensure the system
works as specified in the patent application.

Copyright (c) 2026 Strategickhaos DAO LLC
"""

import math
import sys
import numpy as np
from pathlib import Path

# Test result tracking
test_results = []


def test_result(name, passed, message=""):
    """Record test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    test_results.append((name, passed, message))
    print(f"{status}: {name}")
    if message and not passed:
        print(f"  {message}")


def test_trig6_system():
    """Test TRIG6 trigonometric orchestration system"""
    print("\n" + "=" * 80)
    print("Testing TRIG6 Trigonometric Orchestration System")
    print("=" * 80)
    
    try:
        from HybridWaveCoreState import HybridWaveCoreState, AgentRole, ProjectionMode
        
        # Test 1: Initialization
        core = HybridWaveCoreState(initial_theta=math.pi / 4)
        test_result("TRIG6 initialization", True)
        
        # Test 2: Trigonometric weights
        weights = core.compute_trigonometric_weights(math.pi / 4)
        test_result(
            "Trigonometric weight computation",
            len(weights) == 6 and all(isinstance(w.weight, float) for w in weights.values())
        )
        
        # Test 3: Hyperbolic weights
        hyp_weights = core.compute_hyperbolic_weights(math.pi / 4)
        test_result(
            "Hyperbolic weight computation",
            len(hyp_weights) == 6
        )
        
        # Test 4: Danger zone detection
        danger_zones = core.detect_danger_zones(math.pi / 2)
        test_result(
            "Singularity detection (Claim 5)",
            len(danger_zones) > 0,
            "Should detect danger near π/2"
        )
        
        # Test 5: Orchestration
        agent_outputs = np.random.rand(6)
        agent_outputs = agent_outputs / np.sum(agent_outputs)
        weights, metrics = core.orchestrate(
            task_theta=math.pi / 3,
            agent_outputs=agent_outputs,
            target_theta=math.pi / 4
        )
        test_result(
            "Complete orchestration (Claim 1)",
            len(weights) == 6 and metrics.drift >= 0
        )
        
        # Test 6: Resonance computation
        test_result(
            "Resonance metric (Claim 3a)",
            0 <= metrics.resonance <= 1.0
        )
        
        # Test 7: Drift computation
        test_result(
            "Drift metric (Claim 3b)",
            metrics.drift >= 0
        )
        
        # Test 8: Noise computation
        test_result(
            "Noise metric (Claim 3c)",
            metrics.noise >= 0
        )
        
        # Test 9: Mode switching
        core.update_blend_ratio(0.6)  # High drift should trigger mode switch
        test_result(
            "Hybrid blend control (Claim 1f)",
            core.mode in [ProjectionMode.HYPERBOLIC, ProjectionMode.HYBRID]
        )
        
        print(f"\nTRIG6 Tests: {sum(1 for _, p, _ in test_results[-9:] if p)}/9 passed")
        
    except Exception as e:
        test_result("TRIG6 System", False, str(e))


def test_neurograph_system():
    """Test neurograph visualization system"""
    print("\n" + "=" * 80)
    print("Testing Neurograph Visualization System")
    print("=" * 80)
    
    try:
        from neurograph_builder import NeurographBuilder, NodeTier, EdgeType
        
        # Test 1: Initialization
        builder = NeurographBuilder()
        test_result("Neurograph initialization", True)
        
        # Test 2: Build complete graph
        builder.build_complete_neurograph(
            theta=math.pi / 4,
            alpha=0.3,
            drift=0.25,
            resonance=0.75,
            noise=0.12
        )
        test_result(
            "Complete neurograph construction (Claim 4)",
            len(builder.nodes) > 0 and len(builder.edges) > 0
        )
        
        # Test 3: Check tier structure
        tiers = set(node.tier for node in builder.nodes.values())
        test_result(
            "Five-tier topology (Claim 4c)",
            len(tiers) >= 5
        )
        
        # Test 4: DOT export
        dot_output = builder.to_dot()
        test_result(
            "DOT format export (Claim 4d)",
            "digraph" in dot_output and len(dot_output) > 100
        )
        
        # Test 5: JSON export
        json_output = builder.to_json()
        test_result(
            "JSON format export (Claim 4d)",
            '"nodes"' in json_output and '"edges"' in json_output
        )
        
        # Test 6: Danger indicators
        builder.build_complete_neurograph(theta=math.pi / 2)
        danger_nodes = sum(1 for node in builder.nodes.values() if node.danger_zone)
        test_result(
            "Danger zone indicators (Claim 11)",
            danger_nodes > 0,
            f"Found {danger_nodes} nodes in danger zones"
        )
        
        print(f"\nNeurograph Tests: {sum(1 for _, p, _ in test_results[-6:] if p)}/6 passed")
        
    except Exception as e:
        test_result("Neurograph System", False, str(e))


def test_dna_system():
    """Test DNA evolution tracking system"""
    print("\n" + "=" * 80)
    print("Testing DNA Evolution Tracking System")
    print("=" * 80)
    
    try:
        from dna_codon_registry import DNAStrand, CodonRegistry, Codon, MutationType
        
        # Test 1: Strand initialization with ATG
        strand = DNAStrand("SAGCO")
        test_result(
            "DNA strand initialization with ATG (Claim 7)",
            strand.codons[0].code == "ATG"
        )
        
        # Test 2: Codon registry
        registry = CodonRegistry()
        test_result(
            "Codon registry (Claim 2b)",
            len(registry.codons) >= 16
        )
        
        # Test 3: Add codon with dependencies
        trig6 = registry.get_codon("TRIG6")
        if trig6:
            codon = Codon(
                code=trig6.code,
                subsystem=trig6.subsystem,
                version=trig6.version,
                dependencies=trig6.dependencies.copy()
            )
            
            # Add dependencies first
            for dep_code in ["FLM2", "MSMC2", "P16", "CMD27", "MESH5", "ORB1"]:
                dep = registry.get_codon(dep_code)
                if dep:
                    dep_codon = Codon(
                        code=dep.code,
                        subsystem=dep.subsystem,
                        version=dep.version,
                        dependencies=dep.dependencies.copy()
                    )
                    strand.add_codon(dep_codon, "Test", "Setup")
            
            # Now add TRIG6
            success = strand.add_codon(codon, "Test", "Test codon")
            test_result(
                "Codon append with dependency validation (Claim 2c)",
                success
            )
        else:
            test_result("Codon registry lookup", False, "TRIG6 not found")
        
        # Test 4: Version increment
        success = strand.increment_version("TRIG6", "v6.1", "Test", "Test increment")
        test_result(
            "Version increment mutation (Claim 2c)",
            success
        )
        
        # Test 5: Mutation history
        test_result(
            "Mutation logging (Claim 2c iii)",
            len(strand.mutation_history) > 0
        )
        
        # Test 6: Strand format
        strand_str = strand.get_strand_string()
        test_result(
            "DNA strand format (Claim 2a)",
            strand_str.startswith("SAGCO-ATG") and "TRIG6" in strand_str
        )
        
        # Test 7: Lineage tracking
        history = strand.get_mutation_history()
        test_result(
            "Lineage tracker (Claim 2d)",
            len(history) > 0 and isinstance(history[0], dict)
        )
        
        print(f"\nDNA Tests: {sum(1 for _, p, _ in test_results[-7:] if p)}/7 passed")
        
    except Exception as e:
        test_result("DNA System", False, str(e))


def test_logger_system():
    """Test TRIG6 logger system"""
    print("\n" + "=" * 80)
    print("Testing TRIG6 Logger System")
    print("=" * 80)
    
    try:
        from trig6_logger import TRIG6Logger, EventType, Severity
        
        # Test 1: Logger initialization
        logger = TRIG6Logger(log_dir="/tmp/sagco_test_logs")
        test_result("Logger initialization", True)
        
        # Test 2: Log orchestration event
        logger.log_orchestration(
            theta=math.pi / 4,
            mode="trigonometric",
            alpha=0.0,
            agent_weights={"GPT": 0.7, "Claude": 0.7},
            metrics={"resonance": 0.8, "drift": 0.2, "noise": 0.1}
        )
        test_result(
            "Log orchestration event",
            len(logger.events) > 0
        )
        
        # Test 3: Log danger zone
        logger.log_danger_zone(
            theta=math.pi / 2,
            agents=["Grok", "Web"],
            singularities=["tan at π/2", "sec at π/2"]
        )
        test_result(
            "Log danger zone warning",
            any(e.event_type == EventType.DANGER_ZONE for e in logger.events)
        )
        
        # Test 4: Event filtering
        warnings = logger.get_events(severity=Severity.WARNING)
        test_result(
            "Event filtering",
            len(warnings) > 0
        )
        
        # Test 5: Metrics summary
        logger.log_metric_update(math.pi / 4, {"resonance": 0.9, "drift": 0.15})
        summary = logger.get_metrics_summary()
        test_result(
            "Metrics aggregation",
            "sample_count" in summary
        )
        
        print(f"\nLogger Tests: {sum(1 for _, p, _ in test_results[-5:] if p)}/5 passed")
        
    except Exception as e:
        test_result("Logger System", False, str(e))


def print_summary():
    """Print test summary"""
    print("\n" + "=" * 80)
    print("SAGCO-OS Integration Test Summary")
    print("=" * 80)
    
    total = len(test_results)
    passed = sum(1 for _, p, _ in test_results if p)
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ({100 * passed / total:.1f}%)")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed Tests:")
        for name, passed, message in test_results:
            if not passed:
                print(f"  - {name}")
                if message:
                    print(f"    {message}")
    
    print("\n" + "=" * 80)
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


def main():
    """Run all integration tests"""
    print("=" * 80)
    print("SAGCO-OS Integration Test Suite")
    print("Testing Patent Claims Implementation")
    print("=" * 80)
    
    # Run test suites
    test_trig6_system()
    test_neurograph_system()
    test_dna_system()
    test_logger_system()
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()
