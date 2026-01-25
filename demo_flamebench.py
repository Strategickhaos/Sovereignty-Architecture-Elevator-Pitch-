#!/usr/bin/env python3
"""
Quick demo script for FlameBench
Shows how to use flamebench.py with local test examples
"""

import os
import sys
import shutil
from pathlib import Path

def setup_demo():
    """Setup demo environment with example gists"""
    print("🔥 Setting up FlameBench demo environment...\n")
    
    # Create bench_cache directory
    cache_dir = Path("bench_cache")
    cache_dir.mkdir(exist_ok=True)
    
    # Copy example gists to cache
    examples = [
        ("3_1-max-of-two", "zyb-it145-ch3-3_1-max-of-two"),
        ("3_3-age-category", "zyb-it145-ch3-3_3-age-category"),
    ]
    
    for example_name, cache_name in examples:
        src = Path(f"gist_examples/{example_name}")
        dst = cache_dir / cache_name
        
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"✓ Copied {example_name} -> {cache_name}")
        else:
            print(f"⚠ Example not found: {src}")
    
    print("\n📂 Demo environment ready!\n")

def run_demo():
    """Run FlameBench demo"""
    print("=" * 60)
    print("Running FlameBench...")
    print("=" * 60)
    print()
    
    # Import and run flamebench
    import flamebench
    result = flamebench.main()
    
    if result == 0:
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        print("=" * 60)
        print("\n📋 Check these files:")
        print("  • results.json - Test results in JSON format")
        print("  • bench_cache/ - Cached gist files")
        print("\n📖 Next steps:")
        print("  1. Review FLAMEBENCH_README.md for full documentation")
        print("  2. Read GIST_CREATION_GUIDE.md to create your own gists")
        print("  3. Update GITHUB_USER in flamebench.py to your username")
        print("  4. Create actual GitHub gists for auto-discovery")
        print("\n🔥 FlameBench demo complete!")
    else:
        print("\n⚠ Demo encountered issues")
        return 1
    
    return 0

def cleanup_demo():
    """Clean up demo artifacts"""
    print("\n🧹 Cleaning up demo artifacts...")
    
    artifacts = ["bench_cache", "results.json"]
    for artifact in artifacts:
        path = Path(artifact)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"  ✓ Removed {artifact}")
    
    print("✨ Cleanup complete!\n")

def main():
    """Main demo runner"""
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║          🔥 FlameBench Demo & Quick Start 🔥          ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    print("This demo will:")
    print("  1. Set up example gist capsules locally")
    print("  2. Run FlameBench to test them")
    print("  3. Show the results")
    print()
    
    input("Press Enter to start the demo...")
    print()
    
    try:
        # Setup
        setup_demo()
        
        # Run
        result = run_demo()
        
        # Offer cleanup
        print()
        try:
            cleanup = input("Remove demo artifacts? (y/N): ").strip().lower()
        except EOFError:
            cleanup = 'n'
        
        if cleanup == 'y':
            cleanup_demo()
        else:
            print("\n📁 Demo artifacts kept for inspection")
        
        return result
        
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
