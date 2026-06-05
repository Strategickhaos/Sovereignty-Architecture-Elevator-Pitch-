#!/usr/bin/env python3
"""
72 Names Invention Registry Manager

A Python module for managing and querying the 72 Names Invention Registry
for Strategickhaos DAO LLC.

Usage:
    from registry_manager import InventionRegistry
    
    registry = InventionRegistry()
    sealed = registry.get_sealed_inventions()
    invention = registry.get_by_angel("Haziel")
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime


class InventionRegistry:
    """Manages the 72 Names Invention Registry."""
    
    def __init__(self, registry_path: Optional[str] = None):
        """
        Initialize the registry manager.
        
        Args:
            registry_path: Path to the registry JSON file. If None, uses default location.
        """
        if registry_path is None:
            registry_path = Path(__file__).parent / "72_names_invention_registry.json"
        else:
            registry_path = Path(registry_path)
            
        self.registry_path = registry_path
        self.data = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load the registry from JSON file."""
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save(self) -> None:
        """Save the current registry state to file."""
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    @property
    def meta(self) -> Dict:
        """Get registry metadata."""
        return self.data["meta"]
    
    @property
    def stats(self) -> Dict:
        """Get current statistics."""
        return self.data["stats"]
    
    @property
    def inventions(self) -> List[Dict]:
        """Get all inventions."""
        return self.data["inventions"]
    
    def get_by_id(self, invention_id: int) -> Optional[Dict]:
        """
        Get invention by ID.
        
        Args:
            invention_id: The invention ID (1-72)
            
        Returns:
            Invention dictionary or None if not found
        """
        for inv in self.inventions:
            if inv["id"] == invention_id:
                return inv
        return None
    
    def get_by_angel(self, angel_name: str) -> Optional[Dict]:
        """
        Get invention by angel name.
        
        Args:
            angel_name: The angel's name
            
        Returns:
            Invention dictionary or None if not found
        """
        for inv in self.inventions:
            if inv["angel"].lower() == angel_name.lower():
                return inv
        return None
    
    def get_by_inv_id(self, inv_id: str) -> Optional[Dict]:
        """
        Get invention by invention ID (e.g., "INV-001").
        
        Args:
            inv_id: The invention identifier
            
        Returns:
            Invention dictionary or None if not found
        """
        for inv in self.inventions:
            if inv.get("inv_id") == inv_id:
                return inv
        return None
    
    def get_by_status(self, status: str) -> List[Dict]:
        """
        Get all inventions with a specific status.
        
        Args:
            status: One of "sealed", "in_progress", or "unsealed"
            
        Returns:
            List of invention dictionaries
        """
        return [inv for inv in self.inventions if inv["status"] == status]
    
    def get_sealed_inventions(self) -> List[Dict]:
        """Get all sealed (completed) inventions."""
        return self.get_by_status("sealed")
    
    def get_in_progress_inventions(self) -> List[Dict]:
        """Get all in-progress inventions."""
        return self.get_by_status("in_progress")
    
    def get_unsealed_inventions(self) -> List[Dict]:
        """Get all unsealed (available) slots."""
        return self.get_by_status("unsealed")
    
    def get_by_theta_range(self, min_theta: float, max_theta: float) -> List[Dict]:
        """
        Get inventions within a theta range.
        
        Args:
            min_theta: Minimum theta angle
            max_theta: Maximum theta angle
            
        Returns:
            List of invention dictionaries
        """
        results = []
        for inv in self.inventions:
            theta = inv["theta"]
            if isinstance(theta, (int, float)) and min_theta <= theta <= max_theta:
                results.append(inv)
        return results
    
    def get_meta_positions(self) -> List[Dict]:
        """Get all META positions (65-72)."""
        return [inv for inv in self.inventions if inv["id"] >= 65]
    
    def get_circle_positions(self) -> List[Dict]:
        """Get all circle positions (1-64)."""
        return [inv for inv in self.inventions if inv["id"] <= 64]
    
    def _generate_next_inv_id(self) -> str:
        """Generate the next sequential invention ID."""
        max_inv = 0
        for i in self.inventions:
            if i.get("inv_id"):
                try:
                    num = int(i["inv_id"].split("-")[1])
                    max_inv = max(max_inv, num)
                except (ValueError, IndexError):
                    pass
        return f"INV-{max_inv + 1:03d}"
    
    def seal_invention(
        self,
        invention_id: int,
        name: str,
        inv_id: Optional[str] = None,
        sealed_date: Optional[str] = None
    ) -> bool:
        """
        Seal an invention (mark as complete).
        
        Args:
            invention_id: The invention ID (1-72)
            name: The invention name
            inv_id: The invention identifier (e.g., "INV-009"). Auto-generated if None.
            sealed_date: ISO format date. Uses today if None.
            
        Returns:
            True if successful, False otherwise
        """
        inv = self.get_by_id(invention_id)
        if not inv:
            return False
        
        if inv["status"] == "sealed":
            return False  # Already sealed
        
        # Store original status before updating
        original_status = inv["status"]
        
        # Generate inv_id if not provided
        if inv_id is None:
            inv_id = self._generate_next_inv_id()
        
        # Use today's date if not provided
        if sealed_date is None:
            sealed_date = datetime.now().strftime("%Y-%m-%d")
        
        # Update the invention
        inv["invention"] = name
        inv["status"] = "sealed"
        inv["sealed_date"] = sealed_date
        inv["inv_id"] = inv_id
        
        # Update stats
        self.data["stats"]["sealed"] += 1
        if original_status == "in_progress":
            self.data["stats"]["in_progress"] -= 1
        else:
            self.data["stats"]["unsealed"] -= 1
        
        return True
    
    def mark_in_progress(
        self,
        invention_id: int,
        name: str,
        inv_id: Optional[str] = None
    ) -> bool:
        """
        Mark an invention as in progress.
        
        Args:
            invention_id: The invention ID (1-72)
            name: The invention name
            inv_id: The invention identifier (e.g., "INV-009"). Auto-generated if None.
            
        Returns:
            True if successful, False otherwise
        """
        inv = self.get_by_id(invention_id)
        if not inv:
            return False
        
        if inv["status"] != "unsealed":
            return False  # Can only mark unsealed as in progress
        
        # Generate inv_id if not provided
        if inv_id is None:
            inv_id = self._generate_next_inv_id()
        
        # Update the invention
        inv["invention"] = name
        inv["status"] = "in_progress"
        inv["inv_id"] = inv_id
        
        # Update stats
        self.data["stats"]["in_progress"] += 1
        self.data["stats"]["unsealed"] -= 1
        
        return True
    
    def search(self, query: str) -> List[Dict]:
        """
        Search inventions by text in angel name, meaning, or invention name.
        
        Args:
            query: Search string
            
        Returns:
            List of matching invention dictionaries
        """
        query = query.lower()
        results = []
        for inv in self.inventions:
            if (query in inv["angel"].lower() or
                query in inv["meaning"].lower() or
                (inv["invention"] is not None and query in inv["invention"].lower())):
                results.append(inv)
        return results
    
    def print_summary(self) -> None:
        """Print a summary of the registry."""
        print(f"\n{'='*70}")
        print(f"72 NAMES INVENTION REGISTRY")
        print(f"{'='*70}")
        print(f"Entity: {self.meta['entity']}")
        print(f"EIN: {self.meta['ein']}")
        print(f"Framework: {self.meta['framework']}")
        print(f"Version: {self.meta['version']}")
        print(f"\nSTATISTICS:")
        print(f"  Sealed:      {self.stats['sealed']:3d} inventions")
        print(f"  In Progress: {self.stats['in_progress']:3d} inventions")
        print(f"  Unsealed:    {self.stats['unsealed']:3d} slots available")
        print(f"  Total:       {self.meta['total_slots']:3d} positions")
        print(f"{'='*70}\n")
    
    def _format_theta(self, theta: Union[int, float, str]) -> str:
        """Format theta value with appropriate suffix."""
        if isinstance(theta, (int, float)):
            return f"{theta}°"
        return str(theta)  # For infinity symbol or other strings
    
    def print_sealed(self) -> None:
        """Print all sealed inventions."""
        sealed = self.get_sealed_inventions()
        print(f"\nSEALED INVENTIONS ({len(sealed)}):")
        print(f"{'='*70}")
        for inv in sorted(sealed, key=lambda x: x['id']):
            print(f"[{inv['inv_id']}] {inv['invention']}")
            print(f"  Position: {inv['id']} - {inv['angel']} ({inv['meaning']})")
            print(f"  Theta: {self._format_theta(inv['theta'])}")
            print(f"  Sealed: {inv['sealed_date']}")
            print()
    
    def print_in_progress(self) -> None:
        """Print all in-progress inventions."""
        in_progress = self.get_in_progress_inventions()
        print(f"\nIN PROGRESS INVENTIONS ({len(in_progress)}):")
        print(f"{'='*70}")
        for inv in sorted(in_progress, key=lambda x: x['id']):
            print(f"[{inv['inv_id']}] {inv['invention']}")
            print(f"  Position: {inv['id']} - {inv['angel']} ({inv['meaning']})")
            print(f"  Theta: {self._format_theta(inv['theta'])}")
            print()


