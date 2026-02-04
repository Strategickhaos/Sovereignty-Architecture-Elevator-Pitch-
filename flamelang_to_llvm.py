#!/usr/bin/env python3
"""
FlameLang to LLVM Compiler
flamelang_to_llvm.py

Compiles FlameLang source to optimized native x86_64 binaries via LLVM.
Part of SAGCO Boot Identity Pipeline (SBIP).

Entity: Strategickhaos DAO LLC
EIN: 39-2923503
Wyoming: 2025-001708194

Usage:
    python3 flamelang_to_llvm.py <source_file>
    python3 flamelang_to_llvm.py --eval "add 5 3"
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm
import subprocess
import sys
import os

# Initialize LLVM targets for compilation
# Note: llvm.initialize() is deprecated in newer versions
llvm.initialize_all_targets()
llvm.initialize_all_asmprinters()

VERSION = "1.0.0"
DEFAULT_OPERATION = "add 0 0"  # Default FlameLang program
BANNER = f"""
╔══════════════════════════════════════════════════════════╗
║  FlameLang Compiler v{VERSION}                              ║
║  SAGCO Boot Identity Pipeline                            ║
║  Strategickhaos DAO LLC                                  ║
║  "Ratio Ex Nihilo" - From Nothing, Through Reason        ║
╚══════════════════════════════════════════════════════════╝
"""

def parse_flame(source: str) -> list:
    """
    Parse FlameLang source into AST.
    
    Supported operations (v1.0):
        add <a> <b>   - Addition
        sub <a> <b>   - Subtraction
        mul <a> <b>   - Multiplication
        div <a> <b>   - Division
        ret <val>     - Return value
    """
    ops = []
    lines = source.strip().split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        parts = line.split()
        if len(parts) >= 3:
            op = parts[0].lower()
            try:
                a = int(parts[1])
                b = int(parts[2])
                ops.append((op, a, b))
            except ValueError:
                # Variable references - future feature
                print(f"Warning: Line {line_num}: Could not parse integers from '{line}'. Expected format: <op> <int> <int>")
                ops.append((op, parts[1], parts[2]))
        elif len(parts) == 2 and parts[0].lower() == 'ret':
            try:
                ops.append(('ret', int(parts[1]), None))
            except ValueError:
                print(f"Warning: Line {line_num}: Could not parse return value from '{line}'. Expected format: ret <int>")
    
    return ops if ops else [('add', 0, 0)]  # Default: return 0


def emit_ir(ops: list) -> ir.Module:
    """
    Emit LLVM IR from parsed operations.
    """
    module = ir.Module(name="flamelang")
    module.triple = llvm.get_default_triple()
    
    # Define main function: int main()
    func_type = ir.FunctionType(ir.IntType(32), [])
    func = ir.Function(module, func_type, name="main")
    func.attributes.add("nounwind")
    
    block = func.append_basic_block("entry")
    builder = ir.IRBuilder(block)
    
    result = ir.Constant(ir.IntType(32), 0)
    
    for op in ops:
        opcode = op[0]
        
        if opcode == 'add':
            a = ir.Constant(ir.IntType(32), op[1]) if isinstance(op[1], int) else op[1]
            b = ir.Constant(ir.IntType(32), op[2]) if isinstance(op[2], int) else op[2]
            result = builder.add(a, b, name="add_result")
            
        elif opcode == 'sub':
            a = ir.Constant(ir.IntType(32), op[1])
            b = ir.Constant(ir.IntType(32), op[2])
            result = builder.sub(a, b, name="sub_result")
            
        elif opcode == 'mul':
            a = ir.Constant(ir.IntType(32), op[1])
            b = ir.Constant(ir.IntType(32), op[2])
            result = builder.mul(a, b, name="mul_result")
            
        elif opcode == 'div':
            a = ir.Constant(ir.IntType(32), op[1])
            b = ir.Constant(ir.IntType(32), op[2])
            # Check for division by zero
            if isinstance(op[2], int) and op[2] == 0:
                print("Warning: Division by zero detected. Using 1 as divisor to avoid undefined behavior.")
                b = ir.Constant(ir.IntType(32), 1)
            result = builder.sdiv(a, b, name="div_result")
            
        elif opcode == 'ret':
            result = ir.Constant(ir.IntType(32), op[1])
    
    builder.ret(result)
    return module


def optimize_module(llvm_mod) -> None:
    """
    Apply LLVM optimization passes.
    """
    try:
        # Try new API first (llvmlite 0.40+)
        pm = llvm.create_new_module_pass_manager()
    except AttributeError:
        # Fallback to old API
        pm = llvm.create_module_pass_manager()
    
    # Optimization passes
    try:
        pm.add_global_dce_pass()              # Dead code elimination
        pm.add_dead_arg_elimination_pass()    # Dead argument elimination
        pm.add_aggressive_dce_pass()          # Aggressive DCE
        pm.add_loop_vectorize_pass()          # Auto-vectorization
        pm.add_instruction_combining_pass()   # Instruction combining
        pm.add_sccp_pass()                    # Sparse conditional constant propagation
        pm.add_cfg_simplification_pass()      # Control flow simplification
        pm.add_gvn_pass()                     # Global value numbering
        pm.add_licm_pass()                    # Loop invariant code motion
        
        pm.run(llvm_mod)
    except AttributeError:
        # Some optimization passes may not be available in newer versions
        # In that case, rely on the target machine's optimization level
        pass


def compile_to_object(module: ir.Module, output_path: str = "flamelang.o") -> str:
    """
    Compile LLVM IR to native object file.
    """
    llvm_ir = str(module)
    llvm_mod = llvm.parse_assembly(llvm_ir)
    llvm_mod.verify()
    
    # Apply optimizations
    optimize_module(llvm_mod)
    
    # Create target machine with optimizations
    target = llvm.Target.from_default_triple()
    
    # Get host CPU type or use generic
    try:
        cpu = llvm.get_host_cpu_name()
    except Exception:
        cpu = "generic"
    
    target_machine = target.create_target_machine(
        cpu=cpu,
        features="",
        opt=3,  # -O3
        reloc="pic",
        codemodel="default"
    )
    
    # Emit object code
    obj_code = target_machine.emit_object(llvm_mod)
    
    with open(output_path, "wb") as f:
        f.write(obj_code)
    
    return output_path


def link_executable(obj_path: str, output_path: str = "flamelang_exec") -> str:
    """
    Link object file to executable using clang (safer, handles CRT/libc).
    """
    try:
        # Use clang - handles CRT startup, libc, dynamic loader automatically
        subprocess.run(
            ["clang", obj_path, "-O3", "-o", output_path],
            check=True, capture_output=True
        )
        return output_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to gcc
        try:
            subprocess.run(
                ["gcc", obj_path, "-O3", "-o", output_path],
                check=True, capture_output=True
            )
            return output_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Warning: Linking failed. Object file at: {obj_path}")
            print("Install clang or gcc to link: apt install clang")
            return obj_path


def main():
    print(BANNER)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  flamelang_to_llvm.py <source_file>")
        print("  flamelang_to_llvm.py --eval \"add 5 3\"")
        print("  flamelang_to_llvm.py --ir \"add 5 3\"  # Show LLVM IR only")
        sys.exit(1)
    
    # Parse arguments
    if sys.argv[1] == "--eval":
        source = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OPERATION
    elif sys.argv[1] == "--ir":
        source = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OPERATION
        ops = parse_flame(source)
        module = emit_ir(ops)
        print("=== LLVM IR ===")
        print(module)
        sys.exit(0)
    else:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
    
    # Compile
    print(f"[*] Parsing source...")
    ops = parse_flame(source)
    print(f"    Found {len(ops)} operations")
    
    print(f"[*] Generating LLVM IR...")
    module = emit_ir(ops)
    
    print(f"[*] Compiling to native code (x86_64, -O3)...")
    obj_path = compile_to_object(module)
    print(f"    Object: {obj_path}")
    
    print(f"[*] Linking executable...")
    exec_path = link_executable(obj_path)
    print(f"    Executable: {exec_path}")
    
    # Get file sizes
    obj_size = os.path.getsize(obj_path)
    exec_size = os.path.getsize(exec_path) if os.path.exists(exec_path) else 0
    
    print(f"\n[✓] Compilation complete!")
    print(f"    Object size: {obj_size} bytes")
    if exec_size:
        print(f"    Executable size: {exec_size} bytes")
    print(f"\n    Run with: ./{exec_path}")


if __name__ == "__main__":
    main()
