// [Q10] Na+/K+ Pump: Ejects malformed packets
// FlameLang Clamp Glyph
//
// This is a FlameLang specification for the clamp/ejection system
// In a full implementation, this would be parsed by the FlameLang compiler

// Clamp Glyph - Sodium-Potassium Pump (Packet Ejector)
//
// glyph #clamp {
//     // Configuration
//     config: {
//         max_malformed: 10,   // Max malformed packets before clamping
//         ejection_force: 1.0, // How aggressively to eject
//     },
//
//     // State
//     state: {
//         malformed_count: 0,
//         ejected_count: 0,
//         na_level: 0.5,  // Sodium (external)
//         k_level: 0.5,   // Potassium (internal)
//     },
//
//     // Validation gate
//     validate: |packet| {
//         // Check packet structure
//         if packet.len() == 0 { return false; }
//         if packet.len() > 65535 { return false; }
//         
//         // Check for malformed data
//         let null_bytes = packet.iter().filter(|b| **b == 0).count();
//         if null_bytes > packet.len() / 2 { return false; }
//         
//         return true;
//     },
//
//     // Pump action - maintain gradient
//     pump: |packet| {
//         if !validate(packet) {
//             state.malformed_count += 1;
//             
//             // Eject the packet
//             eject(packet);
//             
//             // Adjust ion concentrations
//             state.na_level += 0.1;  // More sodium outside
//             state.k_level -= 0.05;   // Less potassium inside
//             
//             return PumpResult::Ejected;
//         }
//         
//         // Valid packet - allow through
//         state.na_level -= 0.01;
//         state.k_level += 0.01;
//         
//         return PumpResult::Accepted;
//     },
//
//     // Clamp if too many malformed
//     clamp: || {
//         if state.malformed_count > config.max_malformed {
//             system.quarantine();
//             return ClampResult::Engaged;
//         }
//         return ClampResult::Normal;
//     }
// }

/// Rust placeholder for FlameLang clamp system
pub struct Clamp {
    max_malformed: usize,
    malformed_count: usize,
    ejected_count: usize,
}

impl Clamp {
    pub fn new(max_malformed: usize) -> Self {
        Self {
            max_malformed,
            malformed_count: 0,
            ejected_count: 0,
        }
    }

    pub fn validate(&self, packet: &[u8]) -> bool {
        if packet.is_empty() || packet.len() > 65535 {
            return false;
        }

        // Check for excessive null bytes (malformed data indicator)
        let null_count = packet.iter().filter(|&&b| b == 0).count();
        null_count <= packet.len() / 2
    }

    pub fn pump(&mut self, packet: &[u8]) -> bool {
        if !self.validate(packet) {
            self.malformed_count += 1;
            self.ejected_count += 1;
            false
        } else {
            true
        }
    }

    pub fn should_clamp(&self) -> bool {
        self.malformed_count > self.max_malformed
    }

    pub fn reset(&mut self) {
        self.malformed_count = 0;
    }

    pub fn stats(&self) -> (usize, usize) {
        (self.malformed_count, self.ejected_count)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_clamp_creation() {
        let clamp = Clamp::new(10);
        assert!(!clamp.should_clamp());
    }

    #[test]
    fn test_valid_packet() {
        let mut clamp = Clamp::new(10);
        let packet = vec![1, 2, 3, 4, 5];
        assert!(clamp.pump(&packet));
    }

    #[test]
    fn test_empty_packet() {
        let mut clamp = Clamp::new(10);
        let packet = vec![];
        assert!(!clamp.pump(&packet));
    }

    #[test]
    fn test_oversized_packet() {
        let mut clamp = Clamp::new(10);
        let packet = vec![0u8; 70000];
        assert!(!clamp.pump(&packet));
    }

    #[test]
    fn test_malformed_packet() {
        let mut clamp = Clamp::new(10);
        let packet = vec![0u8; 100]; // All nulls
        assert!(!clamp.pump(&packet));
        assert_eq!(clamp.stats().0, 1);
    }

    #[test]
    fn test_clamp_threshold() {
        let mut clamp = Clamp::new(3);
        
        for _ in 0..5 {
            clamp.pump(&vec![]);
        }
        
        assert!(clamp.should_clamp());
    }

    #[test]
    fn test_clamp_reset() {
        let mut clamp = Clamp::new(3);
        
        for _ in 0..5 {
            clamp.pump(&vec![]);
        }
        
        assert!(clamp.should_clamp());
        
        clamp.reset();
        assert!(!clamp.should_clamp());
    }
}
