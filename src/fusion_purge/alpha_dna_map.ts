// ALPHABET TO DNA MAPPING
// Vectorizes alphabet to DNA codons via trigonometric embeddings
// A→ATG, B→CGC, etc. with 4D trig space representation

export interface DNACodon {
  letter: string;
  codon: string;
  vector: number[];  // 4D trig embedding [sin, cos, tan, phase]
  bioSymbolic: string;
}

/**
 * Generate 4D trigonometric vector for alphabet position
 */
function generateTrigVector(position: number, totalLetters: number = 26): number[] {
  const angle = (position / totalLetters) * 2 * Math.PI;
  return [
    Math.sin(angle),                    // Base frequency
    Math.cos(angle),                    // Quadrature component
    Math.tan(angle % (Math.PI / 2)),   // Harmonic distortion
    (angle / (2 * Math.PI))            // Phase position [0-1]
  ];
}

/**
 * DNA codon mappings for entire alphabet
 */
export const ALPHABET_DNA_MAP: DNACodon[] = [
  { letter: 'A', codon: 'ATG', vector: generateTrigVector(0), bioSymbolic: 'Adenine-Start' },
  { letter: 'B', codon: 'CGC', vector: generateTrigVector(1), bioSymbolic: 'Cytosine-Arginine' },
  { letter: 'C', codon: 'GGT', vector: generateTrigVector(2), bioSymbolic: 'Guanine-Glycine' },
  { letter: 'D', codon: 'GAC', vector: generateTrigVector(3), bioSymbolic: 'Aspartic' },
  { letter: 'E', codon: 'GAA', vector: generateTrigVector(4), bioSymbolic: 'Glutamic' },
  { letter: 'F', codon: 'TTC', vector: generateTrigVector(5), bioSymbolic: 'Phenylalanine' },
  { letter: 'G', codon: 'GGG', vector: generateTrigVector(6), bioSymbolic: 'Glycine-Pure' },
  { letter: 'H', codon: 'CAC', vector: generateTrigVector(7), bioSymbolic: 'Histidine' },
  { letter: 'I', codon: 'ATA', vector: generateTrigVector(8), bioSymbolic: 'Isoleucine' },
  { letter: 'J', codon: 'ATT', vector: generateTrigVector(9), bioSymbolic: 'Isoleucine-Variant' },
  { letter: 'K', codon: 'AAA', vector: generateTrigVector(10), bioSymbolic: 'Lysine' },
  { letter: 'L', codon: 'CTG', vector: generateTrigVector(11), bioSymbolic: 'Leucine' },
  { letter: 'M', codon: 'ATG', vector: generateTrigVector(12), bioSymbolic: 'Methionine-Start' },
  { letter: 'N', codon: 'AAC', vector: generateTrigVector(13), bioSymbolic: 'Asparagine' },
  { letter: 'O', codon: 'TGA', vector: generateTrigVector(14), bioSymbolic: 'Opal-Stop' },
  { letter: 'P', codon: 'CCG', vector: generateTrigVector(15), bioSymbolic: 'Proline' },
  { letter: 'Q', codon: 'CAG', vector: generateTrigVector(16), bioSymbolic: 'Glutamine' },
  { letter: 'R', codon: 'CGG', vector: generateTrigVector(17), bioSymbolic: 'Arginine' },
  { letter: 'S', codon: 'TCG', vector: generateTrigVector(18), bioSymbolic: 'Serine' },
  { letter: 'T', codon: 'ACG', vector: generateTrigVector(19), bioSymbolic: 'Threonine' },
  { letter: 'U', codon: 'TGT', vector: generateTrigVector(20), bioSymbolic: 'Cysteine-Uracil' },
  { letter: 'V', codon: 'GTG', vector: generateTrigVector(21), bioSymbolic: 'Valine' },
  { letter: 'W', codon: 'TGG', vector: generateTrigVector(22), bioSymbolic: 'Tryptophan' },
  { letter: 'X', codon: 'TAG', vector: generateTrigVector(23), bioSymbolic: 'Amber-Stop' },
  { letter: 'Y', codon: 'TAC', vector: generateTrigVector(24), bioSymbolic: 'Tyrosine' },
  { letter: 'Z', codon: 'TAA', vector: generateTrigVector(25), bioSymbolic: 'Ochre-Stop' }
];

/**
 * Convert text to DNA sequence
 */
export function textToDNA(text: string): string {
  return text
    .toUpperCase()
    .split('')
    .map(char => {
      const mapping = ALPHABET_DNA_MAP.find(m => m.letter === char);
      return mapping ? mapping.codon : 'NNN';
    })
    .join('');
}

/**
 * Convert text to vectorized DNA representation
 */
export function textToVectorDNA(text: string): number[][] {
  return text
    .toUpperCase()
    .split('')
    .map(char => {
      const mapping = ALPHABET_DNA_MAP.find(m => m.letter === char);
      return mapping ? mapping.vector : [0, 0, 0, 0];
    });
}

/**
 * Calculate DNA sequence resonance frequency
 */
export function calculateDNAFrequency(dnaSequence: string): number {
  const baseFreqs = { 'A': 440.0, 'T': 493.88, 'G': 523.25, 'C': 587.33 };
  let totalFreq = 0;
  let count = 0;
  
  for (const base of dnaSequence) {
    if (base in baseFreqs) {
      totalFreq += baseFreqs[base as keyof typeof baseFreqs];
      count++;
    }
  }
  
  return count > 0 ? totalFreq / count : 440.0; // Default to A440
}

/**
 * Generate sovereign code from text via DNA vectorization
 */
export function generateSovereignCodeFromText(text: string, freqHz: number = 1000): {
  dnaSequence: string;
  vectors: number[][];
  resonanceFreq: number;
  udapRoute: string;
} {
  const dnaSequence = textToDNA(text);
  const vectors = textToVectorDNA(text);
  const resonanceFreq = calculateDNAFrequency(dnaSequence);
  
  return {
    dnaSequence,
    vectors,
    resonanceFreq,
    udapRoute: `skhaos://pure/alpha/dna/${text}?vector=true&hz=${freqHz}`
  };
}
