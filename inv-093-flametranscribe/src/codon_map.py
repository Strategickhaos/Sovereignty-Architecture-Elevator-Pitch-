"""
DNA Codon Mapping for FlameTranscribe_SAGCO Pipeline
Strategickhaos DAO LLC | INV-093

Maps ASCII characters to DNA codons (3-base sequences).
Each character has a unique codon representation.
"""

from typing import Dict

# Primary codon mappings for alphanumeric characters
# Based on standard genetic code with custom extensions
CODON_MAP: Dict[str, str] = {
    # SAGCO Reference Characters (Special encoding)
    'S': 'AGC',  # Serine - Source/Transcribe
    'A': 'GCT',  # Alanine - Analyze/Hex
    'G': 'GGA',  # Glycine - Generate/Binary
    'C': 'TGC',  # Cysteine - Certify/Seal
    'O': 'TAA',  # Stop codon - Output/NFT
    
    # Uppercase Letters
    'B': 'GCC',  # Alanine
    'D': 'GAT',  # Aspartic acid
    'E': 'GAA',  # Glutamic acid
    'F': 'TTC',  # Phenylalanine
    'H': 'CAT',  # Histidine
    'I': 'ATT',  # Isoleucine
    'J': 'ACA',  # Changed to avoid collision
    'K': 'AAA',  # Lysine
    'L': 'TTG',  # Leucine
    'M': 'ATG',  # Methionine (Start codon)
    'N': 'AAC',  # Asparagine
    'P': 'CCT',  # Proline
    'Q': 'CAA',  # Glutamine
    'R': 'CGT',  # Arginine
    'T': 'ACT',  # Threonine
    'U': 'TGT',  # Changed to avoid collision with C (SAGCO uses TGC)
    'V': 'GTT',  # Valine
    'W': 'TGG',  # Tryptophan
    'X': 'TAG',  # Stop codon (Amber)
    'Y': 'TAT',  # Tyrosine
    'Z': 'TGA',  # Stop codon (Opal)
    
    # Lowercase letters (using alternative codons - carefully chosen to avoid ALL collisions)
    'a': 'GCA',
    'b': 'GCG',
    'c': 'CGG',
    'd': 'GAC',
    'e': 'GAG',
    'f': 'TTT',
    'g': 'GGT',
    'h': 'CAC',
    'i': 'ATA',
    'j': 'AGG',
    'k': 'AAG',
    'l': 'TTA',
    'm': 'TCC',  # Changed to avoid collision with A (SAGCO)
    'n': 'AAT',
    'o': 'ACG',
    'p': 'CCA',
    'q': 'CAG',
    'r': 'CGA',
    's': 'AGT',
    't': 'ACC',
    'u': 'GGC',  # Changed to avoid collision with C (SAGCO)
    'v': 'GTA',
    'w': 'ATC',  # Using available codon
    'x': 'TCG',
    'y': 'TAC',
    'z': 'TCA',
    
    # Numbers (avoiding all collisions)
    '0': 'GGG',
    '1': 'CGC',
    '2': 'CCC',
    '3': 'CCG',
    '4': 'CTC',
    '5': 'CTA',
    '6': 'CTT',  # Changed to avoid collision with Q
    '7': 'GTG',
    '8': 'GTC',
    '9': 'AGA',  # Changed to avoid collision with T
    
    # Special Characters (avoiding collisions)
    ' ': 'NNN',  # Space
    '.': 'GNC',  # Period
    ',': 'NCG',  # Comma
    '!': 'NGC',  # Exclamation
    '?': 'NGG',  # Question
    '-': 'NTT',  # Hyphen
    '_': 'NTA',  # Underscore
    '(': 'NAA',  # Left paren
    ')': 'NAC',  # Right paren
    '[': 'NAG',  # Left bracket
    ']': 'NAT',  # Right bracket
    '{': 'NCA',  # Left brace
    '}': 'NCC',  # Right brace
    ':': 'NCT',  # Colon
    ';': 'NGA',  # Semicolon
    '"': 'NGT',  # Quote
    "'": 'NTC',  # Single quote
    '/': 'NTG',  # Forward slash
    '\\': 'NNA',  # Backslash
    '|': 'NNG',  # Pipe
    '@': 'AAN',  # At sign
    '#': 'ACN',  # Hash
    '$': 'AGN',  # Dollar
    '%': 'ATN',  # Percent
    '&': 'CAN',  # Ampersand
    '*': 'CCN',  # Asterisk
    '+': 'CGN',  # Plus
    '=': 'CTN',  # Equals
    '<': 'GAN',  # Less than
    '>': 'GGN',  # Greater than
    '~': 'GTN',  # Tilde
    '`': 'TAN',  # Backtick
    '\n': 'TCN',  # Newline
    '\t': 'TGN',  # Tab
    '\r': 'TTN',  # Carriage return
}

