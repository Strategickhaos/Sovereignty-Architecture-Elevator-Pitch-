/// Simulated annealing stub for spot instance bidding decisions (SAFE).
pub fn anneal_bid(current: f32, temperature: f32) -> f32 {
    if temperature > 0.5 { current * 0.95 } else { current * 0.99 }
}
