// Hybrid Evolution: Genetic Algorithm for Avian-Cetacean Pattern Synthesis
// Mutates crow low-frequency patterns into cetacean high-frequency dialects

use crate::avian_bio::{BioUnit, Species, frequency_ranges};
use std::collections::HashMap;

/// Genetic algorithm for evolving hybrid bio-acoustic patterns
pub struct HybridEvolver {
    population_size: usize,
    mutation_rate: f64,
    crossover_rate: f64,
    generations: usize,
}

impl HybridEvolver {
    pub fn new(population_size: usize, mutation_rate: f64, crossover_rate: f64, generations: usize) -> Self {
        Self {
            population_size,
            mutation_rate,
            crossover_rate,
            generations,
        }
    }
    
    /// Create default evolver with standard parameters
    pub fn default() -> Self {
        Self::new(50, 0.1, 0.7, 100)
    }
    
    /// Evolve crow patterns into dolphin-crow hybrid
    pub fn evolve_crow_dolphin(&self, crow_units: Vec<BioUnit>) -> Vec<BioUnit> {
        let target_species = Species::Hybrid(
            Box::new(Species::Crow),
            Box::new(Species::Dolphin),
        );
        
        self.evolve_hybrid(
            crow_units,
            (frequency_ranges::CROW_MIN, frequency_ranges::DOLPHIN_MAX),
            target_species,
        )
    }
    
    /// Evolve crow patterns into orca-crow hybrid
    pub fn evolve_crow_orca(&self, crow_units: Vec<BioUnit>) -> Vec<BioUnit> {
        let target_species = Species::Hybrid(
            Box::new(Species::Crow),
            Box::new(Species::Orca),
        );
        
        self.evolve_hybrid(
            crow_units,
            (frequency_ranges::CROW_MIN, frequency_ranges::ORCA_MAX),
            target_species,
        )
    }
    
    /// Generic hybrid evolution
    fn evolve_hybrid(
        &self,
        initial_units: Vec<BioUnit>,
        target_freq_range: (f64, f64),
        target_species: Species,
    ) -> Vec<BioUnit> {
        let mut population = self.initialize_population(initial_units.clone(), target_freq_range);
        
        for generation in 0..self.generations {
            // Evaluate fitness
            let fitness_scores = self.evaluate_population(&population, target_freq_range);
            
            // Select parents
            let parents = self.select_parents(&population, &fitness_scores);
            
            // Create new generation
            population = self.create_next_generation(&parents, target_freq_range);
        }
        
        // Return best individual
        let fitness_scores = self.evaluate_population(&population, target_freq_range);
        let best_idx = fitness_scores
            .iter()
            .enumerate()
            .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
            .map(|(idx, _)| idx)
            .unwrap_or(0);
        
        let mut best = population[best_idx].clone();
        for unit in &mut best {
            unit.species = target_species.clone();
        }
        
        best
    }
    
    /// Initialize population with variations of initial units
    fn initialize_population(
        &self,
        initial: Vec<BioUnit>,
        freq_range: (f64, f64),
    ) -> Vec<Vec<BioUnit>> {
        let mut population = Vec::new();
        
        for _ in 0..self.population_size {
            let mut individual = initial.clone();
            
            // Apply random frequency shifts toward target range
            for unit in &mut individual {
                let shift_factor = rand::random::<f64>();
                unit.frequency = freq_range.0 + (freq_range.1 - freq_range.0) * shift_factor;
            }
            
            population.push(individual);
        }
        
        population
    }
    
    /// Evaluate fitness of population
    /// Fitness = Zipf adherence + frequency coverage + duration efficiency
    fn evaluate_population(
        &self,
        population: &[Vec<BioUnit>],
        target_freq_range: (f64, f64),
    ) -> Vec<f64> {
        population
            .iter()
            .map(|individual| self.calculate_fitness(individual, target_freq_range))
            .collect()
    }
    
    /// Calculate fitness for an individual
    fn calculate_fitness(&self, individual: &[BioUnit], target_freq_range: (f64, f64)) -> f64 {
        let mut fitness = 0.0;
        
        // 1. Zipf adherence (check if ranks follow power law)
        let zipf_score = self.zipf_adherence_score(individual);
        fitness += zipf_score * 0.4;
        
        // 2. Frequency coverage (how well it spans target range)
        let coverage_score = self.frequency_coverage_score(individual, target_freq_range);
        fitness += coverage_score * 0.3;
        
        // 3. Duration efficiency (abbreviation effect)
        let duration_score = self.duration_efficiency_score(individual);
        fitness += duration_score * 0.3;
        
        fitness
    }
    
    fn zipf_adherence_score(&self, individual: &[BioUnit]) -> f64 {
        // Simple approximation: check if high ranks have lower durations
        let mut score = 0.0;
        for i in 0..individual.len().saturating_sub(1) {
            if individual[i].duration >= individual[i + 1].duration {
                score += 1.0;
            }
        }
        score / individual.len().max(1) as f64
    }
    
