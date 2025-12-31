// TRINARY BINARY SYSTEM
// Sovereign binary using wave-states: 0/1/φ (phi) superposition
// sin(0), cos(1), tan(φ) for trinary logic

export type TriState = 0 | 1 | 'φ';

export interface TriBit {
  value: TriState;
  waveForm: 'sin' | 'cos' | 'tan';
  phase: number;  // Phase angle in radians
  amplitude: number;
}

/**
 * Convert binary to trinary representation
 */
export function binaryToTriary(binary: string): TriBit[] {
  const trinary: TriBit[] = [];
  
  for (let i = 0; i < binary.length; i += 2) {
    const pair = binary.substr(i, 2);
    const tribit = convertPairToTriBit(pair, i);
    trinary.push(tribit);
  }
  
  return trinary;
}

/**
 * Convert binary pair to trinary bit
 */
function convertPairToTriBit(pair: string, position: number): TriBit {
  const phase = (position / 10) * Math.PI;
  
  switch (pair) {
    case '00':
      return { value: 0, waveForm: 'sin', phase, amplitude: 0.0 };
    case '01':
    case '10':
      return { value: 1, waveForm: 'cos', phase, amplitude: 1.0 };
    case '11':
      return { value: 'φ', waveForm: 'tan', phase, amplitude: 1.618033988749895 }; // Golden ratio
    default:
      return { value: 0, waveForm: 'sin', phase: 0, amplitude: 0.0 };
  }
}

/**
 * Calculate wave value at given time for tribit
 */
export function calculateWaveValue(tribit: TriBit, time: number, frequency: number): number {
  const omega = 2 * Math.PI * frequency;
  const angle = omega * time + tribit.phase;
  
  switch (tribit.waveForm) {
    case 'sin':
      return tribit.amplitude * Math.sin(angle);
    case 'cos':
      return tribit.amplitude * Math.cos(angle);
    case 'tan':
      // Limit tan to avoid infinities
      const tanValue = Math.tan(angle);
      return tribit.amplitude * Math.max(-10, Math.min(10, tanValue));
    default:
      return 0;
  }
}

/**
 * Encode data as trinary wave states
 */
export function encodeToTriWave(data: Uint8Array): TriBit[] {
  const binary = Array.from(data)
    .map(byte => byte.toString(2).padStart(8, '0'))
    .join('');
  return binaryToTriary(binary);
}

/**
 * Decode trinary wave states to data
 */
export function decodeFromTriWave(tribits: TriBit[]): Uint8Array {
  let binary = '';
  
  for (const tribit of tribits) {
    switch (tribit.value) {
      case 0:
        binary += '00';
        break;
      case 1:
        binary += '01';
        break;
      case 'φ':
        binary += '11';
        break;
    }
  }
  
  // Pad to byte boundary
  while (binary.length % 8 !== 0) {
    binary += '0';
  }
  
  // Convert to bytes
  const bytes: number[] = [];
  for (let i = 0; i < binary.length; i += 8) {
    bytes.push(parseInt(binary.substr(i, 8), 2));
  }
  
  return new Uint8Array(bytes);
}

/**
 * Superposition state: Quantum-like state combining multiple tribits
 */
export interface SuperpositionState {
  tribits: TriBit[];
  collapsed: boolean;
  observationTime: number | null;
}

/**
 * Create superposition from tribits
 */
export function createSuperposition(tribits: TriBit[]): SuperpositionState {
  return {
    tribits,
    collapsed: false,
    observationTime: null
  };
}

/**
 * Collapse superposition to definite state
 */
export function collapseSuperposition(state: SuperpositionState, time: number): TriBit {
  if (!state.collapsed) {
    state.collapsed = true;
    state.observationTime = time;
  }
  
  // Weighted random selection based on amplitudes
  const totalAmplitude = state.tribits.reduce((sum, tb) => sum + Math.abs(tb.amplitude), 0);
  let random = Math.random() * totalAmplitude;
  
  for (const tribit of state.tribits) {
    random -= Math.abs(tribit.amplitude);
    if (random <= 0) {
      return tribit;
    }
  }
  
  return state.tribits[state.tribits.length - 1];
}

/**
 * Generate sovereign binary code using trinary states
 */
export function generateSovereignBinary(input: string, frequency: number = 30000): {
  tribits: TriBit[];
  waveSignature: number[];
  udapRoute: string;
} {
  const encoder = new TextEncoder();
  const data = encoder.encode(input);
  const tribits = encodeToTriWave(data);
  
  // Generate wave signature over time
  const waveSignature: number[] = [];
  const duration = 0.001; // 1ms
  const samples = 100;
  
  for (let i = 0; i < samples; i++) {
    const time = (i / samples) * duration;
    const waveSum = tribits.reduce((sum, tb) => 
      sum + calculateWaveValue(tb, time, frequency), 0
    );
    waveSignature.push(waveSum / tribits.length);
  }
  
  return {
    tribits,
    waveSignature,
    udapRoute: `skhaos://pure/compiler/trinary?freq=${frequency}&input=${encodeURIComponent(input)}`
  };
}
