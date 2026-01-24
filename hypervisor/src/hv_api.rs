// src/hv_api.rs
// Rust FFI implementation of the hypervisor API
// This exposes C-compatible functions for FlameLang to call

use std::ffi::CStr;
use std::os::raw::c_char;
use std::collections::HashMap;
use std::sync::Mutex;

// Allow non-camel-case for C FFI compatibility
#[allow(non_camel_case_types)]
#[repr(C)]
pub enum HvResult {
    HV_OK = 0,
    HV_ERR_INIT = 1,
    HV_ERR_CREATE = 2,
    HV_ERR_START = 3,
    HV_ERR_STOP = 4,
    HV_ERR_DESTROY = 5,
    HV_ERR_INVALID = 6,
}

#[repr(C)]
pub struct HvVmConfig {
    pub name: *const c_char,
    pub disk_path: *const c_char,
    pub kernel_path: *const c_char,
    pub cmdline: *const c_char,
    pub mem_mb: u32,
    pub vcpus: u32,
    pub flags: u32,
}

// Super simple in-memory registry for now
// TODO: Replace with actual KVM file descriptor management
#[allow(dead_code)]
struct VmHandle {
    name: String,
    mem_mb: u32,
    vcpus: u32,
    disk_path: String,
    kernel_path: String,
    cmdline: String,
    // Future fields:
    // kvm_fd: RawFd,
    // vm_fd: RawFd,
    // vcpu_fds: Vec<RawFd>,
}

lazy_static::lazy_static! {
    static ref HV_VMS: Mutex<HashMap<String, VmHandle>> = Mutex::new(HashMap::new());
    static ref HV_INITIALIZED: Mutex<bool> = Mutex::new(false);
}

#[no_mangle]
pub extern "C" fn hv_init() -> HvResult {
    // Open /dev/kvm, sanity-check KVM API version, etc.
    // For Phase 1: Just mark as initialized
    
    let mut initialized = HV_INITIALIZED.lock().unwrap();
    if *initialized {
        eprintln!("Warning: hv_init called multiple times");
        return HvResult::HV_OK;
    }
    
    // TODO: Real KVM initialization:
    // 1. Open /dev/kvm
    // 2. Check KVM_API_VERSION with KVM_GET_API_VERSION ioctl
    // 3. Verify required extensions are available
    
    *initialized = true;
    println!("🔥 SAGCO Hypervisor initialized (Phase 1 - Stub Mode)");
    HvResult::HV_OK
}

#[no_mangle]
pub extern "C" fn hv_shutdown() -> HvResult {
    // Clean up any global resources
    let mut vms = HV_VMS.lock().unwrap();
    
    if !vms.is_empty() {
        eprintln!("Warning: {} VMs still exist during shutdown", vms.len());
    }
    
    vms.clear();
    
    let mut initialized = HV_INITIALIZED.lock().unwrap();
    *initialized = false;
    
    println!("🔥 SAGCO Hypervisor shutdown complete");
    HvResult::HV_OK
}

#[no_mangle]
pub extern "C" fn hv_create_vm(cfg: *const HvVmConfig) -> HvResult {
    if cfg.is_null() {
        eprintln!("Error: NULL configuration passed to hv_create_vm");
        return HvResult::HV_ERR_INVALID;
    }

    let cfg = unsafe { &*cfg };

    // Check initialization
    let initialized = HV_INITIALIZED.lock().unwrap();
    if !*initialized {
        eprintln!("Error: hv_create_vm called before hv_init");
        return HvResult::HV_ERR_INIT;
    }
    drop(initialized);

    // Extract C strings safely
    if cfg.name.is_null() || cfg.disk_path.is_null() {
        eprintln!("Error: name or disk_path is NULL");
        return HvResult::HV_ERR_INVALID;
    }

    let name = unsafe { CStr::from_ptr(cfg.name) }.to_string_lossy().into_owned();
    let disk = unsafe { CStr::from_ptr(cfg.disk_path) }.to_string_lossy().into_owned();
    
    // kernel_path and cmdline are optional
    let kernel = if cfg.kernel_path.is_null() {
        String::new()
    } else {
        unsafe { CStr::from_ptr(cfg.kernel_path) }.to_string_lossy().into_owned()
    };
    
    let cmdline = if cfg.cmdline.is_null() {
        String::new()
    } else {
        unsafe { CStr::from_ptr(cfg.cmdline) }.to_string_lossy().into_owned()
    };

    println!("🔥 Creating VM: {}", name);
    println!("   Memory: {} MB", cfg.mem_mb);
    println!("   vCPUs: {}", cfg.vcpus);
    println!("   Disk: {}", disk);
    if !kernel.is_empty() {
        println!("   Kernel: {}", kernel);
    }
    if !cmdline.is_empty() {
        println!("   Cmdline: {}", cmdline);
    }

    // TODO: Real KVM wiring here (Phase 2+)
    // 1. Open /dev/kvm (if not already open)
    // 2. KVM_CREATE_VM ioctl to get VM fd
    // 3. Allocate guest memory (cfg.mem_mb MB)
    // 4. Set up memory regions with KVM_SET_USER_MEMORY_REGION
    // 5. Load kernel/disk image into guest memory
    // 6. Create vCPUs with KVM_CREATE_VCPU
    // 7. Set up vCPU registers and initial state

    let mut map = HV_VMS.lock().unwrap();
    
    if map.contains_key(&name) {
        eprintln!("Error: VM '{}' already exists", name);
        return HvResult::HV_ERR_CREATE;
    }
    
    map.insert(name.clone(), VmHandle {
        name: name.clone(),
        mem_mb: cfg.mem_mb,
        vcpus: cfg.vcpus,
        disk_path: disk,
        kernel_path: kernel,
        cmdline,
    });

    println!("✅ VM '{}' created successfully", name);
    HvResult::HV_OK
}

