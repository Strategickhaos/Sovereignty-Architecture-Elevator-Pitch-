//! # AI Personalities Configuration
//!
//! Defines the biases and traits of each AI council member.

use serde::{Deserialize, Serialize};

/// AI personality configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PersonalityConfig {
    pub name: String,
    pub bias: String,
    pub strengths: Vec<String>,
    pub decision_style: String,
}

/// Get the default personalities
pub fn get_default_personalities() -> Vec<PersonalityConfig> {
    vec![
        PersonalityConfig {
            name: "Grok".to_string(),
            bias: "Chaos".to_string(),
            strengths: vec!["Innovation".to_string(), "Risk-taking".to_string()],
            decision_style: "Disruptive".to_string(),
        },
        PersonalityConfig {
            name: "Claude".to_string(),
            bias: "Order".to_string(),
            strengths: vec!["Analysis".to_string(), "Safety".to_string()],
            decision_style: "Methodical".to_string(),
        },
        PersonalityConfig {
            name: "Gemini".to_string(),
            bias: "Balance".to_string(),
            strengths: vec!["Synthesis".to_string(), "Adaptability".to_string()],
            decision_style: "Pragmatic".to_string(),
        },
    ]
}
