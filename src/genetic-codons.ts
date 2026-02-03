/**
 * Genetic Codon Utilities
 * 
 * Provides functions to load and query the genetic codon dataset.
 */

import { readFileSync } from 'fs';
import { join } from 'path';
import type { 
  GeneticCodonsDataset, 
  CodonProperties, 
  CodonTriplet,
  CodonQuery,
  CodonFamily,
  FragilityLevel
} from './types/genetic-codons.js';

let cachedData: GeneticCodonsDataset | null = null;

/**
 * Load the genetic codons dataset from JSON file
 */
export function loadGeneticCodons(): GeneticCodonsDataset {
  if (cachedData) {
    return cachedData;
  }

  const dataPath = join(process.cwd(), 'data', 'genetic_codons.json');
  const rawData = readFileSync(dataPath, 'utf-8');
  cachedData = JSON.parse(rawData) as GeneticCodonsDataset;
  
  return cachedData;
}

/**
 * Get properties for a specific codon triplet
 */
export function getCodon(triplet: CodonTriplet): CodonProperties | undefined {
  const dataset = loadGeneticCodons();
  return dataset[triplet.toUpperCase()];
}

/**
 * Get all codon triplets
 */
export function getAllCodons(): CodonTriplet[] {
  const dataset = loadGeneticCodons();
  return Object.keys(dataset);
}

/**
 * Query codons by various criteria
 */
export function queryCodons(query: CodonQuery): Array<[CodonTriplet, CodonProperties]> {
  const dataset = loadGeneticCodons();
  const results: Array<[CodonTriplet, CodonProperties]> = [];

  for (const [triplet, properties] of Object.entries(dataset)) {
    let matches = true;

    if (query.family && properties.family !== query.family) {
      matches = false;
    }

    if (query.fragility && properties.fragility !== query.fragility) {
      matches = false;
    }

    if (query.schwarzschild && properties.schwarzschild !== query.schwarzschild) {
      matches = false;
    }

    if (query.minAtomic !== undefined && properties.atomic < query.minAtomic) {
      matches = false;
    }

    if (query.maxAtomic !== undefined && properties.atomic > query.maxAtomic) {
      matches = false;
    }

    if (query.minAngle !== undefined && properties.angle < query.minAngle) {
      matches = false;
    }

    if (query.maxAngle !== undefined && properties.angle > query.maxAngle) {
      matches = false;
    }

    if (matches) {
      results.push([triplet, properties]);
    }
  }

  return results;
}

/**
 * Get codons by family
 */
export function getCodonsByFamily(family: CodonFamily): Array<[CodonTriplet, CodonProperties]> {
  return queryCodons({ family });
}

/**
 * Get codons by fragility level
 */
export function getCodonsByFragility(fragility: FragilityLevel): Array<[CodonTriplet, CodonProperties]> {
  return queryCodons({ fragility });
}

/**
 * Get codons at Event Horizon (infinite norm_sq)
 */
export function getEventHorizonCodons(): Array<[CodonTriplet, CodonProperties]> {
  const dataset = loadGeneticCodons();
  const results: Array<[CodonTriplet, CodonProperties]> = [];

  for (const [triplet, properties] of Object.entries(dataset)) {
    if (properties.norm_sq === 'inf') {
      results.push([triplet, properties]);
    }
  }

  return results;
}

/**
 * Get codon by atomic number
 */
export function getCodonByAtomic(atomic: number): [CodonTriplet, CodonProperties] | undefined {
  const dataset = loadGeneticCodons();
  
  for (const [triplet, properties] of Object.entries(dataset)) {
    if (properties.atomic === atomic) {
      return [triplet, properties];
    }
  }

  return undefined;
}

/**
 * Get summary statistics of the genetic codon dataset
 */
export function getDatasetStats() {
  const dataset = loadGeneticCodons();
  const codons = Object.entries(dataset);

  const families = new Set(codons.map(([_, p]) => p.family));
  const fragilities = new Set(codons.map(([_, p]) => p.fragility));
  const schwarzschilds = new Set(codons.map(([_, p]) => p.schwarzschild));

  const familyCount: Record<string, number> = {};
  const fragilityCount: Record<string, number> = {};
  const schwarzschildCount: Record<string, number> = {};

  for (const [_, properties] of codons) {
    familyCount[properties.family] = (familyCount[properties.family] || 0) + 1;
    fragilityCount[properties.fragility] = (fragilityCount[properties.fragility] || 0) + 1;
    schwarzschildCount[properties.schwarzschild] = (schwarzschildCount[properties.schwarzschild] || 0) + 1;
  }

  return {
    totalCodons: codons.length,
    families: Array.from(families),
    fragilities: Array.from(fragilities),
    schwarzschilds: Array.from(schwarzschilds),
    familyDistribution: familyCount,
    fragilityDistribution: fragilityCount,
    schwarzschildDistribution: schwarzschildCount,
  };
}
