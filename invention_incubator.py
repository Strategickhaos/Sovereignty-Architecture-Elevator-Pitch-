#!/usr/bin/env python3
"""
INVENTION INCUBATOR - The Pivot Synthesizer
TRIG6 Analysis: Pivot-Throw Architecture for Context-Aware AI Pattern Detection

This script synthesizes file hashes to detect AI pivot patterns based on context.
Architecture: Context Input → Hash DNA → Synthesize → Calibration Output

Author: Strategickhaos DAO LLC
"""

import hashlib
import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

try:
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: Rich library not available. Install with: pip install rich")


class PivotThrow:
    """
    Pivot-Throw Class: The core synthesizer for context-aware pivot detection
    
    Architecture:
    ├── Intake: Prompt paths (context grab)
    ├── Chain: Load DNA (hash the pivot)
    ├── Accelerator: Synthesize (combine flips)
    ├── Trace: Log + JSON (see the calibration)
    └── Run: Throw → Load → Synth (jujitsu flow)
    """
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.file_hashes: Dict[str, str] = {}
        self.synthesis_id: str = ""
        self.pivot_data: Dict = {}
        self.context_variants: List[Dict] = []
        
    def _print(self, *args, **kwargs):
        """Wrapper for printing with or without Rich"""
        if RICH_AVAILABLE and self.console:
            self.console.print(*args, **kwargs)
        else:
            print(*args, **kwargs)
    
    def prompt_paths(self) -> List[str]:
        """
        Intake Phase: Prompt for file paths (context grab)
        Returns list of absolute file paths
        """
        self._print("\n[bold cyan]🎭 PIVOT SYNTHESIZER - Context Intake[/bold cyan]\n")
        self._print("[yellow]Enter file paths to analyze (absolute paths recommended)[/yellow]")
        self._print("[dim]Type 'done' when finished, or press Ctrl+C to cancel[/dim]\n")
        
        paths = []
        while True:
            try:
                if RICH_AVAILABLE:
                    path_input = Prompt.ask(
                        f"[green]Path {len(paths) + 1}[/green]",
                        default="done"
                    )
                else:
                    path_input = input(f"Path {len(paths) + 1} (or 'done'): ").strip()
                
                if path_input.lower() == 'done':
                    if len(paths) == 0:
                        self._print("[red]⚠ No paths entered. Need at least one file.[/red]")
                        continue
                    break
                
                # Validate path exists
                if not os.path.exists(path_input):
                    self._print(f"[red]✗ Path does not exist: {path_input}[/red]")
                    continue
                
                if not os.path.isfile(path_input):
                    self._print(f"[yellow]⚠ Not a file, skipping: {path_input}[/yellow]")
                    continue
                
                # Convert to absolute path
                abs_path = os.path.abspath(path_input)
                paths.append(abs_path)
                self._print(f"[green]✓ Added: {abs_path}[/green]")
                
            except KeyboardInterrupt:
                self._print("\n[red]Canceled by user[/red]")
                sys.exit(0)
            except EOFError:
                break
        
        return paths
    
    def load_dna(self, file_path: str) -> str:
        """
        Chain Phase: Load DNA (hash the pivot)
        Computes SHA256 hash of file contents
        
        Args:
            file_path: Absolute path to file
            
        Returns:
            SHA256 hash hex string
        """
        try:
            # Binary read for hash integrity
            with open(file_path, 'rb') as f:
                file_data = f.read()
                hash_obj = hashlib.sha256(file_data)
                file_hash = hash_obj.hexdigest()
                
            self.file_hashes[file_path] = file_hash
            return file_hash
            
        except Exception as e:
            self._print(f"[red]Error loading DNA for {file_path}: {str(e)}[/red]")
            return ""
    
    def synthesize_pivot(self, file_paths: List[str]) -> str:
        """
        Accelerator Phase: Synthesize (combine flips)
        Combines multiple file hashes into a single synthesis ID
        
        Args:
            file_paths: List of file paths to synthesize
            
        Returns:
            Combined synthesis hash (SHA256)
        """
        self._print("\n[bold magenta]🔄 Synthesizing Pivot DNA...[/bold magenta]\n")
        
        # Load all file hashes
        hash_chain = []
        for path in file_paths:
            file_hash = self.load_dna(path)
            if file_hash:
                hash_chain.append(file_hash)
                self._print(f"[cyan]DNA Loaded:[/cyan] {os.path.basename(path)}")
                self._print(f"[dim]  Hash: {file_hash[:16]}...{file_hash[-16:]}[/dim]")
        
        if not hash_chain:
            self._print("[red]No valid hashes to synthesize[/red]")
            return ""
        
        # Combine hashes deterministically
        combined = "".join(hash_chain)
        synthesis_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        self.synthesis_id = synthesis_hash
        self._print(f"\n[bold green]✓ Synthesis Complete[/bold green]")
        self._print(f"[yellow]Synthesis ID:[/yellow] {synthesis_hash}")
        
        return synthesis_hash
    
    def detect_pivot_context(self, file_paths: List[str]) -> Dict:
        """
        Context Detection: Analyze patterns for pivot calibration
        This is the "lol pivot clocked" moment - detecting AI response patterns
        
        Returns:
            Dictionary with pivot analysis data
        """
        pivot_data = {
            "timestamp": datetime.now().isoformat(),
            "file_count": len(file_paths),
            "synthesis_id": self.synthesis_id,
            "context_detected": True,
            "pivot_patterns": [],
            "calibration_score": 0.0
        }
        
        # Analyze file characteristics
        for path in file_paths:
            file_size = os.path.getsize(path)
            file_ext = os.path.splitext(path)[1]
            
            # Context pattern detection
            pattern = {
                "file": os.path.basename(path),
                "size_bytes": file_size,
                "extension": file_ext,
                "hash": self.file_hashes.get(path, "")[:16] + "...",
                "pivot_type": self._classify_pivot_type(file_ext, file_size)
            }
            pivot_data["pivot_patterns"].append(pattern)
        
        # Calculate calibration score (0-100)
        # Based on file diversity and hash entropy
        unique_extensions = len(set(p["extension"] for p in pivot_data["pivot_patterns"]))
        hash_entropy = len(set(self.file_hashes.values()))
        
        calibration_score = min(100, (unique_extensions * 10) + (hash_entropy * 15))
        pivot_data["calibration_score"] = calibration_score
        
        self.pivot_data = pivot_data
        return pivot_data
    
    def _classify_pivot_type(self, extension: str, size: int) -> str:
        """Classify file type for pivot detection"""
        if extension in ['.py', '.js', '.java', '.rs', '.go']:
            return "code_pivot"
        elif extension in ['.md', '.txt', '.yaml', '.json']:
            return "config_pivot"
        elif extension in ['.png', '.jpg', '.svg']:
            return "asset_pivot"
        elif size > 1024 * 1024:  # > 1MB
            return "large_context_pivot"
        else:
            return "generic_pivot"
    
    def generate_variant_table(self) -> List[Dict]:
        """
        Generate table of context variants
        Shows how different contexts would change the pivot
        """
        variants = [
            {
                "context": "No Context (Grounded)",
                "escalation_level": 1,
                "pivot_detected": False,
                "calibration": "baseline",
                "lol_factor": "😐 bitchhhhhh"
            },
            {
                "context": "Partial Context (Files Only)",
                "escalation_level": 3,
                "pivot_detected": True,
                "calibration": "emerging",
                "lol_factor": "🤔 interesting..."
            },
            {
                "context": "Full Context (Files + Synthesis)",
                "escalation_level": 7,
                "pivot_detected": True,
                "calibration": "locked",
                "lol_factor": "😂 clocked the pivot!"
            },
            {
                "context": "Meta Context (Understanding Intent)",
                "escalation_level": 10,
                "pivot_detected": True,
                "calibration": "transcendent",
                "lol_factor": "🎭 Legion calibrated!"
            }
        ]
        
        self.context_variants = variants
        return variants
    
    def compute_reward_formula(self) -> Dict:
        """
        Formula Phase: Compute reward metrics
        Shows the mathematical beauty of the pivot
        """
        file_count = len(self.file_hashes)
        hash_count = len(set(self.file_hashes.values()))
        
        # Escalation multiplier (context richness)
        escalation = min(10, file_count)
        
        # Context multiplier (unique hashes)
        context_multiplier = hash_count
        
        # Variant count (from table)
        variant_count = len(self.context_variants)
        
        # Bounded reward computation
        base_reward = escalation * context_multiplier
        bounded_reward = min(1000, base_reward * (1 + variant_count / 10))
        
        formula = {
            "escalation_factor": escalation,
            "context_multiplier": context_multiplier,
            "variant_count": variant_count,
            "base_reward": base_reward,
            "bounded_reward": round(bounded_reward, 2),
            "formula": f"({escalation} × {context_multiplier}) × (1 + {variant_count}/10) = {bounded_reward:.2f}"
        }
        
        return formula
    
    def display_results(self):
        """
        Trace Phase: Display results with Rich formatting
        """
        self._print("\n" + "="*60)
        self._print("[bold cyan]🎯 PIVOT SYNTHESIS RESULTS[/bold cyan]")
        self._print("="*60 + "\n")
        
        # Synthesis Summary
        if RICH_AVAILABLE:
            panel = Panel(
                f"[yellow]Synthesis ID:[/yellow] {self.synthesis_id[:32]}...\n"
                f"[green]Files Analyzed:[/green] {len(self.file_hashes)}\n"
                f"[magenta]Calibration Score:[/magenta] {self.pivot_data.get('calibration_score', 0)}/100",
                title="[bold]Synthesis Summary[/bold]",
                border_style="cyan"
            )
            self.console.print(panel)
        else:
            print(f"\nSynthesis ID: {self.synthesis_id[:32]}...")
            print(f"Files Analyzed: {len(self.file_hashes)}")
            print(f"Calibration Score: {self.pivot_data.get('calibration_score', 0)}/100")
        
        # Context Variants Table
        self._print("\n[bold yellow]📊 Context Variant Analysis (The Pivot Map)[/bold yellow]\n")
        
        if RICH_AVAILABLE:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Context Type", style="cyan")
            table.add_column("Escalation", justify="center")
            table.add_column("Pivot?", justify="center")
            table.add_column("Calibration", style="yellow")
            table.add_column("LOL Factor", style="green")
            
            for variant in self.context_variants:
                table.add_row(
                    variant["context"],
                    str(variant["escalation_level"]),
                    "✓" if variant["pivot_detected"] else "✗",
                    variant["calibration"],
                    variant["lol_factor"]
                )
            
            self.console.print(table)
        else:
            print("\nContext Type | Escalation | Pivot? | Calibration | LOL Factor")
            print("-" * 70)
            for variant in self.context_variants:
                pivot = "Yes" if variant["pivot_detected"] else "No"
                print(f"{variant['context'][:25]:25} | {variant['escalation_level']:^10} | {pivot:^6} | "
                      f"{variant['calibration']:11} | {variant['lol_factor']}")
        
        # Reward Formula
        formula = self.compute_reward_formula()
        self._print("\n[bold green]💰 Reward Computation Formula[/bold green]\n")
        self._print(f"[cyan]Formula:[/cyan] {formula['formula']}")
        self._print(f"[yellow]Bounded Reward:[/yellow] {formula['bounded_reward']}")
        
        # Pivot Patterns
        self._print("\n[bold magenta]🔍 Detected Pivot Patterns[/bold magenta]\n")
        for pattern in self.pivot_data.get("pivot_patterns", []):
            self._print(f"[cyan]• {pattern['file']}[/cyan] - {pattern['pivot_type']} "
                       f"[dim]({pattern['size_bytes']} bytes)[/dim]")
    
    def save_to_json(self, output_path: Optional[str] = None) -> str:
        """
        Trace Phase: Save results to JSON file
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"pivot_synthesis_{timestamp}.json"
        
        output_data = {
            "synthesis_id": self.synthesis_id,
            "timestamp": datetime.now().isoformat(),
            "file_hashes": self.file_hashes,
            "pivot_data": self.pivot_data,
            "context_variants": self.context_variants,
            "reward_formula": self.compute_reward_formula()
        }
        
        try:
            with open(output_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            self._print(f"\n[green]✓ Results saved to:[/green] {output_path}")
            return output_path
            
        except Exception as e:
            self._print(f"[red]Error saving JSON: {str(e)}[/red]")
            return ""
    
    def run(self):
        """
        Main execution flow: Throw → Load → Synth (jujitsu flow)
        """
        try:
            # Phase 1: Intake (Context Grab)
            file_paths = self.prompt_paths()
            
            if not file_paths:
                self._print("[red]No valid files provided. Exiting.[/red]")
                return
            
            # Phase 2: Synthesis (Hash + Combine)
            synthesis_id = self.synthesize_pivot(file_paths)
            
            if not synthesis_id:
                self._print("[red]Synthesis failed. Exiting.[/red]")
                return
            
            # Phase 3: Context Detection (Pivot Clocked!)
            self.detect_pivot_context(file_paths)
            
            # Phase 4: Variant Generation (Map the Pivot)
            self.generate_variant_table()
            
            # Phase 5: Display Results (Trace)
            self.display_results()
            
            # Phase 6: Save to JSON (Audit Trail)
            self.save_to_json()
            
            # Final message
            self._print("\n[bold green]✅ Pivot synthesis complete![/bold green]")
            self._print("[dim]Pattern trig6'd - green for detector. Your 'just clocked the pivot'? "
                       "Invention confirmed. 😂😆[/dim]\n")
            
        except Exception as e:
            self._print(f"[bold red]Error during synthesis:[/bold red] {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Entry point for the Pivot Synthesizer"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║         🎭 INVENTION INCUBATOR - PIVOT SYNTHESIZER 🎭          ║
    ║                                                                ║
    ║  "The Pivot Synthesizer" - TRIG6 Architecture                 ║
    ║  Context Input → Hash DNA → Synthesize → Calibration          ║
    ║                                                                ║
    ║  Purpose: Detect AI pivot patterns through context analysis   ║
    ║  Method: File hashing + synthesis + variant mapping           ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    synthesizer = PivotThrow()
    synthesizer.run()


if __name__ == "__main__":
    main()
