#!/usr/bin/env python3
"""
FlameLang to LLVM Compiler
SAGCO Boot Identity Pipeline (SBIP)

Entity: Strategickhaos DAO LLC
EIN: 39-2923503
Wyoming: 2025-001708194
License: Proprietary

Invention ID: INV-102
"""

import sys
import argparse
from typing import List, Optional

try:
    from llvmlite import ir
    from llvmlite import binding as llvm
except ImportError:
    print("ERROR: llvmlite not installed. Install with: pip3 install llvmlite")
    sys.exit(1)


class FlameLangCompiler:
    """Compiles FlameLang source to LLVM IR"""
    
    def __init__(self):
        # Initialize LLVM targets (required for execution)
        try:
            llvm.initialize()
        except (RuntimeError, AttributeError):
            pass  # Already initialized in newer versions
        
        try:
            llvm.initialize_native_target()
        except (RuntimeError, AttributeError):
            pass
            
        try:
            llvm.initialize_native_asmprinter()
        except (RuntimeError, AttributeError):
            pass
        
        # Create LLVM module
        self.module = ir.Module(name="flamelang_module")
        
        try:
            self.module.triple = llvm.get_default_triple()
        except:
            # If triple detection fails, use a default
            self.module.triple = "x86_64-unknown-linux-gnu"
        
        # Create builder
        self.builder = None
        
    def compile_expression(self, expression: str) -> Optional[int]:
        """
        Compile and execute a simple FlameLang expression.
        Supports: add, sub, mul, div
        
        Example: "add 5 3" returns 8
        """
        tokens = expression.strip().split()
        
        if len(tokens) < 3:
            print(f"ERROR: Invalid expression: {expression}")
            return None
            
        op = tokens[0].lower()
        
        try:
            a = int(tokens[1])
            b = int(tokens[2])
        except ValueError:
            print(f"ERROR: Invalid operands in: {expression}")
            return None
        
        # Create function type (int32 -> int32)
        fnty = ir.FunctionType(ir.IntType(32), [])
        
        # Create function
        function = ir.Function(self.module, fnty, name="flamelang_main")
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        
        # Create constants
        const_a = ir.Constant(ir.IntType(32), a)
        const_b = ir.Constant(ir.IntType(32), b)
        
        # Perform operation
        if op == "add":
            result = self.builder.add(const_a, const_b, name="add_result")
        elif op == "sub":
            result = self.builder.sub(const_a, const_b, name="sub_result")
        elif op == "mul":
            result = self.builder.mul(const_a, const_b, name="mul_result")
        elif op == "div":
            result = self.builder.sdiv(const_a, const_b, name="div_result")
        else:
            print(f"ERROR: Unknown operation: {op}")
            return None
        
        # Return result
        self.builder.ret(result)
        
        # Verify and execute
        return self.execute_function(function)
    
    def execute_function(self, function) -> Optional[int]:
        """Execute LLVM IR function and return result"""
        try:
            # Create execution engine
            llvm_ir = str(self.module)
            mod = llvm.parse_assembly(llvm_ir)
            mod.verify()
            
            # Try to get target
            try:
                target = llvm.Target.from_default_triple()
            except:
                # Fallback to x86_64 if auto-detection fails
                target = llvm.Target.from_triple("x86_64-unknown-linux-gnu")
            
            target_machine = target.create_target_machine()
            
            # Create JIT engine
            backing_mod = llvm.parse_assembly("")
            engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
            
            # Add module
            engine.add_module(mod)
            engine.finalize_object()
            
            # Get function pointer and execute
            func_ptr = engine.get_function_address(function.name)
            
            from ctypes import CFUNCTYPE, c_int32
            cfunc = CFUNCTYPE(c_int32)(func_ptr)
            result = cfunc()
            
            return result
            
        except Exception as e:
            print(f"ERROR executing LLVM IR: {e}")
            return None
    
    def get_ir(self) -> str:
        """Return LLVM IR as string"""
        return str(self.module)
    
    def save_ir(self, filename: str):
        """Save LLVM IR to file"""
        with open(filename, 'w') as f:
            f.write(self.get_ir())
        print(f"LLVM IR saved to: {filename}")


def print_banner():
    """Print SAGCO banner"""
    banner = """
   ██████╗  █████╗  ██████╗  ██████╗ ██████╗ 
  ██╔════╝ ██╔══██╗██╔════╝ ██╔════╝██╔═══██╗
  ╚█████╗  ███████║██║  ███╗██║     ██║   ██║
   ╚═══██╗ ██╔══██║██║   ██║██║     ██║   ██║
  ██████╔╝ ██║  ██║╚██████╔╝╚██████╗╚██████╔╝
  ╚═════╝  ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ 
  
  FlameLang → LLVM Compiler v1.0
  RATIO EX NIHILO - From Nothing, Through Reason
"""
    print(banner)


def main():
    parser = argparse.ArgumentParser(
        description="FlameLang to LLVM Compiler - SAGCO SBIP Component"
    )
    parser.add_argument(
        "--eval", 
        type=str,
        help="Evaluate a FlameLang expression (e.g., 'add 5 3')"
    )
    parser.add_argument(
        "--source",
        type=str,
        help="Compile FlameLang source file"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output LLVM IR file"
    )
    parser.add_argument(
        "--ir-only",
        action="store_true",
        help="Generate IR without execution"
    )
    parser.add_argument(
        "--banner",
        action="store_true",
        help="Show SAGCO banner"
    )
    
    args = parser.parse_args()
    
    if args.banner or len(sys.argv) == 1:
        print_banner()
        if len(sys.argv) == 1:
            parser.print_help()
        return
    
    compiler = FlameLangCompiler()
    
    if args.eval:
        print(f"🔥 Evaluating: {args.eval}")
        result = compiler.compile_expression(args.eval)
        
        if result is not None:
            print(f"✓ Result: {result}")
            
            if args.output:
                compiler.save_ir(args.output)
            elif args.ir_only:
                print("\n=== LLVM IR ===")
                print(compiler.get_ir())
        else:
            print("✗ Compilation failed")
            sys.exit(1)
    
    elif args.source:
        print(f"🔥 Compiling: {args.source}")
        try:
            with open(args.source, 'r') as f:
                source = f.read()
            
            # For now, compile as single expression
            result = compiler.compile_expression(source.strip())
            
            if result is not None:
                print(f"✓ Result: {result}")
                
                if args.output:
                    compiler.save_ir(args.output)
            else:
                print("✗ Compilation failed")
                sys.exit(1)
                
        except FileNotFoundError:
            print(f"ERROR: File not found: {args.source}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
