#!/usr/bin/env python3
"""
FlameLang Demo Script - Showcase Meroitic Unicode Conversion
Demonstrates the linguistic layer of the FlameLang pipeline
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from flamelang import (
    english_to_meroitic_root,
    meroitic_hieroglyph_map,
    export_conversion_to_json
)


def demo_basic_conversion():
    """Demonstrate basic English to Meroitic conversion"""
    print("=" * 70)
    print("🔥 FLAMELANG MEROITIC CONVERTER DEMO")
    print("=" * 70)
    print("\n1️⃣  BASIC CONVERSION")
    print("-" * 70)
    
    examples = [
        "Flame Lang",
        "Sovereignty",
        "Strategic Khaos",
        "Reignite",
        "Neural Sync"
    ]
    
    for text in examples:
        spike = english_to_meroitic_root(text)
        print(f"\n📝 Input:  {spike.input}")
        print(f"🔥 Glyphs: {spike.output_glyphs}")
        print(f"🔢 Unicode: {spike.unicode_map}")


def demo_glyph_map():
    """Display the Meroitic glyph mapping"""
    print("\n\n2️⃣  MEROITIC HIEROGLYPH MAP")
    print("-" * 70)
    print(f"Total glyphs: {len(meroitic_hieroglyph_map)}")
    print("Unicode block: U+10980–U+1099F")
    print("\nSample mappings:")
    
    sample_keys = ['a', 'e', 'i', 'o', 'la', 'ma', 'na', 'ra', 'sa', 'ta', 'ka']
    for key in sample_keys:
        if key in meroitic_hieroglyph_map:
            glyph = meroitic_hieroglyph_map[key]
            codepoint = f"U+{ord(glyph):X}"
            print(f"  {key:8} -> {glyph} ({codepoint})")


def demo_phonetic_preprocessing():
    """Demonstrate phonetic preprocessing rules"""
    print("\n\n3️⃣  PHONETIC PREPROCESSING")
    print("-" * 70)
    print("Rules: th→ta, ch→kha, ph→pa\n")
    
    examples = [
        ("the", "th becomes ta"),
        ("chat", "ch becomes kha"),
        ("phone", "ph becomes pa"),
        ("think", "th becomes ta")
    ]
    
    for text, rule in examples:
        spike = english_to_meroitic_root(text)
        print(f"  {text:10} -> {spike.output_glyphs:15} ({rule})")


def demo_density_compression():
    """Demonstrate semantic density improvement"""
    print("\n\n4️⃣  SEMANTIC DENSITY COMPRESSION")
    print("-" * 70)
    
    examples = ["Hello World", "Artificial Intelligence", "Blockchain Technology"]
    
    for text in examples:
        spike = english_to_meroitic_root(text)
        original_len = len(text.replace(' ', ''))
        converted_len = len(spike.output_glyphs)
        ratio = original_len / converted_len if converted_len > 0 else 0
        
        print(f"\n  Original:  '{text}' ({original_len} chars)")
        print(f"  Converted: '{spike.output_glyphs}' ({converted_len} chars)")
        print(f"  Ratio:     {ratio:.2f}x compression")


def demo_json_export():
    """Demonstrate JSON export for pipeline integration"""
    print("\n\n5️⃣  JSON EXPORT FOR PIPELINE INTEGRATION")
    print("-" * 70)
    
    spike = english_to_meroitic_root("FlameLang Pipeline")
    output_file = "/tmp/flamelang_demo_export.json"
    
    export_conversion_to_json(spike, output_file)
    
    print(f"\n✅ Exported conversion to: {output_file}")
    print(f"\n📊 Data structure:")
    print(f"  - conversion.input: {spike.input}")
    print(f"  - conversion.output_glyphs: {spike.output_glyphs}")
    print(f"  - conversion.unicode_map: {spike.unicode_map}")
    print(f"  - conversion.entropy: {spike.entropy}")
    print(f"  - map_summary: [{len(meroitic_hieroglyph_map)} glyphs]")


def demo_integration_points():
    """Show integration points with other components"""
    print("\n\n6️⃣  PIPELINE INTEGRATION POINTS")
    print("-" * 70)
    print("""
The FlameLang Linguistic Layer integrates with:

  1. prompt_absorber.py     - Scan directories for semantic roots
  2. vectorizer.py          - Vectorize Unicode hex for wave layer
  3. brain_arsenal.json     - Store conversion mappings
  4. SynapseBus             - Monitor compilation spikes
  5. alien_epistemology     - Apply paradoxical mapping
  
Next pipeline layers (planned):
  → Numeric Layer:  Unicode hex to wave frequencies
  → Wave Layer:     Frequency/amplitude via astropy
  → DNA Layer:      Biopython codon mapping
  → LLVM Layer:     llvmlite intermediate representation
""")


def main():
    """Run all demo sections"""
    demo_basic_conversion()
    demo_glyph_map()
    demo_phonetic_preprocessing()
    demo_density_compression()
    demo_json_export()
    demo_integration_points()
    
    print("\n" + "=" * 70)
    print("🔥 Demo complete. Reignite.")
    print("=" * 70)
    print("\nRun tests: python3 benchmarks/test_flamelang_meroitic.py")
    print("Learn more: flamelang/README.md\n")


if __name__ == "__main__":
    main()
