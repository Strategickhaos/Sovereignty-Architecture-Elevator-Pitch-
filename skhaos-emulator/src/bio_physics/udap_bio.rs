// UDAP Bio-Physics URI Parser
// Extends Universal Domain Addressing Protocol with bio-physics parameters
// Examples:
//   skhaos://bio/zipf/unit/1?law=entropy&hz=20
//   skhaos://bio/dolphin/whistle?signature=true&pod=matrilineal_a&hz=10000
//   skhaos://physics/rondo/law=conservation&hz=10

use std::collections::HashMap;

/// UDAP Bio URI parser
pub struct UdapBioParser {
    pub scheme: String,
    pub domain: String,
    pub path_segments: Vec<String>,
    pub query_params: HashMap<String, String>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum BioUriType {
    WhaleZipf,
    DolphinWhistle,
    DolphinClick,
    PhysicsLaw,
    MusicForm,
    Unknown,
}

impl UdapBioParser {
    /// Parse UDAP bio-physics URI
    pub fn parse(uri: &str) -> Result<Self, String> {
        // Expected format: skhaos://domain/path/segments?param=value
        
        if !uri.starts_with("skhaos://") {
            return Err(format!("Invalid scheme, expected 'skhaos://', got: {}", uri));
        }

        let without_scheme = &uri[9..]; // Remove "skhaos://"
        
        // Split on '?' to separate path from query
        let parts: Vec<&str> = without_scheme.splitn(2, '?').collect();
        let path_part = parts[0];
        let query_part = if parts.len() > 1 { parts[1] } else { "" };

        // Parse path segments
        let segments: Vec<String> = path_part
            .split('/')
            .filter(|s| !s.is_empty())
            .map(|s| s.to_string())
            .collect();

        if segments.is_empty() {
            return Err("URI path is empty".to_string());
        }

        let domain = segments[0].clone();
        let path_segments = segments[1..].to_vec();

        // Parse query parameters
        let mut query_params = HashMap::new();
        if !query_part.is_empty() {
            for param in query_part.split('&') {
                let kv: Vec<&str> = param.splitn(2, '=').collect();
                if kv.len() == 2 {
                    query_params.insert(kv[0].to_string(), kv[1].to_string());
                } else if kv.len() == 1 {
                    query_params.insert(kv[0].to_string(), "true".to_string());
                }
            }
        }

        Ok(Self {
            scheme: "skhaos".to_string(),
            domain,
            path_segments,
            query_params,
        })
    }

    /// Determine the type of bio URI
    pub fn uri_type(&self) -> BioUriType {
        match self.domain.as_str() {
            "bio" => {
                if self.path_segments.is_empty() {
                    return BioUriType::Unknown;
                }
                match self.path_segments[0].as_str() {
                    "zipf" => BioUriType::WhaleZipf,
                    "dolphin" => {
                        if self.path_segments.len() > 1 {
                            match self.path_segments[1].as_str() {
                                "whistle" => BioUriType::DolphinWhistle,
                                "click" => BioUriType::DolphinClick,
                                _ => BioUriType::Unknown,
                            }
                        } else {
                            BioUriType::Unknown
                        }
                    }
                    _ => BioUriType::Unknown,
                }
            }
            "physics" => BioUriType::PhysicsLaw,
            "music" => BioUriType::MusicForm,
            _ => BioUriType::Unknown,
        }
    }

    /// Get frequency parameter (if present)
    pub fn frequency_hz(&self) -> Option<f64> {
        self.query_params.get("hz")
            .and_then(|s| s.parse::<f64>().ok())
    }

    /// Get Zipf rank parameter
    pub fn zipf_rank(&self) -> Option<u32> {
        self.query_params.get("rank")
            .and_then(|s| s.parse::<u32>().ok())
            .or_else(|| {
                // Try to get rank from path segments
                self.path_segments.last()
                    .and_then(|s| s.parse::<u32>().ok())
            })
    }

    /// Get physics law parameter
    pub fn physics_law(&self) -> Option<String> {
        self.query_params.get("law").cloned()
    }

    /// Get dolphin signature flag
    pub fn is_signature(&self) -> bool {
        self.query_params.get("signature")
            .map(|s| s == "true")
            .unwrap_or(false)
    }

    /// Get pod ID
    pub fn pod_id(&self) -> Option<String> {
        self.query_params.get("pod").cloned()
    }

    /// Get dialect parameter
    pub fn dialect(&self) -> Option<String> {
        self.query_params.get("dialect").cloned()
    }

    /// Get burst count for dolphin clicks
    pub fn burst_count(&self) -> Option<u32> {
        self.query_params.get("burst")
            .and_then(|s| s.parse::<u32>().ok())
    }

    /// Get brevity flag (Menzerath principle)
    pub fn is_brevity(&self) -> bool {
        self.query_params.get("brevity")
            .map(|s| s == "true")
            .unwrap_or(false)
    }

    /// Convert to string representation
    pub fn to_string(&self) -> String {
        let mut uri = format!("{}://{}", self.scheme, self.domain);
        
        for segment in &self.path_segments {
            uri.push('/');
            uri.push_str(segment);
        }

        if !self.query_params.is_empty() {
            uri.push('?');
            let params: Vec<String> = self.query_params.iter()
                .map(|(k, v)| format!("{}={}", k, v))
                .collect();
            uri.push_str(&params.join("&"));
        }

        uri
    }

