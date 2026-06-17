// Main Binary Entry Point
// Synapse-Bus-Core Daemon

use synapse_bus_core::*;
use tracing::{info, warn};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt()
        .with_env_filter("synapse_bus_core=info")
        .init();

    info!("🧠 Synapse-Bus-Core v{}", VERSION);
    info!("📡 {}", VERSION_TAG);
    info!("");
    info!("⚡ Axioms:");
    info!("  • {}", axioms::SOVEREIGNTY);
    info!("  • {}", axioms::TRUE_FIRST);
    info!("  • {}", axioms::BIO_MIMETIC);
    info!("");

    // Initialize the nervous system
    info!("🔌 Initializing Nervous System...");
    let bus = nervous_system::SynapseBus::new().await?;
    
    info!("✅ Synapse-Bus Online");
    info!("🌡️  Homeostasis: STABLE");
    info!("🛡️  Immune System: ACTIVE");
    info!("");
    
    warn!("⚠️  Alpha Release - Event Horizon");
    warn!("   Use in production at your own risk");

    // Run the event loop
    bus.run().await?;

    Ok(())
}
