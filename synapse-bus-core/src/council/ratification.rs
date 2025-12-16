// Ratification - Requires 2/3 Votes (Claude, Grok, Gemini)

/// AI personality for voting
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AIPersonality {
    Claude,  // Order-focused
    Grok,    // Chaos-focused
    Gemini,  // Balance-focused
}

/// Vote result
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Vote {
    Approve,
    Reject,
    Abstain,
}

/// Proposal for ratification
#[derive(Debug, Clone)]
pub struct Proposal {
    pub id: String,
    pub description: String,
    pub votes: Vec<(AIPersonality, Vote)>,
}

impl Proposal {
    pub fn new(id: String, description: String) -> Self {
        Self {
            id,
            description,
            votes: Vec::new(),
        }
    }

    /// Cast a vote
    pub fn vote(&mut self, personality: AIPersonality, vote: Vote) {
        self.votes.push((personality, vote));
    }

    /// Check if proposal is ratified (2/3 approval)
    pub fn is_ratified(&self) -> bool {
        let total = self.votes.len();
        if total < 3 {
            return false; // Need all three votes
        }

        let approvals = self.votes.iter().filter(|(_, v)| *v == Vote::Approve).count();
        approvals >= 2 // 2/3 majority
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_proposal_ratification() {
        let mut proposal = Proposal::new("P001".to_string(), "Test proposal".to_string());
        
        proposal.vote(AIPersonality::Claude, Vote::Approve);
        proposal.vote(AIPersonality::Grok, Vote::Approve);
        proposal.vote(AIPersonality::Gemini, Vote::Reject);
        
        assert!(proposal.is_ratified());
    }

    #[test]
    fn test_proposal_rejected() {
        let mut proposal = Proposal::new("P002".to_string(), "Test proposal".to_string());
        
        proposal.vote(AIPersonality::Claude, Vote::Approve);
        proposal.vote(AIPersonality::Grok, Vote::Reject);
        proposal.vote(AIPersonality::Gemini, Vote::Reject);
        
        assert!(!proposal.is_ratified());
    }
}
