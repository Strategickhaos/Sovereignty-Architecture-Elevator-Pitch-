# FlameLang Examples

This directory contains example FlameLang source files demonstrating the 7-layer transform pipeline.

## basic_bounce.flame

Demonstrates basic LQC bounce suppression with B-mode damping.

```flame
// FlameLang Example: LQC Bounce with B-mode Suppression
intent bounce
intent suppress
דחה  // Hebrew: bounce operator
כבש  // Hebrew: suppress operator
```

Compiles to LLVM IR with:
- Bounce operator: exp(-l/τ) with τ ≈ 0.065
- B-mode suppression: 10-20% damping at low-l
- CMB power spectrum: D_l with bounce modulation
- Anomaly asymmetry functions
- Optimized with fast-math flags

## Advanced Examples

### Full Physics Pipeline

```flame
intent observe    // Wavefunction collapse
intent fluctuate  // Quantum fluctuation
intent unify      // LQC/String unification

// Hebrew operators
ראה  // Observe
נוע  // Fluctuate
אחד  // Unify
פלא  // Anomaly
```

### With Parameters (future enhancement)

```flame
intent bounce(0.065)     // Custom tau parameter
intent suppress(0.15)    // Custom suppression factor
```

## Compiling Examples

```bash
# Build the compiler
cargo build --release

# Compile an example
./target/release/flamec examples/basic_bounce.flame output.ll

# View the generated LLVM IR
less output.ll

# (Optional) Compile to executable with LLVM
llc output.ll -o output.s
gcc output.s -o quantum_sim
./quantum_sim
```

## Generated Output Structure

The compiler produces LLVM IR with:

1. **Module Header** - Target triple and data layout
2. **Type Definitions** - QuantumParams structure
3. **Intrinsic Declarations** - Math functions (exp, sin, pow, etc.)
4. **Quantum Operations** - One function per operation
5. **CMB Physics** - B-mode suppression, power spectrum, anomalies
6. **Main Function** - Executes all quantum operations
7. **Metadata** - Compiler version and optimization info

## Physics Output

Example functions generated:

- `@quantum_op_N` - Individual quantum operations (bounce, suppress, etc.)
- `@b_mode_suppress` - B-mode suppression with low-l damping
- `@cmb_power_spectrum` - CMB D_l with bounce modulation
- `@anomaly_asymmetry` - Hemispheric asymmetry application
- `@chi_squared_fit` - Planck data fit optimization

## Testing Physics

You can test the physics output by:

1. Using LLVM's interpreter: `lli output.ll`
2. Compiling to executable and running simulations
3. Integrating with CMB data analysis pipelines
4. Comparing against Planck constraints

## Next Steps

- Add numeric parameters to operators
- Implement multi-file compilation
- Add optimizer pass configuration
- Generate plots from simulation results
