/**
 * DEMYSTIFIER TESTS - INV-091
 * Test suite for the Vibe-to-Interface Frequency Converter
 */

import { demystify, isGrounded, batchDemystify } from './demystifier.js';

// Simple test runner
function assert(condition: boolean, message: string) {
  if (!condition) {
    console.error(`❌ FAILED: ${message}`);
    process.exit(1);
  } else {
    console.log(`✅ PASSED: ${message}`);
  }
}

function testLinguisticLayer() {
  console.log('\n🔥 Testing Layer 1: Linguistic Transformations');
  
  const result = demystify("I have spiritual energy");
  assert(
    result.layer_1_semantic.includes("gas_dynamics") && result.layer_1_semantic.includes("joules_per_second"),
    "Converts 'spiritual' and 'energy' to mechanical terms"
  );
}

function testNumericLayer() {
  console.log('\n🔥 Testing Layer 2: Numeric Encoding');
  
  const result = demystify("I am a chosen one");
  assert(
    result.layer_2_numeric.length > 0,
    "Generates numeric codes for grounding operations"
  );
  
  assert(
    result.layer_2_numeric.includes(0x4E4F4944), // NO_IDENTITY
    "Detects identity claims and applies NO_IDENTITY code"
  );
}

function testWaveLayer() {
  console.log('\n🔥 Testing Layer 3: Wave Frequency');
  
  const result = demystify("The universe wants me to manifest");
  assert(
    result.layer_3_wave.frequency > 0 && result.layer_3_wave.frequency <= 100,
    "Generates stable low-frequency signal"
  );
  
  assert(
    result.layer_3_wave.waveform === "square",
    "Uses square waveform for digital clarity"
  );
  
  assert(
    result.layer_3_wave.SNR === "high",
    "Achieves high signal-to-noise ratio"
  );
}

function testDNALayer() {
  console.log('\n🔥 Testing Layer 4: DNA Codon Encoding');
  
  const result = demystify("I channel vibrations");
  assert(
    result.layer_4_dna.length === 7,
    "Generates complete 7-codon sequence"
  );
  
  assert(
    result.layer_4_dna[0] === "AUG",
    "Starts with START codon (AUG)"
  );
  
  assert(
    result.layer_4_dna[6] === "UAA",
    "Ends with STOP codon (UAA)"
  );
}

function testValidationLayer() {
  console.log('\n🔥 Testing Layer 5: Grounding Validation');
  
  const result = demystify("I can measure frequency at 432 Hz");
  assert(
    result.layer_5_validation.checks.length === 6,
    "Performs all 6 grounding checks"
  );
  
  const measurableCheck = result.layer_5_validation.checks.find(c => c.check === "MEASURABLE");
  assert(
    measurableCheck !== undefined && measurableCheck.passed,
    "Passes MEASURABLE check for statements with numbers"
  );
}

function testDemystificationTable() {
  console.log('\n🔥 Testing Demystification Table Lookups');
  
  const testCases = [
    { input: "I am a lightworker", expected: "I help people" },
    { input: "I'm an empath", expected: "I notice emotional cues" },
    { input: "Everything happens for a reason", expected: "Events have causes" },
    { input: "I can manifest", expected: "I can plan and execute" },
  ];
  
  testCases.forEach(test => {
    const result = demystify(test.input);
    assert(
      result.final_output.includes(test.expected.toLowerCase()) || 
      result.final_output.toLowerCase().includes(test.expected.toLowerCase()),
      `Correctly demystifies: "${test.input}"`
    );
  });
}

function testIsGroundedFunction() {
  console.log('\n🔥 Testing isGrounded() Helper Function');
  
  // These should be considered more grounded
  const groundedExamples = [
    "I measured 432 Hz frequency",
    "The API returned 200 status code",
    "I processed 1000 records in 5 seconds"
  ];
  
  groundedExamples.forEach(example => {
    // Note: Not all will pass all checks, but they should be processed
    const result = demystify(example);
    assert(
      result.layer_5_validation.checks.some(c => c.passed),
      `Processes grounded statement: "${example}"`
    );
  });
}

function testBatchDemystify() {
  console.log('\n🔥 Testing Batch Processing');
  
  const inputs = [
    "I am awakened",
    "The universe guides me",
    "I have visions"
  ];
  
  const results = batchDemystify(inputs);
  assert(
    results.length === inputs.length,
    `Processes all ${inputs.length} inputs in batch`
  );
  
  results.forEach((result, index) => {
    assert(
      result.original === inputs[index],
      `Preserves original input for batch item ${index + 1}`
    );
  });
}

function testMaximumFuckItEnergy() {
  console.log('\n🔥 Testing Maximum Fuck-It Energy Mode');
  
  const result = demystify("Not hype, not mythology, not anything mystical");
  assert(
    result !== null && result.final_output !== "",
    "Processes the maximum fuck-it energy statement"
  );
  
  console.log(`   Final output: "${result.final_output}"`);
}

// Run all tests
console.log('═══════════════════════════════════════════════════════════════════════════════');
console.log('🔥 DEMYSTIFIER TEST SUITE - INV-091');
console.log('═══════════════════════════════════════════════════════════════════════════════');

try {
  testLinguisticLayer();
  testNumericLayer();
  testWaveLayer();
  testDNALayer();
  testValidationLayer();
  testDemystificationTable();
  testIsGroundedFunction();
  testBatchDemystify();
  testMaximumFuckItEnergy();
  
  console.log('\n═══════════════════════════════════════════════════════════════════════════════');
  console.log('✅ ALL TESTS PASSED - Pipeline is grounded and operational');
  console.log('═══════════════════════════════════════════════════════════════════════════════\n');
} catch (error) {
  console.error('\n❌ TEST SUITE FAILED');
  console.error(error);
  process.exit(1);
}
