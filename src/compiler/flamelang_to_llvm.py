#!/usr/bin/env python3
"""
FlameLang to LLVM Compiler - v1.0
Optimized x86_64 native binary compiler with LLVM backend
"""

import llvmlite.ir as ir
import llvmlite.binding as llvm
import subprocess
import sys

# Initialize LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


def emit_ir(ops):
    """
    Generate LLVM IR from FlameLang operations.
    
    Args:
        ops: List of operations, e.g., [('add', 5, 3), ('mul', 2, 4)]
    
    Returns:
        LLVM IR Module
    """
    module = ir.Module(name="flamelang")
    func_type = ir.FunctionType(ir.IntType(32), [])
    func = ir.Function(module, func_type, name="main")
    block = func.append_basic_block("entry")
    builder = ir.IRBuilder(block)
    
    # Initialize result only if there are operations
    result = None
    
    for op in ops:
        if op[0] == 'add':
            a = ir.Constant(ir.IntType(32), op[1])
            b = ir.Constant(ir.IntType(32), op[2])
            result = builder.add(a, b)
        elif op[0] == 'sub':
            a = ir.Constant(ir.IntType(32), op[1])
            b = ir.Constant(ir.IntType(32), op[2])
            result = builder.sub(a, b)
        elif op[0] == 'mul':
            a = ir.Constant(ir.IntType(32), op[1])
            b = ir.Constant(ir.IntType(32), op[2])
            result = builder.mul(a, b)
    
    # Return result or 0 if no operations
    if result is None:
        result = ir.Constant(ir.IntType(32), 0)
    builder.ret(result)
    return module


def optimize_and_compile(module, output_name="flamelang_exec"):
    """
    Optimize and compile LLVM IR to native x86_64 binary.
    
    Args:
        module: LLVM IR Module
        output_name: Output binary filename
    
    Returns:
        Path to compiled binary
    """
    # Parse the IR module
    llvm_mod = llvm.parse_assembly(str(module))
    
    # Create optimization pass manager
    pm = llvm.create_module_pass_manager()
    pm.add_global_dce_pass()
    pm.add_aggressive_dce_pass()
    pm.add_loop_vectorize_pass()
    pm.add_instruction_combining_pass()
    pm.run(llvm_mod)
    
    # Create target machine with x86_64 optimizations
    target = llvm.Target.from_default_triple().create_target_machine(
        opt=3,  # -O3 optimization level
        cpu='native'  # Native CPU features (AVX2 if available)
    )
    
    # Emit object file
    obj = target.emit_object(llvm_mod)
    obj_filename = f"{output_name}.o"
    with open(obj_filename, "wb") as f:
        f.write(obj)
    
    # Link to executable binary
    try:
        subprocess.run(
            ["ld", obj_filename, "-o", output_name],
            check=True,
            capture_output=True
        )
        return output_name
    except subprocess.CalledProcessError as e:
        print(f"Linking failed: {e.stderr.decode()}", file=sys.stderr)
        raise


def parse_flame(source):
    """
    Parse FlameLang source code into operations.
    
    This is a stub implementation. Extend based on FlameLang syntax.
    
    Args:
        source: FlameLang source code string
    
    Returns:
        List of operations
    """
    # Stub: Simple operation parser
    # Format: "add 5 3\nmul 2 4"
    ops = []
    for line in source.strip().split('\n'):
        parts = line.split()
        if len(parts) == 3:
            op = parts[0]
            arg1 = int(parts[1])
            arg2 = int(parts[2])
            ops.append((op, arg1, arg2))
    return ops


def main():
    """
    Main compiler entry point.
    """
    if len(sys.argv) < 2:
        print("Usage: flamelang_to_llvm.py <source_file> [output_binary]")
        sys.exit(1)
    
    source_file = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else "flamelang_exec"
    
    # Read source
    with open(source_file, 'r') as f:
        source = f.read()
    
    # Compile pipeline
    ops = parse_flame(source)
    module = emit_ir(ops)
    binary = optimize_and_compile(module, output_name)
    
    print(f"✅ Compiled to: {binary}")
    print(f"📊 Optimizations: -O3, DCE, vectorization, native CPU features")


if __name__ == "__main__":
    main()
