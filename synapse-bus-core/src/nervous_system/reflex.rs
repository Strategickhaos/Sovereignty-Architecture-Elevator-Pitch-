// Reflex - Autonomic Response (Local Policy)
// Automatic reactions to specific spike patterns

use crate::nervous_system::spike::{Spike, OrganType};
use tracing::{info, warn};

/// Reflex action result
#[derive(Debug, Clone, PartialEq)]
pub enum ReflexAction {
    Allow,
    Block,
    Escalate,
    Quarantine,
}

/// Reflex - Autonomic response system
pub struct Reflex {
    enabled: bool,
}

impl Reflex {
    /// Create a new reflex system
    pub fn new() -> Self {
        Self { enabled: true }
    }

    /// Evaluate a spike and determine reflexive action
    pub fn evaluate(&self, spike: &Spike) -> ReflexAction {
        if !self.enabled {
            return ReflexAction::Allow;
        }

        // High-risk spikes get quarantined
        if spike.is_high_risk() {
            warn!(
                "High-risk spike detected from {:?} (risk: {:.2})",
                spike.origin, spike.risk_score
            );
            return ReflexAction::Quarantine;
        }

        // System entropy check
        if spike.vector.heat > 0.8 {
            warn!("System overheating (heat: {:.2})", spike.vector.heat);
            return ReflexAction::Block;
        }

        // Negative gravity indicates repulsive/malicious target
        if spike.vector.gravity < -5.0 {
            warn!("Repulsive target detected (gravity: {:.2})", spike.vector.gravity);
            return ReflexAction::Block;
        }

        // Escalate certain organ types for review
        match spike.origin {
            OrganType::Osteon | OrganType::SynapseFire | OrganType::Erosion => {
                info!("Escalating exploit attempt for review");
                ReflexAction::Escalate
            }
            _ => ReflexAction::Allow,
        }
    }

    /// Enable reflexes
    pub fn enable(&mut self) {
        self.enabled = true;
    }

    /// Disable reflexes (dangerous!)
    pub fn disable(&mut self) {
        warn!("⚠️  Reflexes disabled - system vulnerable!");
        self.enabled = false;
    }

    /// Check if reflexes are enabled
    pub fn is_enabled(&self) -> bool {
        self.enabled
    }
}

impl Default for Reflex {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::homeostasis::gradient::PhysicsVector;

    #[test]
    fn test_reflex_high_risk() {
        let reflex = Reflex::new();
        let vector = PhysicsVector::new(0.5, 0.5);
        let spike = Spike::with_risk(OrganType::Retina, vector, vec![], 0.85);

        assert_eq!(reflex.evaluate(&spike), ReflexAction::Quarantine);
    }

    #[test]
    fn test_reflex_overheating() {
        let reflex = Reflex::new();
        let vector = PhysicsVector::new(0.9, 0.0);
        let spike = Spike::new(OrganType::System, vector, vec![]);

        assert_eq!(reflex.evaluate(&spike), ReflexAction::Block);
    }

    #[test]
    fn test_reflex_repulsive_target() {
        let reflex = Reflex::new();
        let vector = PhysicsVector::new(0.3, -10.0);
        let spike = Spike::new(OrganType::Retina, vector, vec![]);

        assert_eq!(reflex.evaluate(&spike), ReflexAction::Block);
    }

    #[test]
    fn test_reflex_exploit_escalation() {
        let reflex = Reflex::new();
        let vector = PhysicsVector::new(0.3, 0.5);
        let spike = Spike::new(OrganType::Osteon, vector, vec![]);

        assert_eq!(reflex.evaluate(&spike), ReflexAction::Escalate);
    }

    #[test]
    fn test_reflex_disabled() {
        let mut reflex = Reflex::new();
        reflex.disable();

        let vector = PhysicsVector::new(0.9, -10.0);
        let spike = Spike::with_risk(OrganType::System, vector, vec![], 0.99);

        assert_eq!(reflex.evaluate(&spike), ReflexAction::Allow);
    }
}
