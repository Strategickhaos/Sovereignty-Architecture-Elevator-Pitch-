/**
 * Simple tests for FLAMELANG Musical Notation System
 */

import { 
  validateNotation, 
  convertToMidiTiming, 
  groupByFamily, 
  calculateStats,
  type MusicalNotation 
} from './flamelang-notation.js';

// Test data
const validNotation: MusicalNotation = {
  meta: {
    tempo: 120,
    base_note: 60,
    beats_per_cycle: 16,
    note_count: 2
  },
  events: [
    {
      glyph_id: 0,
      glyph: "⟋",
      family: "SIN",
      theta: 0,
      midi_note: 60,
      velocity: 80,
      start_beat: 0,
      duration_beats: 0.5
    },
    {
      glyph_id: 1,
      glyph: "—",
      family: "COS",
      theta: 90,
      midi_note: 61,
      velocity: 70,
      start_beat: 1,
      duration_beats: 0.75
    }
  ],
  families: {
    SIN: { base_velocity: 80, duration_mult: 1.0, channel: 0 },
    COS: { base_velocity: 70, duration_mult: 1.5, channel: 0 }
  },
  singularities: [1]
};

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
  console.log(`✅ ${message}`);
}

console.log('🧪 Running FLAMELANG Musical Notation Tests\n');

// Test 1: Validation
console.log('Test 1: Validation');
const result = validateNotation(validNotation);
assert(result.valid, 'Valid notation should pass validation');
assert(result.errors.length === 0, 'Valid notation should have no errors');

// Test 2: Invalid MIDI note
console.log('\nTest 2: Invalid MIDI note detection');
const invalidNote = JSON.parse(JSON.stringify(validNotation));
invalidNote.events[0].midi_note = 150;
const result2 = validateNotation(invalidNote);
assert(!result2.valid, 'Invalid MIDI note should fail validation');
assert(result2.errors.length > 0, 'Should report error for invalid MIDI note');

// Test 3: Invalid theta
console.log('\nTest 3: Invalid theta detection');
const invalidTheta = JSON.parse(JSON.stringify(validNotation));
invalidTheta.events[0].theta = 400;
const result3 = validateNotation(invalidTheta);
assert(!result3.valid, 'Invalid theta should fail validation');

// Test 4: MIDI timing conversion
console.log('\nTest 4: MIDI timing conversion');
const midiEvents = convertToMidiTiming(validNotation);
assert(midiEvents.length === 2, 'Should convert all events');
assert(midiEvents[0].start_ms === 0, 'First event should start at 0ms');
assert(midiEvents[0].duration_ms === 250, 'Duration should be calculated correctly (120 BPM)');
assert(midiEvents[1].start_ms === 500, 'Second event timing should be correct');

// Test 5: Group by family
console.log('\nTest 5: Grouping by family');
const grouped = groupByFamily(validNotation);
assert(Object.keys(grouped).length === 2, 'Should have 2 families');
assert(grouped.SIN.length === 1, 'SIN family should have 1 event');
assert(grouped.COS.length === 1, 'COS family should have 1 event');

// Test 6: Statistics calculation
console.log('\nTest 6: Statistics calculation');
const stats = calculateStats(validNotation);
assert(stats.totalEvents === 2, 'Should count 2 events');
assert(stats.singularityCount === 1, 'Should count 1 singularity');
assert(stats.avgVelocity === 75, 'Average velocity should be 75');
assert(stats.familyCounts.SIN === 1, 'SIN family count should be 1');
assert(stats.familyCounts.COS === 1, 'COS family count should be 1');

// Test 7: Unknown family validation
console.log('\nTest 7: Unknown family detection');
const unknownFamily = JSON.parse(JSON.stringify(validNotation));
unknownFamily.events[0].family = "UNKNOWN";
const result7 = validateNotation(unknownFamily);
assert(!result7.valid, 'Unknown family should fail validation');

// Test 8: Invalid singularity reference
console.log('\nTest 8: Invalid singularity detection');
const invalidSingularity = JSON.parse(JSON.stringify(validNotation));
invalidSingularity.singularities = [999];
const result8 = validateNotation(invalidSingularity);
assert(!result8.valid, 'Non-existent singularity should fail validation');

// Test 9: Negative tempo validation
console.log('\nTest 9: Negative tempo detection');
const negativeTempo = JSON.parse(JSON.stringify(validNotation));
negativeTempo.meta.tempo = -120;
const result9 = validateNotation(negativeTempo);
assert(!result9.valid, 'Negative tempo should fail validation');

// Test 10: Invalid velocity range
console.log('\nTest 10: Velocity range validation');
const invalidVelocity = JSON.parse(JSON.stringify(validNotation));
invalidVelocity.events[0].velocity = 200;
const result10 = validateNotation(invalidVelocity);
assert(!result10.valid, 'Velocity > 127 should fail validation');

console.log('\n' + '═'.repeat(60));
console.log('✨ All tests passed!');
console.log('═'.repeat(60));
