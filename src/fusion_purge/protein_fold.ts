// PROTEIN FOLDING STATE MACHINES
// Foldable state machines from MSMC (Music State Machine Compiler)
// Maps musical forms to protein-like structural states

export interface ProteinState {
  name: string;
  structure: 'alpha_helix' | 'beta_sheet' | 'random_coil' | 'turn';
  energy: number;  // Free energy in kJ/mol
  hydrophobicity: number;  // -1 (hydrophilic) to 1 (hydrophobic)
  transitions: string[];  // Possible next states
}

export interface ProteinFold {
  name: string;
  states: ProteinState[];
  currentState: string;
  foldingPathway: string[];
  totalEnergy: number;
}

/**
 * Standard protein secondary structures
 */
export const PROTEIN_STRUCTURES: Record<string, ProteinState> = {
  'helix_start': {
    name: 'helix_start',
    structure: 'alpha_helix',
    energy: -5.0,
    hydrophobicity: 0.3,
    transitions: ['helix_middle', 'turn_1']
  },
  'helix_middle': {
    name: 'helix_middle',
    structure: 'alpha_helix',
    energy: -8.0,
    hydrophobicity: 0.5,
    transitions: ['helix_middle', 'helix_end', 'turn_1']
  },
  'helix_end': {
    name: 'helix_end',
    structure: 'alpha_helix',
    energy: -4.0,
    hydrophobicity: 0.2,
    transitions: ['turn_1', 'coil_1']
  },
  'sheet_start': {
    name: 'sheet_start',
    structure: 'beta_sheet',
    energy: -6.0,
    hydrophobicity: 0.6,
    transitions: ['sheet_middle', 'turn_2']
  },
  'sheet_middle': {
    name: 'sheet_middle',
    structure: 'beta_sheet',
    energy: -9.0,
    hydrophobicity: 0.7,
    transitions: ['sheet_middle', 'sheet_end', 'turn_2']
  },
  'sheet_end': {
    name: 'sheet_end',
    structure: 'beta_sheet',
    energy: -5.0,
    hydrophobicity: 0.4,
    transitions: ['turn_2', 'coil_1']
  },
  'turn_1': {
    name: 'turn_1',
    structure: 'turn',
    energy: -2.0,
    hydrophobicity: -0.3,
    transitions: ['helix_start', 'sheet_start', 'coil_1']
  },
  'turn_2': {
    name: 'turn_2',
    structure: 'turn',
    energy: -2.5,
    hydrophobicity: -0.2,
    transitions: ['helix_start', 'sheet_start', 'coil_2']
  },
  'coil_1': {
    name: 'coil_1',
    structure: 'random_coil',
    energy: 0.0,
    hydrophobicity: 0.0,
    transitions: ['helix_start', 'sheet_start', 'turn_1', 'coil_2']
  },
  'coil_2': {
    name: 'coil_2',
    structure: 'random_coil',
    energy: 0.5,
    hydrophobicity: -0.1,
    transitions: ['helix_start', 'sheet_start', 'turn_2', 'coil_1']
  }
};

/**
 * Create a protein fold from sequence of states
 */
export function createProteinFold(name: string, initialState: string = 'coil_1'): ProteinFold {
  return {
    name,
    states: Object.values(PROTEIN_STRUCTURES),
    currentState: initialState,
    foldingPathway: [initialState],
    totalEnergy: 0.0
  };
}

/**
 * Transition protein to next state
 */
export function foldProtein(
  protein: ProteinFold,
  targetState: string
): { success: boolean; energyChange: number } {
  const currentState = PROTEIN_STRUCTURES[protein.currentState];
  
  if (!currentState) {
    return { success: false, energyChange: 0 };
  }
  
  // Check if transition is allowed
  if (!currentState.transitions.includes(targetState)) {
    return { success: false, energyChange: 0 };
  }
  
  const nextState = PROTEIN_STRUCTURES[targetState];
  if (!nextState) {
    return { success: false, energyChange: 0 };
  }
  
  // Calculate energy change
  const energyChange = nextState.energy - currentState.energy;
  
  // Update protein state
  protein.currentState = targetState;
  protein.foldingPathway.push(targetState);
  protein.totalEnergy += energyChange;
  
  return { success: true, energyChange };
}

