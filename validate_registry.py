#!/usr/bin/env python3
"""
72 Names Invention Registry Validator

Validates the integrity and consistency of the 72 Names Invention Registry.

Usage:
    python validate_registry.py
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple


class RegistryValidator:
    """Validates the 72 Names Invention Registry."""
    
    def __init__(self, registry_path: str = "72_names_invention_registry.json"):
        """Initialize the validator."""
        self.registry_path = Path(registry_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.data = None
    
    def load_registry(self) -> bool:
        """Load the registry from file."""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"Registry file not found: {self.registry_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON format: {e}")
            return False
    
    def validate_structure(self) -> None:
        """Validate the basic structure of the registry."""
        required_keys = ["meta", "stats", "inventions"]
        for key in required_keys:
            if key not in self.data:
                self.errors.append(f"Missing required key: '{key}'")
        
        # Validate meta structure
        if "meta" in self.data:
            required_meta = ["title", "entity", "ein", "framework", "total_slots", "version"]
            for key in required_meta:
                if key not in self.data["meta"]:
                    self.errors.append(f"Missing required meta key: '{key}'")
        
        # Validate stats structure
        if "stats" in self.data:
            required_stats = ["sealed", "in_progress", "unsealed"]
            for key in required_stats:
                if key not in self.data["stats"]:
                    self.errors.append(f"Missing required stats key: '{key}'")
    
    def validate_inventions(self) -> None:
        """Validate the inventions array."""
        if "inventions" not in self.data:
            return
        
        inventions = self.data["inventions"]
        
        # Check count
        if len(inventions) != 72:
            self.errors.append(f"Expected 72 inventions, found {len(inventions)}")
        
        # Required fields for each invention
        required_fields = ["id", "angel", "hebrew", "meaning", "glyph", "theta", "invention", "status"]
        
        seen_ids = set()
        seen_angels = set()
        
        for i, inv in enumerate(inventions):
            # Check required fields
            for field in required_fields:
                if field not in inv:
                    self.errors.append(f"Invention {i+1} missing required field: '{field}'")
            
            # Validate ID
            if "id" in inv:
                inv_id = inv["id"]
                if inv_id < 1 or inv_id > 72:
                    self.errors.append(f"Invalid invention ID: {inv_id} (must be 1-72)")
                if inv_id in seen_ids:
                    self.errors.append(f"Duplicate invention ID: {inv_id}")
                seen_ids.add(inv_id)
            
            # Validate angel name uniqueness
            if "angel" in inv:
                if inv["angel"] in seen_angels:
                    self.errors.append(f"Duplicate angel name: {inv['angel']}")
                seen_angels.add(inv["angel"])
            
            # Validate status
            if "status" in inv:
                valid_statuses = ["sealed", "in_progress", "unsealed"]
                if inv["status"] not in valid_statuses:
                    self.errors.append(
                        f"Invalid status for invention {inv.get('id')}: '{inv['status']}' "
                        f"(must be one of {valid_statuses})"
                    )
            
            # Validate sealed inventions
            if inv.get("status") == "sealed":
                if not inv.get("invention"):
                    self.errors.append(f"Sealed invention {inv.get('id')} has no invention name")
                if not inv.get("sealed_date"):
                    self.errors.append(f"Sealed invention {inv.get('id')} has no sealed_date")
                if not inv.get("inv_id"):
                    self.errors.append(f"Sealed invention {inv.get('id')} has no inv_id")
            
            # Validate in_progress inventions
            if inv.get("status") == "in_progress":
                if not inv.get("invention"):
                    self.errors.append(f"In-progress invention {inv.get('id')} has no invention name")
                if not inv.get("inv_id"):
                    self.errors.append(f"In-progress invention {inv.get('id')} has no inv_id")
                if inv.get("sealed_date"):
                    self.warnings.append(
                        f"In-progress invention {inv.get('id')} has a sealed_date "
                        "(should only have this when sealed)"
                    )
            
            # Validate unsealed inventions
            if inv.get("status") == "unsealed":
                if inv.get("invention") is not None:
                    self.warnings.append(f"Unsealed invention {inv.get('id')} has an invention name")
                if inv.get("sealed_date"):
                    self.errors.append(f"Unsealed invention {inv.get('id')} has a sealed_date")
                if inv.get("inv_id"):
                    self.errors.append(f"Unsealed invention {inv.get('id')} has an inv_id")
            
            # Validate theta values
            if "theta" in inv and "id" in inv:
                theta = inv["theta"]
                inv_id = inv["id"]
                
                if inv_id <= 64:
                    # Regular positions should have numeric theta
                    if not isinstance(theta, (int, float)):
                        self.errors.append(f"Invention {inv_id} has non-numeric theta: {theta}")
                    else:
                        expected_theta = (inv_id - 1) * 5.625
                        if abs(theta - expected_theta) > 0.001:
                            self.errors.append(
                                f"Invention {inv_id} has incorrect theta: {theta} "
                                f"(expected {expected_theta})"
                            )
                else:
                    # META positions should have infinity symbol
                    if theta != "∞":
                        self.warnings.append(
                            f"META position {inv_id} has theta '{theta}' "
                            "(expected '∞')"
                        )
            
            # Validate glyph values
            if "glyph" in inv and "id" in inv:
                glyph = inv["glyph"]
                inv_id = inv["id"]
                
                if inv_id <= 64:
                    if not isinstance(glyph, int):
                        self.errors.append(f"Invention {inv_id} has non-integer glyph: {glyph}")
                    elif glyph != inv_id - 1:
                        self.errors.append(
                            f"Invention {inv_id} has incorrect glyph: {glyph} "
                            f"(expected {inv_id - 1})"
                        )
                else:
                    expected_glyph = f"META-{inv_id - 64}"
                    if glyph != expected_glyph:
                        self.errors.append(
                            f"Invention {inv_id} has incorrect glyph: '{glyph}' "
                            f"(expected '{expected_glyph}')"
                        )
    
    def validate_statistics(self) -> None:
        """Validate that statistics match the actual inventory."""
        if "stats" not in self.data or "inventions" not in self.data:
            return
        
        stats = self.data["stats"]
        inventions = self.data["inventions"]
        
        # Count actual statuses
        actual_sealed = sum(1 for inv in inventions if inv.get("status") == "sealed")
        actual_in_progress = sum(1 for inv in inventions if inv.get("status") == "in_progress")
        actual_unsealed = sum(1 for inv in inventions if inv.get("status") == "unsealed")
        
        # Validate counts
        if stats.get("sealed") != actual_sealed:
            self.errors.append(
                f"Stats mismatch: sealed count is {stats.get('sealed')}, "
                f"but found {actual_sealed} sealed inventions"
            )
        
        if stats.get("in_progress") != actual_in_progress:
            self.errors.append(
                f"Stats mismatch: in_progress count is {stats.get('in_progress')}, "
                f"but found {actual_in_progress} in-progress inventions"
            )
        
        if stats.get("unsealed") != actual_unsealed:
            self.errors.append(
                f"Stats mismatch: unsealed count is {stats.get('unsealed')}, "
                f"but found {actual_unsealed} unsealed slots"
            )
        
        # Validate total
        total = actual_sealed + actual_in_progress + actual_unsealed
        if total != 72:
            self.errors.append(f"Total invention count is {total}, expected 72")
    
    def validate_inv_ids(self) -> None:
        """Validate invention IDs are unique and sequential."""
        if "inventions" not in self.data:
            return
        
        inv_ids = []
        for inv in self.data["inventions"]:
            if "inv_id" in inv:
                inv_ids.append(inv["inv_id"])
        
        # Check uniqueness
        if len(inv_ids) != len(set(inv_ids)):
            duplicates = [iid for iid in inv_ids if inv_ids.count(iid) > 1]
            self.errors.append(f"Duplicate inv_id values found: {set(duplicates)}")
        
        # Check format
        for inv_id in inv_ids:
            if not inv_id.startswith("INV-"):
                self.errors.append(f"Invalid inv_id format: '{inv_id}' (should start with 'INV-')")
    
    def validate_all(self) -> Tuple[bool, int, int]:
        """
        Run all validations.
        
        Returns:
            Tuple of (is_valid, error_count, warning_count)
        """
        if not self.load_registry():
            return False, len(self.errors), len(self.warnings)
        
        self.validate_structure()
        self.validate_inventions()
        self.validate_statistics()
        self.validate_inv_ids()
        
        return len(self.errors) == 0, len(self.errors), len(self.warnings)
    
    def print_report(self) -> None:
        """Print validation report."""
        print("\n" + "="*70)
        print("72 NAMES INVENTION REGISTRY VALIDATION REPORT")
        print("="*70)
        
        if not self.errors and not self.warnings:
            print("\n✓ Registry is valid! No errors or warnings found.")
        else:
            if self.errors:
                print(f"\n✗ ERRORS ({len(self.errors)}):")
                for i, error in enumerate(self.errors, 1):
                    print(f"  {i}. {error}")
            
            if self.warnings:
                print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"  {i}. {warning}")
        
        print("="*70 + "\n")


def main():
    """Main validation entry point."""
    validator = RegistryValidator()
    is_valid, error_count, warning_count = validator.validate_all()
    validator.print_report()
    
    # Exit with appropriate code
    if error_count > 0:
        sys.exit(1)
    elif warning_count > 0:
        sys.exit(0)  # Warnings don't cause failure
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
