// UDAP (Universal Data Access Protocol) Handler for Avian Bioacoustics
// Parses URIs like: skhaos://avian/crow/caw/rank?hz=1000&law=entropy

use std::collections::HashMap;

/// UDAP URI handler for avian and hybrid bio-acoustic patterns
pub struct UdapAvianHandler {
    schemes: HashMap<String, SchemeHandler>,
}

#[derive(Debug, Clone)]
pub enum SchemeHandler {
    Avian,
    Bio,
    Hybrid,
}

#[derive(Debug, Clone)]
pub struct UdapUri {
    pub scheme: String,
    pub domain: String,
    pub species: String,
    pub pattern_type: String,
    pub rank: Option<usize>,
    pub params: HashMap<String, String>,
}

impl UdapUri {
    /// Parse UDAP URI string
    /// Examples:
    /// - skhaos://avian/crow/caw/1?law=entropy&hz=1000
    /// - skhaos://bio/hybrid/dolphin_crow?hz=50000
    /// - skhaos://bio/hybrid/orca_crow?law=conservation&hz=13000
    pub fn parse(uri: &str) -> Result<Self, String> {
        // Split scheme from rest
        let parts: Vec<&str> = uri.split("://").collect();
        if parts.len() != 2 {
            return Err(format!("Invalid URI format: {}", uri));
        }
        
        let scheme = parts[0].to_string();
        let rest = parts[1];
        
        // Split path from query params
        let path_and_query: Vec<&str> = rest.split('?').collect();
        let path = path_and_query[0];
        let query = if path_and_query.len() > 1 {
            path_and_query[1]
        } else {
            ""
        };
        
        // Parse path components
        let path_parts: Vec<&str> = path.split('/').collect();
        if path_parts.len() < 3 {
            return Err(format!("Invalid path format: {}", path));
        }
        
        let domain = path_parts[0].to_string();
        let species = path_parts[1].to_string();
        let pattern_type = path_parts[2].to_string();
        let rank = if path_parts.len() > 3 {
            path_parts[3].parse().ok()
        } else {
            None
        };
        
        // Parse query parameters
        let params = Self::parse_query_params(query);
        
        Ok(UdapUri {
            scheme,
            domain,
            species,
            pattern_type,
            rank,
            params,
        })
    }
    
    fn parse_query_params(query: &str) -> HashMap<String, String> {
        let mut params = HashMap::new();
        
        if query.is_empty() {
            return params;
        }
        
        for pair in query.split('&') {
            let kv: Vec<&str> = pair.split('=').collect();
            if kv.len() == 2 {
                params.insert(kv[0].to_string(), kv[1].to_string());
            }
        }
        
        params
    }
    
    /// Get frequency parameter (Hz)
    pub fn frequency(&self) -> Option<f64> {
        self.params.get("hz").and_then(|s| s.parse().ok())
    }
    
    /// Get physics law parameter
    pub fn physics_law(&self) -> Option<String> {
        self.params.get("law").cloned()
    }
    
    /// Get Zipf slope parameter
    pub fn zipf_slope(&self) -> Option<f64> {
        self.params.get("zipf_slope").and_then(|s| s.parse().ok())
    }
    
    /// Get Menzerath parameter
    pub fn menzerath(&self) -> Option<bool> {
        self.params.get("menzerath").and_then(|s| s.parse().ok())
    }
    
    /// Check if this is a hybrid pattern
    pub fn is_hybrid(&self) -> bool {
        self.domain == "bio" && self.species == "hybrid" || self.pattern_type.contains("_")
    }
    
    /// Get constituent species for hybrid patterns
    pub fn hybrid_species(&self) -> Option<(String, String)> {
        if !self.is_hybrid() {
            return None;
        }
        
        let parts: Vec<&str> = self.pattern_type.split('_').collect();
        if parts.len() == 2 {
            Some((parts[0].to_string(), parts[1].to_string()))
        } else {
            None
        }
    }
}

impl UdapAvianHandler {
    pub fn new() -> Self {
        let mut schemes = HashMap::new();
        schemes.insert("avian".to_string(), SchemeHandler::Avian);
        schemes.insert("bio".to_string(), SchemeHandler::Bio);
        schemes.insert("hybrid".to_string(), SchemeHandler::Hybrid);
        
        Self { schemes }
    }
    
