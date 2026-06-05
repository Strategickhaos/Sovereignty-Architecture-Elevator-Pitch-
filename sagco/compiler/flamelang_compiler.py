#!/usr/bin/env python3
"""
FlameLang Compiler - SAGCO CPU Layer v1.0

Compiles FlameLang source to either:
1. LLVM IR → Native binaries (via LLVM backend)
2. SAGCO Bytecode → VM execution

Part of the Sovereignty Architecture Guaranteed Compute Overlay (SAGCO)
"""

import sys
import os
from pathlib import Path

# Bytecode Opcodes for SAGCO CPU VM
OP_PUSH = 0x01
OP_ADD = 0x10
OP_SUB = 0x11
OP_MUL = 0x12
OP_DIV = 0x13
OP_POP = 0x02
OP_CALL = 0x20
OP_RET = 0x21
OP_HALT = 0xFF


def compile_to_bytecode(source):
    """
    Compile FlameLang source to SAGCO bytecode.
    
    This is a placeholder parser. In production, this would:
    - Parse FlameLang syntax
    - Generate AST
    - Emit bytecode from AST
    
    Example bytecode: "push 5; push 3; add" → [0x01, 0x05, 0x01, 0x03, 0x10]
    """
    bytecode = bytearray()
    
    # Placeholder: Simple arithmetic example
    # push 5
    bytecode.extend([OP_PUSH, 5])
    # push 3
    bytecode.extend([OP_PUSH, 3])
    # add
    bytecode.extend([OP_ADD])
    # halt
    bytecode.extend([OP_HALT])
    
    return bytecode


def compile_to_llvm(source):
    """
    Compile FlameLang source to LLVM IR.
    
    This generates LLVM IR that can be compiled to native code.
    Requires llvmlite to be installed for production use.
    
    Returns LLVM IR as a string.
    """
    try:
        import llvmlite.ir as ir
        import llvmlite.binding as llvm
        
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        # Create module
        module = ir.Module(name="flamelang")
        module.triple = llvm.get_default_triple()
        
        # Create main function: int main() { return 42; }
        func_type = ir.FunctionType(ir.IntType(32), [])
        func = ir.Function(module, func_type, name="main")
        block = func.append_basic_block("entry")
        builder = ir.IRBuilder(block)
        
        # Placeholder: Return 42
        builder.ret(ir.Constant(ir.IntType(32), 42))
        
        return str(module), module
        
    except ImportError:
        # Fallback if llvmlite not installed
        print("Warning: llvmlite not installed. Returning placeholder LLVM IR.", file=sys.stderr)
        placeholder_ir = """
; ModuleID = 'flamelang'
target triple = "x86_64-unknown-linux-gnu"

define i32 @main() {
entry:
  ret i32 42
}
"""
        return placeholder_ir, None


def compile_to_object(llvm_ir_str, llvm_module, output_path):
    """
    Compile LLVM IR to native object file.
    Requires llvmlite to be installed.
    """
    try:
        import llvmlite.binding as llvm
        
        # Parse IR
        if llvm_module is None:
            llvm_module = llvm.parse_assembly(llvm_ir_str)
        
        # Get target machine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        
        # Emit object code
        obj_code = target_machine.emit_object(llvm_module)
        
        # Write to file
        with open(output_path, "wb") as f:
            f.write(obj_code)
        
        return True
        
    except ImportError:
        print("Error: llvmlite not installed. Cannot generate object file.", file=sys.stderr)
        print("Install with: pip install llvmlite", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error compiling to object: {e}", file=sys.stderr)
        return False


def main():
    """Main compiler entry point."""
    if len(sys.argv) < 2:
        print("Usage: flamelang_compiler.py <mode> [source_file]")
        print("Modes:")
        print("  native  - Compile to LLVM IR and native object file")
        print("  vm      - Compile to SAGCO bytecode for VM execution")
        print("  ir      - Compile to LLVM IR only (human-readable)")
        sys.exit(1)
    
    mode = sys.argv[1]
    source_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Read source (or use placeholder)
    if source_file and os.path.exists(source_file):
        with open(source_file, 'r') as f:
            source = f.read()
    else:
        source = "example"  # Placeholder
    
    # Create artifacts directory
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    
    if mode == "vm":
        # Compile to bytecode
        print("Compiling FlameLang to SAGCO bytecode...")
        bytecode = compile_to_bytecode(source)
        
        output_path = artifacts_dir / "example.bc"
        with open(output_path, "wb") as f:
            f.write(bytecode)
        
        print(f"Bytecode written to: {output_path}")
        print(f"Size: {len(bytecode)} bytes")
        print(f"Hex: {bytecode.hex()}")
        
    elif mode == "native":
        # Compile to native
        print("Compiling FlameLang to LLVM IR and native object...")
        ir_str, llvm_module = compile_to_llvm(source)
        
        # Write IR
        ir_path = artifacts_dir / "example.ll"
        with open(ir_path, "w") as f:
            f.write(ir_str)
        print(f"LLVM IR written to: {ir_path}")
        
        # Compile to object
        obj_path = artifacts_dir / "example.o"
        if compile_to_object(ir_str, llvm_module, obj_path):
            print(f"Object file written to: {obj_path}")
            print("\nTo link and create executable:")
            print(f"  clang {obj_path} -o {artifacts_dir / 'example'}")
        
    elif mode == "ir":
        # LLVM IR only
        print("Compiling FlameLang to LLVM IR...")
        ir_str, _ = compile_to_llvm(source)
        
        ir_path = artifacts_dir / "example.ll"
        with open(ir_path, "w") as f:
            f.write(ir_str)
        print(f"LLVM IR written to: {ir_path}")
        print("\nIR Contents:")
        print(ir_str)
        
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
