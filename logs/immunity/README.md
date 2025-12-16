# Immunity Ledger - Blockchain-Style Vulnerability Log

## Purpose
This directory implements a **blockchain-style ledger** that records every "virus" (bug/vulnerability) the system has ever defeated, preventing that specific pattern from ever compiling again.

## Concept

In biological immune systems:
- Once exposed to a pathogen, B-cells create memory cells
- Future encounters are recognized immediately
- Immune response is faster and stronger

Similarly, this immunity ledger:
- Records every vulnerability ever encountered
- Recognizes similar patterns in future code
- Blocks compilation if vulnerability pattern detected
- Builds institutional memory of security

## Ledger Structure

```rust
use serde::{Serialize, Deserialize};
use chrono::{DateTime, Utc};
use sha2::{Sha256, Digest};

#[derive(Serialize, Deserialize, Clone)]
pub struct ImmunityRecord {
    /// Unique ID (hash of vulnerability)
    pub id: String,
    
    /// When was this vulnerability discovered?
    pub discovered_at: DateTime<Utc>,
    
    /// Vulnerability details
    pub vulnerability: Vulnerability,
    
    /// How was it fixed?
    pub fix: Fix,
    
    /// Pattern signature to detect in future
    pub signature: VulnerabilitySignature,
    
    /// Hash of previous record (blockchain link)
    pub prev_hash: String,
    
    /// Hash of this record
    pub hash: String
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Vulnerability {
    pub vuln_type: VulnerabilityType,
    pub severity: Severity,
    pub cwe_id: Option<String>,  // CWE classification
    pub cve_id: Option<String>,  // CVE if applicable
    pub description: String,
    pub affected_code: String,
    pub exploit_scenario: String
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Fix {
    pub commit_hash: String,
    pub patch: String,
    pub verification: TestResult,
    pub reviewer: String
}

#[derive(Serialize, Deserialize, Clone)]
pub struct VulnerabilitySignature {
    /// Abstract pattern that matches this vulnerability
    pub pattern: String,
    
    /// Regex to detect similar code
    pub regex: String,
    
    /// AST pattern matcher
    pub ast_pattern: Option<String>,
    
    /// Semantic fingerprint
    pub semantic_hash: String
}
```

## Blockchain Properties

```rust
pub struct ImmunityLedger {
    records: Vec<ImmunityRecord>,
    genesis_hash: String
}

impl ImmunityLedger {
    
    /// Add a new immunity record (like mining a block)
    pub fn add_record(&mut self, vuln: Vulnerability, fix: Fix) -> Result<ImmunityRecord> {
        // Generate signature
        let signature = self.generate_signature(&vuln, &fix)?;
        
        // Get previous hash
        let prev_hash = self.records.last()
            .map(|r| r.hash.clone())
            .unwrap_or(self.genesis_hash.clone());
        
        // Create record
        let record = ImmunityRecord {
            id: generate_id(),
            discovered_at: Utc::now(),
            vulnerability: vuln.clone(),
            fix: fix.clone(),
            signature,
            prev_hash: prev_hash.clone(),
            hash: String::new()  // Calculated next
        };
        
        // Calculate hash of this record
        let hash = self.calculate_hash(&record)?;
        let mut record = record;
        record.hash = hash;
        
        // Append to chain
        self.records.push(record.clone());
        
        // Persist to disk
        self.save_to_disk()?;
        
        log::info!("🛡️ New immunity record added: {}", record.id);
        
        Ok(record)
    }
    
    /// Calculate cryptographic hash of record
    fn calculate_hash(&self, record: &ImmunityRecord) -> Result<String> {
        let mut hasher = Sha256::new();
        
        // Hash all fields except the hash itself
        hasher.update(record.id.as_bytes());
        hasher.update(record.discovered_at.to_rfc3339().as_bytes());
        hasher.update(serde_json::to_string(&record.vulnerability)?.as_bytes());
        hasher.update(serde_json::to_string(&record.fix)?.as_bytes());
        hasher.update(record.prev_hash.as_bytes());
        
        let result = hasher.finalize();
        Ok(format!("{:x}", result))
    }
    
    /// Verify integrity of entire chain
    pub fn verify_integrity(&self) -> Result<bool> {
        for i in 0..self.records.len() {
            let record = &self.records[i];
            
            // Verify hash matches computed hash
            let computed_hash = self.calculate_hash(record)?;
            if record.hash != computed_hash {
                return Ok(false);
            }
            
            // Verify prev_hash links correctly
            if i > 0 {
                let prev_record = &self.records[i-1];
                if record.prev_hash != prev_record.hash {
                    return Ok(false);
                }
            }
        }
        
        Ok(true)
    }
    
    /// Check if code contains a known vulnerability pattern
    pub fn check_code(&self, code: &str) -> Vec<ImmunityMatch> {
        let mut matches = Vec::new();
        
        for record in &self.records {
            if self.matches_signature(code, &record.signature) {
                matches.push(ImmunityMatch {
                    record_id: record.id.clone(),
                    vulnerability_type: record.vulnerability.vuln_type,
                    discovered_at: record.discovered_at,
                    severity: record.vulnerability.severity,
                    message: format!(
                        "Code matches known vulnerability pattern: {}",
                        record.vulnerability.description
                    )
                });
            }
        }
        
        matches
    }
    
    fn matches_signature(&self, code: &str, signature: &VulnerabilitySignature) -> bool {
        // 1. Regex match
        if let Ok(re) = regex::Regex::new(&signature.regex) {
            if re.is_match(code) {
                return true;
            }
        }
        
        // 2. Pattern match
        if code.contains(&signature.pattern) {
            return true;
        }
        
        // 3. Semantic match (more sophisticated)
        let code_hash = calculate_semantic_hash(code);
        if code_hash == signature.semantic_hash {
            return true;
        }
        
        false
    }
}

pub struct ImmunityMatch {
    pub record_id: String,
    pub vulnerability_type: VulnerabilityType,
    pub discovered_at: DateTime<Utc>,
    pub severity: Severity,
    pub message: String
}
```