def main():
    """Example usage and CLI interface."""
    import sys
    
    registry = InventionRegistry()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "summary":
            registry.print_summary()
        elif command == "sealed":
            registry.print_sealed()
        elif command == "progress":
            registry.print_in_progress()
        elif command == "search" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            results = registry.search(query)
            print(f"\nSearch results for '{query}': {len(results)} found")
            for inv in results:
                status = f"[{inv['status'].upper()}]"
                invention = inv['invention'] if inv['invention'] else "Available"
                print(f"  {inv['id']:2d}. {inv['angel']:15s} - {invention:30s} {status}")
        elif command == "angel" and len(sys.argv) > 2:
            angel_name = " ".join(sys.argv[2:])
            inv = registry.get_by_angel(angel_name)
            if inv:
                print(f"\nPosition {inv['id']}: {inv['angel']}")
                print(f"Hebrew: {inv['hebrew']}")
                print(f"Meaning: {inv['meaning']}")
                print(f"Glyph: {inv['glyph']}")
                print(f"Theta: {inv['theta']}")
                print(f"Status: {inv['status']}")
                if inv['invention']:
                    print(f"Invention: {inv['invention']}")
                    if inv.get('inv_id'):
                        print(f"ID: {inv['inv_id']}")
                    if inv.get('sealed_date'):
                        print(f"Sealed: {inv['sealed_date']}")
            else:
                print(f"Angel '{angel_name}' not found.")
        else:
            print("Usage:")
            print("  python registry_manager.py summary        - Show registry summary")
            print("  python registry_manager.py sealed         - List sealed inventions")
            print("  python registry_manager.py progress       - List in-progress inventions")
            print("  python registry_manager.py search <query> - Search inventions")
            print("  python registry_manager.py angel <name>   - Get info for specific angel")
    else:
        registry.print_summary()
        registry.print_sealed()
        registry.print_in_progress()


if __name__ == "__main__":
    main()
