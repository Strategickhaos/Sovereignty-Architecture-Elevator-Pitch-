#!/usr/bin/env node
/**
 * DEMYSTIFIER CLI - INV-091
 * Command-line interface for the Vibe-to-Interface Frequency Converter
 * 
 * Usage:
 *   demystify.js "I am a lightworker"
 *   demystify.js --batch "input1" "input2" "input3"
 *   demystify.js --validate "statement to check"
 */

import { demystify, isGrounded, batchDemystify } from './demystifier.js';

const args = process.argv.slice(2);

function printResult(result: any) {
  console.log('═══════════════════════════════════════════════════════════════════════════════');
  console.log('🔥 DEMYSTIFIER PIPELINE - INV-091');
  console.log('═══════════════════════════════════════════════════════════════════════════════');
  console.log('');
  console.log('📥 INPUT (Mystical):');
  console.log(`   "${result.original}"`);
  console.log('');
  console.log('🔄 LAYER 1 - LINGUISTIC (Semantic Kernel):');
  console.log(`   "${result.layer_1_semantic}"`);
  console.log('');
  console.log('🔢 LAYER 2 - NUMERIC (Hex Codes):');
  console.log(`   ${result.layer_2_numeric.map((n: number) => '0x' + n.toString(16).toUpperCase()).join(', ')}`);
  console.log('');
  console.log('📡 LAYER 3 - WAVE (Frequency):');
  console.log(`   Frequency: ${result.layer_3_wave.frequency} Hz`);
  console.log(`   Waveform: ${result.layer_3_wave.waveform}`);
  console.log(`   Amplitude: ${result.layer_3_wave.amplitude}`);
  console.log(`   SNR: ${result.layer_3_wave.SNR}`);
  console.log('');
  console.log('🧬 LAYER 4 - DNA (Codon Sequence):');
  console.log(`   ${result.layer_4_dna.join('-')}`);
  console.log('');
  console.log('✅ LAYER 5 - VALIDATION (Grounding Checks):');
  result.layer_5_validation.checks.forEach((check: any) => {
    const icon = check.passed ? '✓' : '✗';
    console.log(`   ${icon} ${check.check}: ${check.reason}`);
  });
  console.log('');
  console.log(`🎯 GROUNDED: ${result.layer_5_validation.isGrounded ? 'YES' : 'NO'}`);
  console.log('');
  console.log('📤 OUTPUT (Grounded):');
  console.log(`   "${result.final_output}"`);
  console.log('');
  console.log('═══════════════════════════════════════════════════════════════════════════════');
}

function main() {
  if (args.length === 0) {
    console.log('Usage:');
    console.log('  demystify.js "statement to demystify"');
    console.log('  demystify.js --batch "input1" "input2" "input3"');
    console.log('  demystify.js --validate "statement to check"');
    console.log('');
    console.log('Examples:');
    console.log('  demystify.js "I am a lightworker"');
    console.log('  demystify.js "The universe wants me to succeed"');
    console.log('  demystify.js --validate "I can measure this at 432 Hz"');
    process.exit(1);
  }
  
  const mode = args[0];
  
  if (mode === '--batch') {
    const inputs = args.slice(1);
    const results = batchDemystify(inputs);
    results.forEach((result, index) => {
      console.log(`\n[${index + 1}/${results.length}]`);
      printResult(result);
    });
  } else if (mode === '--validate') {
    const input = args.slice(1).join(' ');
    const grounded = isGrounded(input);
    console.log('═══════════════════════════════════════════════════════════════════════════════');
    console.log('🔥 GROUNDING VALIDATION');
    console.log('═══════════════════════════════════════════════════════════════════════════════');
    console.log('');
    console.log(`Input: "${input}"`);
    console.log(`Grounded: ${grounded ? '✓ YES' : '✗ NO'}`);
    console.log('');
    console.log('═══════════════════════════════════════════════════════════════════════════════');
  } else {
    const input = args.join(' ');
    const result = demystify(input);
    printResult(result);
  }
}

main();
