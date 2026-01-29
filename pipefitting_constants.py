#!/usr/bin/env python3
"""
Pipefitting Constants Module with ASME/API Provenance
Strategickhaos DAO LLC

This module provides access to industry-standard pipefitting constants
with full provenance tracking from ASME, API, and AWS standards.

Maintainer: Domenic G. Garza
Certifications: Pipefitter Journeyman, Turner Industries
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class PipefittingConstants:
    """
    Access and validate pipefitting constants with full provenance.
    
    Constants are sourced from:
    - ASME B31.1: Power Piping
    - ASME B31.3: Process Piping
    - ASME B36.10M: Welded and Seamless Wrought Steel Pipe
    - ASME B16.9: Factory-Made Wrought Buttwelding Fittings
    - API 570: Piping Inspection Code
    - AWS D1.1: Structural Welding Code
    """
    
    def __init__(self, constants_file: Optional[str] = None):
        """
        Initialize the constants loader.
        
        Args:
            constants_file: Path to the JSON constants file. 
                          If None, uses default location.
        """
        if constants_file is None:
            # Default to data/pipe/pipefitting_constants.json
            repo_root = Path(__file__).parent
            constants_file = repo_root / "data" / "pipe" / "pipefitting_constants.json"
        
        self.constants_file = Path(constants_file)
        self.data = self._load_constants()
        self.constants_by_key = self._index_constants()
    
    def _load_constants(self) -> Dict[str, Any]:
        """Load constants from JSON file."""
        if not self.constants_file.exists():
            raise FileNotFoundError(
                f"Constants file not found: {self.constants_file}"
            )
        
        with open(self.constants_file, 'r') as f:
            return json.load(f)
    
    def _index_constants(self) -> Dict[str, Dict[str, Any]]:
        """Create an index of constants by key for fast lookup."""
        index = {}
        for constant in self.data.get('constants', []):
            key = constant.get('key')
            if key:
                index[key] = constant
        return index
    
    def get_constant(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get a constant by its key.
        
        Args:
            key: The constant key (e.g., 'pipe.thermal_expansion.carbon_steel')
        
        Returns:
            Dictionary containing the constant data, or None if not found.
        """
        return self.constants_by_key.get(key)
    
    def get_value(self, key: str) -> Optional[float]:
        """
        Get the numeric value of a constant.
        
        Args:
            key: The constant key
        
        Returns:
            The numeric value, or None if not found.
        """
        constant = self.get_constant(key)
        return constant.get('value') if constant else None
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the constants collection."""
        return self.data.get('metadata', {})
    
    def list_constants(self) -> List[str]:
        """Get a list of all constant keys."""
        return list(self.constants_by_key.keys())
    
    def search_constants(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for constants by key or context.
        
        Args:
            search_term: Term to search for in keys and context
        
        Returns:
            List of matching constants
        """
        search_lower = search_term.lower()
        results = []
        
        for constant in self.data.get('constants', []):
            key = constant.get('key', '').lower()
            context = constant.get('context', '').lower()
            
            if search_lower in key or search_lower in context:
                results.append(constant)
        
        return results
    
    def validate_constant(self, key: str) -> Tuple[bool, List[str]]:
        """
        Validate a constant against its constraints.
        
        Args:
            key: The constant key to validate
        
        Returns:
            Tuple of (is_valid, list of validation messages)
        """
        constant = self.get_constant(key)
        if not constant:
            return False, [f"Constant '{key}' not found"]
        
        value = constant.get('value')
        validation = constant.get('validation', {})
        constraints = validation.get('constraints', [])
        
        is_valid = True
        messages = []
        
        # Validate against constraints
        for constraint in constraints:
            try:
                # Evaluate constraint with the value
                if not eval(constraint, {'value': value, 'abs': abs}):
                    is_valid = False
                    messages.append(f"Constraint failed: {constraint}")
            except Exception as e:
                is_valid = False
                messages.append(f"Error evaluating constraint '{constraint}': {e}")
        
        # Validate value is within range
        value_range = constant.get('range')
        if value_range and len(value_range) == 2:
            if not (value_range[0] <= value <= value_range[1]):
                is_valid = False
                messages.append(
                    f"Value {value} outside range [{value_range[0]}, {value_range[1]}]"
                )
        
        if is_valid:
            messages.append("All validations passed")
        
        return is_valid, messages
    
    def validate_all(self) -> Dict[str, Tuple[bool, List[str]]]:
        """
        Validate all constants.
        
        Returns:
            Dictionary mapping constant keys to validation results
        """
        results = {}
        for key in self.list_constants():
            results[key] = self.validate_constant(key)
        return results
    
    def get_provenance(self, key: str) -> List[Dict[str, str]]:
        """
        Get the provenance (sources) for a constant.
        
        Args:
            key: The constant key
        
        Returns:
            List of provenance records with source information
        """
        constant = self.get_constant(key)
        if not constant:
            return []
        return constant.get('provenance', [])
    
    def format_constant(self, key: str, include_provenance: bool = True) -> str:
        """
        Format a constant for display.
        
        Args:
            key: The constant key
            include_provenance: Whether to include provenance information
        
        Returns:
            Formatted string representation of the constant
        """
        constant = self.get_constant(key)
        if not constant:
            return f"Constant '{key}' not found"
        
        output = []
        output.append(f"Key: {constant.get('key')}")
        output.append(f"Value: {constant.get('value')} {constant.get('units')}")
        output.append(f"Range: {constant.get('range')}")
        output.append(f"Context: {constant.get('context')}")
        output.append(f"Confidence: {constant.get('confidence')}")
        
        if include_provenance:
            output.append("\nProvenance:")
            for source in constant.get('provenance', []):
                output.append(f"  - {source.get('source_title')}")
                output.append(f"    Publisher: {source.get('publisher')}")
                output.append(f"    Edition: {source.get('edition_or_rev')}")
                output.append(f"    Section: {source.get('section_or_page')}")
                output.append(f"    Notes: {source.get('notes')}")
        
        return "\n".join(output)


