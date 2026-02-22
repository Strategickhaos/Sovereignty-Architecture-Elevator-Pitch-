/**
 * FLAMELANG Musical Notation System
 * 
 * A glyph-based musical notation system using trigonometric function families
 * to represent musical events with precise timing and MIDI mapping.
 */

/**
 * Metadata for a musical composition
 */
export interface NotationMeta {
  /** Tempo in beats per minute */
  tempo: number;
  /** Base MIDI note (typically C4 = 60) */
  base_note: number;
  /** Number of beats in a complete cycle */
  beats_per_cycle: number;
  /** Total number of notes in the composition */
  note_count: number;
}

/**
 * A single musical event represented by a glyph
 */
export interface NotationEvent {
  /** Unique identifier for this glyph */
  glyph_id: number;
  /** The glyph symbol itself (Unicode character) */
  glyph: string;
  /** Trigonometric function family (SIN, COS, TAN, CSC, SEC, COT) */
  family: string;
  /** Angle in degrees (0-360) */
  theta: number;
  /** MIDI note number (0-127) */
  midi_note: number;
  /** MIDI velocity (0-127) */
  velocity: number;
  /** Starting beat position */
  start_beat: number;
  /** Duration in beats */
  duration_beats: number;
}

/**
 * Family characteristics defining behavior for a group of glyphs
 */
export interface FamilyConfig {
  /** Base velocity for this family */
  base_velocity: number;
  /** Duration multiplier for this family */
  duration_mult: number;
  /** MIDI channel for this family */
  channel: number;
}

/**
 * Complete musical notation structure
 */
export interface MusicalNotation {
  /** Composition metadata */
  meta: NotationMeta;
  /** Array of musical events/glyphs */
  events: NotationEvent[];
  /** Configuration for each family */
  families: Record<string, FamilyConfig>;
  /** Array of glyph IDs that represent singularities (special points) */
  singularities: number[];
}

/**
 * Validates a musical notation object
 */
export function validateNotation(notation: MusicalNotation): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Validate meta
  if (notation.meta.tempo <= 0) {
    errors.push("Tempo must be positive");
  }
  if (notation.meta.base_note < 0 || notation.meta.base_note > 127) {
    errors.push("Base note must be between 0 and 127");
  }
  if (notation.meta.beats_per_cycle <= 0) {
    errors.push("Beats per cycle must be positive");
  }

  // Validate events
  notation.events.forEach((event, index) => {
    if (event.glyph_id !== index) {
      errors.push(`Event ${index} has mismatched glyph_id ${event.glyph_id}`);
    }
    if (event.theta < 0 || event.theta >= 360) {
      errors.push(`Event ${index} has invalid theta ${event.theta} (must be 0-360)`);
    }
    if (event.midi_note < 0 || event.midi_note > 127) {
      errors.push(`Event ${index} has invalid MIDI note ${event.midi_note}`);
    }
    if (event.velocity < 0 || event.velocity > 127) {
      errors.push(`Event ${index} has invalid velocity ${event.velocity}`);
    }
    if (event.start_beat < 0) {
      errors.push(`Event ${index} has negative start_beat`);
    }
    if (event.duration_beats <= 0) {
      errors.push(`Event ${index} has non-positive duration`);
    }
    if (!notation.families[event.family]) {
      errors.push(`Event ${index} references unknown family ${event.family}`);
    }
  });

  // Validate families
  Object.entries(notation.families).forEach(([family, config]) => {
    if (config.base_velocity < 0 || config.base_velocity > 127) {
      errors.push(`Family ${family} has invalid base_velocity`);
    }
    if (config.duration_mult <= 0) {
      errors.push(`Family ${family} has non-positive duration_mult`);
    }
    if (config.channel < 0 || config.channel > 15) {
      errors.push(`Family ${family} has invalid MIDI channel`);
    }
  });

  // Validate singularities
  notation.singularities.forEach((id) => {
    if (!notation.events.find(e => e.glyph_id === id)) {
      errors.push(`Singularity references non-existent glyph_id ${id}`);
    }
  });

  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Converts a musical notation to MIDI timing
 * @param notation The musical notation
 * @returns An array of MIDI events with absolute timing in milliseconds
 */
export function convertToMidiTiming(notation: MusicalNotation) {
  const { tempo, beats_per_cycle } = notation.meta;
  const msPerBeat = 60000 / tempo; // milliseconds per beat

  return notation.events.map(event => ({
    ...event,
    start_ms: event.start_beat * msPerBeat,
    duration_ms: event.duration_beats * msPerBeat,
    end_ms: (event.start_beat + event.duration_beats) * msPerBeat
  }));
}

/**
 * Groups events by their trigonometric family
 */
export function groupByFamily(notation: MusicalNotation) {
  const grouped: Record<string, NotationEvent[]> = {};
  
  notation.events.forEach(event => {
    if (!grouped[event.family]) {
      grouped[event.family] = [];
    }
    grouped[event.family].push(event);
  });

  return grouped;
}

/**
 * Calculates statistics for a musical notation
 */
export function calculateStats(notation: MusicalNotation) {
  const totalDuration = Math.max(...notation.events.map(e => e.start_beat + e.duration_beats));
  const avgVelocity = notation.events.reduce((sum, e) => sum + e.velocity, 0) / notation.events.length;
  const familyCounts = Object.fromEntries(
    Object.keys(notation.families).map(family => [
      family,
      notation.events.filter(e => e.family === family).length
    ])
  );

  return {
    totalDuration,
    avgVelocity,
    familyCounts,
    totalEvents: notation.events.length,
    singularityCount: notation.singularities.length
  };
}
