// Physics Domain Ontology Model (DOM)
// Universal physics laws as computational constraints:
// - Thermodynamics: Entropy (disorder increases in isolated systems)
// - Quantum Mechanics: Uncertainty principle (ΔxΔp ≥ ℏ/2)
// - Conservation Laws: Energy, momentum conservation
// - Relativity: Spacetime coordinate transformations

use std::collections::HashMap;

/// Physics constraints enforcer for bio-pattern state machines
pub struct PhysicsDom {
    pub laws: Vec<PhysicsLaw>,
    pub constraint_violations: Vec<Violation>,
    pub energy_tracker: EnergyTracker,
}

#[derive(Debug, Clone)]
pub struct PhysicsLaw {
    pub law_type: LawType,
    pub enabled: bool,
    pub parameters: HashMap<String, f64>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum LawType {
    Entropy,        // 2nd Law of Thermodynamics
    Uncertainty,    // Heisenberg Uncertainty Principle
    Conservation,   // Energy/Momentum Conservation
    Relativity,     // Spacetime Transformations
}

#[derive(Debug, Clone)]
pub struct Violation {
    pub law_type: LawType,
    pub description: String,
    pub severity: ViolationSeverity,
    pub timestamp_ms: u64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ViolationSeverity {
    Warning,
    Error,
    Critical,
}

/// Energy tracker for conservation law enforcement
#[derive(Debug, Clone)]
pub struct EnergyTracker {
    pub total_energy: f64,
    pub state_energies: HashMap<String, f64>,
    pub energy_history: Vec<EnergySnapshot>,
}

#[derive(Debug, Clone)]
pub struct EnergySnapshot {
    pub timestamp_ms: u64,
    pub total_energy: f64,
    pub delta: f64,
}

/// State machine state for physics validation
#[derive(Debug, Clone)]
pub struct PhysicsState {
    pub state_id: String,
    pub energy: f64,
    pub entropy: f64,
    pub position: (f64, f64, f64),  // x, y, z coordinates
    pub momentum: (f64, f64, f64),  // px, py, pz
}

impl PhysicsDom {
    /// Create new physics domain model with all laws enabled
    pub fn new() -> Self {
        let laws = vec![
            PhysicsLaw {
                law_type: LawType::Entropy,
                enabled: true,
                parameters: HashMap::new(),
            },
            PhysicsLaw {
                law_type: LawType::Uncertainty,
                enabled: true,
                parameters: {
                    let mut p = HashMap::new();
                    p.insert("hbar".to_string(), 1.054571817e-34); // ℏ in J·s
                    p
                },
            },
            PhysicsLaw {
                law_type: LawType::Conservation,
                enabled: true,
                parameters: HashMap::new(),
            },
            PhysicsLaw {
                law_type: LawType::Relativity,
                enabled: true,
                parameters: {
                    let mut p = HashMap::new();
                    p.insert("c".to_string(), 299792458.0); // Speed of light in m/s
                    p
                },
            },
        ];

        Self {
            laws,
            constraint_violations: Vec::new(),
            energy_tracker: EnergyTracker {
                total_energy: 0.0,
                state_energies: HashMap::new(),
                energy_history: Vec::new(),
            },
        }
    }

    /// Enable or disable a specific physics law
    pub fn set_law_enabled(&mut self, law_type: LawType, enabled: bool) {
        if let Some(law) = self.laws.iter_mut().find(|l| l.law_type == law_type) {
            law.enabled = enabled;
        }
    }

    /// Validate entropy constraint (must not decrease in isolated system)
    pub fn validate_entropy(&mut self, old_entropy: f64, new_entropy: f64, timestamp_ms: u64) -> bool {
        let law = self.laws.iter().find(|l| l.law_type == LawType::Entropy);
        if law.is_none() || !law.unwrap().enabled {
            return true;
        }

        if new_entropy < old_entropy {
            self.constraint_violations.push(Violation {
                law_type: LawType::Entropy,
                description: format!(
                    "Entropy decreased from {} to {} (violates 2nd law)",
                    old_entropy, new_entropy
                ),
                severity: ViolationSeverity::Error,
                timestamp_ms,
            });
            return false;
        }
        true
    }