# Reverse mapping: DNA codon to character
DNA_TO_CHAR: Dict[str, str] = {v: k for k, v in CODON_MAP.items()}

# Hebrew to English phonetic mapping (Layer 0)
HEBREW_MAP: Dict[str, str] = {
    'א': 'A',  # Aleph
    'ב': 'B',  # Bet
    'ג': 'G',  # Gimel
    'ד': 'D',  # Dalet
    'ה': 'H',  # He
    'ו': 'V',  # Vav
    'ז': 'Z',  # Zayin
    'ח': 'CH', # Chet
    'ט': 'T',  # Tet
    'י': 'Y',  # Yod
    'כ': 'K',  # Kaf
    'ל': 'L',  # Lamed
    'מ': 'M',  # Mem
    'ן': 'N',  # Nun (final)
    'נ': 'N',  # Nun
    'ס': 'S',  # Samech
    'ע': 'A',  # Ayin
    'פ': 'P',  # Pe
    'ץ': 'TS', # Tsadi (final)
    'צ': 'TS', # Tsadi
    'ק': 'Q',  # Qof
    'ר': 'R',  # Resh
    'ש': 'SH', # Shin
    'ת': 'T',  # Tav
}


def normalize_hebrew(text: str) -> str:
    """
    Normalize Hebrew characters to English phonetics (Layer 0).
    
    Args:
        text: Input text potentially containing Hebrew characters
        
    Returns:
        Text with Hebrew characters converted to English equivalents
    """
    result = []
    for char in text:
        if char in HEBREW_MAP:
            result.append(HEBREW_MAP[char])
        else:
            result.append(char)
    return ''.join(result)


def transcribe_to_dna(text: str, normalize: bool = True) -> str:
    """
    Transcribe text to DNA codon sequence (Layer 1: S-Face).
    
    Args:
        text: Input text to transcribe
        normalize: If True, normalize Hebrew characters first
        
    Returns:
        DNA codon sequence (space-separated)
        
    Example:
        >>> transcribe_to_dna("SAGCO")
        'AGC GCT GGA TGC TAA'
    """
    if normalize:
        text = normalize_hebrew(text)
    
    codons = []
    for char in text:
        codon = CODON_MAP.get(char, 'NNN')
        codons.append(codon)
    
    return ' '.join(codons)


def dna_to_text(dna_sequence: str) -> str:
    """
    Reverse transcribe DNA codon sequence back to text.
    
    Args:
        dna_sequence: Space-separated DNA codon sequence
        
    Returns:
        Original text (best effort)
        
    Example:
        >>> dna_to_text("AGC GCT GGA TGC TAA")
        'SAGCO'
    """
    codons = dna_sequence.split()
    chars = []
    
    for codon in codons:
        char = DNA_TO_CHAR.get(codon, '?')
        chars.append(char)
    
    return ''.join(chars)


def get_codon_info(char: str) -> dict:
    """
    Get detailed information about a character's DNA codon.
    
    Args:
        char: Single character
        
    Returns:
        Dictionary with character encoding details
    """
    codon = CODON_MAP.get(char, 'NNN')
    ascii_dec = ord(char) if len(char) == 1 else 0
    hex_val = hex(ascii_dec)[2:].upper() if ascii_dec else '00'
    binary = bin(ascii_dec)[2:].zfill(8) if ascii_dec else '00000000'
    
    return {
        'char': char,
        'ascii_dec': ascii_dec,
        'hex': hex_val,
        'binary': binary,
        'dna_codon': codon,
    }


# SAGCO reference for quick lookup
SAGCO_REFERENCE = {
    'S': {'ascii': 83, 'hex': '53', 'binary': '01010011', 'codon': 'AGC', 'amino_acid': 'Serine', 'face': 'Transcribe'},
    'A': {'ascii': 65, 'hex': '41', 'binary': '01000001', 'codon': 'GCT', 'amino_acid': 'Alanine', 'face': 'Hex Analysis'},
    'G': {'ascii': 71, 'hex': '47', 'binary': '01000111', 'codon': 'GGA', 'amino_acid': 'Glycine', 'face': 'Binary Generate'},
    'C': {'ascii': 67, 'hex': '43', 'binary': '01000011', 'codon': 'TGC', 'amino_acid': 'Cysteine', 'face': 'Seal/Certify'},
    'O': {'ascii': 79, 'hex': '4F', 'binary': '01001111', 'codon': 'TAA', 'amino_acid': 'Stop', 'face': 'NFT Output'},
}
