//! # Bio-Digital Primitives
//!
//! These are the fundamental building blocks mimicking cellular biology.

pub mod membrane;
pub mod nucleus;
pub mod crypto_cell;

pub use membrane::Membrane;
pub use nucleus::Nucleus;
pub use crypto_cell::CryptoCell;

// Placeholder files for buffer.flame and clamp.flame
// These would be FlameLang files in a full implementation
