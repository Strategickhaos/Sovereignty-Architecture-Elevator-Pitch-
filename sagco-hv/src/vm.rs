//! VM Definition and Management
//! 
//! Structures for defining and managing virtual machines

use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use tracing::info;

/// VM configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VmDefinition {
    /// VM name
    pub name: String,
    
    /// Number of vCPUs
    pub vcpu_count: u32,
    
    /// Memory size in MB
    pub memory_mb: u64,
    
    /// Disk image path
    pub disk_path: Option<PathBuf>,
    
    /// Network configuration
    pub network: NetworkConfig,
    
    /// Autostart on hypervisor boot
    pub autostart: bool,
}

impl VmDefinition {
    /// Create a new VM definition
    pub fn new(name: impl Into<String>, vcpu_count: u32, memory_mb: u64) -> Self {
        Self {
            name: name.into(),
            vcpu_count,
            memory_mb,
            disk_path: None,
            network: NetworkConfig::default(),
            autostart: false,
        }
    }
    
    /// Set disk path
    pub fn with_disk(mut self, path: PathBuf) -> Self {
        self.disk_path = Some(path);
        self
    }
    
    /// Set network configuration
    pub fn with_network(mut self, network: NetworkConfig) -> Self {
        self.network = network;
        self
    }
    
    /// Enable autostart
    pub fn with_autostart(mut self, autostart: bool) -> Self {
        self.autostart = autostart;
        self
    }
    
    /// Validate VM definition
    pub fn validate(&self) -> Result<()> {
        if self.vcpu_count == 0 {
            anyhow::bail!("vCPU count must be greater than 0");
        }
        
        if self.memory_mb == 0 {
            anyhow::bail!("Memory size must be greater than 0");
        }
        
        if self.memory_mb < 64 {
            anyhow::bail!("Memory size must be at least 64 MB");
        }
        
        Ok(())
    }
}

/// Network configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkConfig {
    /// Network name
    pub network_name: String,
    
    /// MAC address (optional)
    pub mac_address: Option<String>,
    
    /// Network mode
    pub mode: NetworkMode,
}

impl Default for NetworkConfig {
    fn default() -> Self {
        Self {
            network_name: "default".to_string(),
            mac_address: None,
            mode: NetworkMode::Nat,
        }
    }
}

/// Network mode
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum NetworkMode {
    /// NAT networking
    Nat,
    
    /// Bridged networking
    Bridge,
    
    /// Host-only networking
    HostOnly,
}

/// VM handle for running instances
pub struct VmHandle {
    pub definition: VmDefinition,
    pub state: VmState,
}

impl VmHandle {
    /// Create a new VM handle
    pub fn new(definition: VmDefinition) -> Self {
        info!("Creating VM handle for '{}'", definition.name);
        
        Self {
            definition,
            state: VmState::Stopped,
        }
    }
    
    /// Start the VM
    pub fn start(&mut self) -> Result<()> {
        info!("Starting VM '{}'", self.definition.name);
        
        self.definition.validate()?;
        
        // In a real implementation:
        // 1. Create KVM VM
        // 2. Set up memory regions
        // 3. Create vCPUs
        // 4. Load kernel/initrd
        // 5. Start vCPU threads
        
        self.state = VmState::Running;
        
        info!("VM '{}' started successfully", self.definition.name);
        
        Ok(())
    }
    
    /// Stop the VM
    pub fn stop(&mut self) -> Result<()> {
        info!("Stopping VM '{}'", self.definition.name);
        
        // In a real implementation:
        // 1. Send shutdown signal to guest
        // 2. Wait for graceful shutdown
        // 3. Force stop if timeout
        // 4. Clean up resources
        
        self.state = VmState::Stopped;
        
        info!("VM '{}' stopped", self.definition.name);
        
        Ok(())
    }
    
    /// Get VM state
    pub fn state(&self) -> VmState {
        self.state
    }
}

/// VM state
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum VmState {
    /// VM is stopped
    Stopped,
    
    /// VM is starting
    Starting,
    
    /// VM is running
    Running,
    
    /// VM is paused
    Paused,
    
    /// VM is stopping
    Stopping,
    
    /// VM encountered an error
    Error,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vm_definition_creation() {
        let vm = VmDefinition::new("test-vm", 2, 4096);
        assert_eq!(vm.name, "test-vm");
        assert_eq!(vm.vcpu_count, 2);
        assert_eq!(vm.memory_mb, 4096);
    }

    #[test]
    fn test_vm_definition_validation() {
        let valid_vm = VmDefinition::new("test", 2, 512);
        assert!(valid_vm.validate().is_ok());
        
        let invalid_vm = VmDefinition::new("test", 0, 512);
        assert!(invalid_vm.validate().is_err());
        
        let too_small = VmDefinition::new("test", 2, 32);
        assert!(too_small.validate().is_err());
    }

    #[test]
    fn test_vm_handle_lifecycle() {
        let vm_def = VmDefinition::new("test-vm", 2, 512);
        let mut handle = VmHandle::new(vm_def);
        
        assert_eq!(handle.state(), VmState::Stopped);
        
        handle.start().unwrap();
        assert_eq!(handle.state(), VmState::Running);
        
        handle.stop().unwrap();
        assert_eq!(handle.state(), VmState::Stopped);
    }
}
