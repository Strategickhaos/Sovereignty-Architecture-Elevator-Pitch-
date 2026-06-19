//! Configuration Management
//! 
//! Load and manage hypervisor and VM configurations

use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

/// Hypervisor configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HypervisorConfig {
    /// Node name in the mesh
    pub node_name: String,
    
    /// Node role
    pub node_role: NodeRole,
    
    /// Configuration directory
    pub config_dir: PathBuf,
    
    /// State directory
    pub state_dir: PathBuf,
    
    /// VM images directory
    pub images_dir: PathBuf,
    
    /// Mesh configuration
    pub mesh: MeshConfig,
}

impl Default for HypervisorConfig {
    fn default() -> Self {
        Self {
            node_name: "sagco-node".to_string(),
            node_role: NodeRole::Worker,
            config_dir: PathBuf::from("/etc/sagco-hv"),
            state_dir: PathBuf::from("/var/lib/sagco-hv"),
            images_dir: PathBuf::from("/var/lib/sagco-hv/images"),
            mesh: MeshConfig::default(),
        }
    }
}

/// Node role in the mesh
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum NodeRole {
    /// Primary controller node
    Controller,
    
    /// Worker node
    Worker,
    
    /// Archive node
    Archive,
}

/// Mesh configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MeshConfig {
    /// Enable mesh networking
    pub enabled: bool,
    
    /// Mesh discovery port
    pub discovery_port: u16,
    
    /// Known mesh nodes
    pub nodes: Vec<MeshNode>,
}

impl Default for MeshConfig {
    fn default() -> Self {
        Self {
            enabled: true,
            discovery_port: 7777,
            nodes: vec![],
        }
    }
}

/// Mesh node information
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MeshNode {
    pub name: String,
    pub address: String,
    pub role: NodeRole,
}

impl HypervisorConfig {
    /// Load configuration from file
    pub fn load(_path: &PathBuf) -> Result<Self> {
        // In a real implementation, load from YAML file
        Ok(Self::default())
    }
    
    /// Save configuration to file
    pub fn save(&self, _path: &PathBuf) -> Result<()> {
        // In a real implementation, save to YAML file
        Ok(())
    }
}
