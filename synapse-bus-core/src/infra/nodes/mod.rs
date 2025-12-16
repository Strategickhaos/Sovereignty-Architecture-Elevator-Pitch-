// Nodes - Personality Injection (Nova, Lyra, Athena)

/// Node personality types
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum NodePersonality {
    Nova,   // Aggressive, high-performance
    Lyra,   // Balanced, adaptive
    Athena, // Strategic, resource-efficient
}

/// Kubernetes node configuration
#[derive(Debug, Clone)]
pub struct Node {
    pub name: String,
    pub personality: NodePersonality,
    pub cpu_cores: u32,
    pub memory_gb: u32,
}

impl Node {
    pub fn new(name: String, personality: NodePersonality, cpu_cores: u32, memory_gb: u32) -> Self {
        Self {
            name,
            personality,
            cpu_cores,
            memory_gb,
        }
    }
}