#[no_mangle]
pub extern "C" fn hv_start_vm(name: *const c_char) -> HvResult {
    if name.is_null() {
        eprintln!("Error: NULL name passed to hv_start_vm");
        return HvResult::HV_ERR_INVALID;
    }
    
    let name_str = unsafe { CStr::from_ptr(name) }.to_string_lossy().into_owned();

    let map = HV_VMS.lock().unwrap();
    
    if !map.contains_key(&name_str) {
        eprintln!("Error: VM '{}' not found", name_str);
        return HvResult::HV_ERR_INVALID;
    }
    
    println!("🚀 Starting VM: {}", name_str);
    
    // TODO: Real KVM execution (Phase 2+)
    // 1. For each vCPU:
    //    - Create thread
    //    - Enter KVM_RUN loop
    //    - Handle VM exits (MMIO, IO, HLT, etc.)
    // 2. Set up signal handling for graceful shutdown
    // 3. Monitor VM state and handle events
    
    println!("✅ VM '{}' started (stub mode - not actually running)", name_str);
    
    HvResult::HV_OK
}

#[no_mangle]
pub extern "C" fn hv_stop_vm(name: *const c_char) -> HvResult {
    if name.is_null() {
        eprintln!("Error: NULL name passed to hv_stop_vm");
        return HvResult::HV_ERR_INVALID;
    }
    
    let name_str = unsafe { CStr::from_ptr(name) }.to_string_lossy().into_owned();

    let map = HV_VMS.lock().unwrap();
    
    if !map.contains_key(&name_str) {
        eprintln!("Error: VM '{}' not found", name_str);
        return HvResult::HV_ERR_INVALID;
    }
    
    println!("🛑 Stopping VM: {}", name_str);
    
    // TODO: Real KVM stop (Phase 2+)
    // 1. Signal vCPU threads to exit KVM_RUN loop
    // 2. Wait for threads to terminate
    // 3. Clean up resources
    
    println!("✅ VM '{}' stopped", name_str);
    
    HvResult::HV_OK
}

#[no_mangle]
pub extern "C" fn hv_destroy_vm(name: *const c_char) -> HvResult {
    if name.is_null() {
        eprintln!("Error: NULL name passed to hv_destroy_vm");
        return HvResult::HV_ERR_INVALID;
    }
    
    let name_str = unsafe { CStr::from_ptr(name) }.to_string_lossy().into_owned();

    let mut map = HV_VMS.lock().unwrap();
    
    if !map.contains_key(&name_str) {
        eprintln!("Error: VM '{}' not found", name_str);
        return HvResult::HV_ERR_INVALID;
    }
    
    println!("💥 Destroying VM: {}", name_str);
    
    // TODO: Real cleanup (Phase 2+)
    // 1. Ensure VM is stopped
    // 2. Close vCPU file descriptors
    // 3. Close VM file descriptor
    // 4. Free guest memory
    // 5. Clean up any other resources
    
    map.remove(&name_str);
    
    println!("✅ VM '{}' destroyed", name_str);
    
    HvResult::HV_OK
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::ffi::CString;

    #[test]
    fn test_init_shutdown() {
        let result = hv_init();
        assert!(matches!(result, HvResult::HV_OK));
        
        let result = hv_shutdown();
        assert!(matches!(result, HvResult::HV_OK));
    }

    #[test]
    fn test_create_vm() {
        hv_init();
        
        let name = CString::new("test_vm").unwrap();
        let disk = CString::new("/tmp/test.iso").unwrap();
        let kernel = CString::new("/boot/vmlinuz").unwrap();
        let cmdline = CString::new("console=ttyS0").unwrap();
        
        let cfg = HvVmConfig {
            name: name.as_ptr(),
            disk_path: disk.as_ptr(),
            kernel_path: kernel.as_ptr(),
            cmdline: cmdline.as_ptr(),
            mem_mb: 512,
            vcpus: 2,
            flags: 0,
        };
        
        let result = hv_create_vm(&cfg);
        assert!(matches!(result, HvResult::HV_OK));
        
        hv_shutdown();
    }

    #[test]
    fn test_vm_lifecycle() {
        hv_init();
        
        let name = CString::new("lifecycle_vm").unwrap();
        let disk = CString::new("/tmp/test.iso").unwrap();
        
        let cfg = HvVmConfig {
            name: name.as_ptr(),
            disk_path: disk.as_ptr(),
            kernel_path: std::ptr::null(),
            cmdline: std::ptr::null(),
            mem_mb: 256,
            vcpus: 1,
            flags: 0,
        };
        
        // Create
        let result = hv_create_vm(&cfg);
        assert!(matches!(result, HvResult::HV_OK));
        
        // Start
        let result = hv_start_vm(name.as_ptr());
        assert!(matches!(result, HvResult::HV_OK));
        
        // Stop
        let result = hv_stop_vm(name.as_ptr());
        assert!(matches!(result, HvResult::HV_OK));
        
        // Destroy
        let result = hv_destroy_vm(name.as_ptr());
        assert!(matches!(result, HvResult::HV_OK));
        
        hv_shutdown();
    }
}
