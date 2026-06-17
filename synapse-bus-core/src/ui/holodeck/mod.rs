// Holodeck - INV-088: Real-time Render Engine

/// Holodeck render engine
pub struct Holodeck {
    enabled: bool,
}

impl Holodeck {
    pub fn new() -> Self {
        Self { enabled: false }
    }

    pub fn enable(&mut self) {
        self.enabled = true;
    }

    pub fn render(&self, scene: &str) -> String {
        if !self.enabled {
            return "Holodeck disabled".to_string();
        }
        format!("Rendering scene: {}", scene)
    }
}

impl Default for Holodeck {
    fn default() -> Self {
        Self::new()
    }
}
