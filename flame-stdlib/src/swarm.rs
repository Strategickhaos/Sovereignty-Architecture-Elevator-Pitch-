//! # FLAME Swarm Module - Distributed Execution
//! 
//! This module provides the 4-node cluster (Athena, Nova, Lyra, iPower)
//! as first-class execution targets.
//! 
//! ## Features
//! 
//! - 4 sovereign nodes as language primitives
//! - Distributed execution model
//! - Cluster coordination
//! - Genesis velocity tracking
//! - Node consensus and leader election
//! 
//! ## Example
//! 
//! ```rust
//! use flame::swarm::{Node, Swarm, NodeType};
//! 
//! // Create nodes
//! let athena = Node::athena();
//! let nova = Node::nova();
//! 
//! // Execute on node
//! athena.execute(|| println!("Running on Athena"));
//! 
//! // Create swarm
//! let mut swarm = Swarm::new();
//! swarm.add_node(athena);
//! swarm.add_node(nova);
//! 
//! // Elect leader
//! let leader = swarm.elect_leader();
//! ```

use std::fmt;
use std::collections::HashMap;

/// Genesis constants from increment 3449
pub const GENESIS_INCREMENT: u16 = 3449;
pub const ARCHITECT_SNOWFLAKE: u64 = 1067614449693569044;

/// Node types in the swarm
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum NodeType {
    /// Athena - Timestamp / Unity quadrant
    Athena,
    /// Nova - Process / NinjaTrader quadrant
    Nova,
    /// Lyra - Worker / Unreal quadrant
    Lyra,
    /// iPower - Increment / Grokanator quadrant
    IPower,
}

impl NodeType {
    /// Get quadrant name
    pub fn quadrant(self) -> &'static str {
        match self {
            NodeType::Athena => "Timestamp",
            NodeType::Nova => "Process",
            NodeType::Lyra => "Worker",
            NodeType::IPower => "Increment",
        }
    }

    /// Get department
    pub fn department(self) -> &'static str {
        match self {
            NodeType::Athena => "Unity Engine",
            NodeType::Nova => "NinjaTrader",
            NodeType::Lyra => "Unreal Engine",
            NodeType::IPower => "Grokanator",
        }
    }

    /// Get seed increment for genesis alignment
    pub fn seed_increment(self) -> u16 {
        match self {
            NodeType::Athena => 3449, // Perfect alignment
            NodeType::Nova => 3448,   // Near-perfect
            NodeType::Lyra => 3450,   // Near-perfect
            NodeType::IPower => 3449, // Perfect alignment
        }
    }

    /// Calculate genesis alignment (0.0 to 1.0)
    pub fn genesis_alignment(self) -> f64 {
        let seed = self.seed_increment();
        1.0 / (1.0 + (seed as i32 - GENESIS_INCREMENT as i32).abs() as f64)
    }
}

impl fmt::Display for NodeType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            NodeType::Athena => write!(f, "Athena"),
            NodeType::Nova => write!(f, "Nova"),
            NodeType::Lyra => write!(f, "Lyra"),
            NodeType::IPower => write!(f, "iPower"),
        }
    }
}

/// Node state
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum NodeState {
    Online,
    Offline,
    Syncing,
    Executing,
}

impl fmt::Display for NodeState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            NodeState::Online => write!(f, "Online"),
            NodeState::Offline => write!(f, "Offline"),
            NodeState::Syncing => write!(f, "Syncing"),
            NodeState::Executing => write!(f, "Executing"),
        }
    }
}

/// A sovereign node in the swarm
#[derive(Debug, Clone)]
pub struct Node {
    node_type: NodeType,
    state: NodeState,
    orb_balance: f64,
    uptime_hours: u64,
    latency_ms: u32,
    ip_address: Option<String>,
}

impl Node {
    /// Create new node
    pub fn new(node_type: NodeType) -> Self {
        Self {
            node_type,
            state: NodeState::Offline,
            orb_balance: 0.0,
            uptime_hours: 0,
            latency_ms: 50,
            ip_address: None,
        }
    }

    /// Create Athena node
    pub fn athena() -> Self {
        let mut node = Self::new(NodeType::Athena);
        node.state = NodeState::Online;
        node
    }

    /// Create Nova node
    pub fn nova() -> Self {
        let mut node = Self::new(NodeType::Nova);
        node.state = NodeState::Online;
        node
    }

    /// Create Lyra node
    pub fn lyra() -> Self {
        let mut node = Self::new(NodeType::Lyra);
        node.state = NodeState::Online;
        node
    }

