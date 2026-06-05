// UDAP Bio-Physics Integration
// Handles URIs like: skhaos://bio/hybrid/crow_orca?law=zipf

pub struct UdapBioHandler;

impl UdapBioHandler {
    pub fn new() -> Self {
        Self
    }
    
    /// Parse bio-physics UDAP URI
    pub fn parse(uri: &str) -> Result<BioAction, String> {
        // Reuse the avian UDAP parser
        let parsed = crate::avian_bio::udap_avian::UdapUri::parse(uri)?;
        
        if parsed.domain != "bio" {
            return Err(format!("Expected 'bio' domain, got '{}'", parsed.domain));
        }
        
        Ok(BioAction {
            species: parsed.species.clone(),
            pattern_type: parsed.pattern_type.clone(),
            frequency: parsed.frequency(),
            physics_law: parsed.physics_law(),
        })
    }
}

#[derive(Debug, Clone)]
pub struct BioAction {
    pub species: String,
    pub pattern_type: String,
    pub frequency: Option<f64>,
    pub physics_law: Option<String>,
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_bio_uri_parsing() {
        let action = UdapBioHandler::parse("skhaos://bio/hybrid/crow_orca?law=conservation&hz=13000").unwrap();
        
        assert_eq!(action.species, "hybrid");
        assert_eq!(action.pattern_type, "crow_orca");
        assert_eq!(action.frequency, Some(13000.0));
        assert_eq!(action.physics_law, Some("conservation".to_string()));
    }
}
