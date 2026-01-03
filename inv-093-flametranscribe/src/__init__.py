"""
FlameTranscribe_SAGCO Pipeline
Strategickhaos DAO LLC | INV-093
Classification: NOVEL | 2026-01-03

A sovereign programming pipeline that transcribes human language through
biological primitives (DNA codons) to machine execution, with cryptographic
sealing and NFT provenance.

Functor Chain:
English/Hebrew → Unicode → Wave → DNA → Hex → Binary → LLVM → Machine → Transistor
                                   ↓
                            NFT Hash (BLAKE2b)
                                   ↓
                            Ed25519 Signature (MRVE)
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC"
__classification__ = "NOVEL"

from .codon_map import CODON_MAP, DNA_TO_CHAR, transcribe_to_dna, dna_to_text, SAGCO_REFERENCE
from .flame_transcribe import (
    FlameTranscribe,
    transcribe,
    to_hex,
    to_binary,
    full_pipeline,
)
from .mrve_seal import seal, verify_seal, MRVESeal
from .nft_algo import generate_nft_id, verify_nft, mint_nft, NFT

__all__ = [
    "CODON_MAP",
    "DNA_TO_CHAR",
    "SAGCO_REFERENCE",
    "transcribe_to_dna",
    "dna_to_text",
    "FlameTranscribe",
    "transcribe",
    "to_hex",
    "to_binary",
    "full_pipeline",
    "seal",
    "verify_seal",
    "MRVESeal",
    "generate_nft_id",
    "verify_nft",
    "mint_nft",
    "NFT",
]
