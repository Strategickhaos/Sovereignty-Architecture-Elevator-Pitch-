//! sagco_guardian.rs - Geometric Guardian for Safety Mapping
//! 
//! Maps uncertainty measures to geometric points on the SAGCO manifold
//! Quadrants: Q1 (Linguistic), Q2 (Numeric), Q3 (Wave), Q4 (DNA)
//! Elements: 60-minute DNA clock with 4 base pairs per quadrant

use crate::probability::Uncertainty;

/// Geometric point on SAGCO manifold
#[derive(Debug, Clone)]
pub struct GeometricPoint {
    pub quadrant: Quadrant,
    pub minute: u8,  // 0-59 in DNA clock
    pub element: Element,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Quadrant {
    Q1Linguistic = 1,  // Container/Error (minutes 0-14)
    Q2Numeric = 2,     // Timeout/Latency (minutes 15-29)
    Q3Wave = 3,        // Runtime/Proof (minutes 30-44)
    Q4DNA = 4,         // System/Race (minutes 45-59)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Element {
    Container,
    Numeric,
    Wave,
    DNA,
}

/// Safety classification result
#[derive(Debug, Clone)]
pub struct SafetyClassification {
    pub should_reject: bool,
    pub reason: String,
    pub confidence: f64,
}

/// Guardian maps uncertainty to geometry and classifies safety
pub struct Guardian {
    kl_reject_threshold: f64,
    entropy_max: f64,
}

impl Guardian {
    pub fn new() -> Self {
        Self {
            kl_reject_threshold: 0.5,
            entropy_max: 10.0,
        }
    }
    
    /// Map uncertainty to geometric point on manifold
    pub fn map_uncertainty_to_geometry(&self, unc: Uncertainty, element_id: u8) -> GeometricPoint {
        // Map entropy to minute (0-59)
        let minute = (unc.entropy.min(self.entropy_max) / self.entropy_max * 60.0) as u8 % 60;
        
        // Determine quadrant from minute
        let quadrant = match minute {
            0..=14 => Quadrant::Q1Linguistic,
            15..=29 => Quadrant::Q2Numeric,
            30..=44 => Quadrant::Q3Wave,
            45..=59 => Quadrant::Q4DNA,
            _ => Quadrant::Q1Linguistic,
        };
        
        // Map element_id to element type
        let element = match element_id % 4 {
            0 => Element::Container,
            1 => Element::Numeric,
            2 => Element::Wave,
            3 => Element::DNA,
            _ => Element::Container,
        };
        
        GeometricPoint { quadrant, minute, element }
    }
    
    /// Classify safety based on geometric point
    pub fn classify_safety(&self, point: &GeometricPoint) -> SafetyClassification {
        // Rejection rules based on quadrant
        match point.quadrant {
            Quadrant::Q1Linguistic if point.minute == 0 && point.element == Element::Container => {
                SafetyClassification {
                    should_reject: true,
                    reason: "Container error at minute 0 with Container element".to_string(),
                    confidence: 0.95,
                }
            }
            Quadrant::Q2Numeric if point.minute == 15 && point.element == Element::Numeric => {
                SafetyClassification {
                    should_reject: true,
                    reason: "Timeout gate at minute 15 with Numeric element".to_string(),
                    confidence: 0.90,
                }
            }
            Quadrant::Q3Wave if point.minute >= 30 && point.minute <= 35 => {
                SafetyClassification {
                    should_reject: false,
                    reason: "Runtime proof acceptable".to_string(),
                    confidence: 0.85,
                }
            }
            Quadrant::Q4DNA if point.minute >= 45 && point.minute <= 50 && point.element == Element::DNA => {
                SafetyClassification {
                    should_reject: true,
                    reason: "System race gate at minute 45-50 with DNA element".to_string(),
                    confidence: 0.88,
                }
            }
            _ => {
                SafetyClassification {
                    should_reject: false,
                    reason: "Safe zone".to_string(),
                    confidence: 0.75,
                }
            }
        }
    }
}

impl Default for Guardian {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_map_to_geometry() {
        let guardian = Guardian::new();
        let unc = Uncertainty::new(0.9, 2.0, 0.1);
        let point = guardian.map_uncertainty_to_geometry(unc, 33);
        
        assert!(point.minute < 60);
        println!("Mapped to quadrant {:?}, minute {}", point.quadrant, point.minute);
    }
    
    #[test]
    fn test_safety_classification() {
        let guardian = Guardian::new();
        
        // Test Q1 container error - must have both minute 0 AND Container element
        let point = GeometricPoint {
            quadrant: Quadrant::Q1Linguistic,
            minute: 0,
            element: Element::Container,
        };
        let safety = guardian.classify_safety(&point);
        assert!(safety.should_reject);
        
        // Test Q1 minute 0 but different element - should NOT reject
        let point_safe_elem = GeometricPoint {
            quadrant: Quadrant::Q1Linguistic,
            minute: 0,
            element: Element::Wave,
        };
        let safety_safe_elem = guardian.classify_safety(&point_safe_elem);
        assert!(!safety_safe_elem.should_reject);
        
        // Test safe zone
        let point_safe = GeometricPoint {
            quadrant: Quadrant::Q3Wave,
            minute: 32,
            element: Element::Wave,
        };
        let safety_safe = guardian.classify_safety(&point_safe);
        assert!(!safety_safe.should_reject);
    }
}
