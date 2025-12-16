// [Q27] Simulated Annealing for Spot instances
// Spot Gambler - Optimizes cloud spot instance bidding

use rand::Rng;

/// Spot instance bid optimizer using simulated annealing
pub struct SpotGambler {
    temperature: f64,
    cooling_rate: f64,
}

impl SpotGambler {
    pub fn new() -> Self {
        Self {
            temperature: 1000.0,
            cooling_rate: 0.003,
        }
    }

    /// Calculate optimal bid using simulated annealing
    pub fn calculate_bid(&mut self, current_price: f64, max_price: f64) -> f64 {
        let mut rng = rand::thread_rng();
        let mut best_bid = current_price * 1.1; // Start 10% above current

        while self.temperature > 1.0 {
            // Generate neighbor solution
            let new_bid = best_bid + (rng.gen::<f64>() - 0.5) * 10.0;
            
            // Constrain to valid range
            let new_bid = new_bid.max(current_price).min(max_price);
            
            // Calculate acceptance probability
            let delta = (new_bid - best_bid).abs();
            let acceptance_prob = (-delta / self.temperature).exp();
            
            if rng.gen::<f64>() < acceptance_prob {
                best_bid = new_bid;
            }
            
            // Cool down
            self.temperature *= 1.0 - self.cooling_rate;
        }

        best_bid
    }

    /// Reset temperature for new optimization
    pub fn reset(&mut self) {
        self.temperature = 1000.0;
    }
}

impl Default for SpotGambler {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spot_gambler_bid() {
        let mut gambler = SpotGambler::new();
        let bid = gambler.calculate_bid(0.5, 1.0);
        
        assert!(bid >= 0.5);
        assert!(bid <= 1.0);
    }

    #[test]
    fn test_spot_gambler_reset() {
        let mut gambler = SpotGambler::new();
        gambler.calculate_bid(0.5, 1.0);
        
        assert!(gambler.temperature < 1000.0);
        
        gambler.reset();
        assert_eq!(gambler.temperature, 1000.0);
    }
}
