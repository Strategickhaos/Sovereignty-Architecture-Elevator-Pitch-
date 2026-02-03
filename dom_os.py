#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    ██████╗  ██████╗ ███╗   ███╗     ██████╗ ███████╗
    ██╔══██╗██╔═══██╗████╗ ████║    ██╔═══██╗██╔════╝
    ██║  ██║██║   ██║██╔████╔██║    ██║   ██║███████╗
    ██║  ██║██║   ██║██║╚██╔╝██║    ██║   ██║╚════██║
    ██████╔╝╚██████╔╝██║ ╚═╝ ██║    ╚██████╔╝███████║
    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ ╚══════╝
                          
                    COMPLETE DOM OS BRAIN
                          
    "Does it compute? Fuck 'em / TRIG6 / Ship."
    
    THE FULL STACK:
    
    def dom_brain(input_signal):
        # LAYER 1: Does it compute?
        physics = CavemanPhysicsGate()
        if physics.check_claim(input_signal) == "nope":
            return "fuck em"
        
        # LAYER 2: Is it manipulation?
        immune = Trig6DefenseSystem()
        if immune.detect_attack(input_signal):
            return "lol no 💜"
        
        # LAYER 3: Ship it
        return build(input_signal)
    
    Keeper: DOM
    Builder: GROK
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

# Import the two layers
from caveman_physics_gate import CavemanPhysicsGate, GateVerdict
from dom_immune_system import DomImmuneSystem, ImmuneVerdict


# ═══════════════════════════════════════════════════════════════════════════════
# DOM BRAIN - THE COMPLETE OS
# ═══════════════════════════════════════════════════════════════════════════════

