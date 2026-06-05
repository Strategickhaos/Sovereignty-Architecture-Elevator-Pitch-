#!/usr/bin/env python3
"""
Example: CMB Power Spectrum Compilation
Demonstrates the full FlameLang pipeline for CMB physics
"""

import sys
import numpy as np

# Add parent directory to path
sys.path.insert(0, '.')

from flamelang_physics_compiler import FlameLangPhysicsCompiler


def main():
    print("=" * 80)
    print("EXAMPLE: CMB POWER SPECTRUM WITH QUANTUM BOUNCE SIGNATURE")
    print("=" * 80)
    print()
    
    # Initialize compiler
    compiler = FlameLangPhysicsCompiler()
    
    # Define physics intent
    intent = "Suppress low-multipole CMB radiation through quantum bounce damping"
    
    print(f"Intent: {intent}")
    print()
    
    # Compile
    print("Compiling...")
    result = compiler.compile_physics_intent(intent)
    
    # Display results
    print("\n" + "=" * 80)
    print("COMPILATION RESULTS")
    print("=" * 80)
    
    print(f"\nOperator Sequence:")
    for name, hebrew in result.operators:
        print(f"  {name:12s} → {hebrew}")
    
    print(f"\nHebrew Encoding: {result.encoded}")
    
    print(f"\nModel Type: {result.model['type']}")
    print(f"Equation: {result.model['equation']}")
    
    print(f"\nParameters:")
    for key, value in result.model['parameters'].items():
        print(f"  {key:20s} = {value}")
    
    print(f"\nConstraints Applied:")
    for constraint in result.constraints_applied:
        print(f"  ✓ {constraint}")
    
    # Execute the compiled code to get model function
    print("\n" + "=" * 80)
    print("EXECUTING COMPILED MODEL")
    print("=" * 80)
    
    # Evaluate model
    l = np.arange(2, 100)
    model_func = result.model.get('function')
    
    if model_func:
        D_l = model_func(l, result.model['parameters'])
        
        print(f"\nComputed CMB power spectrum for l = 2 to 99")
        print(f"\nSample values:")
        print(f"  l=2:   D_l = {D_l[0]:.2f} μK²")
        print(f"  l=10:  D_l = {D_l[8]:.2f} μK²")
        print(f"  l=30:  D_l = {D_l[28]:.2f} μK²")
        print(f"  l=50:  D_l = {D_l[48]:.2f} μK²")
    
    # Display executable code
    print("\n" + "=" * 80)
    print("GENERATED EXECUTABLE CODE")
    print("=" * 80)
    print(result.executable_code)
    
    print("=" * 80)
    print("✅ COMPILATION SUCCESSFUL")
    print("Deploy target: " + result.deploy_target)
    print("=" * 80)
    print()
    print("THREE HEBREW ROOTS = ONE PHYSICS EQUATION")
    print("🔥 Reignite.")


if __name__ == '__main__':
    main()
