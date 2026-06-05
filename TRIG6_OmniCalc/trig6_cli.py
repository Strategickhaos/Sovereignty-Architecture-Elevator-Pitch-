# trig6_cli.py
import math
import sys
import os

# Add parent directory to path for imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trig6_vm import Trig6VM


HELP_TEXT = """
TRIG6 OmniCalc – commands:

  theta <value>        set theta in radians (use 'pi/4', '1.047', etc.)
  alpha <value>        set blend alpha in [0,1]
  theta_opt <value>    set optimal theta
  step                 recompute projections, noise, drift, resonance
  state                print current state (JSON-like)
  deg <degrees>        set theta in degrees
  help                 show this help
  quit / exit          leave

Examples:
  theta pi/3
  alpha 0.3
  theta_opt pi/4
  step
  state
"""


def parse_numeric(expr: str) -> float:
    """
    Parse simple numeric expressions like:
      "1.0", "pi/4", "2*pi/3"
    Uses a safer approach than eval() by only allowing math operations.
    """
    import ast
    import operator
    
    # Replace pi with its value
    expr = expr.replace("pi", str(math.pi))
    
    # Whitelist of safe operations
    safe_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }
    
    def eval_node(node):
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op = safe_ops.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op = safe_ops.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            return op(operand)
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")
    
    try:
        tree = ast.parse(expr, mode='eval')
        return float(eval_node(tree.body))
    except Exception as e:
        # Fall back to simple float parsing if AST fails
        try:
            return float(expr)
        except ValueError:
            raise ValueError(f"Invalid numeric expression: {expr}") from e


def main():
    vm = Trig6VM(theta=math.pi / 4, alpha=0.0, theta_opt=math.pi / 4)
    print("TRIG6 OmniCalc VM")
    print("Type 'help' for commands.\n")

    while True:
        try:
            line = input("trig6> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ("quit", "exit"):
            break
        elif cmd == "help":
            print(HELP_TEXT)
        elif cmd == "theta" and len(parts) >= 2:
            try:
                val = parse_numeric("".join(parts[1:]))
                vm.op_set_theta(val)
                print(f"theta = {val:.6f} rad")
            except Exception as e:
                print(f"Error: {e}")
        elif cmd == "deg" and len(parts) >= 2:
            try:
                deg = float(parts[1])
                val = deg * math.pi / 180.0
                vm.op_set_theta(val)
                print(f"theta = {val:.6f} rad ({deg}°)")
            except Exception as e:
                print(f"Error: {e}")
        elif cmd == "alpha" and len(parts) >= 2:
            try:
                val = float(parts[1])
                vm.op_set_alpha(val)
                print(f"alpha = {vm.state.alpha:.3f}")
            except Exception as e:
                print(f"Error: {e}")
        elif cmd == "theta_opt" and len(parts) >= 2:
            try:
                val = parse_numeric("".join(parts[1:]))
                vm.op_set_theta_opt(val)
                print(f"theta_opt = {val:.6f} rad")
            except Exception as e:
                print(f"Error: {e}")
        elif cmd == "step":
            vm.op_step()
            snap = vm.snapshot()
            print(f"resonance={snap['resonance']:.4f}, drift={snap['drift']:.4f}, noise={snap['noise']:.4f}")
            if snap["danger_zones"]:
                print("danger_zones:", ", ".join(snap["danger_zones"]))
        elif cmd == "state":
            snap = vm.snapshot()
            from pprint import pprint
            pprint(snap)
        else:
            print("Unknown command. Type 'help'.")


if __name__ == "__main__":
    main()