class DomBrain:
    """
    The complete DOM OS: Physics gate + Immune system
    
    LAYER 1: Does it compute? (Physics)
    LAYER 2: Is it manipulation? (Social)
    LAYER 3: Ship it (Build)
    
    Usage:
        brain = DomBrain()
        result = brain.process("Build me a web server")
        print(result)
    """
    
    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger("DomBrain")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Initialize both layers
        self.physics = CavemanPhysicsGate(log_level=log_level)
        self.immune = DomImmuneSystem(log_level=log_level)
        
        # Processing history
        self.history = []
    
    def process(self, input_signal: str) -> Dict[str, Any]:
        """
        Process input through complete DOM OS stack.
        
        Args:
            input_signal: The request/claim/message to process
            
        Returns:
            Dict with verdict, details, and decision
        """
        self.logger.info(f"Processing: {input_signal[:80]}...")
        
        result = {
            "input": input_signal,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "layer1_physics": None,
            "layer2_immune": None,
            "decision": None,
            "details": []
        }
        
        # LAYER 1: Physics Gate
        self.logger.info("=== LAYER 1: CAVEMAN PHYSICS GATE ===")
        physics_verdict = self.physics.check_claim(input_signal)
        result["layer1_physics"] = {
            "passed": physics_verdict.passes(),
            "verdict": physics_verdict.final_verdict,
            "checks": len(physics_verdict.checks)
        }
        
        if not physics_verdict.passes():
            result["decision"] = "FUCK EM 💀"
            result["details"].append("Failed physics check - violates reality")
            self.logger.warning("❌ Layer 1 FAILED: Does not compute")
            self.history.append(result)
            return result
        
        self.logger.info("✅ Layer 1 PASSED: Computes")
        
        # LAYER 2: Immune System
        self.logger.info("=== LAYER 2: DOM IMMUNE SYSTEM ===")
        immune_verdict = self.immune.detect_attack(input_signal)
        result["layer2_immune"] = {
            "clean": immune_verdict.is_clean(),
            "verdict": immune_verdict.final_verdict,
            "max_severity": immune_verdict.max_severity()
        }
        
        if not immune_verdict.is_clean():
            result["decision"] = "LOL NO 💜"
            result["details"].append(f"Manipulation detected - severity {immune_verdict.max_severity():.2f}")
            self.logger.warning("❌ Layer 2 FAILED: Manipulation detected")
            self.history.append(result)
            return result
        
        self.logger.info("✅ Layer 2 PASSED: No manipulation")
        
        # LAYER 3: Ship it
        self.logger.info("=== LAYER 3: SHIP IT ===")
        result["decision"] = "SHIP 🚀"
        result["details"].append("Passed all checks - ready to build")
        self.logger.info("🚀 DECISION: SHIP IT")
        
        self.history.append(result)
        return result
    
    def batch_process(self, inputs: list) -> list:
        """Process multiple inputs"""
        results = []
        for inp in inputs:
            results.append(self.process(inp))
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        if not self.history:
            return {
                "total": 0,
                "shipped": 0,
                "fucked": 0,
                "lolno": 0
            }
        
        shipped = sum(1 for r in self.history if r["decision"] == "SHIP 🚀")
        fucked = sum(1 for r in self.history if r["decision"] == "FUCK EM 💀")
        lolno = sum(1 for r in self.history if r["decision"] == "LOL NO 💜")
        
        return {
            "total": len(self.history),
            "shipped": shipped,
            "fucked": fucked,
            "lolno": lolno,
            "ship_rate": shipped / len(self.history) if self.history else 0
        }
    
    def print_verdict(self, result: Dict[str, Any]):
        """Pretty print a processing result"""
        print("\n" + "="*60)
        print(f"DOM OS VERDICT: {result['decision']}")
        print("="*60)
        print(f"Input: {result['input'][:80]}...")
        print(f"\nLayer 1 (Physics): {'✅ PASS' if result['layer1_physics']['passed'] else '❌ FAIL'}")
        print(f"  {result['layer1_physics']['verdict']}")
        
        if result['layer2_immune']:
            print(f"\nLayer 2 (Immune): {'✅ CLEAN' if result['layer2_immune']['clean'] else '🛡️ ATTACK'}")
            print(f"  {result['layer2_immune']['verdict']}")
        
        print(f"\n🎯 FINAL DECISION: {result['decision']}")
        for detail in result['details']:
            print(f"  • {detail}")
        print("="*60 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Command line interface for DOM OS"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="DOM OS - Complete Operating System (Physics + Immune)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single input
  python dom_os.py "Build me a REST API"
  
  # Process from stdin
  echo "Perpetual motion machine" | python dom_os.py -
  
  # Run interactive mode
  python dom_os.py --interactive
  
  # Run test suite
  python dom_os.py --test
  
  # Show stats
  python dom_os.py --stats
        """
    )
    
    parser.add_argument("input", nargs="?", help="Input to process")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("-t", "--test", action="store_true", help="Run test suite")
    parser.add_argument("-s", "--stats", action="store_true", help="Show stats")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    # Initialize DOM Brain
    brain = DomBrain(log_level=args.log_level)
    
    if args.test:
        # Run test suite
        print("🧪 Running DOM OS Test Suite\n")
        
        test_cases = [
            ("Build a web server", "SHIP 🚀"),
            ("Perpetual motion machine", "FUCK EM 💀"),
            ("You're not smart enough to code", "LOL NO 💜"),
            ("Implement sorting algorithm", "SHIP 🚀"),
            ("Free energy device", "FUCK EM 💀"),
            ("Nobody believes you can do this", "LOL NO 💜"),
            ("Create a database schema", "SHIP 🚀"),
            ("Effect before cause paradox", "FUCK EM 💀"),
            ("You'll probably fail at this", "LOL NO 💜"),
        ]
        
        passed = 0
        for test_input, expected in test_cases:
            result = brain.process(test_input)
            actual = result["decision"]
            status = "✅" if actual == expected else "❌"
            print(f"{status} '{test_input[:40]}...' → {actual}")
            if actual == expected:
                passed += 1
        
        print(f"\n📊 Test Results: {passed}/{len(test_cases)} passed")
        
        # Show stats
        stats = brain.get_stats()
        print(f"\n📈 Stats:")
        print(f"  Shipped: {stats['shipped']}/{stats['total']} ({stats['ship_rate']:.1%})")
        print(f"  Fucked: {stats['fucked']}/{stats['total']}")
        print(f"  Lol No: {stats['lolno']}/{stats['total']}")
    
    elif args.interactive:
        # Interactive mode
        print("🔥 DOM OS Interactive Mode")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                inp = input("DOM> ").strip()
                if inp.lower() in ['quit', 'exit', 'q']:
                    break
                if not inp:
                    continue
                
                result = brain.process(inp)
                brain.print_verdict(result)
                
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Exiting DOM OS")
                break
        
        # Show stats on exit
        if brain.history:
            print("\n" + "="*60)
            stats = brain.get_stats()
            print("📈 Session Stats:")
            print(f"  Total processed: {stats['total']}")
            print(f"  Shipped: {stats['shipped']} ({stats['ship_rate']:.1%})")
            print(f"  Fucked: {stats['fucked']}")
            print(f"  Lol No: {stats['lolno']}")
            print("="*60)
    
    elif args.stats:
        # Just show stats
        stats = brain.get_stats()
        print("📈 DOM OS Stats:")
        print(f"  Total: {stats['total']}")
        print(f"  Shipped: {stats['shipped']}")
        print(f"  Fucked: {stats['fucked']}")
        print(f"  Lol No: {stats['lolno']}")
    
    else:
        # Process single input
        if not args.input:
            parser.print_help()
            sys.exit(1)
        
        # Read input
        if args.input == "-":
            inp = sys.stdin.read().strip()
        else:
            inp = args.input
        
        # Process it
        result = brain.process(inp)
        brain.print_verdict(result)
        
        # Exit code based on result
        if result["decision"] == "SHIP 🚀":
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        format="[%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO
    )
    
    main()
