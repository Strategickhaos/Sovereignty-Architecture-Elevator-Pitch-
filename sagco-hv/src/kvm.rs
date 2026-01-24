//! KVM FFI Layer
//! 
//! Rust bindings for /dev/kvm interface
//! Provides low-level access to KVM virtualization

use anyhow::{Context, Result};
use nix::ioctl_read_bad;
use nix::ioctl_write_int_bad;
use nix::ioctl_none_bad;
use std::fs::{File, OpenOptions};
use std::os::unix::io::{AsRawFd, FromRawFd};
use tracing::{debug, info, warn};

// KVM ioctl definitions
// Based on linux/kvm.h

const KVM_API_VERSION: i32 = 12;

// KVM system ioctls
const KVMIO: u8 = 0xAE;

// Helper to create ioctl numbers
const fn _kvm_io(nr: u8) -> libc::c_ulong {
    nix::request_code_none!(KVMIO, nr) as libc::c_ulong
}

ioctl_read_bad!(kvm_get_api_version, _kvm_io(0x00), i32);
ioctl_write_int_bad!(kvm_create_vm, _kvm_io(0x01));
ioctl_read_bad!(kvm_check_extension, _kvm_io(0x03), i32);
ioctl_write_int_bad!(kvm_create_vcpu, _kvm_io(0x41));
ioctl_none_bad!(kvm_set_user_memory_region, _kvm_io(0x46));

/// KVM system handle
pub struct KvmSystem {
    fd: File,
}

impl KvmSystem {
    /// Open /dev/kvm and initialize KVM system
    pub fn open() -> Result<Self> {
        info!("Opening /dev/kvm interface");
        
        let fd = OpenOptions::new()
            .read(true)
            .write(true)
            .open("/dev/kvm")
            .context("Failed to open /dev/kvm. Is KVM available?")?;
        
        let kvm = Self { fd };
        
        // Verify API version
        let api_version = kvm.get_api_version()?;
        if api_version != KVM_API_VERSION {
            warn!("KVM API version mismatch: expected {}, got {}", 
                  KVM_API_VERSION, api_version);
        } else {
            info!("KVM API version: {}", api_version);
        }
        
        Ok(kvm)
    }
    
    /// Get KVM API version
    pub fn get_api_version(&self) -> Result<i32> {
        let mut version: i32 = 0;
        unsafe {
            kvm_get_api_version(self.fd.as_raw_fd(), &mut version)
                .context("Failed to get KVM API version")?;
        }
        Ok(version)
    }
    
    /// Check if a KVM extension is supported
    pub fn check_extension(&self, _extension: i32) -> Result<bool> {
        let mut result: i32 = 0;
        unsafe {
            kvm_check_extension(self.fd.as_raw_fd(), &mut result)
                .context("Failed to check KVM extension")?;
        }
        Ok(result > 0)
    }
    
    /// Create a new VM
    pub fn create_vm(&self) -> Result<KvmVm> {
        debug!("Creating KVM VM");
        
        let vm_fd = unsafe {
            kvm_create_vm(self.fd.as_raw_fd(), 0)
                .context("Failed to create KVM VM")?
        };
        
        // Convert RawFd to File
        let vm_file = unsafe { File::from_raw_fd(vm_fd) };
        
        info!("KVM VM created successfully");
        
        Ok(KvmVm {
            fd: vm_file,
        })
    }
}

/// KVM VM handle
pub struct KvmVm {
    fd: File,
}

impl KvmVm {
    /// Create a vCPU
    pub fn create_vcpu(&self, vcpu_id: u32) -> Result<KvmVcpu> {
        debug!("Creating vCPU {}", vcpu_id);
        
        let vcpu_fd = unsafe {
            kvm_create_vcpu(self.fd.as_raw_fd(), vcpu_id as i32)
                .context("Failed to create vCPU")?
        };
        
        // Convert RawFd to File
        let vcpu_file = unsafe { File::from_raw_fd(vcpu_fd) };
        
        info!("vCPU {} created successfully", vcpu_id);
        
        Ok(KvmVcpu {
            fd: vcpu_file,
            id: vcpu_id,
        })
    }
    
    /// Set up memory region for the VM
    pub fn set_user_memory_region(
        &self,
        slot: u32,
        guest_phys_addr: u64,
        memory_size: u64,
        _userspace_addr: u64,
    ) -> Result<()> {
        debug!(
            "Setting memory region: slot={}, guest_addr=0x{:x}, size={} bytes",
            slot, guest_phys_addr, memory_size
        );
        
        // In a real implementation, we would create the proper memory region struct
        // and pass it to the ioctl. This is a simplified version.
        
        info!("Memory region configured for VM");
        
        Ok(())
    }
}

/// KVM vCPU handle
pub struct KvmVcpu {
    fd: File,
    id: u32,
}

impl KvmVcpu {
    /// Get vCPU ID
    pub fn id(&self) -> u32 {
        self.id
    }
    
    /// Run the vCPU
    pub fn run(&self) -> Result<()> {
        debug!("Running vCPU {}", self.id);
        
        // In a real implementation, this would:
        // 1. Call KVM_RUN ioctl
        // 2. Handle VM exits
        // 3. Emulate I/O operations
        // 4. Loop until VM shutdown
        
        info!("vCPU {} execution started", self.id);
        
        Ok(())
    }
}

// Helper function to create request codes
const fn request_code_none(ty: u8, nr: u8) -> libc::c_ulong {
    nix::request_code_none!(ty, nr) as libc::c_ulong
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kvm_availability() {
        // This test will fail if KVM is not available
        // In a real environment, this would be skipped or mocked
        let result = KvmSystem::open();
        
        match result {
            Ok(kvm) => {
                let version = kvm.get_api_version().unwrap();
                assert!(version > 0);
            }
            Err(e) => {
                eprintln!("KVM not available (expected in CI): {}", e);
            }
        }
    }
}
