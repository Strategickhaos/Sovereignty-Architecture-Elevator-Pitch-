//! # Vision Organs: Reconnaissance
//!
//! - Retina (f.k.a. Nmap)
//! - Cochlea (f.k.a. Wireshark)
//! - Sonar (f.k.a. Masscan)
//! - Arachnid (f.k.a. Burp Suite)

pub mod retina;
pub mod cochlea;
pub mod sonar;
pub mod arachnid;

/// Register vision organs
pub async fn register() -> crate::error::Result<()> {
    tracing::info!("Registering vision organs");
    Ok(())
}
