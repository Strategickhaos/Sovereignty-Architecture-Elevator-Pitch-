/**
 * Example usage of the Rope Constants module
 * 
 * This script demonstrates how to use the rope constants API
 */

import { getRopeConstants } from './rope/index.js';

console.log('='.repeat(70));
console.log('Rope Access Constants - Example Usage');
console.log('='.repeat(70));

// Get the rope constants instance
const rope = getRopeConstants();

// Display metadata
console.log('\n📋 Metadata:');
const metadata = rope.getMetadata();
console.log(`  Domain: ${metadata.domain}`);
console.log(`  Owner: ${metadata.owner}`);
console.log(`  Maintainer: ${metadata.maintainer}`);
console.log(`  Version: ${metadata.version}`);
console.log(`  Certifications: ${metadata.certifications_held.join(', ')}`);
console.log(`  Regulatory Frameworks: ${metadata.regulatory_frameworks.join(', ')}`);

// Get a specific constant
console.log('\n🪢 Specific Constant: Figure-8 on Bight');
const figure8 = rope.getConstant('rope.knot.figure_8_on_bight');
if (figure8) {
  console.log(`  Key: ${figure8.key}`);
  console.log(`  Value: ${figure8.value} ${figure8.units}`);
  console.log(`  Range: [${figure8.range[0]}, ${figure8.range[1]}]`);
  console.log(`  Context: ${figure8.context}`);
  console.log(`  Confidence: ${figure8.confidence}`);
  console.log(`  Jurisdiction: ${figure8.jurisdiction}`);
  console.log(`  Provenance:`);
  figure8.provenance.forEach((prov, i) => {
    console.log(`    ${i + 1}. ${prov.source_title} (${prov.publisher}, ${prov.date})`);
    console.log(`       Section: ${prov.section_or_page}`);
    console.log(`       Notes: ${prov.notes}`);
  });
}

// Get all knot efficiency constants
console.log('\n🪢 All Knot Efficiency Constants:');
const knots = rope.getConstantsByCategory('knot');
knots.forEach(k => {
  console.log(`  - ${k.key}: ${k.value} ${k.units} (confidence: ${k.confidence})`);
});

// Get all pulley efficiency constants
console.log('\n🔧 All Pulley Efficiency Constants:');
const pulleys = rope.getConstantsByCategory('pulley');
pulleys.forEach(p => {
  console.log(`  - ${p.key}: ${p.value} ${p.units} (confidence: ${p.confidence})`);
});

// Search for constants
console.log('\n🔍 Search Results for "OSHA":');
const oshaResults = rope.searchConstants('OSHA');
oshaResults.forEach(result => {
  console.log(`  - ${result.constant.key}`);
  console.log(`    Matches in: ${result.matches.join(', ')}`);
  console.log(`    Value: ${result.constant.value} ${result.constant.units}`);
});

// Filter by jurisdiction
console.log('\n🌐 USA Jurisdiction Constants:');
const usaConstants = rope.getConstantsByJurisdiction('USA');
usaConstants.forEach(c => {
  console.log(`  - ${c.key}: ${c.value} ${c.units}`);
});

// Filter by confidence
console.log('\n⭐ High Confidence Constants:');
const highConfidence = rope.getConstantsByConfidence('high');
console.log(`  Found ${highConfidence.length} constants with high confidence`);

// Validate all constants
console.log('\n✅ Validation Results:');
const validations = rope.validateAll();
const passed = validations.filter(v => v.valid);
const failed = validations.filter(v => !v.valid);
const warned = validations.filter(v => v.warnings.length > 0);

console.log(`  Total constants: ${validations.length}`);
console.log(`  Passed: ${passed.length}`);
console.log(`  Failed: ${failed.length}`);
console.log(`  Warnings: ${warned.length}`);

if (failed.length > 0) {
  console.log('\n  Failed validations:');
  failed.forEach(v => {
    console.log(`    - ${v.key}:`);
    v.errors.forEach(e => console.log(`      ❌ ${e}`));
  });
}

if (warned.length > 0) {
  console.log('\n  Warnings:');
  warned.forEach(v => {
    console.log(`    - ${v.key}:`);
    v.warnings.forEach(w => console.log(`      ⚠️  ${w}`));
  });
}

// Demonstrate doctor tests
console.log('\n🩺 Doctor Tests:');
console.log(`  Knot efficiency 0.78 in bounds: ${rope.knotEfficiencyInBounds(0.78)}`);
console.log(`  Knot efficiency 0.30 in bounds: ${rope.knotEfficiencyInBounds(0.30)}`);
console.log(`  Pulley efficiency 0.90 in bounds: ${rope.pulleyEfficiencyInBounds(0.90)}`);
console.log(`  Design factor 10.0 meets minimum (5.0): ${rope.designFactorMinimum(10.0, 5.0)}`);
console.log(`  Fall factor 2.0 in bounds: ${rope.fallFactorInBounds(2.0)}`);
console.log(`  Bridle angle 120° passes warning: ${rope.bridleAngleWarning(120.0)}`);
console.log(`  Bridle angle 130° passes warning: ${rope.bridleAngleWarning(130.0)}`);

console.log('\n' + '='.repeat(70));
console.log('✅ Example completed successfully!');
console.log('='.repeat(70));
