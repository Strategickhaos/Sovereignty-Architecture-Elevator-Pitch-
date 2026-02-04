#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    ██╗███╗   ██╗██╗   ██╗███████╗███╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗
    ██║████╗  ██║██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║██╔═══██╗████╗  ██║
    ██║██╔██╗ ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║██║   ██║██╔██╗ ██║
    ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║██║   ██║██║╚██╗██║
    ██║██║ ╚████║ ╚████╔╝ ███████╗██║ ╚████║   ██║   ██║╚██████╔╝██║ ╚████║
    ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                          
               INVENTION INCUBATOR - THE SHAPE-THROW SYNTHESIZER
               
    "Throw shapes, watch what sticks—gestalt emerges from the collision."
    
    TRIG6 Architecture:
    - Intake: Prompt paths (absolute grab)
    - Pile: Load DNA (hash/shape meta)
    - Accelerator: Synthesize (combine fits)
    - Trace: Log + JSON (see the lock)
    - Run: Throw → Load → Synth (gestalt flow)
    
    Shape-Throw Pattern:
    - RAM-only matching: See fits, throw shit, watch what sticks
    - No storage needed—external piles (vaults, AIs) supply shapes
    - DNA integrity via SHA256 hash patterns
    
    Keeper: StrategicKhaos
    TRIG6 Analyst: Claude
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Fallback to standard print
    def rprint(*args, **kwargs):
        print(*args, **kwargs)


