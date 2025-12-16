// Autopilot YAML loader

use std::fs;

/// Load autopilot configuration
pub fn load_autopilot_config() -> Result<String, std::io::Error> {
    fs::read_to_string("src/infra/autopilot.yaml")
}
