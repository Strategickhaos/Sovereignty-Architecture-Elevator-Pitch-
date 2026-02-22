/**
 * Example usage and test of the FLAMELANG Musical Notation System
 */

import { 
  validateNotation, 
  convertToMidiTiming, 
  groupByFamily, 
  calculateStats,
  type MusicalNotation 
} from './flamelang-notation.js';
import { readFileSync } from 'fs';
import { join } from 'path';

// Load the example notation
const notationPath = join(process.cwd(), 'data', 'notation-example.json');
const notation: MusicalNotation = JSON.parse(readFileSync(notationPath, 'utf-8'));

console.log('🎵 FLAMELANG Musical Notation System Demo\n');
console.log('═'.repeat(60));

// 1. Validate the notation
console.log('\n📋 Validation Results:');
console.log('─'.repeat(60));
const validation = validateNotation(notation);
if (validation.valid) {
  console.log('✅ Notation is valid!');
} else {
  console.log('❌ Validation errors found:');
  validation.errors.forEach(error => console.log(`   - ${error}`));
}

// 2. Display metadata
console.log('\n📊 Composition Metadata:');
console.log('─'.repeat(60));
console.log(`Tempo:           ${notation.meta.tempo} BPM`);
console.log(`Base Note:       ${notation.meta.base_note} (MIDI)`);
console.log(`Beats per Cycle: ${notation.meta.beats_per_cycle}`);
console.log(`Total Notes:     ${notation.meta.note_count}`);

// 3. Calculate statistics
console.log('\n📈 Statistics:');
console.log('─'.repeat(60));
const stats = calculateStats(notation);
console.log(`Total Duration:  ${stats.totalDuration.toFixed(2)} beats`);
console.log(`Average Velocity: ${stats.avgVelocity.toFixed(1)}`);
console.log(`Total Events:    ${stats.totalEvents}`);
console.log(`Singularities:   ${stats.singularityCount}`);

// 4. Family distribution
console.log('\n🎼 Family Distribution:');
console.log('─'.repeat(60));
const grouped = groupByFamily(notation);
Object.entries(stats.familyCounts).forEach(([family, count]) => {
  const config = notation.families[family];
  const percentage = ((count / stats.totalEvents) * 100).toFixed(1);
  console.log(`${family.padEnd(4)}: ${count.toString().padStart(2)} events (${percentage}%) ` +
              `| Vel: ${config.base_velocity}, Dur: ${config.duration_mult}x, Ch: ${config.channel}`);
});

// 5. Show singularities
console.log('\n⚠️  Singularities (Key Points):');
console.log('─'.repeat(60));
notation.singularities.forEach(id => {
  const event = notation.events.find(e => e.glyph_id === id);
  if (event) {
    console.log(`ID ${id.toString().padStart(2)}: ${event.glyph.padEnd(3)} | ` +
                `${event.family.padEnd(4)} | θ=${event.theta.toString().padStart(5)}° | ` +
                `Beat ${event.start_beat.toFixed(2)} | ` +
                `Note ${event.midi_note} | Vel ${event.velocity}`);
  }
});

// 6. Sample MIDI timing conversion
console.log('\n⏱️  Sample MIDI Timing (First 5 Events):');
console.log('─'.repeat(60));
const midiEvents = convertToMidiTiming(notation);
midiEvents.slice(0, 5).forEach((event, idx) => {
  console.log(`${idx}: ${event.glyph.padEnd(3)} | ` +
              `Start: ${event.start_ms.toFixed(0).padStart(5)}ms | ` +
              `Duration: ${event.duration_ms.toFixed(0).padStart(4)}ms | ` +
              `Note: ${event.midi_note.toString().padStart(2)} | ` +
              `Vel: ${event.velocity}`);
});

// 7. Theta distribution analysis
console.log('\n🌀 Theta (Angle) Distribution:');
console.log('─'.repeat(60));
const thetaRanges = {
  '0-90°':    notation.events.filter(e => e.theta >= 0 && e.theta < 90).length,
  '90-180°':  notation.events.filter(e => e.theta >= 90 && e.theta < 180).length,
  '180-270°': notation.events.filter(e => e.theta >= 180 && e.theta < 270).length,
  '270-360°': notation.events.filter(e => e.theta >= 270 && e.theta < 360).length,
};
Object.entries(thetaRanges).forEach(([range, count]) => {
  const bar = '█'.repeat(Math.floor(count / 2));
  console.log(`${range.padEnd(10)}: ${count.toString().padStart(2)} ${bar}`);
});

// 8. Velocity distribution
console.log('\n🔊 Velocity Distribution:');
console.log('─'.repeat(60));
const velocities = notation.events.map(e => e.velocity);
const minVel = Math.min(...velocities);
const maxVel = Math.max(...velocities);
console.log(`Range: ${minVel} - ${maxVel}`);
console.log(`Mean:  ${stats.avgVelocity.toFixed(1)}`);

// Create histogram
const velBuckets = {
  '60-69':  velocities.filter(v => v >= 60 && v < 70).length,
  '70-79':  velocities.filter(v => v >= 70 && v < 80).length,
  '80-89':  velocities.filter(v => v >= 80 && v < 90).length,
  '90-99':  velocities.filter(v => v >= 90 && v < 100).length,
  '100-127': velocities.filter(v => v >= 100 && v <= 127).length,
};
Object.entries(velBuckets).forEach(([range, count]) => {
  if (count > 0) {
    const bar = '▓'.repeat(Math.floor(count / 3));
    console.log(`${range.padEnd(8)}: ${count.toString().padStart(2)} ${bar}`);
  }
});

console.log('\n' + '═'.repeat(60));
console.log('🔥 Demo Complete - FLAMELANG Musical Notation System');
console.log('═'.repeat(60) + '\n');