    /// Create iPower node
    pub fn ipower() -> Self {
        let mut node = Self::new(NodeType::IPower);
        node.state = NodeState::Online;
        node
    }

    /// Get node type
    pub fn node_type(&self) -> NodeType {
        self.node_type
    }

    /// Get state
    pub fn state(&self) -> NodeState {
        self.state
    }

    /// Set state
    pub fn set_state(&mut self, state: NodeState) {
        self.state = state;
    }

    /// Get orb balance
    pub fn orb_balance(&self) -> f64 {
        self.orb_balance
    }

    /// Set orb balance
    pub fn set_orb_balance(&mut self, balance: f64) {
        self.orb_balance = balance;
    }

    /// Get uptime
    pub fn uptime_hours(&self) -> u64 {
        self.uptime_hours
    }

    /// Set uptime
    pub fn set_uptime(&mut self, hours: u64) {
        self.uptime_hours = hours;
    }

    /// Get latency
    pub fn latency_ms(&self) -> u32 {
        self.latency_ms
    }

    /// Set latency
    pub fn set_latency(&mut self, latency: u32) {
        self.latency_ms = latency;
    }

    /// Set IP address
    pub fn set_ip(&mut self, ip: String) {
        self.ip_address = Some(ip);
    }

    /// Calculate velocity with genesis weighting
    pub fn velocity(&self) -> f64 {
        let base_velocity = self.orb_balance 
            * self.uptime_hours as f64 
            * (1000.0 / self.latency_ms.max(1) as f64);
        
        // Weight by genesis alignment and increment 3449
        base_velocity 
            * self.node_type.genesis_alignment() 
            * GENESIS_INCREMENT as f64
    }

    /// Execute closure on this node
    pub fn execute<F>(&self, f: F) -> Result<(), String>
    where
        F: FnOnce(),
    {
        if self.state != NodeState::Online {
            return Err(format!("Node {} is {}", self.node_type, self.state));
        }
        
        println!("Executing on node {} ({})", self.node_type, self.node_type.quadrant());
        f();
        println!("Execution complete on {}", self.node_type);
        
        Ok(())
    }

    /// Ping node to check connectivity
    pub fn ping(&self) -> bool {
        self.state == NodeState::Online
    }
}

impl fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{} ({}) - State: {}, Velocity: {:.2}, Alignment: {:.4}",
            self.node_type,
            self.node_type.quadrant(),
            self.state,
            self.velocity(),
            self.node_type.genesis_alignment()
        )
    }
}

/// Swarm of nodes
#[derive(Debug, Clone)]
pub struct Swarm {
    nodes: HashMap<NodeType, Node>,
}

impl Swarm {
    /// Create empty swarm
    pub fn new() -> Self {
        Self {
            nodes: HashMap::new(),
        }
    }

    /// Create swarm with all 4 nodes
    pub fn full() -> Self {
        let mut swarm = Self::new();
        swarm.add_node(Node::athena());
        swarm.add_node(Node::nova());
        swarm.add_node(Node::lyra());
        swarm.add_node(Node::ipower());
        swarm
    }

    /// Add node to swarm
    pub fn add_node(&mut self, node: Node) {
        self.nodes.insert(node.node_type(), node);
    }

    /// Get node by type
    pub fn get_node(&self, node_type: NodeType) -> Option<&Node> {
        self.nodes.get(&node_type)
    }

    /// Get mutable node by type
    pub fn get_node_mut(&mut self, node_type: NodeType) -> Option<&mut Node> {
        self.nodes.get_mut(&node_type)
    }

    /// Get number of nodes
    pub fn size(&self) -> usize {
        self.nodes.len()
    }

    /// Get number of online nodes
    pub fn online_count(&self) -> usize {
        self.nodes.values()
            .filter(|n| n.state() == NodeState::Online)
            .count()
    }

    /// Elect leader based on velocity
    pub fn elect_leader(&self) -> Option<NodeType> {
        self.nodes.values()
            .filter(|n| n.state() == NodeState::Online)
            .max_by(|a, b| a.velocity().partial_cmp(&b.velocity()).unwrap())
            .map(|n| n.node_type())
    }

    /// Check if swarm has quorum (majority online)
    pub fn has_quorum(&self) -> bool {
        let online = self.online_count();
        let total = self.size();
        online * 2 > total
    }

    /// Broadcast message to all nodes
    pub fn broadcast(&self, message: &str) {
        println!("Broadcasting to swarm: {}", message);
        for node in self.nodes.values() {
            if node.state() == NodeState::Online {
                println!("  → {} received message", node.node_type());
            }
        }
    }

