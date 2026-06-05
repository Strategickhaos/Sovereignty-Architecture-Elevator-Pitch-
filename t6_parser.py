#!/usr/bin/env python3
"""
TRIG6 Recipe Parser
Parses .t6 recipe files and creates Recipe objects for simulation.
"""

import re
import math
from typing import Dict, Any, Optional
from trig6_simulator import Recipe


class T6Parser:
    """Parser for .t6 recipe files."""
    
    @staticmethod
    def parse_file(filepath: str) -> Recipe:
        """Parse a .t6 file and return a Recipe object."""
        with open(filepath, 'r') as f:
            content = f.read()
        
        return T6Parser.parse_content(content)
    
    @staticmethod
    def parse_content(content: str) -> Recipe:
        """Parse .t6 file content."""
        sections = T6Parser._split_into_sections(content)
        
        # Extract metadata
        metadata = T6Parser._parse_section(sections.get('metadata', ''))
        recipe_id = metadata.get('id', 'UNKNOWN')
        name = metadata.get('name', 'Unknown Recipe')
        hazard_level = metadata.get('hazard_level', 'MEDIUM')
        
        # Extract ingredients (parameters)
        ingredients_section = sections.get('ingredients', '')
        ingredients = T6Parser._parse_ingredients(ingredients_section)
        
        # Extract custom hooks
        custom_hooks_section = sections.get('custom_hooks', '')
        custom_hooks = T6Parser._parse_custom_hooks(custom_hooks_section)
        
        return Recipe(
            id=recipe_id,
            name=name,
            hazard_level=hazard_level,
            ingredients=ingredients,
            custom_hooks=custom_hooks
        )
    
    @staticmethod
    def _split_into_sections(content: str) -> Dict[str, str]:
        """Split .t6 content into sections."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # Check for section header
            section_match = re.match(r'^\[(\w+)\]', line.strip())
            if section_match:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = section_match.group(1)
                current_content = []
            else:
                # Skip comments and empty lines at section start
                if not line.strip() or line.strip().startswith('#'):
                    if current_content or current_section:
                        current_content.append(line)
                else:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    @staticmethod
    def _parse_section(section_content: str) -> Dict[str, str]:
        """Parse a simple key=value section."""
        result = {}
        for line in section_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
        
        return result
    
    @staticmethod
    def _parse_ingredients(section_content: str) -> Dict[str, float]:
        """Parse ingredients section into float parameters."""
        ingredients = {}
        for line in section_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                try:
                    ingredients[key] = float(value)
                except ValueError:
                    # Skip non-numeric values
                    pass
        
        return ingredients
    
    @staticmethod
    def _parse_custom_hooks(section_content: str) -> Dict[str, Any]:
        """Parse custom hooks section (R, D, N functions)."""
        hooks = {}
        
        # Look for R_function, D_function, N_function
        for hook_name in ['R_function', 'D_function', 'N_function']:
            pattern = rf'{hook_name}\s*=\s*"""(.*?)"""'
            match = re.search(pattern, section_content, re.DOTALL)
            
            if match:
                func_code = match.group(1).strip()
                # Extract the actual function definition
                func_match = re.search(r'def\s+(\w+)\s*\((.*?)\):(.*)', func_code, re.DOTALL)
                
                if func_match:
                    func_name = func_match.group(1)
                    func_params = func_match.group(2)
                    func_body = func_match.group(3)
                    
                    # Create a callable function
                    # For safety, we'll just store the code and mark it as custom
                    # Real implementation would need safe execution
                    hook_type = hook_name.split('_')[0]  # R, D, or N
                    hooks[hook_type] = T6Parser._create_hook_function(
                        func_name, func_params, func_body, hook_type
                    )
        
        return hooks
    
    @staticmethod
    def _create_hook_function(func_name: str, params: str, body: str, hook_type: str):
        """
        Create a hook function from parsed code.
        
        NOTE: Current implementation returns placeholder functions for safety.
        Custom hook code from .t6 files is parsed but not executed.
        
        For production use, consider:
        1. Use ast.parse() with restricted globals for safe execution
        2. Implement a domain-specific language for mathematical expressions
        3. Use a sandboxed execution environment
        
        This is a security measure to prevent arbitrary code execution.
        """
        # For safety, create a simple wrapper that returns default values
        # In production, you'd want to use ast.parse and safe execution
        
        # This is a placeholder - real implementation would execute the custom code
        def placeholder_hook(*args, **kwargs):
            # Return reasonable defaults based on hook type
            if hook_type == 'R':
                return 0.3  # Low resonance for undeciphered scripts
            elif hook_type == 'D':
                return 0.4  # Moderate drift
            elif hook_type == 'N':
                return 0.3  # Moderate noise
            return 0.0
        
        placeholder_hook.__name__ = func_name
        return placeholder_hook


def load_recipe_from_t6(filepath: str) -> Recipe:
    """Convenience function to load a recipe from a .t6 file."""
    return T6Parser.parse_file(filepath)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python t6_parser.py <recipe.t6>")
        sys.exit(1)
    
    recipe_file = sys.argv[1]
    recipe = load_recipe_from_t6(recipe_file)
    
    print(f"Loaded recipe: {recipe.name}")
    print(f"ID: {recipe.id}")
    print(f"Hazard Level: {recipe.hazard_level}")
    print(f"Ingredients: {recipe.ingredients}")
    print(f"Custom Hooks: {list(recipe.custom_hooks.keys())}")
