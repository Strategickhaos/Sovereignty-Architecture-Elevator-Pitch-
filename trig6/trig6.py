#!/usr/bin/env python3
"""
TRIG6 CLI - Trigonometric Computation Engine
Sovereign, offline mathematical operations for the Strategickhaos ecosystem.
"""
import argparse
import json
import math
import sys
from pathlib import Path


class TRIG6:
    """TRIG6 - Trigonometric Reasoning and Inference Geometric Engine"""
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.constants_dir = Path(__file__).parent / "constants"
        
    def bridle(self, angle_degrees: float, operation: str = "sin") -> dict:
        """
        Calculate trigonometric values (bridle calculations)
        
        Args:
            angle_degrees: Angle in degrees
            operation: sin, cos, tan, or all
            
        Returns:
            Dictionary with calculated values
        """
        angle_rad = math.radians(angle_degrees)
        
        results = {
            "angle_degrees": angle_degrees,
            "angle_radians": angle_rad,
            "timestamp": None,  # Would use datetime if needed
        }
        
        if operation in ["sin", "all"]:
            results["sin"] = math.sin(angle_rad)
        if operation in ["cos", "all"]:
            results["cos"] = math.cos(angle_rad)
        if operation in ["tan", "all"]:
            try:
                results["tan"] = math.tan(angle_rad)
            except:
                results["tan"] = "undefined"
                
        return results
    
    def explain(self, concept: str) -> str:
        """
        Explain TRIG6 concepts with citations
        
        Args:
            concept: The concept to explain
            
        Returns:
            Explanation text with citations
        """
        explanations = {
            "bridle": "Bridle calculations are sovereign trigonometric computations that operate offline without external dependencies. [TRIG6:CORE]",
            "sovereignty": "TRIG6 maintains computational sovereignty through pure Python mathematics with no vendor lock-in. [TRIG6:PHILOSOPHY]",
            "doctor": "The doctor module performs health checks and validation of TRIG6 operations. [TRIG6:MONITORING]"
        }
        
        return explanations.get(concept.lower(), f"Unknown concept: {concept}. Available: bridle, sovereignty, doctor")
    
    def cite(self, reference: str) -> dict:
        """
        Provide citation information for governance/audit
        
        Args:
            reference: Citation reference code
            
        Returns:
            Citation metadata
        """
        citations = {
            "TRIG6:CORE": {
                "source": "TRIG6 Core Specification v1.0",
                "type": "implementation",
                "sovereignty_level": "SOVEREIGN"
            },
            "TRIG6:PHILOSOPHY": {
                "source": "Zero Vendor Lock-in Principles (Invention #12)",
                "type": "philosophy",
                "sovereignty_level": "SOVEREIGN"
            },
            "TRIG6:MONITORING": {
                "source": "TRIG6 Doctor Module Specification",
                "type": "operational",
                "sovereignty_level": "SOVEREIGN"
            }
        }
        
        return citations.get(reference, {"error": f"Unknown reference: {reference}"})


def main():
    parser = argparse.ArgumentParser(
        description="TRIG6 - Sovereign Trigonometric Computation Engine"
    )
    parser.add_argument("command", choices=["bridle", "explain", "cite", "doctor", "version"])
    parser.add_argument("--angle", type=float, help="Angle in degrees for bridle")
    parser.add_argument("--operation", default="all", choices=["sin", "cos", "tan", "all"])
    parser.add_argument("--concept", help="Concept to explain")
    parser.add_argument("--reference", help="Citation reference")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    trig6 = TRIG6()
    
    if args.command == "version":
        result = {"version": TRIG6.VERSION, "name": "TRIG6"}
    elif args.command == "bridle":
        if args.angle is None:
            print("Error: --angle required for bridle command", file=sys.stderr)
            sys.exit(1)
        result = trig6.bridle(args.angle, args.operation)
    elif args.command == "explain":
        if args.concept is None:
            print("Error: --concept required for explain command", file=sys.stderr)
            sys.exit(1)
        result = trig6.explain(args.concept)
    elif args.command == "cite":
        if args.reference is None:
            print("Error: --reference required for cite command", file=sys.stderr)
            sys.exit(1)
        result = trig6.cite(args.reference)
    elif args.command == "doctor":
        # Import and run doctor module
        from doctor import Doctor
        doctor = Doctor()
        result = doctor.run()
    else:
        result = {"error": "Unknown command"}
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)


if __name__ == "__main__":
    main()
