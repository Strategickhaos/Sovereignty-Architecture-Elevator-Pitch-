#!/usr/bin/env python3
"""
TRIG6 Pack Validator and Demo

This script validates the TRIG6 constants pack configuration and demonstrates
how to load and use the domain constants.
"""

import json
import sys
from pathlib import Path


def load_pack(pack_file="trig6-pack.json"):
    """Load and validate the main pack configuration."""
    try:
        with open(pack_file, 'r') as f:
            pack = json.load(f)
        print(f"✓ Loaded pack: {pack['metadata']['pack_name']} v{pack['metadata']['version']}")
        return pack
    except Exception as e:
        print(f"✗ Error loading pack: {e}")
        sys.exit(1)


def validate_domain_files(pack):
    """Validate that all domain constant files exist and are valid JSON."""
    print("\n" + "="*60)
    print("DOMAIN VALIDATION")
    print("="*60)
    
    all_valid = True
    for domain_name, domain_config in pack['domains'].items():
        constants_file = domain_config['constants_file']
        enabled = domain_config['enabled']
        status = "ENABLED" if enabled else "DISABLED"
        
        print(f"\n{domain_name.upper()} [{status}]")
        print(f"  Description: {domain_config['description']}")
        
        if not enabled and 'gate_reason' in domain_config:
            print(f"  ⚠️  GATED: {domain_config['gate_reason']}")
            print(f"  🔓 Unlock with: {domain_config.get('unlock_flag', 'N/A')}")
        
        # Validate file exists
        file_path = Path(constants_file)
        if not file_path.exists():
            print(f"  ✗ File not found: {constants_file}")
            all_valid = False
            continue
        
        # Validate JSON
        try:
            with open(file_path, 'r') as f:
                constants = json.load(f)
            print(f"  ✓ Valid JSON: {constants_file}")
            
            # Show some statistics
            if 'constants' in constants:
                const_count = len(constants['constants'])
                print(f"  📊 Contains {const_count} constant groups")
            
            if 'provenance' in constants:
                prov = constants['provenance']
                print(f"  📝 Verified by: {prov.get('verified_by', 'N/A')}")
                
        except json.JSONDecodeError as e:
            print(f"  ✗ Invalid JSON: {e}")
            all_valid = False
        except Exception as e:
            print(f"  ✗ Error: {e}")
            all_valid = False
    
    return all_valid


def demonstrate_usage(pack):
    """Demonstrate how to use the constants."""
    print("\n" + "="*60)
    print("USAGE DEMONSTRATION")
    print("="*60)
    
    # Example 1: Load rope constants
    print("\nExample 1: Loading Rope Access Constants")
    print("-" * 40)
    rope_file = pack['domains']['rope']['constants_file']
    with open(rope_file, 'r') as f:
        rope = json.load(f)
    
    safety_factors = rope['constants']['safety_factors']
    print(f"Static Line Safety Factor: {safety_factors['static_line']}")
    print(f"Dynamic Line Safety Factor: {safety_factors['dynamic_line']}")
    print(f"Anchor Point Safety Factor: {safety_factors['anchor_point']}")
    
    # Example 2: Check gated domain
    print("\nExample 2: Checking Gated Domain")
    print("-" * 40)
    ndt_config = pack['domains']['ndt']
    if not ndt_config['enabled']:
        print(f"⚠️  NDT domain is GATED")
        print(f"Reason: {ndt_config['gate_reason']}")
        print(f"To enable: {ndt_config['unlock_flag']}")
    
    # Example 3: Load KHAOS glyphs
    print("\nExample 3: Loading KHAOS Symbolic Constants")
    print("-" * 40)
    khaos_file = pack['domains']['khaos']['constants_file']
    with open(khaos_file, 'r') as f:
        khaos = json.load(f)
    
    glyphs = khaos['constants']['glyph_mappings']
    print("System Glyphs:")
    for name, info in list(glyphs.items())[:3]:
        print(f"  {info['symbol']} {name}: {info['meaning']}")


def validate_settings(pack):
    """Validate and display pack settings."""
    print("\n" + "="*60)
    print("PACK SETTINGS")
    print("="*60)
    
    settings = pack['settings']
    for setting, value in settings.items():
        status = "✓" if value else "✗"
        print(f"{status} {setting}: {value}")


def main():
    """Main validation and demonstration."""
    print("="*60)
    print("TRIG6 CONSTANTS PACK VALIDATOR")
    print("="*60)
    
    # Load pack
    pack = load_pack()
    
    # Display metadata
    print(f"\nOwner: {pack['metadata']['owner']}")
    print(f"Version: {pack['metadata']['version']}")
    print(f"Created: {pack['metadata']['created']}")
    print(f"Last Updated: {pack['metadata']['last_updated']}")
    
    # Validate domains
    valid = validate_domain_files(pack)
    
    # Validate settings
    validate_settings(pack)
    
    # Demonstrate usage
    demonstrate_usage(pack)
    
    # Final result
    print("\n" + "="*60)
    if valid:
        print("✓ VALIDATION SUCCESSFUL - All domains are properly configured")
        print("="*60)
        return 0
    else:
        print("✗ VALIDATION FAILED - Some domains have errors")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