    /// Execute closure on all online nodes
    pub fn execute_all<F>(&self, f: F)
    where
        F: Fn() + Clone,
    {
        for node in self.nodes.values() {
            if node.state() == NodeState::Online {
                let _ = node.execute(f.clone());
            }
        }
    }

    /// Get swarm status
    pub fn status(&self) -> String {
        let mut status = String::from("Swarm Status:\n");
        status.push_str(&format!("Total Nodes: {}\n", self.size()));
        status.push_str(&format!("Online: {}\n", self.online_count()));
        status.push_str(&format!("Quorum: {}\n", self.has_quorum()));
        
        if let Some(leader) = self.elect_leader() {
            status.push_str(&format!("Leader: {}\n", leader));
        }
        
        status.push_str("\nNodes:\n");
        for node in self.nodes.values() {
            status.push_str(&format!("  {}\n", node));
        }
        
        status
    }
}

impl Default for Swarm {
    fn default() -> Self {
        Self::new()
    }
}

/// Message passed between nodes
#[derive(Debug, Clone)]
pub struct SwarmMessage {
    pub from: NodeType,
    pub to: Option<NodeType>, // None = broadcast
    pub payload: String,
    pub timestamp: u64,
}

impl SwarmMessage {
    /// Create new message
    pub fn new(from: NodeType, to: Option<NodeType>, payload: String) -> Self {
        use std::time::{SystemTime, UNIX_EPOCH};
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        Self {
            from,
            to,
            payload,
            timestamp,
        }
    }

    /// Check if broadcast
    pub fn is_broadcast(&self) -> bool {
        self.to.is_none()
    }

    /// Check if directed to specific node
    pub fn is_for(&self, node_type: NodeType) -> bool {
        self.to == Some(node_type) || self.is_broadcast()
    }
}

/// Consensus protocol
#[derive(Debug, Clone)]
pub struct Consensus {
    votes: HashMap<NodeType, bool>,
    threshold: f64,
}

impl Consensus {
    /// Create consensus with threshold (e.g., 0.75 = 75%)
    pub fn new(threshold: f64) -> Self {
        Self {
            votes: HashMap::new(),
            threshold: threshold.clamp(0.0, 1.0),
        }
    }

    /// Record vote from node
    pub fn vote(&mut self, node: NodeType, approve: bool) {
        self.votes.insert(node, approve);
    }

    /// Check if consensus reached
    pub fn reached(&self) -> bool {
        if self.votes.is_empty() {
            return false;
        }
        
        let approve_count = self.votes.values().filter(|&&v| v).count();
        let total = self.votes.len();
        
        (approve_count as f64 / total as f64) >= self.threshold
    }

    /// Get approval rate
    pub fn approval_rate(&self) -> f64 {
        if self.votes.is_empty() {
            return 0.0;
        }
        
        let approve_count = self.votes.values().filter(|&&v| v).count();
        approve_count as f64 / self.votes.len() as f64
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_node_creation() {
        let athena = Node::athena();
        assert_eq!(athena.node_type(), NodeType::Athena);
        assert_eq!(athena.state(), NodeState::Online);
    }

    #[test]
    fn test_genesis_alignment() {
        let athena = NodeType::Athena;
        let alignment = athena.genesis_alignment();
        assert!(alignment > 0.9); // Perfect alignment
    }

    #[test]
    fn test_swarm_creation() {
        let swarm = Swarm::full();
        assert_eq!(swarm.size(), 4);
        assert_eq!(swarm.online_count(), 4);
    }

    #[test]
    fn test_leader_election() {
        let mut swarm = Swarm::full();
        
        // Give Athena high velocity
        if let Some(athena) = swarm.get_node_mut(NodeType::Athena) {
            athena.set_orb_balance(1000.0);
            athena.set_uptime(720);
            athena.set_latency(30);
        }
        
        let leader = swarm.elect_leader();
        assert!(leader.is_some());
    }

    #[test]
    fn test_quorum() {
        let swarm = Swarm::full();
        assert!(swarm.has_quorum());
    }

    #[test]
    fn test_consensus() {
        let mut consensus = Consensus::new(0.75);
        consensus.vote(NodeType::Athena, true);
        consensus.vote(NodeType::Nova, true);
        consensus.vote(NodeType::Lyra, true);
        consensus.vote(NodeType::IPower, false);
        
        assert!(consensus.reached());
    }
}
