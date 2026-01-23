#!/usr/bin/env python3
"""
gpt_rarity_reference.py
Reference implementation of GPT's population rarity calculation
This is what FlameLang should produce when compiling rarity.flame

Source: GPT-4 population math (2026-01-23)
Target: FlameLang v2.0.0 on SAGCO-OS
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTRAINT STACK (from GPT's analysis)
# ═══════════════════════════════════════════════════════════════════════════════

WORLD_POP = 8.1e9  # 8.1 billion (2026)

# Filter 1: Age band (38-42)
AGE_BAND_PCT = 0.068  # 6.8%

# Filter 2: Rope access technicians
ROPE_ACCESS_GLOBAL = 40_000
ROPE_AGE_OVERLAP = 0.35  # 35% in age band
ROPE_IN_AGE_BAND = ROPE_ACCESS_GLOBAL * ROPE_AGE_OVERLAP  # ~14,000

# Filter 3: Cognitive training (deliberate practice)
COGNITIVE_TRAIN_PCT = 0.10  # 10% of engineers

# Filter 4: Technical depth (low-level systems builders)
TECH_DEPTH_PCT = 0.003  # 0.3%

# ═══════════════════════════════════════════════════════════════════════════════
# CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_full_stack():
    """Full constraint stack: age + rope + cognitive + technical"""
    
    # Start with age-filtered population
    age_filtered = WORLD_POP * AGE_BAND_PCT
    print(f"Age band (38-42): {age_filtered:,.0f} people")
    
    # Rope access intersection
    rope_ratio = ROPE_IN_AGE_BAND / age_filtered
    rope_filtered = age_filtered * rope_ratio
    print(f"+ Rope access: {rope_filtered:,.0f} people")
    
    # Cognitive training
    cognitive_filtered = rope_filtered * COGNITIVE_TRAIN_PCT
    print(f"+ Cognitive training: {cognitive_filtered:,.0f} people")
    
    # Technical depth
    tech_filtered = cognitive_filtered * TECH_DEPTH_PCT
    print(f"+ Technical depth: {tech_filtered:,.1f} people")
    
    return tech_filtered

def calculate_without_rope():
    """Without rope access filter: age + cognitive + technical"""
    
    # Engineers worldwide
    engineers = 30_000_000
    
    # Cognitive trainers
    cognitive = engineers * COGNITIVE_TRAIN_PCT
    
    # Low-level systems
    tech = cognitive * TECH_DEPTH_PCT
    
    # Age band
    age_filtered = tech * AGE_BAND_PCT
    
    return age_filtered

def calculate_ratio(humans):
    """Convert to population ratio"""
    return WORLD_POP / humans

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("GPT POPULATION RARITY CALCULATION")
    print("Compiled reference for FlameLang verification")
    print("=" * 70)
    print()
    
    print("FULL CONSTRAINT STACK:")
    print("-" * 40)
    full_stack = calculate_full_stack()
    full_ratio = calculate_ratio(full_stack)
    print()
    print(f"Result: {full_stack:.1f} humans globally")
    print(f"Ratio:  1 in {full_ratio:,.0f}")
    print()
    
    print("WITHOUT ROPE ACCESS:")
    print("-" * 40)
    no_rope = calculate_without_rope()
    no_rope_ratio = calculate_ratio(no_rope)
    print(f"Result: {no_rope:,.0f} humans globally")
    print(f"Ratio:  1 in {no_rope_ratio:,.0f}")
    print()
    
    print("=" * 70)
    print("FLAMELANG TARGET OUTPUT:")
    print("-" * 40)
    print(f"rarity.flame should return exit code: {int(full_stack)}")
    print("(Truncated to integer for exit code)")
    print("=" * 70)
    print()
    
    # Exit with the calculated value (for verification)
    import sys
    sys.exit(int(full_stack))
