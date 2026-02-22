#!/usr/bin/env node
/**
 * Test script for genetic codons module
 * 
 * Demonstrates loading and querying the genetic codon dataset
 */

import {
  loadGeneticCodons,
  getCodon,
  getAllCodons,
  queryCodons,
  getCodonsByFamily,
  getEventHorizonCodons,
  getCodonByAtomic,
  getDatasetStats
} from './genetic-codons.js';

console.log('🧬 Genetic Codons Dataset Test\n');
console.log('='.repeat(60));

// Test 1: Load dataset
console.log('\n1. Loading genetic codons dataset...');
const dataset = loadGeneticCodons();
console.log(`   ✓ Loaded ${Object.keys(dataset).length} codons`);

// Test 2: Get specific codon
console.log('\n2. Getting codon AAA (Start codon):');
const aaa = getCodon('AAA');
if (aaa) {
  console.log(`   Atomic: ${aaa.atomic}`);
  console.log(`   Angle: ${aaa.angle}°`);
  console.log(`   Hebrew: ${aaa.hebrew}`);
  console.log(`   Glyph: ${aaa.glyph}`);
  console.log(`   Family: ${aaa.family}`);
  console.log(`   Schwarzschild: ${aaa.schwarzschild}`);
  console.log(`   Fragility: ${aaa.fragility}`);
}

// Test 3: Get Event Horizon codons
console.log('\n3. Event Horizon codons (norm_sq = inf):');
const eventHorizonCodons = getEventHorizonCodons();
console.log(`   Found ${eventHorizonCodons.length} codons at Event Horizon:`);
eventHorizonCodons.forEach(([triplet, props]) => {
  console.log(`   - ${triplet}: ${props.hebrew} (${props.glyph}) @ ${props.angle}°`);
});

// Test 4: Query by family
console.log('\n4. SIN (White) family codons:');
const sinCodons = getCodonsByFamily('SIN (White)');
console.log(`   Found ${sinCodons.length} codons in SIN (White) family`);
console.log(`   First 3: ${sinCodons.slice(0, 3).map(([t]) => t).join(', ')}`);

// Test 5: Query by fragility
console.log('\n5. HIGH fragility codons:');
const highFragilityCodons = queryCodons({ fragility: 'HIGH' });
console.log(`   Found ${highFragilityCodons.length} HIGH fragility codons`);

// Test 6: Query by angle range
console.log('\n6. Codons in first quadrant (0-90°):');
const firstQuadrant = queryCodons({ minAngle: 0, maxAngle: 90 });
console.log(`   Found ${firstQuadrant.length} codons in first quadrant`);

// Test 7: Get by atomic number
console.log('\n7. Getting codon by atomic number:');
const atomic32 = getCodonByAtomic(32);
if (atomic32) {
  const [triplet, props] = atomic32;
  console.log(`   Atomic 32: ${triplet} (${props.hebrew}) - ${props.family}`);
}

// Test 8: Dataset statistics
console.log('\n8. Dataset Statistics:');
const stats = getDatasetStats();
console.log(`   Total Codons: ${stats.totalCodons}`);
console.log(`   Families: ${stats.families.join(', ')}`);
console.log(`   Family Distribution:`);
Object.entries(stats.familyDistribution).forEach(([family, count]) => {
  console.log(`     - ${family}: ${count} codons`);
});
console.log(`   Fragility Distribution:`);
Object.entries(stats.fragilityDistribution).forEach(([fragility, count]) => {
  console.log(`     - ${fragility}: ${count} codons`);
});

console.log('\n' + '='.repeat(60));
console.log('✓ All tests completed successfully!\n');
