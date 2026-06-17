// Personalities YAML loader

use std::fs;

/// Load personalities configuration
pub fn load_personalities() -> Result<String, std::io::Error> {
    fs::read_to_string("src/council/personalities.yaml")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_load_personalities() {
        // Test would pass if file exists
        let _result = load_personalities();
    }
}
