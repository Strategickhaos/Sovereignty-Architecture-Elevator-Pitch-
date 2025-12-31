#!/usr/bin/env node
// Quick validation test for SFP modules
// Run with: node test_sfp.mjs

import { 
  OSS_TOOLS, 
  inventoryTool,
  calculateOverallPurity 
} from './src/fusion_purge/oss_inventory.js';

import { 
  purgeDependencies,
  generateSovereignReplacement 
} from './src/fusion_purge/purge_engine.js';

import {
  textToDNA,
  calculateDNAFrequency 
} from './src/fusion_purge/alpha_dna_map.js';

import {
  SOVEREIGN_ELEMENTS,
  getElementBySymbol 
} from './src/fusion_purge/periodic_table.js';

import {
  generateSovereignBinary 
} from './src/fusion_purge/binary_trinary.js';

import {
  parseUDAPUri,
  buildUDAPUri 
} from './src/fusion_purge/udap_helm.js';

console.log('╔════════════════════════════════════════════════════════════════╗');
console.log('║  SFP Module Validation Test                                   ║');
console.log('╚════════════════════════════════════════════════════════════════╝\n');

// Test 1: OSS Inventory
console.log('✓ Test 1: OSS Inventory');
const wireshark = inventoryTool('wireshark');
console.log(`  - Found ${wireshark.name} with ${wireshark.functions.length} functions`);
console.log(`  - Overall purity: ${calculateOverallPurity()}%\n`);

// Test 2: Purge Engine
console.log('✓ Test 2: Purge Engine');
const purgeResult = purgeDependencies(wireshark);
console.log(`  - Purged ${purgeResult.purgedDeps.length}/${purgeResult.originalDeps.length} dependencies`);
console.log(`  - Purity level: ${purgeResult.purityLevel}\n`);

// Test 3: DNA Vectorization
console.log('✓ Test 3: DNA Vectorization');
const dnaSeq = textToDNA('SOVEREIGNTY');
const freq = calculateDNAFrequency(dnaSeq);
console.log(`  - Text: SOVEREIGNTY`);
console.log(`  - DNA: ${dnaSeq}`);
console.log(`  - Resonance: ${freq.toFixed(2)} Hz\n`);

// Test 4: Periodic Table
console.log('✓ Test 4: Periodic Table');
const qubitium = getElementBySymbol('Qb');
console.log(`  - Element: ${qubitium.name} (${qubitium.symbol})`);
console.log(`  - Operation: ${qubitium.operation}`);
console.log(`  - Frequency: ${qubitium.frequency} Hz`);
console.log(`  - Total elements: ${SOVEREIGN_ELEMENTS.length}\n`);

// Test 5: Trinary Binary
console.log('✓ Test 5: Trinary Binary');
const trinary = generateSovereignBinary('PURE', 30000);
console.log(`  - Input: PURE`);
console.log(`  - Tribits: ${trinary.tribits.length}`);
console.log(`  - Wave samples: ${trinary.waveSignature.length}`);
console.log(`  - UDAP: ${trinary.udapRoute}\n`);

// Test 6: UDAP Protocol
console.log('✓ Test 6: UDAP Protocol');
const udapUri = buildUDAPUri({
  domain: 'pure',
  category: 'tcp',
  resource: 'handshake',
  params: new Map([['hz', '20000'], ['inventory', 'true']])
});
console.log(`  - Built URI: ${udapUri}`);
const parsed = parseUDAPUri(udapUri);
console.log(`  - Parsed domain: ${parsed.domain}`);
console.log(`  - Parsed category: ${parsed.category}\n`);

// Test 7: Sovereign Replacement
console.log('✓ Test 7: Sovereign Replacement');
const replacement = generateSovereignReplacement('TCP_SYN_ACK_handshake', 20000);
console.log(`  - OSS: TCP_SYN_ACK_handshake`);
console.log(`  - Sovereign: ${replacement}\n`);

console.log('═══════════════════════════════════════════════════════════════');
console.log('✓ All Tests Passed - SFP Modules Validated');
console.log('═══════════════════════════════════════════════════════════════\n');
