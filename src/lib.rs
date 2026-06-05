pub mod claims;
pub mod primitives;
pub mod homeostasis;
pub mod nervous_system;
pub mod council;
pub mod immune_system;
pub mod organs;
pub mod infra;
pub mod ui;

pub type Result<T> = core::result::Result<T, crate::primitives::error::SynapseError>;
