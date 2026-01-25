#!/usr/bin/env python3
# trig6_cli.py
"""
TRIG6 CLI - Interactive REPL for TRIG6 OmniCalc.
Provides interactive calculator with .t6 script loading capability.
"""

import math
import ast
import operator
import sys
from pathlib import Path

from trig6_vm import Trig6VM
from trig6_compiler import Trig6Compiler, SafeExpressionEvaluator


class Trig6CLI:
    """Interactive CLI for TRIG6 OmniCalc."""
    
    def __init__(self):
        self.vm = Trig6VM()
        self.running = True
    
    def print_banner(self):
        """Print welcome banner."""
        print("\n" + "=" * 60)
        print("TRIG6 OmniCalc - Interactive Calculator")
        print("Version 1.0 - Your Math, Alive")
        print("=" * 60)
        print("Type 'help' for commands, 'exit' to quit")
        print()
    
    def print_help(self):
        """Print help message."""
        help_text = """
Available Commands:
  
  === Angle Operations ===
  theta <radians>        Set theta in radians (e.g., theta pi/4)
  deg <degrees>          Set theta in degrees (e.g., deg 45)
  theta_opt <radians>    Set optimal theta
  
  === Blend Operations ===
  alpha <value>          Set alpha blend [0,1] (e.g., alpha 0.5)
  blend on|off           Toggle full hyperbolic blend
  
  === Computation ===
  step                   Compute projections and metrics
  state                  Show current VM state (detailed)
  snapshot               Show state as JSON
  
  === Script Operations ===
  load <file.t6>         Load and run a .t6 script
  
  === Utility ===
  reset                  Reset VM to initial state
  help                   Show this help
  exit                   Exit the REPL
  
Examples:
  > theta pi/4
  > alpha 0.5
  > step
  > state
  > load examples/demo_script.t6
"""
        print(help_text)
    
    def execute_command(self, line: str) -> None:
        """Execute a single command line."""
        line = line.strip()
        
        if not line:
            return
        
        parts = line.split()
        cmd = parts[0].lower()
        
        # === Help and Exit ===
        if cmd == "help":
            self.print_help()
        
        elif cmd == "exit" or cmd == "quit":
            print("Exiting TRIG6 OmniCalc. Goodbye!")
            self.running = False
        
        # === VM Operations ===
        elif cmd == "theta" and len(parts) >= 2:
            try:
                # Parse expression safely
                expr = " ".join(parts[1:])
                evaluator = SafeExpressionEvaluator({})
                val = evaluator.eval(expr)
                self.vm.op_set_theta(val)
                print(f"Set theta = {val:.6f} rad ({math.degrees(val):.2f}°)")
            except Exception as e:
                print(f"Error: {e}")
        
        elif cmd == "deg" and len(parts) >= 2:
            try:
                deg = float(parts[1])
                self.vm.op_set_theta_degrees(deg)
                print(f"Set theta = {deg}° ({deg * math.pi / 180:.6f} rad)")
            except Exception as e:
                print(f"Error: {e}")
        
        elif cmd == "theta_opt" and len(parts) >= 2:
            try:
                expr = " ".join(parts[1:])
                evaluator = SafeExpressionEvaluator({})
                val = evaluator.eval(expr)
                self.vm.op_set_theta_opt(val)
                print(f"Set theta_opt = {val:.6f} rad ({math.degrees(val):.2f}°)")
            except Exception as e:
                print(f"Error: {e}")
        
        elif cmd == "alpha" and len(parts) >= 2:
            try:
                val = float(parts[1])
                self.vm.op_set_alpha(val)
                print(f"Set alpha = {val:.6f}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif cmd == "blend" and len(parts) >= 2:
            mode = parts[1].lower()
            if mode == "on":
                self.vm.op_toggle_blend(True)
                print("Blend mode: ON (alpha = 1.0, full hyperbolic)")
            elif mode == "off":
                self.vm.op_toggle_blend(False)
                print("Blend mode: OFF (alpha = 0.0, pure circular)")
            else:
                print("Error: blend requires 'on' or 'off'")
        
        elif cmd == "step":
            self.vm.op_step()
            print("Step executed. Use 'state' to view results.")
        
        elif cmd == "state":
            self.vm.print_state()
        
        elif cmd == "snapshot":
            print(self.vm.snapshot())
        
        elif cmd == "reset":
            self.vm.reset()
            print("VM reset to initial state.")
        
        # === Script Loading ===
        elif cmd == "load" and len(parts) >= 2:
            file_path = parts[1]
            try:
                # Read script file
                with open(file_path, "r") as f:
                    script = f.read()
                
                # Create compiler and share VM state
                compiler = Trig6Compiler()
                compiler.vm = self.vm  # Share VM state with compiler
                
                # Compile and run
                print(f"Loading {file_path}...")
                ops = compiler.compile(script)
                compiler.run(ops)
                print(f"✓ Loaded and executed {file_path}")
                
            except FileNotFoundError:
                print(f"Error: File not found: {file_path}")
            except Exception as e:
                print(f"Error loading script: {e}")
        
        # === Unknown Command ===
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands.")
    
    def run(self):
        """Run the interactive REPL."""
        self.print_banner()
        
        while self.running:
            try:
                line = input("trig6> ")
                self.execute_command(line)
            except EOFError:
                print("\nExiting TRIG6 OmniCalc. Goodbye!")
                break
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")


def main():
    """Main entry point."""
    cli = Trig6CLI()
    
    # Check if script file provided as argument
    if len(sys.argv) > 1:
        script_file = sys.argv[1]
        print(f"Running script: {script_file}")
        try:
            with open(script_file, "r") as f:
                script = f.read()
            
            compiler = Trig6Compiler()
            compiler.compile_and_run(script)
            print(f"✓ Script completed: {script_file}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Run interactive REPL
        cli.run()


if __name__ == "__main__":
    main()