    /// Validate URI structure
    pub fn validate(&self) -> Result<(), String> {
        if self.scheme != "skhaos" {
            return Err("Invalid scheme".to_string());
        }

        if self.domain.is_empty() {
            return Err("Empty domain".to_string());
        }

        match self.uri_type() {
            BioUriType::Unknown => Err("Unknown URI type".to_string()),
            _ => Ok(()),
        }
    }
}

/// Builder for UDAP bio URIs
pub struct UdapBioBuilder {
    domain: String,
    path: Vec<String>,
    params: HashMap<String, String>,
}

impl UdapBioBuilder {
    pub fn new(domain: &str) -> Self {
        Self {
            domain: domain.to_string(),
            path: Vec::new(),
            params: HashMap::new(),
        }
    }

    pub fn path(mut self, segment: &str) -> Self {
        self.path.push(segment.to_string());
        self
    }

    pub fn param(mut self, key: &str, value: &str) -> Self {
        self.params.insert(key.to_string(), value.to_string());
        self
    }

    pub fn frequency(self, hz: f64) -> Self {
        self.param("hz", &hz.to_string())
    }

    pub fn zipf_rank(self, rank: u32) -> Self {
        self.param("rank", &rank.to_string())
    }

    pub fn physics_law(self, law: &str) -> Self {
        self.param("law", law)
    }

    pub fn signature(self, is_sig: bool) -> Self {
        self.param("signature", &is_sig.to_string())
    }

    pub fn pod(self, pod_id: &str) -> Self {
        self.param("pod", pod_id)
    }

    pub fn build(self) -> String {
        let mut uri = format!("skhaos://{}", self.domain);
        
        for segment in &self.path {
            uri.push('/');
            uri.push_str(segment);
        }

        if !self.params.is_empty() {
            uri.push('?');
            let params: Vec<String> = self.params.iter()
                .map(|(k, v)| format!("{}={}", k, v))
                .collect();
            uri.push_str(&params.join("&"));
        }

        uri
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_zipf_uri() {
        let uri = "skhaos://bio/zipf/unit/1?law=entropy&hz=20";
        let parser = UdapBioParser::parse(uri).unwrap();
        
        assert_eq!(parser.scheme, "skhaos");
        assert_eq!(parser.domain, "bio");
        assert_eq!(parser.uri_type(), BioUriType::WhaleZipf);
        assert_eq!(parser.frequency_hz(), Some(20.0));
        assert_eq!(parser.physics_law(), Some("entropy".to_string()));
        assert_eq!(parser.zipf_rank(), Some(1));
    }

    #[test]
    fn test_parse_dolphin_whistle() {
        let uri = "skhaos://bio/dolphin/whistle?signature=true&pod=matrilineal_a&hz=10000";
        let parser = UdapBioParser::parse(uri).unwrap();
        
        assert_eq!(parser.uri_type(), BioUriType::DolphinWhistle);
        assert!(parser.is_signature());
        assert_eq!(parser.pod_id(), Some("matrilineal_a".to_string()));
        assert_eq!(parser.frequency_hz(), Some(10000.0));
    }

    #[test]
    fn test_parse_dolphin_click() {
        let uri = "skhaos://bio/dolphin/click?burst=200&hz=120000";
        let parser = UdapBioParser::parse(uri).unwrap();
        
        assert_eq!(parser.uri_type(), BioUriType::DolphinClick);
        assert_eq!(parser.burst_count(), Some(200));
        assert_eq!(parser.frequency_hz(), Some(120000.0));
    }

    #[test]
    fn test_parse_physics_uri() {
        let uri = "skhaos://physics/rondo/law=conservation&hz=10";
        let parser = UdapBioParser::parse(uri).unwrap();
        
        assert_eq!(parser.domain, "physics");
        assert_eq!(parser.uri_type(), BioUriType::PhysicsLaw);
    }

    #[test]
    fn test_invalid_scheme() {
        let uri = "http://bio/zipf/unit/1";
        let result = UdapBioParser::parse(uri);
        assert!(result.is_err());
    }

    #[test]
    fn test_builder() {
        let uri = UdapBioBuilder::new("bio")
            .path("zipf")
            .path("unit")
            .path("1")
            .frequency(20.0)
            .physics_law("entropy")
            .build();
        
        assert!(uri.contains("skhaos://bio/zipf/unit/1"));
        assert!(uri.contains("hz=20"));
        assert!(uri.contains("law=entropy"));
    }

    #[test]
    fn test_dolphin_builder() {
        let uri = UdapBioBuilder::new("bio")
            .path("dolphin")
            .path("whistle")
            .signature(true)
            .pod("matrilineal_a")
            .frequency(10000.0)
            .build();
        
        let parser = UdapBioParser::parse(&uri).unwrap();
        assert_eq!(parser.uri_type(), BioUriType::DolphinWhistle);
        assert!(parser.is_signature());
    }

    #[test]
    fn test_to_string() {
        let original = "skhaos://bio/zipf/unit/1?law=entropy&hz=20";
        let parser = UdapBioParser::parse(original).unwrap();
        let reconstructed = parser.to_string();
        
        // Should contain all parts (order of query params may differ)
        assert!(reconstructed.contains("skhaos://bio/zipf/unit/1"));
        assert!(reconstructed.contains("law=entropy"));
        assert!(reconstructed.contains("hz=20"));
    }
}
