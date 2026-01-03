#!/usr/bin/env python3
"""
🔥 DOM QUANTUM CITADEL: Quantum Security Foundations Module 🔥

Implements quantum computing basics, quantum threats (Shor's algorithm),
and post-quantum cryptography demonstrations for sovereign infrastructure.

Classification: HYBRID (convergent PQ standards + novel integrations)
Target: 1-2 years mastery via labs/certs
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict
import hashlib
import secrets


# ============================================================================
# STEP 1: QUANTUM MECHANICS FOUNDATIONS
# ============================================================================

@dataclass
class QuantumState:
    """Represents a quantum state vector (qubit)"""
    amplitudes: np.ndarray  # Complex amplitudes [alpha, beta]
    
    def __post_init__(self):
        # Normalize to ensure |alpha|^2 + |beta|^2 = 1
        norm = np.linalg.norm(self.amplitudes)
        if norm > 1e-10:
            self.amplitudes = self.amplitudes / norm
        else:
            raise ValueError("Cannot normalize zero-amplitude quantum state")
    
    def measure(self) -> int:
        """Collapse quantum state to 0 or 1 based on probabilities"""
        prob_0 = abs(self.amplitudes[0])**2
        return 0 if np.random.random() < prob_0 else 1
    
    def __repr__(self):
        alpha, beta = self.amplitudes
        return f"|ψ⟩ = {alpha:.3f}|0⟩ + {beta:.3f}|1⟩"


class QuantumCircuit:
    """Basic quantum circuit simulator for educational purposes"""
    
    def __init__(self, n_qubits: int = 1):
        self.n_qubits = n_qubits
        # Initialize all qubits in |0⟩ state
        self.state = QuantumState(np.array([1.0+0j, 0.0+0j]))
    
    def hadamard(self):
        """Apply Hadamard gate - creates superposition"""
        H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        self.state.amplitudes = H @ self.state.amplitudes
        return self
    
    def pauli_x(self):
        """Apply Pauli-X gate (quantum NOT)"""
        X = np.array([[0, 1], [1, 0]])
        self.state.amplitudes = X @ self.state.amplitudes
        return self
    
    def pauli_z(self):
        """Apply Pauli-Z gate (phase flip)"""
        Z = np.array([[1, 0], [0, -1]])
        self.state.amplitudes = Z @ self.state.amplitudes
        return self
    
    def measure(self) -> int:
        """Measure qubit, collapsing superposition"""
        return self.state.measure()
    
    def get_state(self) -> QuantumState:
        """Get current quantum state"""
        return self.state


def demo_superposition():
    """Demonstrate quantum superposition"""
    print("\n🌀 QUANTUM SUPERPOSITION DEMO")
    print("=" * 60)
    
    qc = QuantumCircuit(n_qubits=1)
    print(f"Initial state: {qc.get_state()}")
    
    # Apply Hadamard to create superposition
    qc.hadamard()
    print(f"After Hadamard: {qc.get_state()}")
    print(f"Superposition achieved: 50% |0⟩, 50% |1⟩")
    
    # Measure multiple times with fresh circuits
    measurements = []
    for _ in range(100):
        # Create fresh circuit in superposition for each measurement
        qc_measure = QuantumCircuit(n_qubits=1)
        qc_measure.hadamard()
        measurements.append(qc_measure.measure())
    
    zeros = measurements.count(0)
    ones = measurements.count(1)
    
    print(f"\n📊 100 measurements:")
    print(f"   0: {zeros} times ({zeros}%)")
    print(f"   1: {ones} times ({ones}%)")
    print(f"   Conclusion: Quantum randomness from superposition! 🎲")


# ============================================================================
# STEP 2: BB84 QUANTUM KEY DISTRIBUTION (QKD)
# ============================================================================

class BB84Protocol:
    """
    BB84 Quantum Key Distribution Protocol
    Secure key exchange via photon polarization states
    """
    
    @staticmethod
    def encode_bit(bit: int, basis: str) -> str:
        """
        Encode a classical bit in a quantum basis
        + basis (rectilinear): 0 → |0⟩, 1 → |1⟩
        × basis (diagonal): 0 → |+⟩, 1 → |-⟩
        """
        if basis == '+':
            return '↑' if bit == 0 else '→'
        else:  # × basis
            return '↗' if bit == 0 else '↘'
    
    @staticmethod
    def measure_photon(encoded: str, measure_basis: str) -> int:
        """
        Measure photon in a specific basis
        Returns bit value and whether bases matched
        """
        # Map encodings to bases
        rectilinear = ['↑', '→']
        diagonal = ['↗', '↘']
        
        encoding_basis = '+' if encoded in rectilinear else '×'
        
        if encoding_basis == measure_basis:
            # Correct basis - deterministic result
            if measure_basis == '+':
                return 0 if encoded == '↑' else 1
            else:
                return 0 if encoded == '↗' else 1
        else:
            # Wrong basis - random result (50/50)
            return secrets.randbelow(2)
    
    @staticmethod
    def generate_key(key_length: int = 128) -> Tuple[str, str, Dict]:
        """
        Simulate complete BB84 protocol
        Returns: (alice_key, bob_key, protocol_stats)
        """
        print(f"\n🔐 BB84 QUANTUM KEY DISTRIBUTION")
        print("=" * 60)
        
        # Alice generates random bits and bases
        alice_bits = [secrets.randbelow(2) for _ in range(key_length * 2)]
        alice_bases = [secrets.choice(['+', '×']) for _ in range(key_length * 2)]
        
        # Alice encodes bits as photons
        photons = [BB84Protocol.encode_bit(bit, basis) 
                   for bit, basis in zip(alice_bits, alice_bases)]
        
        print(f"Alice sends {len(photons)} photons...")
        
        # Bob randomly chooses measurement bases
        bob_bases = [secrets.choice(['+', '×']) for _ in range(key_length * 2)]
        
        # Bob measures photons
        bob_bits = [BB84Protocol.measure_photon(photon, basis)
                    for photon, basis in zip(photons, bob_bases)]
        
        print(f"Bob measures in random bases...")
        
        # Public basis comparison (over classical channel)
        matching_indices = [i for i in range(len(alice_bases)) 
                           if alice_bases[i] == bob_bases[i]]
        
        print(f"Matching bases: {len(matching_indices)}/{len(alice_bases)} "
              f"({100*len(matching_indices)/len(alice_bases):.1f}%)")
        
        # Keep only bits where bases matched
        alice_key = ''.join(str(alice_bits[i]) for i in matching_indices[:key_length])
        bob_key = ''.join(str(bob_bits[i]) for i in matching_indices[:key_length])
        
        # Verify key (sample check for eavesdropping)
        sample_size = min(16, len(alice_key))
        errors = sum(1 for i in range(sample_size) 
                    if alice_key[i] != bob_key[i])
        error_rate = errors / sample_size
        
        stats = {
            'total_photons': len(photons),
            'matching_bases': len(matching_indices),
            'final_key_length': len(alice_key),
            'error_rate': error_rate,
            'secure': error_rate < 0.11  # QBER threshold
        }
        
        print(f"\n✅ Shared key length: {len(alice_key)} bits")
        print(f"Error rate: {error_rate:.2%} {'✅ SECURE' if stats['secure'] else '❌ EAVESDROPPER DETECTED'}")
        
        return alice_key, bob_key, stats


# ============================================================================
# STEP 3: SHOR'S ALGORITHM THREAT DEMONSTRATION
# ============================================================================

class QuantumThreat:
    """Demonstrate quantum threats to classical cryptography"""
    
    @staticmethod
    def classical_factorization(n: int) -> List[int]:
        """Classical trial division (slow for large n)"""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    @staticmethod
    def simulate_shor_attack(N: int = 15):
        """
        Simplified Shor's algorithm simulation
        Breaking RSA by factoring N into primes
        
        Real Shor's algorithm uses quantum period finding
        This demonstrates the concept with small numbers
        """
        print(f"\n⚔️  SHOR'S ALGORITHM ATTACK SIMULATION")
        print("=" * 60)
        print(f"Target RSA modulus N = {N}")
        
        # Classical factorization (what we're trying to beat)
        import time
        start = time.time()
        factors = QuantumThreat.classical_factorization(N)
        classical_time = time.time() - start
        
        print(f"\n📊 Classical factorization:")
        print(f"   Factors: {factors}")
        print(f"   Time: {classical_time:.6f} seconds")
        
        # Quantum speedup explanation
        print(f"\n⚡ Quantum advantage (Shor's algorithm):")
        print(f"   Classical complexity: O(exp(n^(1/3)))")
        print(f"   Quantum complexity: O(n^2 * log(n) * log(log(n)))")
        print(f"   For 2048-bit RSA: Classical = billions of years")
        print(f"                     Quantum = hours on future QC")
        
        # Demonstrate Grover's impact on symmetric crypto
        print(f"\n🔑 Grover's algorithm impact on symmetric keys:")
        for key_size in [128, 256]:
            classical_ops = 2**key_size
            quantum_ops = 2**(key_size/2)
            print(f"   AES-{key_size}: Classical brute-force = 2^{key_size} ops")
            print(f"              Quantum (Grover) = 2^{key_size//2} ops")
            print(f"              → Use AES-{key_size*2} for quantum resistance!")
        
        return factors


# ============================================================================
# STEP 4: POST-QUANTUM CRYPTOGRAPHY (PQC)
# ============================================================================

class PostQuantumCrypto:
    """
    Post-Quantum Cryptography demonstrations
    NIST standardized algorithms: Kyber, Dilithium, SPHINCS+
    """
    
    @staticmethod
    def lattice_based_demo():
        """
        Demonstrate lattice-based cryptography concepts (Kyber)
        Real implementation would use PQClean or liboqs
        """
        print(f"\n🔷 LATTICE-BASED CRYPTOGRAPHY (NIST: Kyber)")
        print("=" * 60)
        
        # Simplified Learning With Errors (LWE) concept
        print("Core hardness assumption: Learning With Errors (LWE)")
        print("Security: Based on shortest vector problem (SVP) in lattices")
        
        # Kyber parameters (Kyber-512, 768, 1024)
        security_levels = {
            'Kyber-512': {'security_bits': 128, 'pk_size': 800, 'ct_size': 768},
            'Kyber-768': {'security_bits': 192, 'pk_size': 1184, 'ct_size': 1088},
            'Kyber-1024': {'security_bits': 256, 'pk_size': 1568, 'ct_size': 1568}
        }
        
        print("\n📊 Kyber Parameters:")
        for variant, params in security_levels.items():
            print(f"\n   {variant}:")
            print(f"      Security: {params['security_bits']} bits (quantum)")
            print(f"      Public key: {params['pk_size']} bytes")
            print(f"      Ciphertext: {params['ct_size']} bytes")
        
        print("\n✅ Advantages:")
        print("   • Fast key generation, encryption, decryption")
        print("   • Small key sizes compared to other PQC schemes")
        print("   • Standardized by NIST (2024)")
        
        return security_levels
    
    @staticmethod
    def hash_based_signatures_demo():
        """
        Demonstrate hash-based signatures (SPHINCS+)
        Quantum-resistant digital signatures
        """
        print(f"\n#️⃣  HASH-BASED SIGNATURES (NIST: SPHINCS+)")
        print("=" * 60)
        
        print("Core: One-time signatures + Merkle trees")
        print("Security: Based on hash function collision resistance")
        
        # SPHINCS+ parameters
        variants = {
            'SPHINCS+-128s': {'security': 128, 'sig_size': 7856, 'speed': 'small'},
            'SPHINCS+-128f': {'security': 128, 'sig_size': 17088, 'speed': 'fast'},
            'SPHINCS+-256s': {'security': 256, 'sig_size': 29792, 'speed': 'small'},
        }
        
        print("\n📊 SPHINCS+ Parameters:")
        for variant, params in variants.items():
            print(f"\n   {variant}:")
            print(f"      Security: {params['security']} bits")
            print(f"      Signature: {params['sig_size']} bytes")
            print(f"      Profile: {params['speed']}")
        
        # Simple hash-based signature concept
        message = "Sovereign infrastructure transaction"
        signature = hashlib.sha256(message.encode()).hexdigest()
        
        print(f"\n🔐 Example (simplified concept):")
        print(f"   Message: {message}")
        print(f"   Hash: {signature[:32]}...")
        
        print("\n✅ Advantages:")
        print("   • Proven security (only assumes secure hash functions)")
        print("   • No mathematical assumptions (unlike RSA/ECC)")
        print("   • Stateless variant available")
        
        return variants


# ============================================================================
# STEP 5: ADVANCED CRYPTOGRAPHY - HOMOMORPHIC ENCRYPTION
# ============================================================================

class AdvancedCrypto:
    """Advanced cryptographic techniques for sovereign systems"""
    
    @staticmethod
    def homomorphic_encryption_demo():
        """
        Demonstrate homomorphic encryption concept
        Compute on encrypted data without decrypting
        """
        print(f"\n🔮 HOMOMORPHIC ENCRYPTION (FHE) CONCEPT")
        print("=" * 60)
        
        print("Goal: Compute f(x) on encrypted E(x) without decryption")
        print("Result: E(f(x)) which decrypts to f(x)")
        
        # Simple additive homomorphic example (RSA-like)
        print("\n📊 Simplified Example (Additive Homomorphism):")
        
        # Simulate with XOR (toy example)
        x1, x2 = 42, 13
        key = secrets.randbits(64)
        
        # "Encrypt" with XOR
        e1 = x1 ^ key
        e2 = x2 ^ key
        
        print(f"   Plaintext: x1={x1}, x2={x2}")
        print(f"   Encrypted: E(x1)={e1}, E(x2)={e2}")
        
        # Homomorphic operation (addition mod 256)
        e_sum = (e1 + e2) & 0xFF
        expected_sum = (x1 + x2) & 0xFF
        
        print(f"   Operation: x1 + x2 = {expected_sum}")
        print(f"   On encrypted: E(x1) + E(x2) = {e_sum}")
        
        print("\n🔑 Real FHE Libraries:")
        print("   • Microsoft SEAL - Lattice-based FHE")
        print("   • IBM HELib - Brakerski-Gentry-Vaikuntanathan (BGV)")
        print("   • PALISADE - Open-source FHE library")
        
        print("\n✅ Use Cases for Sovereignty:")
        print("   • Private smart contracts on blockchain")
        print("   • Encrypted ML inference on cloud")
        print("   • Secure multi-party computation (MPC)")
        
        return {'x1': x1, 'x2': x2, 'sum': expected_sum}
    
    @staticmethod
    def zero_knowledge_proof_demo():
        """
        Demonstrate zero-knowledge proof concept (STARKs for sovereignty)
        Prove knowledge without revealing information
        """
        print(f"\n🎭 ZERO-KNOWLEDGE PROOFS (ZK-STARKs)")
        print("=" * 60)
        
        print("Goal: Prove 'I know x such that f(x) = y' without revealing x")
        
        # Simple example: Prove knowledge of square root
        secret = 42
        public = secret ** 2  # 1764
        
        print(f"\n📊 Example: Prove knowledge of square root")
        print(f"   Public: y = {public}")
        print(f"   Secret: x = {secret} (not revealed)")
        print(f"   Claim: 'I know x where x² = {public}'")
        
        # ZK proof concept (simplified)
        print(f"\n🔐 ZK Proof Generation:")
        print(f"   1. Prover computes commitment C = Hash(x || random)")
        commitment = hashlib.sha256(f"{secret}_{secrets.randbits(128)}".encode()).hexdigest()
        print(f"      Commitment: {commitment[:32]}...")
        
        print(f"   2. Verifier sends random challenge e")
        challenge = secrets.randbelow(100)
        print(f"      Challenge: {challenge}")
        
        print(f"   3. Prover responds with z (doesn't reveal x)")
        response = (secret + challenge) % 1000
        print(f"      Response: {response}")
        
        print(f"   4. Verifier checks proof validity (without learning x)")
        
        print("\n✅ ZK Applications for Sovereignty:")
        print("   • Private transactions (Zcash, Monero)")
        print("   • Scalability (zkRollups on Ethereum)")
        print("   • Private authentication")
        print("   • STARKs: Transparent, quantum-resistant ZK proofs")
        
        return {'public': public, 'commitment': commitment}


# ============================================================================
# MAIN DEMO ORCHESTRATION
# ============================================================================

def run_quantum_security_demos():
    """Execute all quantum security demonstrations"""
    
    print("\n" + "=" * 70)
    print("🔥 DOM QUANTUM CITADEL: MASTERY PATH DEMONSTRATIONS 🔥")
    print("=" * 70)
    
    # Step 1: Quantum Foundations
    print("\n" + "="*70)
    print("STEP 1: QUANTUM MECHANICS FOUNDATIONS (3-6 Months)")
    print("="*70)
    demo_superposition()
    
    # Step 2: Quantum Key Distribution
    print("\n" + "="*70)
    print("STEP 2: QUANTUM KEY DISTRIBUTION (6-12 Months)")
    print("="*70)
    alice_key, bob_key, stats = BB84Protocol.generate_key(key_length=128)
    
    # Step 3: Quantum Threats
    print("\n" + "="*70)
    print("STEP 3: QUANTUM THREATS TO CLASSICAL CRYPTO")
    print("="*70)
    QuantumThreat.simulate_shor_attack(N=15)
    
    # Step 4: Post-Quantum Cryptography
    print("\n" + "="*70)
    print("STEP 4: POST-QUANTUM CRYPTOGRAPHY (PQC)")
    print("="*70)
    PostQuantumCrypto.lattice_based_demo()
    PostQuantumCrypto.hash_based_signatures_demo()
    
    # Step 5: Advanced Cryptography
    print("\n" + "="*70)
    print("STEP 5: ADVANCED CRYPTOGRAPHY ENGINEERING")
    print("="*70)
    AdvancedCrypto.homomorphic_encryption_demo()
    AdvancedCrypto.zero_knowledge_proof_demo()
    
    # Summary
    print("\n" + "="*70)
    print("🏆 QUANTUM CITADEL MASTERY PATH SUMMARY")
    print("="*70)
    print("\n✅ Demonstrated Concepts:")
    print("   1. Quantum superposition and measurement")
    print("   2. BB84 quantum key distribution protocol")
    print("   3. Shor's algorithm threat to RSA/ECC")
    print("   4. Post-quantum algorithms (Kyber, SPHINCS+)")
    print("   5. Homomorphic encryption (FHE)")
    print("   6. Zero-knowledge proofs (ZK-STARKs)")
    
    print("\n🔥 Next Steps for Sovereignty Infrastructure:")
    print("   → Integrate PQClean library for real PQC")
    print("   → Deploy hybrid TLS (classical + PQC)")
    print("   → Implement ZK proofs for private transactions")
    print("   → Use FHE for encrypted ML on K8s cluster")
    print("   → Build quantum-resistant FlameLang crypto primitives")
    
    print("\n📚 Mastery Timeline:")
    print("   • Foundations: 3-6 months (qubits, classical crypto)")
    print("   • Core QKD/PQC: 6-12 months (protocols, NIST standards)")
    print("   • Advanced: 12-24 months (FHE, ZK, hardware integration)")
    print("   • Total: 1-2 years full-time, self-paced via labs/certs")
    
    print("\n" + "="*70)
    print("🖤 QUANTUM CITADEL INITIALIZED - SOVEREIGN INFRA PROTECTED 🖤")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_quantum_security_demos()