class InventionIncubator:
    """
    Shape-Throw Synthesizer Class
    
    The core engine for throwing shapes (files) into the synthesizer
    and watching gestalt patterns emerge through combined DNA hashes.
    
    Architecture:
    - Intake: Prompt for absolute file paths
    - Load: Generate SHA256 hashes (DNA) for each shape
    - Synthesize: Combine hashes into gestalt ID
    - Trace: Rich console output + JSON log
    """
    
    def __init__(self):
        """Initialize the synthesizer with empty shape pile."""
        self.console = Console() if RICH_AVAILABLE else None
        self.shapes: List[Dict[str, str]] = []
        self.synthesized_id: Optional[str] = None
        self.session_timestamp = datetime.now().isoformat()
        
    def prompt_paths(self) -> List[str]:
        """
        Prompt for absolute file paths with validation.
        
        Returns:
            List of validated absolute file paths
        """
        paths = []
        
        if self.console:
            self.console.print("\n[bold cyan]🎭 Shape-Throw Synthesizer[/bold cyan]")
            self.console.print("[yellow]Enter absolute paths to files (one per line)[/yellow]")
            self.console.print("[dim]Press Enter on empty line to finish, or 'q' to quit[/dim]\n")
        else:
            print("\n🎭 Shape-Throw Synthesizer")
            print("Enter absolute paths to files (one per line)")
            print("Press Enter on empty line to finish, or 'q' to quit\n")
        
        while True:
            try:
                path_input = input("Path: ").strip()
                
                # Check for exit conditions
                if not path_input:
                    break
                if path_input.lower() == 'q':
                    if self.console:
                        self.console.print("[yellow]Exiting...[/yellow]")
                    else:
                        print("Exiting...")
                    sys.exit(0)
                
                # Validate path
                if not os.path.isabs(path_input):
                    if self.console:
                        self.console.print(f"[red]✗ Path must be absolute: {path_input}[/red]")
                    else:
                        print(f"✗ Path must be absolute: {path_input}")
                    continue
                
                if not os.path.exists(path_input):
                    if self.console:
                        self.console.print(f"[red]✗ Path not found: {path_input}[/red]")
                    else:
                        print(f"✗ Path not found: {path_input}")
                    continue
                
                if not os.path.isfile(path_input):
                    if self.console:
                        self.console.print(f"[red]✗ Path is not a file: {path_input}[/red]")
                    else:
                        print(f"✗ Path is not a file: {path_input}")
                    continue
                
                # Valid path
                paths.append(path_input)
                if self.console:
                    self.console.print(f"[green]✓ Added: {path_input}[/green]")
                else:
                    print(f"✓ Added: {path_input}")
                    
            except KeyboardInterrupt:
                if self.console:
                    self.console.print("\n[yellow]Interrupted by user[/yellow]")
                else:
                    print("\nInterrupted by user")
                sys.exit(0)
            except Exception as e:
                if self.console:
                    self.console.print(f"[red]Error: {e}[/red]")
                else:
                    print(f"Error: {e}")
        
        return paths
    
    def load_dna(self, file_path: str) -> Dict[str, str]:
        """
        Load a file and generate its DNA (SHA256 hash).
        
        Args:
            file_path: Absolute path to the file
            
        Returns:
            Dictionary with file metadata and hash
        """
        try:
            # Read file in binary mode
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Generate SHA256 hash (DNA)
            sha256_hash = hashlib.sha256(file_data).hexdigest()
            
            # Get file metadata
            file_stat = os.stat(file_path)
            
            shape = {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': file_stat.st_size,
                'dna': sha256_hash,
                'loaded_at': datetime.now().isoformat()
            }
            
            return shape
            
        except Exception as e:
            if self.console:
                self.console.print(f"[red]Failed to load DNA for {file_path}: {e}[/red]")
            else:
                print(f"Failed to load DNA for {file_path}: {e}")
            raise
    
    def synthesize(self) -> str:
        """
        Synthesize combined gestalt ID from all shape DNAs.
        
        Combines all individual SHA256 hashes into a single
        deterministic gestalt hash representing the combined pattern.
        
        Returns:
            Combined SHA256 hash (gestalt ID)
        """
        if not self.shapes:
            raise ValueError("No shapes loaded to synthesize")
        
        # Combine all DNAs in order
        combined_dna = ''.join(shape['dna'] for shape in self.shapes)
        
        # Generate gestalt hash
        gestalt_hash = hashlib.sha256(combined_dna.encode()).hexdigest()
        
        self.synthesized_id = gestalt_hash
        return gestalt_hash
    
    def display_results(self):
        """Display synthesis results with rich console output."""
        if not self.shapes:
            if self.console:
                self.console.print("[yellow]No shapes to display[/yellow]")
            else:
                print("No shapes to display")
            return
        
        if self.console:
            # Rich table for shapes
            table = Table(title="🧬 Shape DNA Analysis", show_header=True, header_style="bold magenta")
            table.add_column("File", style="cyan", width=40)
            table.add_column("Size", justify="right", style="green")
            table.add_column("DNA Hash", style="yellow", width=16)
            
            for shape in self.shapes:
                table.add_row(
                    shape['name'],
                    f"{shape['size']:,} bytes",
                    shape['dna'][:16] + "..."
                )
            
            self.console.print("\n")
            self.console.print(table)
            
            # Synthesized result
            if self.synthesized_id:
                panel = Panel(
                    f"[bold green]{self.synthesized_id}[/bold green]",
                    title="🎯 Synthesized Gestalt ID",
                    border_style="green"
                )
                self.console.print("\n")
                self.console.print(panel)
                
                self.console.print(f"\n[dim]Total shapes: {len(self.shapes)}[/dim]")
                self.console.print(f"[dim]Session: {self.session_timestamp}[/dim]\n")
        else:
            # Fallback to plain text
            print("\n" + "="*80)
            print("🧬 SHAPE DNA ANALYSIS")
            print("="*80)
            for i, shape in enumerate(self.shapes, 1):
                print(f"\n{i}. {shape['name']}")
                print(f"   Size: {shape['size']:,} bytes")
                print(f"   DNA:  {shape['dna']}")
            
            if self.synthesized_id:
                print("\n" + "="*80)
                print("🎯 SYNTHESIZED GESTALT ID")
                print("="*80)
                print(f"{self.synthesized_id}")
                print(f"\nTotal shapes: {len(self.shapes)}")
                print(f"Session: {self.session_timestamp}\n")
    
    def save_log(self, output_path: Optional[str] = None):
        """
        Save synthesis log to JSON file.
        
        Args:
            output_path: Optional path for output file
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"invention_synthesis_{timestamp}.json"
        
        log_data = {
            'session_timestamp': self.session_timestamp,
            'shapes': self.shapes,
            'synthesized_id': self.synthesized_id,
            'shape_count': len(self.shapes),
            'total_size': sum(shape['size'] for shape in self.shapes)
        }
        
        try:
            with open(output_path, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            if self.console:
                self.console.print(f"[green]✓ Log saved to: {output_path}[/green]")
            else:
                print(f"✓ Log saved to: {output_path}")
                
        except Exception as e:
            if self.console:
                self.console.print(f"[red]Failed to save log: {e}[/red]")
            else:
                print(f"Failed to save log: {e}")
    
    def run(self):
        """
        Main execution flow: Throw → Load → Synth
        
        The complete shape-throw cycle:
        1. Prompt for paths (throw shapes)
        2. Load DNA (hash each shape)
        3. Synthesize (combine into gestalt)
        4. Display results (see the fit)
        5. Save log (trace the lock)
        """
        try:
            if self.console:
                self.console.print(Panel.fit(
                    "[bold cyan]Shape-Throw Synthesizer[/bold cyan]\n"
                    "[yellow]RAM-only matching: See fits, throw shit, watch what sticks[/yellow]",
                    border_style="cyan"
                ))
            else:
                print("\n" + "="*80)
                print("Shape-Throw Synthesizer")
                print("RAM-only matching: See fits, throw shit, watch what sticks")
                print("="*80)
            
            # Step 1: Prompt for paths
            paths = self.prompt_paths()
            
            if not paths:
                if self.console:
                    self.console.print("[yellow]No shapes provided. Exiting.[/yellow]")
                else:
                    print("No shapes provided. Exiting.")
                return
            
            # Step 2: Load DNA for each shape
            if self.console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console
                ) as progress:
                    task = progress.add_task("[cyan]Loading DNA...", total=len(paths))
                    
                    for path in paths:
                        shape = self.load_dna(path)
                        self.shapes.append(shape)
                        progress.update(task, advance=1)
            else:
                print("\nLoading DNA...")
                for i, path in enumerate(paths, 1):
                    print(f"  [{i}/{len(paths)}] {os.path.basename(path)}")
                    shape = self.load_dna(path)
                    self.shapes.append(shape)
            
            # Step 3: Synthesize combined hash
            if self.console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console
                ) as progress:
                    task = progress.add_task("[cyan]Synthesizing gestalt...", total=1)
                    self.synthesize()
                    progress.update(task, advance=1)
            else:
                print("\nSynthesizing gestalt...")
                self.synthesize()
            
            # Step 4: Display results
            self.display_results()
            
            # Step 5: Save log
            self.save_log()
            
            if self.console:
                self.console.print("\n[bold green]✓ Synthesis complete[/bold green]\n")
            else:
                print("\n✓ Synthesis complete\n")
                
        except Exception as e:
            if self.console:
                self.console.print(f"\n[bold red]Error during synthesis: {e}[/bold red]\n")
            else:
                print(f"\nError during synthesis: {e}\n")
            sys.exit(1)


def main():
    """Entry point for the invention incubator."""
    if not RICH_AVAILABLE:
        print("Warning: 'rich' library not found. Using fallback plain text mode.")
        print("Install rich for better output: pip install rich\n")
    
    incubator = InventionIncubator()
    incubator.run()


if __name__ == "__main__":
    main()