## Compiler Integration

```rust
/// Compiler hook to check code against immunity ledger
pub fn immunity_check(code: &str) -> Result<(), CompilationError> {
    let ledger = ImmunityLedger::load()?;
    
    // Check for known vulnerability patterns
    let matches = ledger.check_code(code);
    
    if !matches.is_empty() {
        let mut error_msg = String::from("❌ COMPILATION BLOCKED - Known Vulnerability Detected\n\n");
        
        for m in matches {
            error_msg.push_str(&format!(
                "  🦠 {}\n     Severity: {:?}\n     First seen: {}\n     Record ID: {}\n\n",
                m.message,
                m.severity,
                m.discovered_at.format("%Y-%m-%d"),
                m.record_id
            ));
        }
        
        error_msg.push_str("This vulnerability pattern is permanently blocked.\n");
        error_msg.push_str("Please revise your code to use the documented fix.\n");
        
        return Err(CompilationError::ImmunityViolation(error_msg));
    }
    
    Ok(())
}
```

## Example Records

```json
{
  "id": "imm_001",
  "discovered_at": "2024-11-15T10:30:00Z",
  "vulnerability": {
    "vuln_type": "SQL_INJECTION",
    "severity": "CRITICAL",
    "cwe_id": "CWE-89",
    "description": "SQL query with unsanitized user input",
    "affected_code": "SELECT * FROM users WHERE username = '{username}'",
    "exploit_scenario": "Attacker can inject ' OR '1'='1 to bypass auth"
  },
  "fix": {
    "commit_hash": "abc123...",
    "patch": "Use parameterized queries: SELECT * FROM users WHERE username = $1",
    "verification": "PASSED",
    "reviewer": "Claude"
  },
  "signature": {
    "pattern": "SELECT * FROM .* WHERE .* = '.*'",
    "regex": "SELECT.*WHERE.*=\\s*'[^?]+'",
    "ast_pattern": "StringInterpolation(SQLQuery)",
    "semantic_hash": "def456..."
  },
  "prev_hash": "genesis",
  "hash": "1a2b3c..."
}
```

## Visualization

```
Genesis Block
    ↓
┌─────────────────┐
│ Record #1       │
│ SQL Injection   │
│ 2024-11-15      │
│ Hash: 1a2b3c... │
└─────────────────┘
    ↓
┌─────────────────┐
│ Record #2       │
│ XSS Attack      │
│ 2024-11-20      │
│ Hash: 4d5e6f... │
└─────────────────┘
    ↓
┌─────────────────┐
│ Record #3       │
│ Buffer Overflow │
│ 2024-12-01      │
│ Hash: 7g8h9i... │
└─────────────────┘
    ↓
  [Future Records]
```

## Query API

```rust
impl ImmunityLedger {
    /// Get all vulnerabilities of a specific type
    pub fn get_by_type(&self, vuln_type: VulnerabilityType) -> Vec<&ImmunityRecord> {
        self.records.iter()
            .filter(|r| r.vulnerability.vuln_type == vuln_type)
            .collect()
    }
    
    /// Get vulnerabilities by severity
    pub fn get_by_severity(&self, severity: Severity) -> Vec<&ImmunityRecord> {
        self.records.iter()
            .filter(|r| r.vulnerability.severity == severity)
            .collect()
    }
    
    /// Get timeline of vulnerabilities
    pub fn get_timeline(&self) -> Vec<(DateTime<Utc>, &ImmunityRecord)> {
        self.records.iter()
            .map(|r| (r.discovered_at, r))
            .collect()
    }
    
    /// Export to various formats
    pub fn export_json(&self) -> Result<String> {
        serde_json::to_string_pretty(&self.records)
    }
    
    pub fn export_csv(&self) -> Result<String> {
        // CSV export for reporting
        unimplemented!()
    }
}
```

## Statistics

```rust
pub struct ImmunityStats {
    pub total_vulnerabilities: usize,
    pub by_type: HashMap<VulnerabilityType, usize>,
    pub by_severity: HashMap<Severity, usize>,
    pub blocked_compilations: u64,
    pub avg_time_to_fix: Duration,
    pub most_common_vuln: VulnerabilityType
}

impl ImmunityLedger {
    pub fn stats(&self) -> ImmunityStats {
        // Calculate statistics from ledger
        unimplemented!()
    }
}
```

## Benefits

1. **Permanent Memory**: Never repeat the same mistake twice
2. **Institutional Knowledge**: New developers benefit from past lessons
3. **Automated Prevention**: Compiler blocks known bad patterns
4. **Audit Trail**: Complete history of security evolution
5. **Tamper-Proof**: Blockchain structure prevents rewriting history

This creates a system with **evolving immunity** that gets stronger over time.
