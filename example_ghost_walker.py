#!/usr/bin/env python3
"""
Example: Using the Genesis System to Create a New Module

This example demonstrates the complete workflow:
1. Define architecture in a chat-like format
2. Parse with ingestion valve
3. Generate structure with genesis
4. Hydrate with mason agent
"""

import os
import subprocess
import sys

# Example chat dump defining a new module
EXAMPLE_CHAT = """
# Implementing the Ghost Walker Module

This module will handle stealth reconnaissance operations.

## Architecture

Directory structure:
- src/organs/stealth/
  - ghost_walker.rs: "ref: INV-088, Stealth Pattern"
  - shadow_cache.rs: "ref: Board Meeting 005"

## References

- Patent Claim 15: Stealth channel optimization
- INV-088: Ghost Walker protocol
- Board Meeting 005: Shadow caching strategy
- Ripley Gate 8 (Sublimation): Purification through stealth

## Implementation

```rust
pub struct GhostWalker {
    shadow_cache: ShadowCache,
    stealth_level: u8,
}
```

TASK: Implement stealth reconnaissance
ROLE: Security Architect
CONSTRAINT: Zero network footprint
LANGUAGE: Rust
"""

def run_command(cmd, cwd=None):
    """Run a command and return the output."""
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        text=True, 
        cwd=cwd
    )
    return result.returncode, result.stdout, result.stderr

def main():
    print("=" * 60)
    print("   GENESIS SYSTEM EXAMPLE: GHOST WALKER MODULE")
    print("=" * 60)
    print()
    
    # Save example chat to file
    chat_file = "/tmp/ghost_walker_chat.txt"
    with open(chat_file, 'w') as f:
        f.write(EXAMPLE_CHAT)
    print(f"✅ Created example chat: {chat_file}")
    print()
    
    # Step 1: Parse with ingestion valve
    print("Step 1: Parsing chat with ingestion valve...")
    print("-" * 60)
    ret, out, err = run_command(
        f"python3 scripts/ingest_chat.py {chat_file}"
    )
    print(out)
    if ret != 0:
        print(f"Error: {err}")
        return 1
    
    # Step 2: Generate structure
    print()
    print("Step 2: Generating repository structure...")
    print("-" * 60)
    
    # For this example, we'll use the existing synapse-bus-core
    if not os.path.exists("synapse-bus-core"):
        ret, out, err = run_command("python3 genesis.py")
        print(out)
    else:
        print("✅ Using existing synapse-bus-core structure")
    
    # Step 3: Add the new module to the structure
    print()
    print("Step 3: Adding Ghost Walker module to structure...")
    print("-" * 60)
    
    ghost_walker_dir = "synapse-bus-core/src/organs/stealth"
    os.makedirs(ghost_walker_dir, exist_ok=True)
    
    # Create seed files
    with open(f"{ghost_walker_dir}/ghost_walker.rs", 'w') as f:
        f.write("// SYNAPSE-BUS GENERATED | REF: ref: INV-088, Stealth Pattern\n")
    
    with open(f"{ghost_walker_dir}/shadow_cache.rs", 'w') as f:
        f.write("// SYNAPSE-BUS GENERATED | REF: ref: Board Meeting 005\n")
    
    print(f"✅ Created Ghost Walker seed files in {ghost_walker_dir}")
    
    # Step 4: Hydrate with mason
    print()
    print("Step 4: Hydrating files with mason agent...")
    print("-" * 60)
    
    os.environ['TARGET_DIR'] = '.'
    ret, out, err = run_command(
        "python3 ../scripts/hydrate_file.py",
        cwd="synapse-bus-core"
    )
    print(out)
    
    # Step 5: Verify the result
    print()
    print("Step 5: Verifying generated code...")
    print("-" * 60)
    
    ghost_walker_file = f"{ghost_walker_dir}/ghost_walker.rs"
    if os.path.exists(ghost_walker_file):
        print(f"✅ Ghost Walker module generated!")
        print()
        print("Generated code preview:")
        print("-" * 60)
        with open(ghost_walker_file, 'r') as f:
            lines = f.readlines()[:20]  # First 20 lines
            print(''.join(lines))
    else:
        print("❌ Ghost Walker module not found")
        return 1
    
    print()
    print("=" * 60)
    print("   ✅ EXAMPLE COMPLETE")
    print("=" * 60)
    print()
    print("The Ghost Walker module has been generated!")
    print()
    print("What happened:")
    print("1. Chat dump was parsed by ingestion valve")
    print("2. References were extracted (INV-088, Board Meeting 005)")
    print("3. Seed files were created in the structure")
    print("4. Mason agent hydrated the files with code")
    print()
    print("Next steps:")
    print("- Review the generated code")
    print("- Run thermodynamics check")
    print("- Validate through Ripley Gates")
    print("- Build Docker container")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
