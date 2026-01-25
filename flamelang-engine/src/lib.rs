use sagco_guardian::flamelang_bindings::EngineRegistrar;

/// FlameLang Engine for executing cognitive scripts
pub struct Engine {
    // Function registry would go here in a real implementation
    // For now, we keep it simple
}

impl Engine {
    pub fn new() -> Self {
        Self {}
    }
}

impl Default for Engine {
    fn default() -> Self {
        Self::new()
    }
}

impl EngineRegistrar for Engine {
    fn register_fn<F>(&mut self, _name: &str, _func: F)
    where
        F: 'static,
    {
        // In a real implementation, this would store the function
        // in a registry (HashMap) for later invocation
        // For now, we just accept the registration
    }
}

/// Register all Guardian functions with the engine
pub fn register_all(engine: &mut Engine) {
    sagco_guardian::flamelang_bindings::register_guardian_functions(engine);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_engine_creation() {
        let _engine = Engine::new();
    }

    #[test]
    fn test_register_all() {
        let mut engine = Engine::new();
        register_all(&mut engine);
        // If this doesn't panic, registration worked
    }
}