    fn frequency_coverage_score(&self, individual: &[BioUnit], range: (f64, f64)) -> f64 {
        let freqs: Vec<f64> = individual.iter().map(|u| u.frequency).collect();
        let min = freqs.iter().cloned().fold(f64::INFINITY, f64::min);
        let max = freqs.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
        
        let coverage = (max - min) / (range.1 - range.0);
        coverage.min(1.0)
    }
    
    fn duration_efficiency_score(&self, individual: &[BioUnit]) -> f64 {
        // Check if high-frequency units have shorter durations
        let mut correlation = 0.0;
        let avg_duration: f64 = individual.iter().map(|u| u.duration).sum::<f64>() / individual.len() as f64;
        
        for unit in individual {
            if unit.duration < avg_duration {
                correlation += 1.0;
            }
        }
        
        correlation / individual.len() as f64
    }
    
    /// Select parents for next generation using tournament selection
    fn select_parents(
        &self,
        population: &[Vec<BioUnit>],
        fitness_scores: &[f64],
    ) -> Vec<Vec<BioUnit>> {
        let mut parents = Vec::new();
        
        for _ in 0..self.population_size {
            // Tournament selection with size 3
            let mut best_idx = rand::random::<usize>() % population.len();
            let mut best_fitness = fitness_scores[best_idx];
            
            for _ in 0..2 {
                let idx = rand::random::<usize>() % population.len();
                if fitness_scores[idx] > best_fitness {
                    best_idx = idx;
                    best_fitness = fitness_scores[idx];
                }
            }
            
            parents.push(population[best_idx].clone());
        }
        
        parents
    }
    
    /// Create next generation through crossover and mutation
    fn create_next_generation(
        &self,
        parents: &[Vec<BioUnit>],
        freq_range: (f64, f64),
    ) -> Vec<Vec<BioUnit>> {
        let mut next_gen = Vec::new();
        
        for i in (0..parents.len()).step_by(2) {
            let parent1 = &parents[i];
            let parent2 = &parents[(i + 1) % parents.len()];
            
            let (mut child1, mut child2) = if rand::random::<f64>() < self.crossover_rate {
                self.crossover(parent1, parent2)
            } else {
                (parent1.clone(), parent2.clone())
            };
            
            self.mutate(&mut child1, freq_range);
            self.mutate(&mut child2, freq_range);
            
            next_gen.push(child1);
            if next_gen.len() < self.population_size {
                next_gen.push(child2);
            }
        }
        
        next_gen
    }
    
    /// Crossover two parents
    fn crossover(&self, parent1: &[BioUnit], parent2: &[BioUnit]) -> (Vec<BioUnit>, Vec<BioUnit>) {
        let len = parent1.len().min(parent2.len());
        let crossover_point = rand::random::<usize>() % len;
        
        let mut child1 = parent1[..crossover_point].to_vec();
        child1.extend_from_slice(&parent2[crossover_point..len]);
        
        let mut child2 = parent2[..crossover_point].to_vec();
        child2.extend_from_slice(&parent1[crossover_point..len]);
        
        (child1, child2)
    }
    
    /// Mutate individual
    fn mutate(&self, individual: &mut [BioUnit], freq_range: (f64, f64)) {
        for unit in individual.iter_mut() {
            if rand::random::<f64>() < self.mutation_rate {
                // Mutate frequency within range
                let mutation = (rand::random::<f64>() - 0.5) * (freq_range.1 - freq_range.0) * 0.1;
                unit.frequency = (unit.frequency + mutation)
                    .max(freq_range.0)
                    .min(freq_range.1);
                
                // Mutate duration slightly
                let duration_mutation = (rand::random::<f64>() - 0.5) * unit.duration * 0.2;
                unit.duration = (unit.duration + duration_mutation).max(1.0);
            }
        }
    }
}

// Simple random number generation for deterministic testing
mod rand {
    use std::cell::Cell;
    
    thread_local! {
        static SEED: Cell<u64> = Cell::new(12345);
    }
    
    pub fn random<T>() -> T
    where
        T: From<u64>,
    {
        SEED.with(|seed| {
            let mut s = seed.get();
            s ^= s << 13;
            s ^= s >> 7;
            s ^= s << 17;
            seed.set(s);
            T::from(s)
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_hybrid_evolver_creation() {
        let evolver = HybridEvolver::default();
        assert_eq!(evolver.population_size, 50);
        assert_eq!(evolver.generations, 100);
    }
    
    #[test]
    fn test_population_initialization() {
        let evolver = HybridEvolver::new(10, 0.1, 0.7, 10);
        let initial = vec![
            BioUnit {
                frequency: 1000.0,
                duration: 200.0,
                rank: 1,
                species: Species::Crow,
            }
        ];
        
        let population = evolver.initialize_population(
            initial,
            (frequency_ranges::CROW_MIN, frequency_ranges::DOLPHIN_MAX),
        );
        
        assert_eq!(population.len(), 10);
    }
}