/**
 * Auto-fold protein using energy minimization
 */
export function autoFoldProtein(
  protein: ProteinFold,
  maxSteps: number = 10
): {
  finalState: string;
  pathway: string[];
  totalEnergy: number;
  stable: boolean;
} {
  let steps = 0;
  let previousEnergy = protein.totalEnergy;
  
  while (steps < maxSteps) {
    const currentState = PROTEIN_STRUCTURES[protein.currentState];
    if (!currentState) break;
    
    // Find lowest energy transition
    let bestTransition = '';
    let lowestEnergy = Infinity;
    
    for (const transition of currentState.transitions) {
      const nextState = PROTEIN_STRUCTURES[transition];
      if (nextState && nextState.energy < lowestEnergy) {
        lowestEnergy = nextState.energy;
        bestTransition = transition;
      }
    }
    
    if (!bestTransition) break;
    
    // Fold to best state
    const result = foldProtein(protein, bestTransition);
    if (!result.success) break;
    
    steps++;
    
    // Check if converged (energy change < threshold)
    if (Math.abs(protein.totalEnergy - previousEnergy) < 0.1) {
      break;
    }
    previousEnergy = protein.totalEnergy;
  }
  
  return {
    finalState: protein.currentState,
    pathway: protein.foldingPathway,
    totalEnergy: protein.totalEnergy,
    stable: steps > 0
  };
}

/**
 * Map MSMC musical form to protein fold
 */
export function mapMusicToProtein(musicalForm: string): ProteinFold {
  const protein = createProteinFold(`MSMC_${musicalForm}`);
  
  // Map musical structures to protein structures
  const musicToProteinMap: Record<string, string[]> = {
    'rondo': ['helix_start', 'helix_middle', 'turn_1', 'helix_start', 'helix_middle', 'turn_1', 'helix_start'],
    'sonata': ['helix_start', 'helix_middle', 'turn_1', 'sheet_start', 'sheet_middle', 'turn_2', 'helix_start'],
    'fugue': ['sheet_start', 'sheet_middle', 'sheet_middle', 'turn_2', 'sheet_start', 'sheet_middle'],
    'theme_variation': ['helix_start', 'turn_1', 'sheet_start', 'turn_2', 'helix_start', 'turn_1']
  };
  
  const pathway = musicToProteinMap[musicalForm.toLowerCase()] || ['coil_1', 'helix_start', 'helix_middle'];
  
  // Execute folding pathway
  for (const state of pathway) {
    foldProtein(protein, state);
  }
  
  return protein;
}

/**
 * Generate sovereign protein from OSS function
 */
export function generateSovereignProtein(
  ossFunction: string,
  frequencyHz: number
): {
  protein: ProteinFold;
  structure: string;
  stability: number;
  udapRoute: string;
} {
  // Create protein based on function complexity
  const protein = createProteinFold(`SFP_${ossFunction}`);
  
  // Complex functions get more elaborate folds
  const complexity = ossFunction.length + ossFunction.split('_').length;
  const steps = Math.min(complexity, 10);
  
  // Auto-fold with energy minimization
  const result = autoFoldProtein(protein, steps);
  
  // Calculate stability (based on energy and pathway length)
  const stability = Math.max(0, Math.min(1, 
    (10 + result.totalEnergy) / 20 * (result.pathway.length / steps)
  ));
  
  return {
    protein,
    structure: result.pathway.join(' → '),
    stability,
    udapRoute: `skhaos://pure/protein/${ossFunction}?freq=${frequencyHz}&fold=true`
  };
}
