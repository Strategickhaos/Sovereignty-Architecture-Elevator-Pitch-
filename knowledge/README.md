# Knowledge Base - Vector Database Linkage

## Purpose
This directory ensures that every function in `src/` has a corresponding back-link to a specific note in the 10,000-note Obsidian Vault for semantic grounding.

## Architecture

```
knowledge/
├── vector_db/              # Vector database integration
│   ├── embeddings.rs       # Generate embeddings for code
│   ├── search.rs           # Semantic search
│   └── indexing.rs         # Index code and docs
├── obsidian_link/          # Obsidian vault linkage
│   ├── bidirectional.rs    # Bidirectional links
│   ├── sync.rs             # Keep in sync
│   └── validator.rs        # Ensure all functions linked
├── semantic_ground/        # Semantic grounding
│   ├── context.rs          # Context enrichment
│   └── meaning.rs          # Meaning extraction
└── README.md
```

## Bidirectional Linking

Every function must have:
1. **Forward Link**: Code → Obsidian note
2. **Back Link**: Obsidian note → Code

```flame
/**
 * Example function with Obsidian link
 * 
 * @obsidian_link [[GSCH/Gradient-Reconciliation]]
 * @vault_path /Obsidian/Patents/GSCH/Gradient-Reconciliation.md
 * @semantic_context "Homeostasis, Proton/Electron gradients, Buffer systems"
 */
pub fn reconcile_gradients(protons: Vec<Gradient>, electrons: Vec<Gradient>) 
    -> Result<EquilibriumState, DissolveEvent> {
    // Implementation...
}
```

## Validation

At build time, verify all functions are linked:

```rust
#[test]
fn test_all_functions_linked_to_obsidian() {
    let functions = find_all_functions("src/");
    let mut unlinked = Vec::new();
    
    for func in functions {
        if !has_obsidian_link(&func) {
            unlinked.push(func.name);
        }
    }
    
    if !unlinked.is_empty() {
        panic!(
            "Functions missing Obsidian links: {:?}",
            unlinked
        );
    }
}
```

## Vector Database Integration

```rust
use pgvector::Vector;
use openai::embeddings;

/// Generate embedding for code function
pub async fn embed_function(func: &Function) -> Result<Vector> {
    let text = format!(
        "{}\n{}\n{}",
        func.signature,
        func.documentation,
        func.body
    );
    
    let embedding = embeddings::create(text).await?;
    
    Ok(Vector::from(embedding.data[0].embedding))
}

/// Find semantically similar functions
pub async fn find_similar_functions(
    query: &str,
    limit: usize
) -> Result<Vec<Function>> {
    let query_embedding = embeddings::create(query).await?;
    
    let results = db.query(
        "SELECT * FROM functions 
         ORDER BY embedding <-> $1 
         LIMIT $2",
        &[&Vector::from(query_embedding.data[0].embedding), &limit]
    ).await?;
    
    results.iter()
        .map(|row| Function::from_row(row))
        .collect()
}
```

## Semantic Grounding

Link code to domain knowledge:

```yaml
# knowledge/semantic_ground/mappings.yaml

function: "reconcile_gradients"
obsidian_note: "[[GSCH/Gradient-Reconciliation]]"
concepts:
  - "Homeostasis"
  - "Proton gradient"
  - "Electron gradient"
  - "Buffer systems"
  - "pH regulation"
related_functions:
  - "buffer.flame::absorb"
  - "clamp.flame::eject_packet"
  - "feedback.flame::compute"
patent_claims:
  - "US Provisional - Claim 8"
biological_analogy: "Mitochondrial proton gradient"
papers:
  - "Mitchell, P. (1961). Coupling of phosphorylation to electron"
```

## Obsidian Vault Structure

```
Obsidian/
├── Patents/
│   ├── GSCH/
│   │   ├── Gradient-Reconciliation.md
│   │   ├── Buffer-Systems.md
│   │   └── Homeostasis.md
│   └── Legion-of-Minds/
│       ├── Consensus.md
│       └── Ratifiable-Trait.md
├── Architecture/
│   ├── Sovereignty-Layers.md
│   ├── Ripley-Gates.md
│   └── Bio-Digital-Interface.md
├── Implementation/
│   ├── Code-Snippets/
│   └── Design-Decisions/
└── Knowledge-Base/
    ├── Biology/
    ├── Computer-Science/
    └── Business-Strategy/
```

## Sync Process

```bash
# Bidirectional sync between code and Obsidian
./knowledge/sync.sh

# 1. Extract @obsidian_link annotations from code
# 2. Verify corresponding notes exist in Obsidian
# 3. Update Obsidian notes with code references
# 4. Generate missing notes for unlinked functions
# 5. Update vector database with new embeddings
```

## Example Obsidian Note

```markdown
# Gradient Reconciliation

## Overview
Core implementation of GSCH (Gradient Stabilization Controlled Homeostasis).

## Code Reference
- **File**: `src/flame/homeostasis/gradient.flame`
- **Function**: `reconcile_gradients()`
- **Git**: `66c2d0d` (commit hash)

## Biological Basis
In mitochondria, the proton gradient across the inner membrane drives ATP synthesis.
We model this as Push (Protons) and Pull (Electrons) forces that must be balanced.

## Implementation Details
When gradients mismatch:
1. Calculate net vectors
2. Check unit compatibility
3. Compute equilibrium point
4. Trigger Dissolve if out of bounds

## Related Concepts
- [[Buffer Systems]]
- [[Homeostasis]]
- [[Dissolution Protocol]]
- [[Patent Claim 8]]

## References
- Mitchell, P. (1961). "Coupling of phosphorylation to electron..."
- Code: [[gradient.flame]]
```

## Benefits

1. **Semantic Grounding**: Every function has documented meaning
2. **Knowledge Traceability**: Track ideas from concept to code
3. **Patent Support**: Direct links to patent claims
4. **Onboarding**: New developers can understand context
5. **AI Assistance**: Vector search finds relevant code semantically

## Integration with Legion of Minds

AI agents can query the knowledge base:

```rust
// Claude needs to understand a function
let context = knowledge::get_context("reconcile_gradients").await?;

// Grok searches for similar patterns
let similar = knowledge::find_similar("homeostasis balance").await?;

// Human explores connections
let graph = knowledge::build_knowledge_graph("GSCH").await?;
```

This creates a **living knowledge base** that grows with the codebase.