    /// Handle UDAP URI and return appropriate action
    pub fn handle(&self, uri: &str) -> Result<UdapAction, String> {
        let parsed = UdapUri::parse(uri)?;
        
        match parsed.domain.as_str() {
            "avian" => self.handle_avian(&parsed),
            "bio" => self.handle_bio(&parsed),
            _ => Err(format!("Unknown domain: {}", parsed.domain)),
        }
    }
    
    fn handle_avian(&self, uri: &UdapUri) -> Result<UdapAction, String> {
        match uri.species.as_str() {
            "crow" => Ok(UdapAction::SimulateCrow {
                pattern_type: uri.pattern_type.clone(),
                frequency: uri.frequency(),
                rank: uri.rank,
            }),
            _ => Err(format!("Unknown avian species: {}", uri.species)),
        }
    }
    
    fn handle_bio(&self, uri: &UdapUri) -> Result<UdapAction, String> {
        if uri.species == "hybrid" {
            if let Some((species1, species2)) = uri.hybrid_species() {
                Ok(UdapAction::EvolveHybrid {
                    species1,
                    species2,
                    frequency: uri.frequency(),
                    physics_law: uri.physics_law(),
                })
            } else {
                Err("Invalid hybrid pattern format".to_string())
            }
        } else {
            Ok(UdapAction::SimulateBio {
                species: uri.species.clone(),
                pattern_type: uri.pattern_type.clone(),
                frequency: uri.frequency(),
            })
        }
    }
}

#[derive(Debug, Clone)]
pub enum UdapAction {
    SimulateCrow {
        pattern_type: String,
        frequency: Option<f64>,
        rank: Option<usize>,
    },
    SimulateBio {
        species: String,
        pattern_type: String,
        frequency: Option<f64>,
    },
    EvolveHybrid {
        species1: String,
        species2: String,
        frequency: Option<f64>,
        physics_law: Option<String>,
    },
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_avian_uri() {
        let uri = UdapUri::parse("skhaos://avian/crow/caw/1?law=entropy&hz=1000").unwrap();
        
        assert_eq!(uri.scheme, "skhaos");
        assert_eq!(uri.domain, "avian");
        assert_eq!(uri.species, "crow");
        assert_eq!(uri.pattern_type, "caw");
        assert_eq!(uri.rank, Some(1));
        assert_eq!(uri.frequency(), Some(1000.0));
        assert_eq!(uri.physics_law(), Some("entropy".to_string()));
    }
    
    #[test]
    fn test_parse_hybrid_uri() {
        let uri = UdapUri::parse("skhaos://bio/hybrid/dolphin_crow?hz=50000").unwrap();
        
        assert_eq!(uri.domain, "bio");
        assert_eq!(uri.species, "hybrid");
        assert_eq!(uri.pattern_type, "dolphin_crow");
        assert_eq!(uri.frequency(), Some(50000.0));
        assert!(uri.is_hybrid());
        
        let (s1, s2) = uri.hybrid_species().unwrap();
        assert_eq!(s1, "dolphin");
        assert_eq!(s2, "crow");
    }
    
    #[test]
    fn test_parse_orca_crow_hybrid() {
        let uri = UdapUri::parse("skhaos://bio/hybrid/orca_crow?law=conservation&hz=13000").unwrap();
        
        assert!(uri.is_hybrid());
        assert_eq!(uri.frequency(), Some(13000.0));
        assert_eq!(uri.physics_law(), Some("conservation".to_string()));
        
        let (s1, s2) = uri.hybrid_species().unwrap();
        assert_eq!(s1, "orca");
        assert_eq!(s2, "crow");
    }
    
    #[test]
    fn test_udap_handler() {
        let handler = UdapAvianHandler::new();
        
        // Test crow simulation
        let action = handler.handle("skhaos://avian/crow/caw/1?hz=1000").unwrap();
        match action {
            UdapAction::SimulateCrow { pattern_type, frequency, rank } => {
                assert_eq!(pattern_type, "caw");
                assert_eq!(frequency, Some(1000.0));
                assert_eq!(rank, Some(1));
            }
            _ => panic!("Wrong action type"),
        }
        
        // Test hybrid evolution
        let action = handler.handle("skhaos://bio/hybrid/dolphin_crow?hz=50000").unwrap();
        match action {
            UdapAction::EvolveHybrid { species1, species2, frequency, .. } => {
                assert_eq!(species1, "dolphin");
                assert_eq!(species2, "crow");
                assert_eq!(frequency, Some(50000.0));
            }
            _ => panic!("Wrong action type"),
        }
    }
}