    /// Validate Heisenberg uncertainty principle: Δx·Δp ≥ ℏ/2
    pub fn validate_uncertainty(
        &mut self,
        delta_position: f64,
        delta_momentum: f64,
        timestamp_ms: u64,
    ) -> bool {
        let law = self.laws.iter().find(|l| l.law_type == LawType::Uncertainty);
        if law.is_none() || !law.unwrap().enabled {
            return true;
        }

        let hbar = law.unwrap().parameters.get("hbar").copied().unwrap_or(1.054571817e-34);
        let uncertainty_product = delta_position * delta_momentum;
        let min_uncertainty = hbar / 2.0;

        if uncertainty_product < min_uncertainty {
            self.constraint_violations.push(Violation {
                law_type: LawType::Uncertainty,
                description: format!(
                    "Uncertainty product {} < ℏ/2 = {} (violates Heisenberg)",
                    uncertainty_product, min_uncertainty
                ),
                severity: ViolationSeverity::Critical,
                timestamp_ms,
            });
            return false;
        }
        true
    }

    /// Validate energy conservation in state transition
    pub fn validate_conservation(
        &mut self,
        initial_energy: f64,
        final_energy: f64,
        timestamp_ms: u64,
        tolerance: f64,
    ) -> bool {
        let law = self.laws.iter().find(|l| l.law_type == LawType::Conservation);
        if law.is_none() || !law.unwrap().enabled {
            return true;
        }

        let energy_diff = (final_energy - initial_energy).abs();
        if energy_diff > tolerance {
            self.constraint_violations.push(Violation {
                law_type: LawType::Conservation,
                description: format!(
                    "Energy not conserved: ΔE = {} exceeds tolerance {}",
                    energy_diff, tolerance
                ),
                severity: ViolationSeverity::Warning,
                timestamp_ms,
            });
            return false;
        }

        // Track energy
        self.energy_tracker.energy_history.push(EnergySnapshot {
            timestamp_ms,
            total_energy: final_energy,
            delta: final_energy - initial_energy,
        });

        true
    }

    /// Apply Lorentz transformation (special relativity)
    pub fn lorentz_transform(
        &self,
        position: (f64, f64, f64, f64),  // (t, x, y, z)
        velocity: f64,                    // v along x-axis
    ) -> (f64, f64, f64, f64) {
        let law = self.laws.iter().find(|l| l.law_type == LawType::Relativity);
        if law.is_none() || !law.unwrap().enabled {
            return position;
        }

        let c = law.unwrap().parameters.get("c").copied().unwrap_or(299792458.0);
        let beta = velocity / c;
        let gamma = 1.0 / (1.0 - beta * beta).sqrt();

        let (t, x, y, z) = position;

        let t_prime = gamma * (t - beta * x / c);
        let x_prime = gamma * (x - velocity * t);
        let y_prime = y;
        let z_prime = z;

        (t_prime, x_prime, y_prime, z_prime)
    }

    /// Calculate entropy increase for swarm mutation
    pub fn calculate_entropy_increase(&self, mutation_count: u32, diversity: f64) -> f64 {
        // S = k_B * ln(Ω) where Ω is number of microstates
        // Simplified: entropy increases with mutations and diversity
        let k_boltzmann = 1.380649e-23; // J/K
        let microstates = (mutation_count as f64) * diversity;
        if microstates <= 0.0 {
            return 0.0;
        }
        k_boltzmann * microstates.ln()
    }

