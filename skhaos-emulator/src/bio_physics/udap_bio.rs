// UDAP Bio-Physics URI Parser
// Format: skhaos://bio/{domain}/{resource}?params

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Bio-Physics URI representation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BioURI {
    pub scheme: String,
    pub domain: String,
    pub resource: String,
    pub params: HashMap<String, String>,
}

/// UDAP Bio-Physics URI Parser
pub struct UDAPBioParser;

impl UDAPBioParser {
    /// Parse UDAP bio-physics URI
    /// Format: skhaos://bio/{domain}/{resource}?param1=value1&param2=value2
    pub fn parse(uri: &str) -> Result<BioURI, String> {
        // Split scheme
        let parts: Vec<&str> = uri.split("://").collect();
        if parts.len() != 2 {
            return Err(format!("Invalid URI format: {}", uri));
        }
        
        let scheme = parts[0].to_string();
        if scheme != "skhaos" {
            return Err(format!("Invalid scheme: {}. Expected 'skhaos'", scheme));
        }

        // Split path and query
        let rest = parts[1];
        let path_query: Vec<&str> = rest.split('?').collect();
        let path = path_query[0];
        let query = if path_query.len() > 1 {
            path_query[1]
        } else {
            ""
        };

        // Parse path: bio/{domain}/{resource}
        let path_parts: Vec<&str> = path.split('/').collect();
        if path_parts.len() < 3 {
            return Err(format!("Invalid path format: {}. Expected bio/{domain}/{resource}", path));
        }

        if path_parts[0] != "bio" {
            return Err(format!("Invalid bio path: {}. Expected 'bio' as first segment", path_parts[0]));
        }

        let domain = path_parts[1].to_string();
        let resource = path_parts[2..].join("/");

        // Parse query parameters
        let params = Self::parse_query(query);

        Ok(BioURI {
            scheme,
            domain,
            resource,
            params,
        })
    }

    /// Parse query string into parameter map
    fn parse_query(query: &str) -> HashMap<String, String> {
        let mut params = HashMap::new();
        
        if query.is_empty() {
            return params;
        }

        for pair in query.split('&') {
            let kv: Vec<&str> = pair.split('=').collect();
            if kv.len() == 2 {
                params.insert(kv[0].to_string(), kv[1].to_string());
            } else if kv.len() == 1 {
                params.insert(kv[0].to_string(), "true".to_string());
            }
        }

        params
    }

    /// Build URI from components
    pub fn build(domain: &str, resource: &str, params: HashMap<String, String>) -> String {
        let mut uri = format!("skhaos://bio/{}/{}", domain, resource);
        
        if !params.is_empty() {
            let query: Vec<String> = params
                .iter()
                .map(|(k, v)| format!("{}={}", k, v))
                .collect();
            uri.push('?');
            uri.push_str(&query.join("&"));
        }

        uri
    }

    /// Validate bio-physics URI
    pub fn validate(uri: &str) -> Result<(), String> {
        Self::parse(uri)?;
        Ok(())
    }
}

impl BioURI {
    /// Get parameter value
    pub fn get_param(&self, key: &str) -> Option<&String> {
        self.params.get(key)
    }

    /// Get parameter as integer
    pub fn get_param_int(&self, key: &str) -> Option<i64> {
        self.params.get(key)?.parse().ok()
    }

    /// Get parameter as float
    pub fn get_param_float(&self, key: &str) -> Option<f64> {
        self.params.get(key)?.parse().ok()
    }

    /// Get parameter as boolean
    pub fn get_param_bool(&self, key: &str) -> bool {
        self.params.get(key)
            .map(|v| v == "true" || v == "1")
            .unwrap_or(false)
    }

    /// Check if this is a Zipf URI
    pub fn is_zipf(&self) -> bool {
        self.domain == "zipf"
    }

