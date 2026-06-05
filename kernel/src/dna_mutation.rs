// DNA Mutation Module
// Evolves the DNA strand based on benchmark performance

use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct DnaSpec {
    pub version: String,
    pub dna_strand: String,
}

/// Suggest FLM mutation based on performance
/// Returns new DNA strand if mutation is recommended
pub fn suggest_flm_mutation(
    current: &str,
    p_success: f64,
    threshold: f64,
) -> Option<String> {
    if p_success >= threshold {
        // Check if current strand contains FLM2
        if current.contains("FLM2") && !current.contains("FLM2.1") {
            let new = current.replace("FLM2", "FLM2.1");
            return Some(new);
        }
    }
    None
}

/// Suggest CMD mutation based on command count
pub fn suggest_cmd_mutation(
    current: &str,
    command_count: u32,
    threshold: u32,
) -> Option<String> {
    if command_count >= threshold {
        if current.contains("CMD1") && !current.contains("CMD2") {
            let new = current.replace("CMD1", "CMD2");
            return Some(new);
        }
    }
    None
}

/// Suggest MESH mutation based on node count
pub fn suggest_mesh_mutation(
    current: &str,
    node_count: u32,
    current_mesh: u32,
) -> Option<String> {
    if node_count > current_mesh {
        let old_pattern = format!("MESH{}", current_mesh);
        let new_pattern = format!("MESH{}", node_count);
        if current.contains(&old_pattern) {
            let new = current.replace(&old_pattern, &new_pattern);
            return Some(new);
        }
    }
    None
}

/// Suggest ORB mutation based on oracle performance
pub fn suggest_orb_mutation(
    current: &str,
    safety_score: f64,
    threshold: f64,
) -> Option<String> {
    if safety_score >= threshold {
        if current.contains("ORB1") && !current.contains("ORB2") {
            let new = current.replace("ORB1", "ORB2");
            return Some(new);
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_flm_mutation() {
        let current = "FLM2-CMD1-MESH5-ORB1";
        let result = suggest_flm_mutation(current, 0.96, 0.95);
        assert_eq!(result, Some("FLM2.1-CMD1-MESH5-ORB1".to_string()));
    }

    #[test]
    fn test_cmd_mutation() {
        let current = "FLM2-CMD1-MESH5-ORB1";
        let result = suggest_cmd_mutation(current, 10, 10);
        assert_eq!(result, Some("FLM2-CMD2-MESH5-ORB1".to_string()));
    }

    #[test]
    fn test_mesh_mutation() {
        let current = "FLM2-CMD1-MESH5-ORB1";
        let result = suggest_mesh_mutation(current, 6, 5);
        assert_eq!(result, Some("FLM2-CMD1-MESH6-ORB1".to_string()));
    }

    #[test]
    fn test_orb_mutation() {
        let current = "FLM2-CMD1-MESH5-ORB1";
        let result = suggest_orb_mutation(current, 0.91, 0.90);
        assert_eq!(result, Some("FLM2-CMD1-MESH5-ORB2".to_string()));
    }

    #[test]
    fn test_no_mutation_below_threshold() {
        let current = "FLM2-CMD1-MESH5-ORB1";
        let result = suggest_flm_mutation(current, 0.94, 0.95);
        assert_eq!(result, None);
    }
}
