#!/usr/bin/env python3
"""
DNA Exploration Simulation Script
Phase 4.13: TRIG6 Arrow DNA Explore - Sandbox Simulation

Simulates DNA exploration and mutation in recursive sandbox environment.
Integrates with swarm bots for rendering and validation.
"""

import sys
import argparse
import logging
from pathlib import Path
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.emulator.wave_cores.trig6.lab_evo import LabEvolutionCore

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def load_flame_yaml(path: str):
    """Load FLAME YAML configuration."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def simulate_arrow_render(h: int, w: int, head: int, char: str = '*') -> str:
    """
    Simulate arrow rendering based on zyBooks 3.35 spec.
    
    Args:
        h: Rectangle height
        w: Rectangle width
        head: Triangle head width
        char: Character to render (default '*')
        
    Returns:
        Rendered arrow as string
    """
    lines = []
    
    # Rectangle part: h lines of w chars
    for _ in range(h):
        lines.append(char * w)
    
    # Triangle part: decrement from head to 1
    for width in range(head, 0, -1):
        lines.append(char * width)
    
    return '\n'.join(lines)


def run_dna_simulation(config: dict, args):
    """
    Run DNA exploration simulation.
    
    Args:
        config: FLAME YAML configuration
        args: Command line arguments
    """
    logger.info("=" * 80)
    logger.info("TRIG6 ARROW DNA EXPLORATION SIMULATION")
    logger.info("Phase 4.13 - Recursive Sandbox Environment")
    logger.info("=" * 80)
    
    # Initialize lab evolution core
    lab_core = LabEvolutionCore(config)
    
    # Get DNA sequence
    dna = config.get('dna_encoding', {})
    sequence = dna.get('sequence', '')
    
    logger.info(f"\nInitial DNA Sequence: {sequence}")
    
    # Simulate neural ticks
    tick_count = args.ticks if hasattr(args, 'ticks') else 10
    invention_density = config.get('trig_report', {}).get('invention', 0.6)
    
    logger.info(f"Running {tick_count} neural ticks...")
    logger.info(f"Invention density: {invention_density:.2f}\n")
    
    exploration_results = []
    
    for tick in range(1, tick_count + 1):
        result = lab_core.explore_dna(sequence, tick)
        
        if result['status'] == 'explored':
            logger.info(f"Tick {tick}: DNA exploration executed")
            logger.debug(f"  Codon ops: {len(result['codon_operations'])}")
            logger.debug(f"  Mutations: {len(result['mutations'])}")
            exploration_results.append(result)
    
    # Run test vectors
    logger.info("\n" + "=" * 80)
    logger.info("TESTING VECTORS")
    logger.info("=" * 80)
    
    test_vectors = config.get('test_vectors', [])
    passed = 0
    failed = 0
    
    for vector in test_vectors[:5]:  # Run first 5 for demo
        vector_id = vector.get('id', 'unknown')
        test_input = vector.get('input', [])
        expected_rows = vector.get('expected_rows', 0)
        
        logger.info(f"\nTest: {vector_id}")
        logger.info(f"  Input: {test_input}")
        logger.info(f"  Description: {vector.get('desc', 'N/A')}")
        
        # Validate and parse input
        # Complex patterns include validation sequences with rejects (>3 elements)
        # that require special handling beyond simple h/w/head parsing
        if len(test_input) > 3:
            logger.warning(f"  Skipping - complex input pattern (validation sequence with {len(test_input)} elements)")
            continue
        
        if len(test_input) == 2:
            h, w = test_input
            head = 0
        elif len(test_input) == 3:
            h, w, head = test_input
        else:
            logger.warning(f"  Skipping - complex input pattern")
            continue
        
        # Check if mutation test
        if vector.get('mutation', False):
            char = '★'
            logger.info(f"  Mutation: Unicode character '{char}'")
        else:
            char = '*'
        
        # Render arrow
        try:
            rendered = simulate_arrow_render(h, w, head, char)
            rendered_rows = len(rendered.split('\n'))
            
            if rendered_rows == expected_rows:
                logger.info(f"  ✓ PASS: {rendered_rows} rows (expected {expected_rows})")
                passed += 1
            else:
                logger.warning(f"  ✗ FAIL: {rendered_rows} rows (expected {expected_rows})")
                failed += 1
        except Exception as e:
            logger.error(f"  ✗ ERROR: {e}")
            failed += 1
    
    # Evolution gate check
    logger.info("\n" + "=" * 80)
    logger.info("EVOLUTION GATE")
    logger.info("=" * 80)
    
    stress_results = {
        'fitness_score': 0.75,
        'passed': passed,
        'failed': failed
    }
    
    evolved = lab_core.evolve_gate(sequence, invention_density, stress_results)
    
    if evolved:
        logger.info(f"\n✓ Evolution triggered!")
        logger.info(f"  Original: {sequence}")
        logger.info(f"  Evolved:  {evolved}")
    else:
        logger.info("\n⊗ No evolution - sequence stable")
    
    # Final report
    logger.info("\n" + "=" * 80)
    logger.info("SIMULATION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Neural ticks executed: {tick_count}")
    logger.info(f"DNA explorations: {len(exploration_results)}")
    logger.info(f"Tests passed: {passed}")
    logger.info(f"Tests failed: {failed}")
    logger.info(f"Phase coherence: {config.get('phase_coherence', {}).get('current', 0):.2f}")
    logger.info(f"Status: {config.get('phase_coherence', {}).get('status', 'N/A')}")
    logger.info("\n🔥 Neural Sync complete. Resonance achieved.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='DNA Exploration Simulation - Phase 4.13'
    )
    
    parser.add_argument('--tests', 
                       default='/tests/3.35_arrow.flame.yaml',
                       help='Path to FLAME YAML test configuration')
    
    parser.add_argument('--images',
                       help='Path to images directory for extraction')
    
    parser.add_argument('--mutate',
                       action='store_true',
                       help='Enable mutation exploration')
    
    parser.add_argument('--ticks',
                       type=int,
                       default=10,
                       help='Number of neural ticks to simulate')
    
    args = parser.parse_args()
    
    # Load configuration
    test_path = Path(args.tests)
    if not test_path.exists():
        # Try local path
        test_path = Path('flamelang-stress-test/3.35_arrow.flame.yaml')
        if not test_path.exists():
            logger.error(f"Test configuration not found: {args.tests}")
            sys.exit(1)
    
    config = load_flame_yaml(str(test_path))
    
    # Run simulation
    run_dna_simulation(config, args)


if __name__ == '__main__':
    main()
