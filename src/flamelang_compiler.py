#!/usr/bin/env python3
"""
FlameLang LLVM-Native Compiler
SBIP v1.0 Compliant - Strategickhaos DAO LLC

This compiler demonstrates the correct LLVM-native linking approach
using clang as the linker driver instead of direct ld invocation.

Engineering Fix:
  ❌ WRONG: subprocess.run(["ld", "flamelang.o", "-o", "flamelang_exec"])
  ✅ RIGHT: subprocess.run(["clang", "flamelang.o", "-o", "flamelang_exec"])

Why clang over ld:
  - Automatically includes CRT startup objects (crt1.o, crti.o, crtn.o)
  - Proper libc linkage
  - Correct dynamic loader path
  - Cross-platform portability
"""

import subprocess
import sys
import os
from pathlib import Path


class FlameLangCompiler:
    """SBIP v1.0 compliant FlameLang compiler using LLVM toolchain."""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.temp_files = []
    
    def log(self, message):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def run_command(self, cmd, description):
        """Run a command and handle errors."""
        self.log(f"\n{description}")
        self.log(f"  Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                self.log(f"  Output: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during {description}")
            print(f"  Command: {' '.join(cmd)}")
            print(f"  Exit code: {e.returncode}")
            if e.stderr:
                print(f"  Error output:\n{e.stderr}")
            return False
        except FileNotFoundError:
            print(f"❌ Command not found: {cmd[0]}")
            print(f"  Please install LLVM toolchain: apt install clang llvm")
            return False
    
    def compile_to_llvm_ir(self, source_file):
        """Phase 1: Compile source to LLVM IR (.ll file)."""
        ll_file = f"{source_file}.ll"
        self.temp_files.append(ll_file)
        
        success = self.run_command(
            ["clang", "-S", "-emit-llvm", source_file, "-o", ll_file],
            "🔥 Phase 1: Compiling to LLVM IR"
        )
        return ll_file if success else None
    
    def optimize_ir(self, ll_file):
        """Phase 2: Optimize LLVM IR with opt."""
        bc_file = ll_file.replace(".ll", ".bc")
        self.temp_files.append(bc_file)
        
        success = self.run_command(
            ["opt", "-O3", ll_file, "-o", bc_file],
            "⚡ Phase 2: Optimizing LLVM IR"
        )
        return bc_file if success else None
    
    def generate_object_code(self, bc_file):
        """Phase 3: Generate object code from optimized IR."""
        obj_file = "flamelang.o"
        self.temp_files.append(obj_file)
        
        success = self.run_command(
            ["llc", "-filetype=obj", bc_file, "-o", obj_file],
            "🔧 Phase 3: Generating object code"
        )
        return obj_file if success else None
    
    def link_executable(self, obj_file, output_file, optimize=True):
        """
        Phase 4: Link object file to executable using clang.
        
        CRITICAL: This uses clang instead of ld directly.
        
        Why this matters:
        - Direct ld fails because it skips CRT startup objects
        - clang automatically includes crt1.o, crti.o, crtn.o
        - clang handles libc linkage correctly
        - clang sets the correct dynamic loader path
        """
        cmd = ["clang", obj_file]
        
        if optimize:
            cmd.append("-O3")
        
        cmd.extend(["-o", output_file])
        
        success = self.run_command(
            cmd,
            "🔗 Phase 4: Linking with clang (SBIP v1.0 compliant)"
        )
        return success
    
    def link_executable_wrong_way(self, obj_file, output_file):
        """
        EXAMPLE OF WRONG APPROACH - DO NOT USE IN PRODUCTION
        
        This demonstrates why direct ld invocation fails:
        ❌ subprocess.run(["ld", "flamelang.o", "-o", "flamelang_exec"])
        
        This will fail with errors like:
        - ld: warning: cannot find entry symbol _start
        - undefined reference to `__libc_start_main'
        - undefined reference to `printf'
        """
        print("\n⚠️  WARNING: Attempting direct ld (will likely fail)")
        print("   This demonstrates why we need clang as linker driver")
        
        success = self.run_command(
            ["ld", obj_file, "-o", output_file],
            "❌ WRONG: Direct ld invocation (for demonstration)"
        )
        
        if not success:
            print("\n✅ Expected failure: This is why SBIP v1.0 mandates clang!")
            print("   Direct ld skips:")
            print("     - CRT startup objects (crt1.o, crti.o, crtn.o)")
            print("     - libc linkage")
            print("     - Dynamic loader path configuration")
        
        return False
    
    def compile(self, source_file, output_file, optimize=True):
        """
        Complete compilation pipeline using LLVM-native toolchain.
        
        Pipeline:
          1. Source (.c/.cpp) -> LLVM IR (.ll)
          2. LLVM IR (.ll) -> Optimized Bitcode (.bc)
          3. Bitcode (.bc) -> Object Code (.o)
          4. Object Code (.o) -> Executable (using clang as linker)
        """
        print(f"\n🔥 FlameLang LLVM-Native Compiler - SBIP v1.0")
        print(f"   Source: {source_file}")
        print(f"   Output: {output_file}")
        print(f"   Optimization: {'O3' if optimize else 'None'}\n")
        
        # Verify source file exists
        if not os.path.isfile(source_file):
            print(f"❌ Source file not found: {source_file}")
            return False
        
        # Phase 1: Compile to LLVM IR
        ll_file = self.compile_to_llvm_ir(source_file)
        if not ll_file:
            return False
        
        # Phase 2: Optimize IR
        bc_file = self.optimize_ir(ll_file)
        if not bc_file:
            return False
        
        # Phase 3: Generate object code
        obj_file = self.generate_object_code(bc_file)
        if not obj_file:
            return False
        
        # Phase 4: Link executable (THE CRITICAL FIX)
        success = self.link_executable(obj_file, output_file, optimize)
        
        if success:
            print(f"\n✅ Compilation complete: {output_file}")
            print(f"   SBIP v1.0 compliant: Used clang for linking")
            print(f"   Ready for execution")
        
        return success
    
    def cleanup(self, keep_temps=False):
        """Clean up temporary files."""
        if not keep_temps:
            for temp_file in self.temp_files:
                if os.path.isfile(temp_file):
                    os.remove(temp_file)
                    self.log(f"  Removed: {temp_file}")


def main():
    """Command-line interface for FlameLang compiler."""
    if len(sys.argv) < 3:
        print("Usage: flamelang_compiler.py <source.c> <output_executable>")
        print("\nOptions:")
        print("  -v, --verbose    Enable verbose output")
        print("  -k, --keep-temps Keep temporary files")
        print("  -O0              Disable optimization")
        print("\nExample:")
        print("  python flamelang_compiler.py hello.c hello_exec")
        sys.exit(1)
    
    # Parse arguments
    source_file = sys.argv[1]
    output_file = sys.argv[2]
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    keep_temps = "-k" in sys.argv or "--keep-temps" in sys.argv
    optimize = "-O0" not in sys.argv
    
    # Create compiler instance
    compiler = FlameLangCompiler(verbose=verbose)
    
    # Compile
    success = compiler.compile(source_file, output_file, optimize=optimize)
    
    # Cleanup
    if not keep_temps:
        compiler.cleanup()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
