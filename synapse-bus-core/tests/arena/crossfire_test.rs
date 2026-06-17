// Arena Tests - Crossfire Test Harness

#[cfg(test)]
mod tests {
    use synapse_bus_core::immune_system::red_team::crossfire::CrossfireArena;

    #[test]
    fn arena_generate_100_vectors() {
        let mut arena = CrossfireArena::new();
        arena.generate_vectors(100);
        assert_eq!(arena.count(), 100);
    }
}
