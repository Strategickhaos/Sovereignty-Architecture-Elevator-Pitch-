//! sagco_tables.rs - Trigonometric Lookup Tables
//! 
//! O(1) sine/cosine lookups for performance-critical operations
//! Used in timing jitter simulation and geometry mapping

use std::f64::consts::PI;

const TABLE_SIZE: usize = 360;

lazy_static::lazy_static! {
    static ref SIN_TABLE: Vec<f64> = {
        (0..TABLE_SIZE)
            .map(|i| (i as f64 * PI / 180.0).sin())
            .collect()
    };
    
    static ref COS_TABLE: Vec<f64> = {
        (0..TABLE_SIZE)
            .map(|i| (i as f64 * PI / 180.0).cos())
            .collect()
    };
}

/// O(1) sine lookup from precomputed table
pub fn sin_lookup(x: f64) -> f64 {
    let degrees = (x * 180.0 / PI) % 360.0;
    let index = degrees.abs() as usize % TABLE_SIZE;
    SIN_TABLE[index]
}

/// O(1) cosine lookup from precomputed table
pub fn cos_lookup(x: f64) -> f64 {
    let degrees = (x * 180.0 / PI) % 360.0;
    let index = degrees.abs() as usize % TABLE_SIZE;
    COS_TABLE[index]
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sin_lookup() {
        let result = sin_lookup(0.0);
        assert!((result - 0.0).abs() < 0.01);
        
        let result = sin_lookup(PI / 2.0);
        assert!((result - 1.0).abs() < 0.01);
    }
    
    #[test]
    fn test_cos_lookup() {
        let result = cos_lookup(0.0);
        assert!((result - 1.0).abs() < 0.01);
        
        let result = cos_lookup(PI);
        assert!((result + 1.0).abs() < 0.01);
    }
}
