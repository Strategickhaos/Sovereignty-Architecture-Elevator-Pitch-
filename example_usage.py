#!/usr/bin/env python3
"""
TRIG6 Citation System - Usage Example
======================================
Demonstrates how to use the TRIG6 Citation System to create,
load, and manage constants with full provenance tracking.

Owner: Strategickhaos DAO LLC
"""

from trig6_citation import Provenance, Validation, ConstantRecord, load_constants_file

def main():
    print("=" * 60)
    print("TRIG6 Citation System - Usage Example")
    print("=" * 60)
    print()
    
    # Example 1: Load existing constants from file
    print("1. Loading Example Constants from File")
    print("-" * 60)
    constants = load_constants_file("data/constants/example_constants.json")
    print(f"✅ Loaded {len(constants)} constants\n")
    
    # Display each constant
    for constant in constants:
        print(f"🔹 {constant.key}")
        print(f"   Value: {constant.value} {constant.units}")
        print(f"   Context: {constant.context[:60]}...")
        print(f"   Jurisdiction: {constant.jurisdiction}")
        print(f"   Confidence: {constant.confidence}")
        print(f"   Source: {constant.provenance[0].source_title}")
        print()
    
    # Example 2: Create a new constant with full provenance
    print("2. Creating a New Constant with Full Provenance")
    print("-" * 60)
    
    new_constant = ConstantRecord(
        key="safety.harness.load_rating",
        value=5000.0,
        units="lbf",
        context="Minimum breaking strength for full-body safety harness per ANSI Z359.11",
        provenance=[
            Provenance(
                source_title="ANSI/ASSP Z359.11-2021",
                publisher="American National Standards Institute",
                edition_or_rev="2021 Edition",
                date="2021",
                section_or_page="Section 5.2.1",
                url="https://www.ansi.org",
                notes="Full-body harness requirements"
            )
        ],
        entered_by="Safety Engineer",
        entered_date="2026-01-29",
        range=(5000.0, 10000.0),
        jurisdiction="USA",
        confidence="high",
        validation=Validation(
            doctor_test="safety.harness_strength_check",
            constraints=["value >= 5000", "value <= 15000"]
        )
    )
    
    print("✅ Created new constant:")
    print(f"   Key: {new_constant.key}")
    print(f"   Value: {new_constant.value} {new_constant.units}")
    print()
    
    # Example 3: Format citation
    print("3. Formatted Citation Output")
    print("-" * 60)
    print(new_constant.format_full())
    print()
    
    # Example 4: Query specific constant
    print("4. Query Specific Constant")
    print("-" * 60)
    target_key = "physics.gravity.earth_surface"
    gravity_constant = next((c for c in constants if c.key == target_key), None)
    
    if gravity_constant:
        print(f"Found constant: {gravity_constant.key}")
        print(f"Value: {gravity_constant.value} {gravity_constant.units}")
        print(f"Expected range: {gravity_constant.range}")
        print()
        print("Full citation:")
        print(gravity_constant.provenance[0].format_citation())
    
    print()
    print("=" * 60)
    print("✅ TRIG6 Citation System Example Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
