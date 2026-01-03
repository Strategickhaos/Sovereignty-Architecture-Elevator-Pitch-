"""
MRVE Cryptographic Seal Module
Strategickhaos DAO LLC | INV-093

Provides cryptographic sealing using BLAKE2b for DNA sequences.
MRVE (Minimal Recursive Verification Engine) ensures data integrity.
"""

from hashlib import blake2b
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class MRVESeal:
    """Represents an MRVE cryptographic seal."""
    
    seal_id: str
    content_hash: str
    timestamp: str
    algorithm: str = "BLAKE2b-16"
    
    def __str__(self) -> str:
        return f"MRVE-SEAL-{self.seal_id}"
    
    def to_dict(self) -> dict:
        """Convert seal to dictionary."""
        return {
            'seal_id': self.seal_id,
            'content_hash': self.content_hash,
            'timestamp': self.timestamp,
            'algorithm': self.algorithm,
            'full_seal': str(self),
        }


def seal(dna: str, prefix: str = "MRVE") -> MRVESeal:
    """
    Create MRVE cryptographic seal for DNA sequence (Layer 4: C-Face).
    
    Uses BLAKE2b with 16-byte digest for compact yet secure sealing.
    
    Args:
        dna: DNA codon sequence to seal
        prefix: Prefix for seal identification (default: "MRVE")
        
    Returns:
        MRVESeal object containing seal information
        
    Example:
        >>> seal_obj = seal("AGC GCT GGA TGC TAA")
        >>> print(seal_obj)
        MRVE-SEAL-a1b2c3d4e5f6...
    """
    # Create content hash with MRVE prefix
    content_with_prefix = f"{prefix}:{dna}"
    
    # Generate BLAKE2b seal (16 bytes = 32 hex chars)
    seal_hash = blake2b(
        content_with_prefix.encode('utf-8'),
        digest_size=16
    ).hexdigest()
    
    # Generate content hash for verification
    content_hash = blake2b(
        dna.encode('utf-8'),
        digest_size=16
    ).hexdigest()
    
    # Create timestamp
    timestamp = datetime.now(timezone.utc).isoformat()
    
    return MRVESeal(
        seal_id=seal_hash,
        content_hash=content_hash,
        timestamp=timestamp,
    )


def verify_seal(dna: str, seal_obj: MRVESeal, prefix: str = "MRVE") -> bool:
    """
    Verify MRVE seal authenticity.
    
    Args:
        dna: DNA codon sequence to verify
        seal_obj: MRVESeal object to verify against
        prefix: Prefix used in seal generation
        
    Returns:
        True if seal is valid, False otherwise
        
    Example:
        >>> seal_obj = seal("AGC GCT GGA")
        >>> verify_seal("AGC GCT GGA", seal_obj)
        True
        >>> verify_seal("AGC GCT GGG", seal_obj)
        False
    """
    # Regenerate seal for comparison
    new_seal = seal(dna, prefix)
    
    # Verify seal ID matches
    return new_seal.seal_id == seal_obj.seal_id


def batch_seal(dna_sequences: list[str], prefix: str = "MRVE") -> list[MRVESeal]:
    """
    Create seals for multiple DNA sequences.
    
    Args:
        dna_sequences: List of DNA codon sequences
        prefix: Prefix for seal identification
        
    Returns:
        List of MRVESeal objects
    """
    return [seal(dna, prefix) for dna in dna_sequences]


def generate_seal_chain(dna_sequences: list[str]) -> dict:
    """
    Generate a chain of seals with dependencies.
    
    Each seal includes the previous seal's ID, creating a chain
    similar to blockchain structure.
    
    Args:
        dna_sequences: List of DNA codon sequences
        
    Returns:
        Dictionary with chain information
    """
    chain = []
    previous_seal_id = "GENESIS"
    
    for idx, dna in enumerate(dna_sequences):
        # Include previous seal in hash
        content_with_chain = f"{previous_seal_id}:{dna}"
        seal_hash = blake2b(
            content_with_chain.encode('utf-8'),
            digest_size=16
        ).hexdigest()
        
        seal_obj = MRVESeal(
            seal_id=seal_hash,
            content_hash=blake2b(dna.encode('utf-8'), digest_size=16).hexdigest(),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        chain.append({
            'index': idx,
            'seal': seal_obj.to_dict(),
            'previous_seal': previous_seal_id,
            'dna': dna,
        })
        
        previous_seal_id = seal_hash
    
    return {
        'chain': chain,
        'length': len(chain),
        'final_seal': previous_seal_id,
    }


def seal_to_hex(seal_obj: MRVESeal) -> str:
    """
    Convert seal to hexadecimal representation.
    
    Args:
        seal_obj: MRVESeal object
        
    Returns:
        Hexadecimal string representation
    """
    return seal_obj.seal_id


def seal_to_binary(seal_obj: MRVESeal) -> str:
    """
    Convert seal to binary representation.
    
    Args:
        seal_obj: MRVESeal object
        
    Returns:
        Binary string representation
    """
    # Convert hex seal to binary
    seal_bytes = bytes.fromhex(seal_obj.seal_id)
    binary = ''.join(format(byte, '08b') for byte in seal_bytes)
    return binary


if __name__ == "__main__":
    # Example usage
    dna_sequence = "AGC GCT GGA TGC TAA"
    
    print("=== MRVE Seal Example ===")
    print(f"DNA Sequence: {dna_sequence}")
    
    # Create seal
    seal_obj = seal(dna_sequence)
    print(f"\nSeal: {seal_obj}")
    print(f"Seal ID: {seal_obj.seal_id}")
    print(f"Content Hash: {seal_obj.content_hash}")
    print(f"Timestamp: {seal_obj.timestamp}")
    
    # Verify seal
    is_valid = verify_seal(dna_sequence, seal_obj)
    print(f"\nSeal Valid: {is_valid}")
    
    # Test with modified sequence
    modified_dna = "AGC GCT GGA TGC TAC"
    is_valid_modified = verify_seal(modified_dna, seal_obj)
    print(f"Modified DNA Valid: {is_valid_modified}")
