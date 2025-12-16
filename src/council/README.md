# Council Module - The Consensus Interface

## Purpose
This directory implements the **Legion of Minds** governance system. It creates a `Ratifiable` trait that requires boolean `APPROVE` votes from at least two distinct AI models before a function can execute.

## Core Concept

No single AI (or human) should have unilateral control over critical system functions. Instead, we implement a **multi-model consensus mechanism** where decisions require agreement from multiple independent intelligences.

## Architecture

```
src/council/
├── ratifiable.flame         # Core trait definition
├── voters.flame             # AI model voter implementations
├── quorum.flame             # Quorum calculation logic
├── voting_record.rs         # Persistent voting ledger
└── README.md
```

## The Ratifiable Trait

```flame
/**
 * Ratifiable - Requires multi-model consensus
 */
trait Ratifiable {
    /// Get the proposal that needs ratification
    fn proposal(&self) -> Proposal;
    
    /// Request votes from the Legion
    async fn request_votes(&self) -> Vec<Vote>;
    
    /// Check if quorum is reached (default: 2 of 3)
    fn has_quorum(&self, votes: &[Vote]) -> bool {
        let approvals = votes.iter()
            .filter(|v| v.decision == Decision::Approve)
            .count();
        
        approvals >= 2  // Minimum 2 approvals required
    }
    
    /// Execute only if ratified
    async fn execute_if_ratified(&self) -> Result<(), ExecutionError> {
        let votes = self.request_votes().await;
        
        if !self.has_quorum(&votes) {
            return Err(ExecutionError::QuorumNotReached {
                approvals: votes.iter().filter(|v| v.decision == Decision::Approve).count(),
                required: 2
            });
        }
        
        // Log ratification to immunity ledger
        log_ratification(&self.proposal(), &votes);
        
        // Execute the ratified action
        self.execute()
    }
    
    /// The actual execution logic
    fn execute(&self) -> Result<(), ExecutionError>;
}
```

## AI Voter Implementations

### Claude (Structured Reasoning)
```flame
struct ClaudeVoter {
    api_key: String,
    model: String  // "claude-3-opus-20240229"
}

impl Voter for ClaudeVoter {
    async fn vote(&self, proposal: &Proposal) -> Vote {
        let prompt = format!(
            "You are Claude, a structured reasoning agent in the Legion of Minds governance system.\n\
             \n\
             Proposal: {}\n\
             \n\
             Analyze this proposal for:\n\
             1. Logical consistency\n\
             2. Security implications\n\
             3. Alignment with system architecture\n\
             \n\
             Vote: APPROVE or REJECT\n\
             Rationale: (brief explanation)",
            proposal.description
        );
        
        let response = self.query_api(prompt).await;
        
        Vote {
            voter: "Claude".to_string(),
            decision: parse_decision(&response),
            rationale: extract_rationale(&response),
            timestamp: DateTime::now()
        }
    }
}
```

### Grok (Chaotic Creativity)
```flame
struct GrokVoter {
    api_key: String,
    model: String  // "grok-beta"
}

impl Voter for GrokVoter {
    async fn vote(&self, proposal: &Proposal) -> Vote {
        let prompt = format!(
            "You are Grok, the chaotic creative force in the Legion of Minds.\n\
             \n\
             Proposal: {}\n\
             \n\
             Consider:\n\
             1. Novel possibilities this unlocks\n\
             2. Unconventional risks\n\
             3. Emergent potential\n\
             \n\
             Vote with your gut: APPROVE or REJECT\n\
             Why: (intuitive explanation)",
            proposal.description
        );
        
        let response = self.query_api(prompt).await;
        
        Vote {
            voter: "Grok".to_string(),
            decision: parse_decision(&response),
            rationale: extract_rationale(&response),
            timestamp: DateTime::now()
        }
    }
}
```

### Human (Domenic Garza)
```flame
struct HumanVoter {
    name: String,
    contact: String
}

impl Voter for HumanVoter {
    async fn vote(&self, proposal: &Proposal) -> Vote {
        // Send notification to human
        notify_human(&self.contact, proposal).await;
        
        // Wait for human response (with timeout)
        let response = wait_for_human_vote(proposal.id, Duration::from_hours(24)).await;
        
        response.unwrap_or(Vote {
            voter: self.name.clone(),
            decision: Decision::Abstain,
            rationale: "Timeout - no response within 24 hours".to_string(),
            timestamp: DateTime::now()
        })
    }
}
```

## Quorum Rules

The system supports flexible quorum configurations:

```yaml
# config/council.yaml
quorum:
  default: 2  # Minimum 2 approvals
  
  critical_operations:  # Require all 3
    - kernel_write
    - security_policy_change
    - key_rotation
  
  routine_operations:  # Require only 2
    - feature_addition
    - documentation_update
    - test_modification
  
  emergency_override:  # Human can override in emergencies
    enabled: true
    requires_justification: true
```

## Example Usage

```flame
struct KernelWriteProposal {
    path: String,
    content: String,
    rationale: String
}

impl Ratifiable for KernelWriteProposal {
    fn proposal(&self) -> Proposal {
        Proposal {
            id: generate_id(),
            title: format!("Write to kernel/{}", self.path),
            description: self.rationale.clone(),
            category: ProposalCategory::Critical
        }
    }
    
    async fn request_votes(&self) -> Vec<Vote> {
        let claude = ClaudeVoter::new();
        let grok = GrokVoter::new();
        let human = HumanVoter::new("Domenic Garza");
        
        // Request votes in parallel
        let (vote_claude, vote_grok, vote_human) = tokio::join!(
            claude.vote(&self.proposal()),
            grok.vote(&self.proposal()),
            human.vote(&self.proposal())
        );
        
        vec![vote_claude, vote_grok, vote_human]
    }
    
    fn execute(&self) -> Result<(), ExecutionError> {
        // Write to kernel (only called if ratified)
        kernel::write(&self.path, &self.content)
    }
}

// Usage
let proposal = KernelWriteProposal {
    path: "core/memory.rs".to_string(),
    content: "/* new implementation */".to_string(),
    rationale: "Optimize memory allocator for GSCH buffers".to_string()
};

proposal.execute_if_ratified().await?;
```

## Voting Record

All votes are permanently recorded:

```json
{
  "proposal_id": "prop_123abc",
  "timestamp": "2024-12-16T17:22:33.897Z",
  "proposal": {
    "title": "Write to kernel/core/memory.rs",
    "description": "Optimize memory allocator",
    "category": "Critical"
  },
  "votes": [
    {
      "voter": "Claude",
      "decision": "APPROVE",
      "rationale": "Optimization is sound and improves performance",
      "timestamp": "2024-12-16T17:23:00.000Z"
    },
    {
      "voter": "Grok",
      "decision": "APPROVE",
      "rationale": "Bold move, I like it. Go for it.",
      "timestamp": "2024-12-16T17:23:15.000Z"
    },
    {
      "voter": "Domenic Garza",
      "decision": "APPROVE",
      "rationale": "Reviewed the code, looks good",
      "timestamp": "2024-12-16T17:25:00.000Z"
    }
  ],
  "outcome": "RATIFIED",
  "execution_status": "SUCCESS"
}
```

## Security Properties

1. **No Single Point of Failure**: No single AI can approve critical changes
2. **Diverse Perspectives**: Claude (structured) + Grok (creative) = balanced decisions
3. **Human Override**: Human can break ties or override in emergencies
4. **Audit Trail**: Every decision is permanently recorded
5. **Fail-Safe**: Default is REJECT if quorum not reached
