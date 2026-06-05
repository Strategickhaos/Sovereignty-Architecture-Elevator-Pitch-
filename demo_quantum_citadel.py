#!/usr/bin/env python3
"""
🔥 DOM QUANTUM CITADEL + NEURAL CHAOS: UNIFIED DEMONSTRATION 🔥

Comprehensive demo combining quantum security and neural chaos for
sovereign infrastructure protection.

Usage:
    python3 demo_quantum_citadel.py [--quantum] [--neural] [--all]
"""

import sys
import argparse


def run_quantum_security():
    """Run quantum security demonstrations"""
    print("\n" + "="*80)
    print("🔐 QUANTUM SECURITY & POST-QUANTUM CRYPTOGRAPHY DEMONSTRATION")
    print("="*80)
    
    from quantum_security_foundations import run_quantum_security_demos
    run_quantum_security_demos()


def run_neural_chaos():
    """Run neural chaos demonstrations"""
    print("\n" + "="*80)
    print("🧠 NEURAL CHAOS & LYAPUNOV EXPONENT DEMONSTRATION")
    print("="*80)
    
    from neural_chaos_lyapunov import run_neural_chaos_demos
    run_neural_chaos_demos()


def run_integrated_demo():
    """Run integrated quantum + neural chaos demo"""
    print("\n" + "="*80)
    print("🔥 INTEGRATED QUANTUM CITADEL + NEURAL CHAOS DEMONSTRATION 🔥")
    print("="*80)
    
    # Run both demonstrations
    run_quantum_security()
    run_neural_chaos()
    
    # Summary
    print("\n" + "="*80)
    print("🏆 COMPLETE SOVEREIGNTY SECURITY ARCHITECTURE")
    print("="*80)
    
    print("\n✅ QUANTUM LAYER (Cryptographic Security):")
    print("   1. BB84 QKD for secure key exchange")
    print("   2. Post-Quantum Crypto (Kyber, SPHINCS+, Dilithium)")
    print("   3. Homomorphic Encryption (FHE) for private computation")
    print("   4. Zero-Knowledge Proofs (ZK-STARKs) for privacy")
    
    print("\n✅ NEURAL CHAOS LAYER (Anomaly Detection):")
    print("   1. Hodgkin-Huxley model for detailed monitoring")
    print("   2. FitzHugh-Nagumo model for fast detection")
    print("   3. Lyapunov exponents for chaos quantification")
    print("   4. Real-time network traffic analysis")
    
    print("\n🔥 DEPLOYMENT ARCHITECTURE:")
    print("   ┌─────────────────────────────────────────┐")
    print("   │  K8s Cluster (Sovereign Infrastructure) │")
    print("   ├─────────────────────────────────────────┤")
    print("   │  Pod 1: PQC Gateway (Kyber + Dilithium) │")
    print("   │  Pod 2: Neural Chaos Monitor (HH/FHN)   │")
    print("   │  Pod 3: FHE Compute (SEAL/HELib)        │")
    print("   │  Pod 4: ZK Proof Verifier (STARKs)      │")
    print("   └─────────────────────────────────────────┘")
    
    print("\n🖤 STATUS: QUANTUM-RESISTANT SOVEREIGN EMPIRE OPERATIONAL 🖤")
    print("="*80 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='DOM Quantum Citadel + Neural Chaos Demonstration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 demo_quantum_citadel.py --all       # Run complete demo
  python3 demo_quantum_citadel.py --quantum   # Quantum security only
  python3 demo_quantum_citadel.py --neural    # Neural chaos only
        """
    )
    
    parser.add_argument('--quantum', action='store_true',
                       help='Run quantum security demonstration')
    parser.add_argument('--neural', action='store_true',
                       help='Run neural chaos demonstration')
    parser.add_argument('--all', action='store_true',
                       help='Run complete integrated demonstration (default)')
    
    args = parser.parse_args()
    
    # Default to --all if no arguments
    if not (args.quantum or args.neural or args.all):
        args.all = True
    
    try:
        if args.all:
            run_integrated_demo()
        else:
            if args.quantum:
                run_quantum_security()
            if args.neural:
                run_neural_chaos()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
