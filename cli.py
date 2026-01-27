"""TRIG6 CLI - Interactive mathematician calculator tool."""
import sys
import math
from main import omni_calc


def format_trig6(result):
    """Format TRIG6 results for display."""
    trig6_vals = result['trig6']
    labels = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']
    
    output = []
    output.append("TRIG6 Results:")
    output.append("-" * 50)
    
    for label, val in zip(labels, trig6_vals):
        if val == float('inf'):
            output.append(f"  {label:>4}: ∞ (singularity)")
        elif val == float('-inf'):
            output.append(f"  {label:>4}: -∞ (singularity)")
        else:
            output.append(f"  {label:>4}: {val:>12.8f}")
    
    output.append("")
    output.append(f"Unit Circle: ({result['unit_circle'][0]:.8f}, {result['unit_circle'][1]:.8f})")
    
    if result['roll_offset'] == float('inf'):
        output.append(f"Rolling Offset: ∞ (singularity)")
    else:
        output.append(f"Rolling Offset: {result['roll_offset']:.8f}")
    
    dro = result['double_roll']
    dro_str = f"({dro[0]:.8f}, "
    if dro[1] == float('inf'):
        dro_str += "∞)"
    else:
        dro_str += f"{dro[1]:.8f})"
    output.append(f"Double Rolling Offset: {dro_str}")
    
    return "\n".join(output)


def parse_theta_expr(expr):
    """Safely parse theta expression.
    
    Supports:
    - Numeric values: '1.5708', '0.785398'
    - Math constants: 'math.pi', 'math.e'
    - Math operations: 'math.pi/4', 'math.pi/2', etc.
    """
    import re
    
    # Allow only safe characters and patterns
    if not re.match(r'^[0-9math\.\+\-\*/\(\) piePI]+$', expr):
        raise ValueError("Invalid theta expression. Use numeric values or math.pi operations.")
    
    # Create a safe namespace with only math constants and basic operations
    safe_dict = {
        'math': math,
        'pi': math.pi,
        'e': math.e,
        'PI': math.pi,
        '__builtins__': {}
    }
    
    try:
        return eval(expr, safe_dict, {})
    except Exception as e:
        raise ValueError(f"Could not evaluate theta expression: {e}")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 3 or sys.argv[1] != '--theta':
        print("TRIG6 Omni Calculator - Mathematician CLI Tool")
        print()
        print("Usage: python cli.py --theta <value>")
        print()
        print("Examples:")
        print("  python cli.py --theta 'math.pi/4'")
        print("  python cli.py --theta '0.785398'")
        print("  python cli.py --theta 'math.pi/2'")
        print()
        sys.exit(1)
    
    theta_expr = sys.argv[2]
    
    try:
        # Parse theta expression safely
        theta = parse_theta_expr(theta_expr)
        
        print(f"Computing TRIG6 for θ = {theta_expr}")
        print(f"(θ ≈ {theta:.8f} radians)")
        print()
        
        result = omni_calc(theta)
        print(format_trig6(result))
        
    except ZeroDivisionError:
        print("Singularity Error: Code 6 - Division by zero at danger zone.")
        print("This occurs at critical angles where trig functions are undefined.")
        sys.exit(6)
    except Exception as e:
        print(f"Error: {e}")
        print("Please provide a valid theta expression.")
        sys.exit(1)


if __name__ == '__main__':
    main()