# Doctor test functions referenced in validation
def thermal_expansion_in_range(value: float) -> bool:
    """Validate thermal expansion coefficient is in reasonable range."""
    return 1e-6 <= value <= 20e-6


def wall_thickness_positive(value: float) -> bool:
    """Validate wall thickness is positive."""
    return value > 0


def takeout_positive(value: float) -> bool:
    """Validate fitting takeout dimension is positive."""
    return value > 0


def weld_gap_in_range(value: float) -> bool:
    """Validate weld gap is in reasonable range."""
    return 0 <= value <= 0.25


def pi_is_pi(value: float) -> bool:
    """Validate pi constant is close to mathematical value."""
    return abs(value - 3.14159) < 0.001


if __name__ == "__main__":
    # Demo usage
    constants = PipefittingConstants()
    
    print("=== Pipefitting Constants Demo ===\n")
    
    # Display metadata
    metadata = constants.get_metadata()
    print(f"Domain: {metadata.get('domain')}")
    print(f"Maintainer: {metadata.get('maintainer')}")
    print(f"Version: {metadata.get('version')}")
    print(f"Regulatory Frameworks: {', '.join(metadata.get('regulatory_frameworks', []))}")
    print()
    
    # List all constants
    print(f"Available constants ({len(constants.list_constants())}):")
    for key in constants.list_constants():
        print(f"  - {key}")
    print()
    
    # Display a specific constant
    print("=== Example Constant ===")
    print(constants.format_constant('pipe.thermal_expansion.carbon_steel'))
    print()
    
    # Validate all constants
    print("=== Validation Results ===")
    validation_results = constants.validate_all()
    all_valid = all(result[0] for result in validation_results.values())
    
    for key, (is_valid, messages) in validation_results.items():
        status = "✓" if is_valid else "✗"
        print(f"{status} {key}")
        if not is_valid:
            for msg in messages:
                print(f"    {msg}")
    
    print(f"\nAll constants valid: {all_valid}")
