#!/usr/bin/env python3
"""
SAGCO CPU VM - Stack-Based Bytecode Interpreter

A lightweight VM for executing FlameLang bytecode in a sandboxed environment.
Part of the Sovereignty Architecture Guaranteed Compute Overlay (SAGCO).

Architecture:
- Stack-based execution model (similar to Lua, Python bytecode)
- Simple opcode set for arithmetic, memory, and control flow
- Can be started as a systemd service via SBIP
- Verifies bytecode integrity before execution

Usage:
    sagco_cpu_vm.py <bytecode_file>           # Execute bytecode
    sagco_cpu_vm.py --daemon --load-dir <dir> # Run as daemon
"""

import sys
import os
import time
from pathlib import Path
from typing import List, Optional

# Bytecode Opcodes (must match compiler)
OP_PUSH = 0x01
OP_POP = 0x02
OP_ADD = 0x10
OP_SUB = 0x11
OP_MUL = 0x12
OP_DIV = 0x13
OP_CALL = 0x20
OP_RET = 0x21
OP_HALT = 0xFF


class SagcoCPUVM:
    """
    SAGCO CPU Virtual Machine - Stack-based bytecode interpreter.
    
    Features:
    - Stack-based execution
    - Integer arithmetic operations
    - Function calls (placeholder)
    - Sandbox-friendly (no direct system access in bytecode)
    """
    
    def __init__(self, debug: bool = False):
        self.stack: List[int] = []
        self.debug = debug
        self.ip = 0  # Instruction pointer
        self.halted = False
        
    def log(self, msg: str):
        """Log debug message if debug mode enabled."""
        if self.debug:
            print(f"[VM DEBUG] {msg}", file=sys.stderr)
    
    def execute(self, bytecode: bytes) -> Optional[int]:
        """
        Execute bytecode.
        
        Args:
            bytecode: Byte array of SAGCO bytecode
            
        Returns:
            Top of stack value if available, None otherwise
        """
        self.ip = 0
        self.halted = False
        bytecode_len = len(bytecode)
        
        self.log(f"Starting execution of {bytecode_len} bytes")
        self.log(f"Bytecode hex: {bytecode.hex()}")
        
        while self.ip < bytecode_len and not self.halted:
            opcode = bytecode[self.ip]
            self.log(f"IP={self.ip}, Opcode=0x{opcode:02x}, Stack={self.stack}")
            self.ip += 1
            
            if opcode == OP_PUSH:
                # Push value onto stack
                if self.ip >= bytecode_len:
                    raise RuntimeError("Unexpected end of bytecode (PUSH)")
                value = bytecode[self.ip]
                self.stack.append(value)
                self.log(f"PUSH {value}")
                self.ip += 1
                
            elif opcode == OP_POP:
                # Pop and print value
                if not self.stack:
                    raise RuntimeError("Stack underflow (POP)")
                value = self.stack.pop()
                print(f"POP: {value}")
                self.log(f"POP {value}")
                
            elif opcode == OP_ADD:
                # Add top two stack values
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow (ADD)")
                b = self.stack.pop()
                a = self.stack.pop()
                result = a + b
                self.stack.append(result)
                self.log(f"ADD {a} + {b} = {result}")
                
            elif opcode == OP_SUB:
                # Subtract top two stack values
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow (SUB)")
                b = self.stack.pop()
                a = self.stack.pop()
                result = a - b
                self.stack.append(result)
                self.log(f"SUB {a} - {b} = {result}")
                
            elif opcode == OP_MUL:
                # Multiply top two stack values
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow (MUL)")
                b = self.stack.pop()
                a = self.stack.pop()
                result = a * b
                self.stack.append(result)
                self.log(f"MUL {a} * {b} = {result}")
                
            elif opcode == OP_DIV:
                # Divide top two stack values
                if len(self.stack) < 2:
                    raise RuntimeError("Stack underflow (DIV)")
                b = self.stack.pop()
                a = self.stack.pop()
                if b == 0:
                    raise RuntimeError("Division by zero")
                result = a // b  # Integer division
                self.stack.append(result)
                self.log(f"DIV {a} / {b} = {result}")
                
            elif opcode == OP_CALL:
                # Function call (placeholder)
                self.log("CALL (not implemented)")
                
            elif opcode == OP_RET:
                # Return from function (placeholder)
                self.log("RET (not implemented)")
                
            elif opcode == OP_HALT:
                # Halt execution
                self.log("HALT")
                self.halted = True
                break
                
            else:
                raise RuntimeError(f"Unknown opcode: 0x{opcode:02x} at IP={self.ip-1}")
        
        # Return top of stack if available
        if self.stack:
            result = self.stack[-1]
            self.log(f"Execution complete. Result: {result}")
            return result
        else:
            self.log("Execution complete. Stack empty.")
            return None


