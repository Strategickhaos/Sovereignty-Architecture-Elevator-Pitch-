# Synapse-Bus-Core Test Suite

This directory contains tests for the Synapse-Bus-Core system.

## Structure

- `sanity/` - Basic sanity checks and hallucination firewall
- `arena/` - Crossfire test harness for security testing

## Running Tests

```bash
# Run all tests
cargo test

# Run specific test module
cargo test --test sanity

# Run with output
cargo test -- --nocapture

# Run in parallel
cargo test -- --test-threads=4
```

## Test Categories

### Sanity Tests
- Spike creation and validation
- Physics gate functionality
- Homeostasis engine
- Dendrite network
- Reflex system

### Arena Tests
- Attack vector generation
- Immune system response
- Council ratification
- Organ functionality