    /// Check if this is a dolphin URI
    pub fn is_dolphin(&self) -> bool {
        self.domain == "dolphin"
    }

    /// Check if this is a physics URI
    pub fn is_physics(&self) -> bool {
        self.domain == "physics"
    }

    /// Get Zipf rank if available
    pub fn zipf_rank(&self) -> Option<usize> {
        self.get_param_int("rank").map(|r| r as usize)
    }

    /// Get frequency in Hz
    pub fn frequency_hz(&self) -> Option<f64> {
        self.get_param_float("hz")
    }

    /// Get physics law
    pub fn physics_law(&self) -> Option<String> {
        self.params.get("law").cloned()
    }

    /// Get pod identifier
    pub fn pod_id(&self) -> Option<String> {
        self.params.get("pod").cloned()
    }

    /// Check if signature flag is set
    pub fn is_signature(&self) -> bool {
        self.get_param_bool("signature")
    }

    /// Get burst count
    pub fn burst_count(&self) -> Option<usize> {
        self.get_param_int("burst").map(|b| b as usize)
    }

    /// Convert to string
    pub fn to_string(&self) -> String {
        UDAPBioParser::build(&self.domain, &self.resource, self.params.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_zipf_uri() {
        let uri = "skhaos://bio/zipf/unit/1?law=entropy&hz=20";
        let parsed = UDAPBioParser::parse(uri).unwrap();
        
        assert_eq!(parsed.scheme, "skhaos");
        assert_eq!(parsed.domain, "zipf");
        assert_eq!(parsed.resource, "unit/1");
        assert_eq!(parsed.params.get("law").unwrap(), "entropy");
        assert_eq!(parsed.params.get("hz").unwrap(), "20");
    }

    #[test]
    fn test_parse_dolphin_uri() {
        let uri = "skhaos://bio/dolphin/whistle?signature=true&hz=10";
        let parsed = UDAPBioParser::parse(uri).unwrap();
        
        assert_eq!(parsed.domain, "dolphin");
        assert_eq!(parsed.resource, "whistle");
        assert!(parsed.is_signature());
        assert_eq!(parsed.frequency_hz().unwrap(), 10.0);
    }

    #[test]
    fn test_parse_physics_uri() {
        let uri = "skhaos://bio/physics/rondo?law=conservation&hz=10";
        let parsed = UDAPBioParser::parse(uri).unwrap();
        
        assert_eq!(parsed.domain, "physics");
        assert_eq!(parsed.resource, "rondo");
        assert_eq!(parsed.physics_law().unwrap(), "conservation");
    }

    #[test]
    fn test_build_uri() {
        let mut params = HashMap::new();
        params.insert("hz".to_string(), "20".to_string());
        params.insert("rank".to_string(), "1".to_string());
        
        let uri = UDAPBioParser::build("zipf", "unit", params);
        assert!(uri.contains("skhaos://bio/zipf/unit"));
        assert!(uri.contains("hz=20"));
    }

    #[test]
    fn test_uri_validation() {
        assert!(UDAPBioParser::validate("skhaos://bio/zipf/unit?hz=20").is_ok());
        assert!(UDAPBioParser::validate("invalid://uri").is_err());
    }

    #[test]
    fn test_bio_uri_helpers() {
        let uri = UDAPBioParser::parse("skhaos://bio/zipf/unit?rank=5&hz=100").unwrap();
        assert!(uri.is_zipf());
        assert_eq!(uri.zipf_rank().unwrap(), 5);
        assert_eq!(uri.frequency_hz().unwrap(), 100.0);
    }

    #[test]
    fn test_dolphin_burst_uri() {
        let uri = UDAPBioParser::parse("skhaos://bio/dolphin/click?burst=200&hz=120").unwrap();
        assert!(uri.is_dolphin());
        assert_eq!(uri.burst_count().unwrap(), 200);
        assert_eq!(uri.frequency_hz().unwrap(), 120.0);
    }
}
