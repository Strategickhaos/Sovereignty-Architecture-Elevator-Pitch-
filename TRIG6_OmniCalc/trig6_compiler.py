# trig6_compiler.py
"""
TRIG6 Compiler - Parser and compiler for .t6 micro-language.
Compiles .t6 scripts to VM operations and executes them.
"""

import math
from typing import List, Callable, Dict, Any

from trig6_vm import Trig6VM


class Trig6Compiler:
    """Compiler for .t6 micro-language to VM operations."""
    
    def __init__(self):
        self.vm = Trig6VM()
        self.vars: Dict[str, float] = {}  # User-defined variables
    
    def parse_expr(self, expr: str) -> float:
        """
        Evaluate simple math expression with variables and pi.
        Supports: pi, basic arithmetic (+, -, *, /), user variables.
        """
        expr = expr.strip()
        
        # Replace pi with actual value
        expr = expr.replace("pi", str(math.pi))
        
        # Replace user-defined variables
        for var_name, var_value in self.vars.items():
            expr = expr.replace(var_name, str(var_value))
        
        # Safely evaluate the expression
        try:
            # Use eval with restricted namespace for safety
            result = float(eval(expr, {"__builtins__": {}}, {}))
            return result
        except Exception as e:
            raise ValueError(f"Failed to parse expression '{expr}': {e}")
    
    def compile_line(self, line: str) -> Callable[[], None]:
        """
        Compile a single line of .t6 code to a VM operation.
        Returns a callable that executes the operation.
        """
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith("#"):
            return lambda: None
        
        parts = line.split()
        cmd = parts[0].lower()
        
        # === Variable assignment ===
        if cmd == "set" and len(parts) >= 3:
            var_name = parts[1]
            expr = " ".join(parts[2:])
            val = self.parse_expr(expr)
            
            def op_set_var():
                self.vars[var_name] = val
            
            return op_set_var
        
        # === Theta operations ===
        elif cmd == "theta" and len(parts) >= 2:
            expr = " ".join(parts[1:])
            val = self.parse_expr(expr)
            return lambda: self.vm.op_set_theta(val)
        
        elif cmd == "deg" and len(parts) >= 2:
            expr = " ".join(parts[1:])
            deg = self.parse_expr(expr)
            return lambda: self.vm.op_set_theta_degrees(deg)
        
        elif cmd == "theta_opt" and len(parts) >= 2:
            expr = " ".join(parts[1:])
            val = self.parse_expr(expr)
            return lambda: self.vm.op_set_theta_opt(val)
        
        # === Alpha operations ===
        elif cmd == "alpha" and len(parts) >= 2:
            expr = " ".join(parts[1:])
            val = self.parse_expr(expr)
            return lambda: self.vm.op_set_alpha(val)
        
        elif cmd == "blend" and len(parts) >= 2:
            mode = parts[1].lower()
            enable = (mode == "on")
            return lambda: self.vm.op_toggle_blend(enable)
        
        # === Computation ===
        elif cmd == "step":
            return self.vm.op_step
        
        # === Output ===
        elif cmd == "state":
            return lambda: print(self.vm.snapshot())
        
        # === Conditional execution ===
        elif cmd == "if" and "then" in parts:
            # Parse: if <left> <op> <right> then <cmd...>
            try:
                then_idx = parts.index("then")
                cond_parts = parts[1:then_idx]
                cmd_parts = parts[then_idx + 1:]
                
                if len(cond_parts) < 3:
                    raise ValueError("Conditional requires: if <left> <op> <right> then <cmd>")
                
                left = cond_parts[0]
                op = cond_parts[1]
                right_expr = " ".join(cond_parts[2:])
                
                # Compile the conditional command
                sub_cmd = self.compile_line(" ".join(cmd_parts))
                
                def eval_and_execute():
                    # Get left value (from metrics or variables)
                    if left == "resonance":
                        lval = self.vm.state.resonance
                    elif left == "drift":
                        lval = self.vm.state.drift
                    elif left == "noise":
                        lval = self.vm.state.noise
                    elif left in self.vars:
                        lval = self.vars[left]
                    else:
                        lval = 0.0  # Default to 0 if undefined
                    
                    # Get right value
                    rval = self.parse_expr(right_expr)
                    
                    # Evaluate condition
                    condition_met = False
                    if op == "<":
                        condition_met = lval < rval
                    elif op == ">":
                        condition_met = lval > rval
                    elif op == "=":
                        condition_met = abs(lval - rval) < 1e-6
                    elif op == "<=":
                        condition_met = lval <= rval
                    elif op == ">=":
                        condition_met = lval >= rval
                    else:
                        raise ValueError(f"Unknown operator: {op}")
                    
                    # Execute if condition is met
                    if condition_met:
                        sub_cmd()
                
                return eval_and_execute
                
            except ValueError as e:
                raise ValueError(f"Conditional parse error: {e}")
        
        # === Control flow ===
        elif cmd == "exit":
            return lambda: print("Script exit.")
        
        # === Unknown command ===
        else:
            raise ValueError(f"Unknown command: {line}")
    
    def compile(self, script: str) -> List[Callable[[], None]]:
        """
        Compile entire .t6 script to list of VM operations.
        
        Args:
            script: Full .t6 script text
        
        Returns:
            List of callable operations
        """
        ops = []
        line_number = 0
        
        for line in script.splitlines():
            line_number += 1
            try:
                op = self.compile_line(line)
                ops.append(op)
            except ValueError as e:
                print(f"Compile error on line {line_number}: {e}")
                print(f"  Line: {line}")
        
        return ops
    
    def run(self, ops: List[Callable[[], None]]) -> None:
        """
        Execute compiled operations sequentially.
        
        Args:
            ops: List of compiled operations
        """
        for op in ops:
            try:
                op()
            except Exception as e:
                print(f"Runtime error: {e}")
    
    def compile_and_run(self, script: str) -> None:
        """
        Compile and execute a .t6 script in one call.
        
        Args:
            script: Full .t6 script text
        """
        ops = self.compile(script)
        self.run(ops)


# Example usage and testing
if __name__ == "__main__":
    compiler = Trig6Compiler()
    
    # Test script
    test_script = """
# Test TRIG6 compiler
theta pi/4
alpha 0.5
step
state

# Test conditional
set low_res 0.5
if resonance > low_res then theta_opt pi/3

step
state
"""
    
    print("=== Running Test Script ===\n")
    compiler.compile_and_run(test_script)
    
    print("\n=== Test Complete ===")
