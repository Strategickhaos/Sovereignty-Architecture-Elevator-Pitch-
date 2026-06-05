// ATOM SIMULATION
// Simulates protons, neutrons, electrons, and cellular particles
// Wave-based particle physics for sovereign computing

export interface Particle {
  type: 'proton' | 'neutron' | 'electron' | 'cellular';
  mass: number;  // Relative mass units
  charge: number;  // -1, 0, or +1
  spin: number;  // Angular momentum
  position: [number, number, number];  // 3D coordinates
  velocity: [number, number, number];  // 3D velocity vector
  waveFrequency: number;  // De Broglie frequency in Hz
}

export interface Atom {
  element: string;
  protons: Particle[];
  neutrons: Particle[];
  electrons: Particle[];
  energyLevel: number;
}

/**
 * Create a proton particle
 */
export function createProton(position: [number, number, number] = [0, 0, 0]): Particle {
  return {
    type: 'proton',
    mass: 1.0,
    charge: 1,
    spin: 0.5,
    position,
    velocity: [0, 0, 0],
    waveFrequency: 1000.0  // Base proton frequency
  };
}

/**
 * Create a neutron particle
 */
export function createNeutron(position: [number, number, number] = [0, 0, 0]): Particle {
  return {
    type: 'neutron',
    mass: 1.0,
    charge: 0,
    spin: 0.5,
    position,
    velocity: [0, 0, 0],
    waveFrequency: 150000.0  // High neutron frequency
  };
}

/**
 * Create an electron particle
 */
export function createElectron(position: [number, number, number] = [0, 0, 0]): Particle {
  return {
    type: 'electron',
    mass: 0.0005,
    charge: -1,
    spin: 0.5,
    position,
    velocity: [0, 0, 0],
    waveFrequency: 10000.0
  };
}

/**
 * Create a cellular particle (for biological simulations)
 */
export function createCellularParticle(position: [number, number, number] = [0, 0, 0]): Particle {
  return {
    type: 'cellular',
    mass: 100.0,  // Much larger than atomic particles
    charge: 0,
    spin: 0,
    position,
    velocity: [0, 0, 0],
    waveFrequency: 20000.0  // Membrane phasing frequency
  };
}

/**
 * Simulate atom with given proton count
 */
export function simulateAtom(protonCount: number, elementSymbol: string): Atom {
  const protons: Particle[] = [];
  const neutrons: Particle[] = [];
  const electrons: Particle[] = [];
  
  // Create protons in nucleus
  for (let i = 0; i < protonCount; i++) {
    const angle = (i / protonCount) * 2 * Math.PI;
    const radius = 0.1;
    protons.push(createProton([
      radius * Math.cos(angle),
      radius * Math.sin(angle),
      0
    ]));
  }
  
  // Create neutrons (typically equal or more than protons)
  const neutronCount = Math.ceil(protonCount * 1.2);
  for (let i = 0; i < neutronCount; i++) {
    const angle = (i / neutronCount) * 2 * Math.PI;
    const radius = 0.1;
    neutrons.push(createNeutron([
      radius * Math.cos(angle + Math.PI / neutronCount),
      radius * Math.sin(angle + Math.PI / neutronCount),
      0.05
    ]));
  }
  
  // Create electrons in shells
  for (let i = 0; i < protonCount; i++) {
    const shell = Math.floor(i / 8);  // Simple shell model
    const posInShell = i % 8;
    const angle = (posInShell / 8) * 2 * Math.PI;
    const radius = 1.0 + (shell * 0.5);
    
    electrons.push(createElectron([
      radius * Math.cos(angle),
      radius * Math.sin(angle),
      0
    ]));
  }
  
  return {
    element: elementSymbol,
    protons,
    neutrons,
    electrons,
    energyLevel: protonCount * 1000.0
  };
}

/**
 * Calculate wave function for particle at time t
 */
export function calculateParticleWave(particle: Particle, time: number): number {
  const omega = 2 * Math.PI * particle.waveFrequency;
  const [x, y, z] = particle.position;
  const r = Math.sqrt(x * x + y * y + z * z);
  
  // Simplified wave function: amplitude modulated by distance
  const amplitude = Math.exp(-r / 5.0);  // Decay with distance
  return amplitude * Math.sin(omega * time + particle.spin * Math.PI);
}

/**
 * Simulate cellular membrane phasing at resonant frequency
 */
export function simulateMembranePhasing(
  cellularParticles: Particle[],
  resonantFreqHz: number,
  duration: number
): {
  phaseAchieved: boolean;
  resonanceMatch: number;  // 0-1 scale
  entryPoints: number;
} {
  let totalResonance = 0;
  let entryPoints = 0;
  
  for (const particle of cellularParticles) {
    const freqDiff = Math.abs(particle.waveFrequency - resonantFreqHz);
    const resonance = Math.exp(-freqDiff / 10000.0);
    
    totalResonance += resonance;
    
    // Entry achieved if resonance > 0.9
    if (resonance > 0.9) {
      entryPoints++;
    }
  }
  
  const avgResonance = totalResonance / cellularParticles.length;
  
  return {
    phaseAchieved: avgResonance > 0.8,
    resonanceMatch: avgResonance,
    entryPoints
  };
}

/**
 * Simulate partial acceleration in synthesis
 */
export function simulateSynthesisAcceleration(
  atom: Atom,
  targetFreqHz: number
): {
  accelerated: boolean;
  newEnergyLevel: number;
  particleAccelerations: Map<string, number>;
} {
  const accelerations = new Map<string, number>();
  let totalAcceleration = 0;
  
  // Accelerate protons
  for (let i = 0; i < atom.protons.length; i++) {
    const accel = (targetFreqHz / 1000.0) * (1 + Math.random() * 0.1);
    accelerations.set(`proton_${i}`, accel);
    totalAcceleration += accel;
  }
  
  // Accelerate neutrons
  for (let i = 0; i < atom.neutrons.length; i++) {
    const accel = (targetFreqHz / 150000.0) * (1 + Math.random() * 0.1);
    accelerations.set(`neutron_${i}`, accel);
    totalAcceleration += accel;
  }
  
  const avgAcceleration = totalAcceleration / (atom.protons.length + atom.neutrons.length);
  const newEnergyLevel = atom.energyLevel * (1 + avgAcceleration);
  
  return {
    accelerated: avgAcceleration > 0.5,
    newEnergyLevel,
    particleAccelerations: accelerations
  };
}