def verify_bytecode(bytecode: bytes) -> bool:
    """
    Verify bytecode integrity.
    
    In production, this would:
    - Check cryptographic signature
    - Verify hash against trusted database
    - Validate bytecode structure
    
    For now, just basic validation.
    """
    if len(bytecode) == 0:
        return False
    
    # Check for valid opcodes
    valid_opcodes = {OP_PUSH, OP_POP, OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_CALL, OP_RET, OP_HALT}
    i = 0
    while i < len(bytecode):
        op = bytecode[i]
        if op not in valid_opcodes:
            print(f"Warning: Unknown opcode 0x{op:02x} at position {i}", file=sys.stderr)
            return False
        if op == OP_PUSH:
            i += 2  # Skip value
        else:
            i += 1
    
    return True


def run_daemon(load_dir: str, debug: bool = False):
    """
    Run VM as a daemon, monitoring directory for new bytecode files.
    
    This is intended to be started as a systemd service via SBIP.
    
    Note: Currently uses polling (1 second interval). For production,
    consider using inotify or watchdog library for event-based monitoring.
    """
    print(f"SAGCO CPU VM daemon starting...")
    print(f"Monitoring directory: {load_dir}")
    print(f"Debug mode: {debug}")
    
    load_path = Path(load_dir)
    if not load_path.exists():
        print(f"Error: Directory not found: {load_dir}", file=sys.stderr)
        sys.exit(1)
    
    processed = set()
    
    while True:
        # Scan for .bc files
        for bc_file in load_path.glob("*.bc"):
            if bc_file in processed:
                continue
            
            print(f"\nProcessing: {bc_file}")
            try:
                with open(bc_file, "rb") as f:
                    bytecode = f.read()
                
                if not verify_bytecode(bytecode):
                    print(f"Error: Bytecode verification failed for {bc_file}", file=sys.stderr)
                    continue
                
                vm = SagcoCPUVM(debug=debug)
                result = vm.execute(bytecode)
                print(f"Result: {result}")
                print(f"Final stack: {vm.stack}")
                
                processed.add(bc_file)
                
            except Exception as e:
                print(f"Error executing {bc_file}: {e}", file=sys.stderr)
        
        time.sleep(1)  # Poll every second (consider inotify for production)


def main():
    """Main VM entry point."""
    if len(sys.argv) < 2:
        print("Usage: sagco_cpu_vm.py [--debug] <bytecode_file>")
        print("       sagco_cpu_vm.py --daemon --load-dir <directory> [--debug]")
        print("\nOptions:")
        print("  --debug     Enable debug output")
        sys.exit(1)
    
    debug = "--debug" in sys.argv
    
    if "--daemon" in sys.argv:
        # Daemon mode
        try:
            load_dir_idx = sys.argv.index("--load-dir") + 1
            load_dir = sys.argv[load_dir_idx]
        except (ValueError, IndexError):
            print("Error: --daemon requires --load-dir <directory>", file=sys.stderr)
            sys.exit(1)
        
        run_daemon(load_dir, debug=debug)
        
    else:
        # Single file execution - find bytecode file (ignore --debug flag)
        bytecode_file = None
        for arg in sys.argv[1:]:
            if not arg.startswith("--"):
                bytecode_file = arg
                break
        
        if bytecode_file is None:
            print("Error: No bytecode file specified", file=sys.stderr)
            sys.exit(1)
        
        if not os.path.exists(bytecode_file):
            print(f"Error: File not found: {bytecode_file}", file=sys.stderr)
            sys.exit(1)
        
        print(f"SAGCO CPU VM - Executing: {bytecode_file}")
        
        with open(bytecode_file, "rb") as f:
            bytecode = f.read()
        
        if not verify_bytecode(bytecode):
            print("Error: Bytecode verification failed", file=sys.stderr)
            sys.exit(1)
        
        vm = SagcoCPUVM(debug=debug)
        result = vm.execute(bytecode)
        
        print(f"\nResult: {result}")
        print(f"Final stack: {vm.stack}")


if __name__ == "__main__":
    main()
