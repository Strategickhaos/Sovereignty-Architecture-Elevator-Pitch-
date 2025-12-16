// Crossfire - The Arena (SQLi, XSS, Buffer Overflow gen)

/// Attack vector categories
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AttackCategory {
    SqlInjection,
    XSS,
    BufferOverflow,
    RaceCondition,
    DoS,
    Cryptographic,
    Authentication,
    Authorization,
}

/// Attack vector
#[derive(Debug, Clone)]
pub struct AttackVector {
    pub id: usize,
    pub category: AttackCategory,
    pub description: String,
    pub severity: String,
}

/// Crossfire arena - generates attack vectors
pub struct CrossfireArena {
    vectors: Vec<AttackVector>,
}

impl CrossfireArena {
    pub fn new() -> Self {
        Self {
            vectors: Vec::new(),
        }
    }

    /// Generate attack vectors
    pub fn generate_vectors(&mut self, count: usize) {
        let categories = vec![
            AttackCategory::SqlInjection,
            AttackCategory::XSS,
            AttackCategory::BufferOverflow,
            AttackCategory::RaceCondition,
            AttackCategory::DoS,
        ];

        for i in 0..count {
            let category = categories[i % categories.len()].clone();
            self.vectors.push(AttackVector {
                id: i + 1,
                category: category.clone(),
                description: format!("{:?} attack vector {}", category, i + 1),
                severity: if i % 2 == 0 { "high".to_string() } else { "medium".to_string() },
            });
        }
    }

    /// Get all vectors
    pub fn vectors(&self) -> &[AttackVector] {
        &self.vectors
    }

    /// Get vector count
    pub fn count(&self) -> usize {
        self.vectors.len()
    }
}

impl Default for CrossfireArena {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_crossfire_generation() {
        let mut arena = CrossfireArena::new();
        arena.generate_vectors(100);
        assert_eq!(arena.count(), 100);
    }

    #[test]
    fn test_attack_categories() {
        let mut arena = CrossfireArena::new();
        arena.generate_vectors(10);
        
        let vectors = arena.vectors();
        assert!(!vectors.is_empty());
        assert!(vectors.iter().any(|v| v.category == AttackCategory::SqlInjection));
    }
}
