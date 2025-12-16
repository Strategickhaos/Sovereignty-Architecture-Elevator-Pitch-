//! # Organs: The Purified Tool Arsenal
//!
//! 16 organs rebuilt from standard security tools.

pub mod vision;
pub mod touch;
pub mod speech;
pub mod immune;

/// Register all organs with the system
pub async fn register_all_organs() -> crate::error::Result<()> {
    tracing::info!("Registering all 16 organs");
    
    vision::register().await?;
    touch::register().await?;
    speech::register().await?;
    immune::register().await?;
    
    Ok(())
}
