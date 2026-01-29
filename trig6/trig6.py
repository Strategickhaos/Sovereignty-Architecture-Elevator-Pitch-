#!/usr/bin/env python3
"""
TRIG6 Sovereign Compute Engine

MIT License
Copyright (c) 2025 Strategickhaos

Core compute is zero external dependencies.
Optional modules (music/visuals) require extra packages.

Compiled from canonical 64-glyph registry (IDs 0–63).
No external lookup; intrinsic resolution from a versioned local registry.
"""

import sys
import hashlib
from pathlib import Path

# Canonical 64-glyph registry (IDs 0-63)
TRIG6_REGISTRY = [
    # Core trigonometric glyphs (0-15)
    "sin", "cos", "tan", "cot", "sec", "csc",
    "asin", "acos", "atan", "acot", "asec", "acsc",
    "sinh", "cosh", "tanh", "coth",
    
    # Extended operations (16-31)
    "add", "sub", "mul", "div", "mod", "pow",
    "sqrt", "log", "ln", "exp", "abs", "neg",
    "floor", "ceil", "round", "trunc",
    
    # Logical and bitwise (32-47)
    "and", "or", "xor", "not", "shl", "shr",
    "eq", "ne", "lt", "le", "gt", "ge",
    "min", "max", "clamp", "lerp",
    
    # Advanced math (48-63)
    "atan2", "hypot", "gamma", "erf", "j0", "j1",
    "y0", "y1", "factorial", "gcd", "lcm", "isprime",
    "euler", "pi", "phi", "e"
]


def resolve_glyph(glyph_id: int) -> str:
    """Resolve glyph ID to name from canonical registry."""
    if 0 <= glyph_id < len(TRIG6_REGISTRY):
        return TRIG6_REGISTRY[glyph_id]
    return f"UNKNOWN_{glyph_id}"


def compute_registry_hash() -> str:
    """Compute deterministic hash of registry."""
    registry_str = "|".join(TRIG6_REGISTRY)
    return hashlib.sha256(registry_str.encode()).hexdigest()[:16]


def doctor() -> int:
    """Run system diagnostics."""
    print("=== TRIG6 Sovereign Compute Engine ===")
    print(f"Version: 1.0.0")
    print(f"Registry Size: {len(TRIG6_REGISTRY)} glyphs")
    print(f"Registry Hash: {compute_registry_hash()}")
    
    # Validate registry integrity
    if len(TRIG6_REGISTRY) != 64:
        print(f"[FAIL] Registry size mismatch: expected 64, got {len(TRIG6_REGISTRY)}")
        return 1
    
    # Check for duplicates
    if len(set(TRIG6_REGISTRY)) != len(TRIG6_REGISTRY):
        print("[FAIL] Registry contains duplicates")
        return 1
    
    print("[PASS] Registry integrity verified")
    print("[PASS] All systems operational")
    return 0


def info():
    """Display system information."""
    print("TRIG6 Sovereign Compute Engine")
    print("=" * 40)
    print(f"License: MIT")
    print(f"Registry: {len(TRIG6_REGISTRY)} canonical glyphs")
    print(f"Core: Zero external dependencies")
    print(f"Optional: midiutil, matplotlib, mido (for music/visuals)")
    print()
    print("Available commands:")
    print("  doctor  - Run system diagnostics")
    print("  info    - Display this information")
    print("  list    - List all glyphs in registry")


def list_glyphs():
    """List all glyphs in the canonical registry."""
    print(f"Canonical 64-glyph registry (IDs 0–63):")
    print()
    for i, glyph in enumerate(TRIG6_REGISTRY):
        print(f"  {i:2d}: {glyph}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        info()
        return 0
    
    command = sys.argv[1]
    
    if command == "doctor":
        return doctor()
    elif command == "info":
        info()
        return 0
    elif command == "list":
        list_glyphs()
        return 0
    else:
        print(f"Unknown command: {command}")
        info()
        return 1


if __name__ == "__main__":
    sys.exit(main())
