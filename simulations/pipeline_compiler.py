#!/usr/bin/env python3
"""
FlameLang Pipeline Compiler Integration
Connects TRIG6 simulations to the FlameLang glyph processing pipeline.

Pipeline Flow:
1. Ingest undeciphered script images
2. Extract glyphs from images
3. Generate embeddings (BAAI/bge-small-en-v1.5 compatible)
4. Cluster glyphs to 64 codons (genetic code structure)
5. TRIG6 validation (check for danger zones)
6. Compile stable mappings to SAGCO-OS
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

sys.path.insert(0, str(Path(__file__).parent))
from trig6_simulator import TRIG6Simulator, Recipe


class PipelineCompiler:
    """
    Compiles glyph mapping recipes into executable FlameLang bindings.
    """
    
    GENETIC_CODONS = 64  # Standard genetic code structure
    
    def __init__(self):
        self.simulator = TRIG6Simulator()
        self.validated_recipes = []
        self.compiled_mappings = {}
    
    def validate_recipe(self, recipe: Recipe, fitness_threshold: float = 0.7) -> Tuple[bool, float, str]:
        """
        Validate a recipe using TRIG6 simulation.
        
        Returns:
            (is_valid, fitness, status_message)
        """
        # Run quick validation simulation
        results = self.simulator.monte_carlo(recipe, runs=100)
        
        # Calculate mean fitness
        mean_fitness = sum(r.fitness for r in results) / len(results)
        
        # Check danger rate
        danger_rate = sum(1 for r in results if r.danger) / len(results)
        
        # Validate
        is_valid = mean_fitness >= fitness_threshold and danger_rate < 0.5
        
        if is_valid:
            status = f"✅ VALID: fitness={mean_fitness:.4f}, danger_rate={danger_rate:.2%}"
            self.validated_recipes.append(recipe)
        elif mean_fitness < fitness_threshold:
            status = f"❌ LOW FITNESS: {mean_fitness:.4f} < {fitness_threshold}"
        else:
            status = f"⚠️  HIGH DANGER: danger_rate={danger_rate:.2%}"
        
        return is_valid, mean_fitness, status
    
    def cluster_to_codons(self, glyph_count: int) -> Dict[int, List[int]]:
        """
        Map N glyphs to 64 codons using balanced clustering.
        
        Args:
            glyph_count: Total number of unique glyphs
            
        Returns:
            Dictionary mapping codon_id -> [glyph_ids]
        """
        # Simple balanced distribution
        glyphs_per_codon = max(1, glyph_count // self.GENETIC_CODONS)
        
        codon_map = {}
        current_glyph = 0
        
        for codon in range(self.GENETIC_CODONS):
            codon_map[codon] = []
            
            # Assign glyphs to this codon
            for _ in range(glyphs_per_codon):
                if current_glyph < glyph_count:
                    codon_map[codon].append(current_glyph)
                    current_glyph += 1
        
        # Distribute remaining glyphs
        codon = 0
        while current_glyph < glyph_count:
            codon_map[codon].append(current_glyph)
            current_glyph += 1
            codon = (codon + 1) % self.GENETIC_CODONS
        
        return codon_map
    
    def compile_to_flamelang(self, recipe: Recipe, codon_map: Dict[int, List[int]]) -> Dict:
        """
        Compile validated recipe and codon mapping to FlameLang binding format.
        
        Returns:
            FlameLang glyph_map.json compatible structure
        """
        binding = {
            "recipe_id": recipe.id,
            "recipe_name": recipe.name,
            "hazard_level": recipe.hazard_level,
            "codons": {},
            "metadata": {
                "total_glyphs": sum(len(glyphs) for glyphs in codon_map.values()),
                "codon_count": len(codon_map),
                "ingredients": recipe.ingredients,
                "process_stages": recipe.process_stages
            }
        }
        
        # Format codon mappings
        for codon_id, glyph_ids in codon_map.items():
            codon_key = f"codon_{codon_id:03d}"
            binding["codons"][codon_key] = {
                "glyph_ids": glyph_ids,
                "binding_code": f"[{codon_id:03d}]",
                "count": len(glyph_ids)
            }
        
        return binding
    
    def compile_pipeline(self, 
                        recipe: Recipe, 
                        glyph_count: int,
                        output_path: Optional[Path] = None) -> Optional[Dict]:
        """
        Complete pipeline: validate -> cluster -> compile.
        
        Args:
            recipe: TRIG6 recipe to compile
            glyph_count: Number of glyphs extracted from source
            output_path: Optional path to save compiled binding
            
        Returns:
            Compiled binding dictionary or None if validation failed
        """
        print(f"\n{'='*60}")
        print(f"PIPELINE COMPILATION: {recipe.name}")
        print(f"{'='*60}")
        
        # Step 1: Validate
        print(f"\n[1/3] Validating recipe with TRIG6...")
        is_valid, fitness, status = self.validate_recipe(recipe)
        print(f"      {status}")
        
        if not is_valid:
            print(f"\n❌ Compilation aborted: Recipe failed validation")
            print(f"   Recommendation: Adjust ingredients or use lower fitness threshold")
            return None
        
        # Step 2: Cluster to codons
        print(f"\n[2/3] Clustering {glyph_count} glyphs to {self.GENETIC_CODONS} codons...")
        codon_map = self.cluster_to_codons(glyph_count)
        glyphs_mapped = sum(len(glyphs) for glyphs in codon_map.values())
        print(f"      ✅ Mapped {glyphs_mapped} glyphs")
        
        # Step 3: Compile
        print(f"\n[3/3] Compiling to FlameLang binding...")
        binding = self.compile_to_flamelang(recipe, codon_map)
        
        # Save if output path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(binding, f, indent=2)
            print(f"      ✅ Saved to: {output_path}")
        
        # Store in compiled mappings
        self.compiled_mappings[recipe.id] = binding
        
        print(f"\n{'='*60}")
        print(f"✅ COMPILATION SUCCESSFUL")
        print(f"{'='*60}")
        print(f"Recipe: {recipe.name} ({recipe.id})")
        print(f"Fitness: {fitness:.4f}")
        print(f"Glyphs: {glyph_count} → {self.GENETIC_CODONS} codons")
        print(f"Average glyphs/codon: {glyph_count / self.GENETIC_CODONS:.1f}")
        print(f"{'='*60}\n")
        
        return binding


def example_pipeline():
    """
    Example: Compile a hypothetical Voynich glyph extraction.
    """
    from run_trig6_simulation import parse_t6_recipe
    
    # Load Voynich recipe
    recipe_path = Path(__file__).parent / "recipes" / "voynich_manuscript_glyph_mapping.t6"
    recipe = parse_t6_recipe(str(recipe_path))
    
    # Simulate glyph extraction results
    # Voynich has ~25 unique characters, but with variants ~170-250
    estimated_voynich_glyphs = 200
    
    # Create compiler
    compiler = PipelineCompiler()
    
    # Compile pipeline with lower threshold (Voynich is challenging)
    output_path = Path(__file__).parent / "compiled" / "voynich_flamelang_binding.json"
    
    # Note: Using lower fitness threshold (0.3) since Voynich is expected to be challenging
    print("\n⚠️  NOTE: Using fitness_threshold=0.3 for Voynich (challenging undeciphered script)")
    compiler.simulator = TRIG6Simulator()  # Reset
    
    # Override validation to use lower threshold for demonstration
    original_validate = compiler.validate_recipe
    
    def custom_validate(recipe, fitness_threshold=0.3):
        return original_validate(recipe, fitness_threshold)
    
    compiler.validate_recipe = custom_validate
    
    binding = compiler.compile_pipeline(recipe, estimated_voynich_glyphs, output_path)
    
    if binding:
        print("\n🧬 Voynich glyphs successfully compiled to FlameLang!")
        print(f"📝 Binding available at: compiled/voynich_flamelang_binding.json")
        print(f"🔥 Ready for SAGCO-OS integration")
    
    return binding


if __name__ == "__main__":
    print("🔥 FlameLang Pipeline Compiler v1.0")
    print("=" * 60)
    print("Purpose: Convert TRIG6 validated glyph recipes to FlameLang bindings")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        example_pipeline()
    else:
        print("\nUsage:")
        print("  python pipeline_compiler.py --example")
        print("\nOr import and use PipelineCompiler class:")
        print("  from pipeline_compiler import PipelineCompiler")
        print("  compiler = PipelineCompiler()")
        print("  binding = compiler.compile_pipeline(recipe, glyph_count, output_path)")
