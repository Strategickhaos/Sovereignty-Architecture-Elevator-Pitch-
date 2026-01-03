#!/usr/bin/env python3
"""
FlameTranscribe_SAGCO Main Pipeline
Strategickhaos DAO LLC | INV-093

Main pipeline orchestrator for DNA transcription with hex, binary,
sealing, and NFT generation capabilities.

Functor Chain:
English/Hebrew → DNA → Hex → Binary → MRVE Seal → NFT Hash
"""

import sys
import argparse
from typing import Optional

# Support both package and direct execution
try:
    from .codon_map import (
        transcribe_to_dna,
        dna_to_text,
        get_codon_info,
        SAGCO_REFERENCE,
    )
    from .mrve_seal import seal, verify_seal, MRVESeal
    from .nft_algo import generate_nft_id, verify_nft, quantum_state_stub, NFT
except ImportError:
    from codon_map import (
        transcribe_to_dna,
        dna_to_text,
        get_codon_info,
        SAGCO_REFERENCE,
    )
    from mrve_seal import seal, verify_seal, MRVESeal
    from nft_algo import generate_nft_id, verify_nft, quantum_state_stub, NFT


class FlameTranscribe:
    """
    Main pipeline class for FlameTranscribe_SAGCO.
    
    Implements the complete functor chain from text to NFT.
    """
    
    def __init__(self, content: str):
        """
        Initialize pipeline with content.
        
        Args:
            content: Input text to process
        """
        self.content = content
        self.dna: Optional[str] = None
        self.hex_encoding: Optional[str] = None
        self.binary_encoding: Optional[str] = None
        self.seal: Optional[MRVESeal] = None
        self.nft: Optional[NFT] = None
        self.quantum_state: Optional[str] = None
    
    def transcribe(self) -> str:
        """
        Layer 1: DNA Transcription (S-Face).
        
        Returns:
            DNA codon sequence
        """
        self.dna = transcribe_to_dna(self.content)
        return self.dna
    
    def to_hex(self) -> str:
        """
        Layer 2: Hex Encoding (A-Face).
        
        Returns:
            Hexadecimal representation
        """
        if not self.dna:
            self.transcribe()
        
        # Convert DNA string to hex
        dna_clean = self.dna.replace(' ', '')
        hex_values = [hex(ord(c))[2:].upper() for c in dna_clean]
        self.hex_encoding = ' '.join(hex_values)
        return self.hex_encoding
    
    def to_binary(self) -> str:
        """
        Layer 3: Binary Encoding (G-Face).
        
        Returns:
            Binary representation
        """
        if not self.dna:
            self.transcribe()
        
        # Convert DNA string to binary
        dna_clean = self.dna.replace(' ', '')
        binary_values = [bin(ord(c))[2:].zfill(8) for c in dna_clean]
        self.binary_encoding = ' '.join(binary_values)
        return self.binary_encoding
    
    def create_seal(self) -> MRVESeal:
        """
        Layer 4: MRVE Seal (C-Face).
        
        Returns:
            MRVESeal object
        """
        if not self.dna:
            self.transcribe()
        
        self.seal = seal(self.dna)
        return self.seal
    
    def generate_nft(self) -> NFT:
        """
        Layer 5: NFT Hash (O-Face).
        
        Returns:
            NFT object
        """
        if not self.dna:
            self.transcribe()
        
        self.nft = generate_nft_id(self.content, self.dna)
        return self.nft
    
    def quantum_stub(self) -> str:
        """
        Layer 6: Quantum State (Future).
        
        Returns:
            Quantum state stub
        """
        if not self.dna:
            self.transcribe()
        
        self.quantum_state = quantum_state_stub(self.dna)
        return self.quantum_state
    
    def run_full_pipeline(self) -> dict:
        """
        Execute complete pipeline through all layers.
        
        Returns:
            Dictionary with all pipeline results
        """
        # Execute each layer
        dna = self.transcribe()
        hex_enc = self.to_hex()
        binary_enc = self.to_binary()
        seal_obj = self.create_seal()
        nft_obj = self.generate_nft()
        quantum = self.quantum_stub()
        
        # Verify round-trip
        decoded = dna_to_text(dna)
        verified = (decoded == self.content)
        
        return {
            'input': self.content,
            'dna': dna,
            'hex': hex_enc,
            'binary': binary_enc,
            'mrve_seal': str(seal_obj),
            'seal_id': seal_obj.seal_id,
            'nft_id': nft_obj.nft_id,
            'nft_algorithm': nft_obj.algorithm,
            'quantum_state': quantum,
            'decoded': decoded,
            'verified': verified,
        }
    
    def get_sagco_info(self) -> dict:
        """
        Get SAGCO-specific encoding information.
        
        Returns:
            Dictionary with SAGCO reference data
        """
        if not all(c in 'SAGCO' for c in self.content):
            return {'error': 'Content must be SAGCO characters only'}
        
        info = []
        for char in self.content:
            info.append(SAGCO_REFERENCE.get(char, {}))
        
        return {
            'content': self.content,
            'sagco_info': info,
            'dna_sequence': ' '.join(ref['codon'] for ref in info),
            'hex_sequence': ' '.join(ref['hex'] for ref in info),
            'binary_sequence': ' '.join(ref['binary'] for ref in info),
        }


# Convenience functions for direct use

