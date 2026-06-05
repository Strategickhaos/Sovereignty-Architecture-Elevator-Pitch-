// PERIODIC TABLE OF SOVEREIGN ELEMENTS
// Own symbolic elements for sovereign operations
// 118 elements mapped to computational operations

export interface SovereignElement {
  number: number;
  symbol: string;
  name: string;
  operation: string;
  frequency: number;  // Resonant frequency in Hz
  properties: string[];
}

/**
 * Core sovereign elements (first 20 for MVP)
 */
export const SOVEREIGN_ELEMENTS: SovereignElement[] = [
  {
    number: 1,
    symbol: 'H',
    name: 'Hydrogenium',
    operation: 'proton_simulation',
    frequency: 1000.0,
    properties: ['fundamental', 'wave_base', 'entanglement_seed']
  },
  {
    number: 2,
    symbol: 'Qb',
    name: 'Qubitium',
    operation: 'quantum_entanglement',
    frequency: 2000.0,
    properties: ['superposition', 'collapse_ready', 'dual_state']
  },
  {
    number: 3,
    symbol: 'Sy',
    name: 'Synapsium',
    operation: 'neural_tick',
    frequency: 3449.0,  // Genesis increment
    properties: ['cognitive', 'temporal_sync', 'consciousness']
  },
  {
    number: 4,
    symbol: 'Tr',
    name: 'Trinium',
    operation: 'trinary_state',
    frequency: 4000.0,
    properties: ['wave_superposition', 'phi_state', 'ternary_logic']
  },
  {
    number: 5,
    symbol: 'Ec',
    name: 'Echolium',
    operation: 'bat_echolocation',
    frequency: 100000.0,  // 100kHz bat frequency
    properties: ['sonar', 'phase_detection', 'membrane_penetration']
  },
  {
    number: 6,
    symbol: 'Wh',
    name: 'Whalium',
    operation: 'whale_song_modulation',
    frequency: 20000.0,
    properties: ['infrasonic', 'communication', 'resonance']
  },
  {
    number: 7,
    symbol: 'Cr',
    name: 'Corvium',
    operation: 'crow_pattern_recognition',
    frequency: 5000.0,
    properties: ['intelligence', 'tool_use', 'problem_solving']
  },
  {
    number: 8,
    symbol: 'Dl',
    name: 'Delphinium',
    operation: 'dolphin_whistle',
    frequency: 15000.0,
    properties: ['acoustic', 'signature_id', 'social_bond']
  },
  {
    number: 9,
    symbol: 'Dn',
    name: 'DNAsium',
    operation: 'genetic_encoding',
    frequency: 1000.0,
    properties: ['hereditary', 'mutation', 'evolution']
  },
  {
    number: 10,
    symbol: 'Pr',
    name: 'Proteinium',
    operation: 'protein_folding',
    frequency: 10000.0,
    properties: ['structural', 'catalytic', 'state_machine']
  },
  {
    number: 11,
    symbol: 'Ne',
    name: 'Neutronium',
    operation: 'neutron_simulation',
    frequency: 150000.0,
    properties: ['nuclear', 'stability', 'mass_carrier']
  },
  {
    number: 12,
    symbol: 'En',
    name: 'Entropium',
    operation: 'entropy_harvest',
    frequency: 7000.0,
    properties: ['decay', 'disorder', 'information_loss']
  },
  {
    number: 13,
    symbol: 'Un',
    name: 'Uncertainium',
    operation: 'quantum_uncertainty',
    frequency: 8000.0,
    properties: ['probabilistic', 'measurement_affect', 'observer_dependent']
  },
  {
    number: 14,
    symbol: 'Cs',
    name: 'Curiosium',
    operation: 'curiosity_evolution',
    frequency: 12000.0,
    properties: ['exploration', 'novelty_seek', 'learning']
  },
  {
    number: 15,
    symbol: 'Mb',
    name: 'Membranium',
    operation: 'membrane_phasing',
    frequency: 20000.0,
    properties: ['permeabilization', 'resonant_entry', 'cellular_access']
  },
  {
    number: 16,
    symbol: 'Tm',
    name: 'Temporium',
    operation: 'time_sync',
    frequency: 3449.0,
    properties: ['chronological', 'genesis_lock', 'temporal_coherence']
  },
  {
    number: 17,
    symbol: 'Ud',
    name: 'UDAPium',
    operation: 'protocol_routing',
    frequency: 30000.0,
    properties: ['universal', 'sovereign_routing', 'pure_protocol']
  },
  {
    number: 18,
    symbol: 'Cp',
    name: 'Compilium',
    operation: 'code_compilation',
    frequency: 30000.0,
    properties: ['translation', 'optimization', 'machine_code']
  },
  {
    number: 19,
    symbol: 'Pk',
    name: 'Packetium',
    operation: 'packet_crafting',
    frequency: 20000.0,
    properties: ['network', 'data_frame', 'protocol_stack']
  },
  {
    number: 20,
    symbol: 'Br',
    name: 'Browserium',
    operation: 'browser_automation',
    frequency: 100000.0,
    properties: ['DOM_access', 'rendering', 'interaction']
  }
];

/**
 * Get element by symbol
 */
export function getElementBySymbol(symbol: string): SovereignElement | undefined {
  return SOVEREIGN_ELEMENTS.find(e => e.symbol === symbol);
}

/**
 * Get element by atomic number
 */
export function getElementByNumber(number: number): SovereignElement | undefined {
  return SOVEREIGN_ELEMENTS.find(e => e.number === number);
}

/**
 * Get elements by operation type
 */
export function getElementsByOperation(operation: string): SovereignElement[] {
  return SOVEREIGN_ELEMENTS.filter(e => 
    e.operation.toLowerCase().includes(operation.toLowerCase())
  );
}

/**
 * Get elements by frequency range
 */
export function getElementsByFrequencyRange(minHz: number, maxHz: number): SovereignElement[] {
  return SOVEREIGN_ELEMENTS.filter(e => 
    e.frequency >= minHz && e.frequency <= maxHz
  );
}

/**
 * Generate element for custom operation
 */
export function createCustomElement(
  number: number,
  symbol: string,
  name: string,
  operation: string,
  frequency: number
): SovereignElement {
  return {
    number,
    symbol,
    name,
    operation,
    frequency,
    properties: ['custom', 'synthetic', 'sovereign']
  };
}