    /// Enforce conservation in state machine transition
    pub fn enforce_conservation(&mut self, state_id: String, energy: f64) {
        let old_energy = self.energy_tracker.state_energies.get(&state_id).copied().unwrap_or(0.0);
        self.energy_tracker.state_energies.insert(state_id.clone(), energy);
        
        let total_before = self.energy_tracker.total_energy;
        self.energy_tracker.total_energy = self.energy_tracker.total_energy - old_energy + energy;
        
        println!(
            "State {} energy: {} -> {} (total: {} -> {})",
            state_id, old_energy, energy, total_before, self.energy_tracker.total_energy
        );
    }

    /// Get constraint violations summary
    pub fn violations_summary(&self) -> ViolationsSummary {
        let mut by_type: HashMap<String, usize> = HashMap::new();
        let mut by_severity: HashMap<String, usize> = HashMap::new();

        for violation in &self.constraint_violations {
            let type_key = format!("{:?}", violation.law_type);
            *by_type.entry(type_key).or_insert(0) += 1;

            let severity_key = format!("{:?}", violation.severity);
            *by_severity.entry(severity_key).or_insert(0) += 1;
        }

        ViolationsSummary {
            total_violations: self.constraint_violations.len(),
            by_type,
            by_severity,
        }
    }

    /// Get enabled laws
    pub fn enabled_laws(&self) -> Vec<LawType> {
        self.laws.iter()
            .filter(|l| l.enabled)
            .map(|l| l.law_type)
            .collect()
    }
}

#[derive(Debug)]
pub struct ViolationsSummary {
    pub total_violations: usize,
    pub by_type: HashMap<String, usize>,
    pub by_severity: HashMap<String, usize>,
}

impl Default for PhysicsDom {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_physics_dom_creation() {
        let dom = PhysicsDom::new();
        assert_eq!(dom.laws.len(), 4);
        assert!(dom.laws.iter().all(|l| l.enabled));
    }

    #[test]
    fn test_entropy_validation() {
        let mut dom = PhysicsDom::new();
        
        // Entropy increase should be valid
        assert!(dom.validate_entropy(1.0, 2.0, 1000));
        
        // Entropy decrease should be invalid
        assert!(!dom.validate_entropy(2.0, 1.0, 2000));
        assert_eq!(dom.constraint_violations.len(), 1);
    }

    #[test]
    fn test_conservation_validation() {
        let mut dom = PhysicsDom::new();
        
        // Within tolerance
        assert!(dom.validate_conservation(100.0, 100.01, 1000, 0.1));
        
        // Exceeds tolerance
        assert!(!dom.validate_conservation(100.0, 105.0, 2000, 0.1));
    }

    #[test]
    fn test_uncertainty_principle() {
        let mut dom = PhysicsDom::new();
        
        // Large uncertainties - should pass
        assert!(dom.validate_uncertainty(1e-10, 1e-24, 1000));
        
        // Too precise - should fail
        assert!(!dom.validate_uncertainty(1e-50, 1e-50, 2000));
    }

    #[test]
    fn test_lorentz_transform() {
        let dom = PhysicsDom::new();
        let position = (1.0, 100.0, 0.0, 0.0);
        let velocity = 0.5 * 299792458.0; // 0.5c
        
        let transformed = dom.lorentz_transform(position, velocity);
        // Should get different t' and x' coordinates
        assert_ne!(transformed.0, position.0);
        assert_ne!(transformed.1, position.1);
        // y and z should be unchanged
        assert_eq!(transformed.2, position.2);
        assert_eq!(transformed.3, position.3);
    }

    #[test]
    fn test_entropy_increase_calculation() {
        let dom = PhysicsDom::new();
        let entropy = dom.calculate_entropy_increase(10, 2.5);
        assert!(entropy > 0.0);
    }

    #[test]
    fn test_law_enable_disable() {
        let mut dom = PhysicsDom::new();
        dom.set_law_enabled(LawType::Entropy, false);
        
        // Should pass even with decreasing entropy when disabled
        assert!(dom.validate_entropy(2.0, 1.0, 1000));
        assert_eq!(dom.constraint_violations.len(), 0);
    }
}