def transcribe(text: str) -> str:
    """
    Convenience function: English → DNA codons (Layer 1: S-Face).
    
    Args:
        text: Input text
        
    Returns:
        DNA codon sequence
        
    Example:
        >>> transcribe("SAGCO")
        'AGC GCT GGA TGC TAA'
    """
    return transcribe_to_dna(text)


def to_hex(dna: str) -> str:
    """
    Convenience function: DNA → Hexadecimal (Layer 2: A-Face).
    
    Args:
        dna: DNA codon sequence
        
    Returns:
        Hexadecimal representation
        
    Example:
        >>> to_hex("AGCGCT")
        '41 47 43 47 43 54'
    """
    dna_clean = dna.replace(' ', '')
    return ' '.join(hex(ord(c))[2:].upper() for c in dna_clean)


def to_binary(dna: str) -> str:
    """
    Convenience function: DNA → Binary (Layer 3: G-Face).
    
    Args:
        dna: DNA codon sequence
        
    Returns:
        Binary representation
        
    Example:
        >>> to_binary("A")
        '01000001'
    """
    dna_clean = dna.replace(' ', '')
    return ' '.join(bin(ord(c))[2:].zfill(8) for c in dna_clean)


def full_pipeline(content: str, face: Optional[str] = None) -> dict:
    """
    Execute full FlameTranscribe pipeline.
    
    Args:
        content: Input text
        face: Optional specific face to execute (S/A/G/C/O)
        
    Returns:
        Pipeline results
    """
    pipeline = FlameTranscribe(content)
    
    if face:
        face = face.upper()
        if face == 'S':
            return {'face': 'S-Transcribe', 'result': pipeline.transcribe()}
        elif face == 'A':
            pipeline.transcribe()
            return {'face': 'A-Hex', 'result': pipeline.to_hex()}
        elif face == 'G':
            pipeline.transcribe()
            return {'face': 'G-Binary', 'result': pipeline.to_binary()}
        elif face == 'C':
            pipeline.transcribe()
            return {'face': 'C-Seal', 'result': str(pipeline.create_seal())}
        elif face == 'O':
            pipeline.transcribe()
            return {'face': 'O-NFT', 'result': pipeline.generate_nft().nft_id}
        else:
            return {'error': f'Unknown face: {face}. Use S/A/G/C/O'}
    
    return pipeline.run_full_pipeline()


def print_pipeline_output(result: dict) -> None:
    """
    Pretty-print pipeline output.
    
    Args:
        result: Pipeline result dictionary
    """
    print("\n" + "="*70)
    print("FLAMETRANSCRIBE_SAGCO PIPELINE OUTPUT")
    print("="*70)
    
    if 'error' in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    if 'face' in result:
        # Single face output
        print(f"\n[FACE] {result['face']}")
        print(f"Result: {result['result']}")
        return
    
    # Full pipeline output
    print(f"\n[INPUT]     {result.get('input', 'N/A')}")
    print(f"[DNA]       {result.get('dna', 'N/A')}")
    
    # Show first 80 chars of hex/binary if too long
    hex_val = result.get('hex', 'N/A')
    if len(hex_val) > 80:
        hex_val = hex_val[:80] + "..."
    print(f"[HEX]       {hex_val}")
    
    binary_val = result.get('binary', 'N/A')
    if len(binary_val) > 80:
        binary_val = binary_val[:80] + "..."
    print(f"[BINARY]    {binary_val}")
    
    print(f"[MRVE]      {result.get('mrve_seal', 'N/A')}")
    print(f"[SEAL_ID]   {result.get('seal_id', 'N/A')}")
    print(f"[NFT_ID]    {result.get('nft_id', 'N/A')}")
    print(f"[ALGORITHM] {result.get('nft_algorithm', 'N/A')}")
    print(f"[QUANTUM]   {result.get('quantum_state', 'N/A')}")
    print(f"[DECODED]   {result.get('decoded', 'N/A')}")
    
    verified = result.get('verified', False)
    status = "✓" if verified else "✗"
    print(f"[VERIFIED]  {status}")
    
    print("="*70 + "\n")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='FlameTranscribe_SAGCO Pipeline - DNA-based sovereign programming',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "SAGCO"                    # Full pipeline
  %(prog)s "Hello World" --face S     # DNA transcription only
  %(prog)s "Test" --face O            # NFT generation only
  %(prog)s --sagco                    # Show SAGCO reference
        """
    )
    
    parser.add_argument(
        'content',
        nargs='?',
        default='SAGCO',
        help='Input text to process (default: SAGCO)'
    )
    parser.add_argument(
        '--face',
        choices=['S', 'A', 'G', 'C', 'O', 's', 'a', 'g', 'c', 'o'],
        help='Execute specific SAGCO face only'
    )
    parser.add_argument(
        '--sagco',
        action='store_true',
        help='Show SAGCO reference table'
    )
    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        help='Minimal output'
    )
    
    args = parser.parse_args()
    
    # Show SAGCO reference
    if args.sagco:
        print("\n=== SAGCO ENCODING REFERENCE ===\n")
        for char, info in SAGCO_REFERENCE.items():
            print(f"{char}: {info['codon']:3} | {info['hex']:2} | {info['binary']:8} | {info['amino_acid']:8} | {info['face']}")
        print()
        return 0
    
    # Run pipeline
    try:
        result = full_pipeline(args.content, args.face)
        
        if not args.quiet:
            print_pipeline_output(result)
        else:
            # Quiet mode: just print key result
            if 'face' in result:
                print(result['result'])
            else:
                print(result.get('nft_id', ''))
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
