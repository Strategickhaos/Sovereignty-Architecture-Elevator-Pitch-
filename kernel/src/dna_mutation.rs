use serde::{Deserialize, Serialize};
use regex::Regex;

/// DNA specification structure matching sagco_unified_spec.yaml
#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct DnaSpec {
    pub dna_strand: String,
    pub metadata: Option<DnaMetadata>,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct DnaMetadata {
    pub version: String,
    pub created: String,
}

/// Parse a DNA strand into its components
///
/// Format: [Compiler]-[CMD]-[MESH]-[ORB]
/// Example: FLM2-CMD4-MESH5-ORB1
#[derive(Debug, Clone, PartialEq)]
pub struct DnaComponents {
    pub compiler: String,
    pub compiler_version: Option<String>,
    pub cmd_count: u32,
    pub mesh_count: u32,
    pub orb_level: u32,
}

impl DnaComponents {
    /// Parse a DNA strand string into components
    pub fn parse(strand: &str) -> anyhow::Result<Self> {
        let re = Regex::new(r"^([A-Z]+)(\d+(?:\.\d+)?)-CMD(\d+)-MESH(\d+)-ORB(\d+)$")?;
        
        if let Some(caps) = re.captures(strand) {
            let compiler_base = caps.get(1).unwrap().as_str().to_string();
            let compiler_ver = caps.get(2).unwrap().as_str().to_string();
            let cmd_count = caps.get(3).unwrap().as_str().parse()?;
            let mesh_count = caps.get(4).unwrap().as_str().parse()?;
            let orb_level = caps.get(5).unwrap().as_str().parse()?;

            Ok(Self {
                compiler: format!("{}{}", compiler_base, compiler_ver),
                compiler_version: Some(compiler_ver),
                cmd_count,
                mesh_count,
                orb_level,
            })
        } else {
            anyhow::bail!("Invalid DNA strand format: {}", strand)
        }
    }

    /// Convert components back to DNA strand string
    pub fn to_strand(&self) -> String {
        format!(
            "{}-CMD{}-MESH{}-ORB{}",
            self.compiler, self.cmd_count, self.mesh_count, self.orb_level
        )
    }
}

/// Suggest a mutation to the FLM compiler version based on success metrics
///
/// # Arguments
/// * `current_strand` - Current DNA strand (e.g., "FLM2-CMD4-MESH5-ORB1")
/// * `p_success` - Probability of success from Guardian metrics (0.0 to 1.0)
/// * `entropy` - Entropy measure from Guardian (lower is better)
///
/// # Returns
/// * `Some(String)` - New DNA strand if mutation is suggested
/// * `None` - No mutation suggested
///
/// # Example
/// ```
/// use sagco_kernel::dna_mutation::suggest_flm_mutation;
///
/// let new_strand = suggest_flm_mutation("FLM2-CMD4-MESH5-ORB1", 0.96, 0.25);
/// assert_eq!(new_strand, Some("FLM2.1-CMD4-MESH5-ORB1".to_string()));
/// ```
pub fn suggest_flm_mutation(
    current_strand: &str,
    p_success: f64,
    entropy: f64,
) -> Option<String> {
    // Mutation threshold: p_success >= 0.95 and entropy < 0.3
    if p_success < 0.95 || entropy >= 0.3 {
        return None;
    }

    let components = DnaComponents::parse(current_strand).ok()?;
    
    // Check if compiler is FLM2 (without decimal version)
    if components.compiler == "FLM2" {
        let mut new_components = components;
        new_components.compiler = "FLM2.1".to_string();
        new_components.compiler_version = Some("2.1".to_string());
        return Some(new_components.to_strand());
    }
    
    // If already on a decimal version (e.g., FLM2.1), increment minor version
    if let Ok(re) = Regex::new(r"^FLM(\d+)\.(\d+)$") {
        if let Some(caps) = re.captures(&components.compiler) {
            let major: u32 = caps.get(1).unwrap().as_str().parse().ok()?;
            let minor: u32 = caps.get(2).unwrap().as_str().parse().ok()?;
            let new_minor = minor + 1;
            
            let mut new_components = components;
            new_components.compiler = format!("FLM{}.{}", major, new_minor);
            new_components.compiler_version = Some(format!("{}.{}", major, new_minor));
            return Some(new_components.to_strand());
        }
    }
    
    None
}

/// Suggest mesh expansion mutation
pub fn suggest_mesh_mutation(current_strand: &str, new_node_verified: bool) -> Option<String> {
    if !new_node_verified {
        return None;
    }

    let components = DnaComponents::parse(current_strand).ok()?;
    let mut new_components = components;
    new_components.mesh_count += 1;
    Some(new_components.to_strand())
}

/// Suggest orbit elevation mutation
pub fn suggest_orbit_mutation(
    current_strand: &str,
    security_score: f64,
    baseline: f64,
) -> Option<String> {
    // Elevate orbit if security_score > baseline + 2 standard deviations
    // Assuming std dev is ~0.1 for this example
    if security_score <= baseline + 0.2 {
        return None;
    }

    let components = DnaComponents::parse(current_strand).ok()?;
    let mut new_components = components;
    new_components.orb_level += 1;
    Some(new_components.to_strand())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_dna_components() {
        let strand = "FLM2-CMD4-MESH5-ORB1";
        let components = DnaComponents::parse(strand).unwrap();
        
        assert_eq!(components.compiler, "FLM2");
        assert_eq!(components.cmd_count, 4);
        assert_eq!(components.mesh_count, 5);
        assert_eq!(components.orb_level, 1);
    }

    #[test]
    fn test_suggest_flm_mutation() {
        // Should suggest mutation when p_success >= 0.95 and entropy < 0.3
        let result = suggest_flm_mutation("FLM2-CMD4-MESH5-ORB1", 0.96, 0.25);
        assert_eq!(result, Some("FLM2.1-CMD4-MESH5-ORB1".to_string()));

        // Should not suggest when p_success is too low
        let result = suggest_flm_mutation("FLM2-CMD4-MESH5-ORB1", 0.90, 0.25);
        assert_eq!(result, None);

        // Should not suggest when entropy is too high
        let result = suggest_flm_mutation("FLM2-CMD4-MESH5-ORB1", 0.96, 0.35);
        assert_eq!(result, None);
    }

    #[test]
    fn test_suggest_flm_mutation_incremental() {
        // Test incrementing from FLM2.1 to FLM2.2
        let result = suggest_flm_mutation("FLM2.1-CMD4-MESH5-ORB1", 0.96, 0.25);
        assert_eq!(result, Some("FLM2.2-CMD4-MESH5-ORB1".to_string()));
    }

    #[test]
    fn test_suggest_mesh_mutation() {
        let result = suggest_mesh_mutation("FLM2-CMD4-MESH5-ORB1", true);
        assert_eq!(result, Some("FLM2-CMD4-MESH6-ORB1".to_string()));

        let result = suggest_mesh_mutation("FLM2-CMD4-MESH5-ORB1", false);
        assert_eq!(result, None);
    }

    #[test]
    fn test_suggest_orbit_mutation() {
        let result = suggest_orbit_mutation("FLM2-CMD4-MESH5-ORB1", 0.9, 0.7);
        assert_eq!(result, Some("FLM2-CMD4-MESH5-ORB2".to_string()));

        let result = suggest_orbit_mutation("FLM2-CMD4-MESH5-ORB1", 0.8, 0.7);
        assert_eq!(result, None);
    }
}
