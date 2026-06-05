//! # Ratification: Requires 2/3 Votes
//!
//! Council voting system (Claude, Grok, Gemini).

use crate::error::{Result, SynapseError};

/// AI personality types
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AIPersonality {
    Claude,
    Grok,
    Gemini,
}

/// A vote from an AI personality
#[derive(Debug, Clone)]
pub struct Vote {
    pub personality: AIPersonality,
    pub approved: bool,
    pub reasoning: String,
}

/// Ratify a decision with the council
pub async fn ratify(proposal: &str, votes: Vec<Vote>) -> Result<bool> {
    if votes.len() < 3 {
        return Err(SynapseError::RatificationFailed(
            "Need at least 3 votes".to_string()
        ));
    }
    
    let approved_count = votes.iter().filter(|v| v.approved).count();
    let total_count = votes.len();
    
    // Require 2/3 majority
    let threshold = (total_count * 2 + 2) / 3;
    
    Ok(approved_count >= threshold)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_ratification_pass() {
        let votes = vec![
            Vote {
                personality: AIPersonality::Claude,
                approved: true,
                reasoning: "Good idea".to_string(),
            },
            Vote {
                personality: AIPersonality::Grok,
                approved: true,
                reasoning: "Approved".to_string(),
            },
            Vote {
                personality: AIPersonality::Gemini,
                approved: false,
                reasoning: "Needs work".to_string(),
            },
        ];
        
        let result = ratify("Test proposal", votes).await.unwrap();
        assert!(result);
    }

    #[tokio::test]
    async fn test_ratification_fail() {
        let votes = vec![
            Vote {
                personality: AIPersonality::Claude,
                approved: true,
                reasoning: "OK".to_string(),
            },
            Vote {
                personality: AIPersonality::Grok,
                approved: false,
                reasoning: "No".to_string(),
            },
            Vote {
                personality: AIPersonality::Gemini,
                approved: false,
                reasoning: "No".to_string(),
            },
        ];
        
        let result = ratify("Test proposal", votes).await.unwrap();
        assert!(!result);
    }
}
