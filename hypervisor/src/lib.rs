// lib.rs
// Main library entry point for SAGCO Hypervisor Core

// Allow macro_use for lazy_static
#[allow(unused_imports)]
#[macro_use]
extern crate lazy_static;

pub mod hv_api;

// Re-export the main API types and functions
pub use hv_api::{
    HvResult,
    HvVmConfig,
    hv_init,
    hv_shutdown,
    hv_create_vm,
    hv_start_vm,
    hv_stop_vm,
    hv_destroy_vm,
};
