/**
 * Genetic Codon Type Definitions
 * 
 * Represents the 64 genetic codon triplets with associated properties
 * including physics, Hebrew letters, and glyph representations.
 */

/**
 * Trigonometric family classifications for codons
 */
export type CodonFamily = 
  | "SIN (White)" 
  | "COS (Yellow)" 
  | "TAN (Orange)" 
  | "CSC (Red)" 
  | "SEC (Blue)" 
  | "COT (Green)";

/**
 * Schwarzschild radius classifications based on black hole physics
 */
export type SchildLocation = 
  | "Event Horizon" 
  | "Near Horizon" 
  | "Exterior" 
  | "ISCO (stable)";

/**
 * Fragility levels indicating stability
 */
export type FragilityLevel = "MAX" | "HIGH" | "MEDIUM" | "LOW";

/**
 * Individual codon properties
 */
export interface CodonProperties {
  /** Atomic number (1-64) */
  atomic: number;
  
  /** Angular position in degrees (0-360) */
  angle: number;
  
  /** Associated Hebrew letter */
  hebrew: string;
  
  /** Unicode glyph representation */
  glyph: string;
  
  /** Trigonometric family classification */
  family: CodonFamily;
  
  /** Norm squared value (can be numeric or "inf") */
  norm_sq: number | "inf";
  
  /** Schwarzschild radius classification */
  schwarzschild: SchildLocation;
  
  /** Critical xi value */
  xi_crit: number;
  
  /** Fragility classification */
  fragility: FragilityLevel;
}

/**
 * Genetic codon triplet (e.g., "AAA", "AAC", "TTT")
 */
export type CodonTriplet = string;

/**
 * Complete genetic codon dataset mapping triplets to their properties
 */
export type GeneticCodonsDataset = Record<CodonTriplet, CodonProperties>;

/**
 * Query interface for codon filtering
 */
export interface CodonQuery {
  family?: CodonFamily;
  fragility?: FragilityLevel;
  schwarzschild?: SchildLocation;
  minAtomic?: number;
  maxAtomic?: number;
  minAngle?: number;
  maxAngle?: number;
}
