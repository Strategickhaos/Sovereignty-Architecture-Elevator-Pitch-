# INV-067: FlameLang ABI Specification
## Stable Binary Interface for Library Linking

**Status:** Specification Phase  
**Priority:** Critical (Required for ecosystem)  
**Timeline:** 3-6 months during compiler development  
**Dependencies:** FlameLang compiler v0.2+, LLVM backend  

---

## 1. EXECUTIVE SUMMARY

The FlameLang ABI (Application Binary Interface) defines how compiled FlameLang code interacts at the binary level, enabling:
- Stable library interfaces across compiler versions
- C/C++ interoperability
- Dynamic linking support
- Cross-platform compatibility

---

## 2. ABI COMPONENTS

### 2.1 Calling Convention

**DNA-Aware Stack Alignment:**
```
Stack Frame Layout:
┌──────────────────────┐ ← High Address
│  Return Address      │ 8 bytes
├──────────────────────┤
│  Saved RBP           │ 8 bytes
├──────────────────────┤
│  DNA Sequence Data   │ 16-byte aligned
├──────────────────────┤
│  Quantum States      │ 32-byte aligned
├──────────────────────┤
│  Physics Tensors     │ 64-byte aligned
├──────────────────────┤
│  Local Variables     │ Platform default
└──────────────────────┘ ← Low Address (RSP)
```

**Register Usage (x86_64):**
```
RDI: 1st argument
RSI: 2nd argument
RDX: 3rd argument
RCX: 4th argument
R8:  5th argument
R9:  6th argument
Stack: Additional arguments

RAX: Return value
XMM0-XMM7: Floating point arguments/returns
YMM0-YMM15: Quantum state vectors (AVX2)
```

---

### 2.2 Symbol Mangling

**Mangling Scheme: Glyph → Unicode → Base64**

```flamelang
func ⚔️combat(energy: joules) -> force
```

Mangles to:
```
_ZN4flame5U26946combat1Ejoules5forceE

Breakdown:
_Z        = FlameLang mangling prefix
N         = Nested name
4flame    = Namespace "flame" (4 chars)
5U2694    = Glyph ⚔️ (Unicode U+2694, 5 chars "U2694")
6combat   = Function "combat" (6 chars)
1E        = End of name
joules    = Parameter type
5force    = Return type
E         = End of signature
```

**Mangling Rules:**
1. All Unicode glyphs encoded as `U{codepoint}`
2. Type names use length-prefixed encoding
3. Templates include full specialization
4. Physics units embedded in type signatures

---

### 2.3 Type Layouts

**Primitive Types:**
```
bool         1 byte
i8/u8        1 byte
i16/u16      2 bytes
i32/u32      4 bytes
i64/u64      8 bytes
f32          4 bytes
f64          8 bytes
```

**FlameLang-Specific Types:**
```
Glyph        16 bytes (Unicode + metadata)
Codon        3 bytes (ACGT encoding)
DNASequence  24 bytes (pointer + length + capacity)
Energy       16 bytes (f64 value + unit tag)
Qubit        32 bytes (complex amplitudes)
```

**Memory Layout Example:**
```c
// C equivalent of FlameLang DNASequence
struct DNASequence {
    uint8_t* data;       // 8 bytes
    uint64_t length;     // 8 bytes
    uint64_t capacity;   // 8 bytes
    // Total: 24 bytes, 8-byte aligned
};
```

---

### 2.4 Name Decoration

**Function Categories:**
```
Standard functions:   _ZN{...}
Template functions:   _ZN{...}I{template_args}E
Operators:           _ZN{...}operator{op}E
Destructors:         _ZN{...}D1E
Constructors:        _ZN{...}C1E
```

**Example Mangling Table:**
```
Source                          | Mangled Symbol
--------------------------------|--------------------------------
func add(a: i32, b: i32) -> i32 | _ZN4flame3add2i32E
func ⚔️::apply(e: Energy)       | _ZN5U26946apply6EnergyE
template<T> func max(a: T) -> T | _ZN4flame3maxI1TE
```

---

## 3. VERSIONING SCHEME

### 3.1 Codon-Based Semantic Versioning

```
Version: Major.Minor.Patch
Example: 2.1.4

DNA Encoding:
Major 2 → GCA (Alanine)
Minor 1 → AAC (Asparagine)
Patch 4 → ACG (Threonine)

Full Version DNA: GCA-AAC-ACG
```

**Version Compatibility:**
```
┌─────────────┬──────────┬──────────┬──────────┐
│   Version   │   2.0.x  │   2.1.x  │   3.0.x  │
├─────────────┼──────────┼──────────┼──────────┤
│  ABI Level  │    1     │    1     │    2     │
│  DNA Family │  GCA-xxx │  GCA-xxx │  ATG-xxx │
│  Compatible │   Yes    │   Yes    │    No    │
└─────────────┴──────────┴──────────┴──────────┘
```

**Compatibility Rules:**
1. Same major version: ABI compatible
2. Minor version bump: Additive changes only
3. Patch version: No ABI changes
4. Major version bump: Breaking ABI changes allowed

---

### 3.2 ABI Version Embedding

```flamelang
// Compiler automatically embeds ABI version
@abi_version(2, 1, 0)
module flame::quantum;

// Symbol includes ABI version
_ZN4flame7quantum_v2_1_0_8EntangleE
```

---

## 4. C/C++ INTEROPERABILITY

### 4.1 C FFI

```flamelang
// FlameLang side
@extern_c
func calculate_energy(mass: f64, velocity: f64) -> f64 {
    return 0.5 * mass * velocity * velocity;
}
```

```c
// C side
extern double calculate_energy(double mass, double velocity);

int main() {
    double energy = calculate_energy(10.0, 5.0);
    printf("Energy: %f\n", energy);
}
```

### 4.2 C++ Interop

```flamelang
// FlameLang calling C++
@link_cpp("libphysics.so")
extern func cpp_simulate_particle(
    mass: f64,
    charge: f64
) -> Vector3D;
```

```cpp
// C++ implementation
extern "C" Vector3D cpp_simulate_particle(double mass, double charge) {
    // C++ physics simulation
}
```

---

## 5. DYNAMIC LINKING

### 5.1 Shared Library Format

```bash
# Compile FlameLang to shared library
flame build --crate-type=dylib --output=libquantum.so

# Library contains:
# - Mangled symbols
# - ABI version metadata
# - DNA hash checksums
# - Physics constraint tables
```

### 5.2 Symbol Visibility

```flamelang
// Public (exported) symbol
pub func entangle(q1: Qubit, q2: Qubit) -> BellPair;

// Private (internal) symbol
func internal_collapse(q: Qubit) -> bool;

// Exported with explicit name
#[export_name = "flame_entangle"]
pub func entangle(...);
```

---

## 6. EXCEPTION HANDLING

### 6.1 Unwinding ABI

FlameLang uses DWARF-based unwinding compatible with C++:
```
┌─────────────────────────────────┐
│  FlameLang Exception            │
│  (frequency dissonance)         │
├─────────────────────────────────┤
│  DWARF Unwinding Info           │
├─────────────────────────────────┤
│  Stack Frame Cleanup            │
│  (DNA sequence cleanup)         │
├─────────────────────────────────┤
│  Catch Handler                  │
│  (resonance harmonization)      │
└─────────────────────────────────┘
```

### 6.2 Cross-Language Exceptions

```flamelang
@catch_cpp_exceptions
func call_cpp_code() -> Result<T, Error> {
    try {
        cpp_function();
    } catch (std::exception& e) {
        return Err(Error::from_cpp(e));
    }
}
```

---

## 7. THREAD LOCAL STORAGE

```flamelang
// Thread-local quantum state
@thread_local
static QUANTUM_CONTEXT: QuantumContext;

// ABI ensures proper TLS initialization
// across shared library boundaries
```

---

## 8. VALIDATION & TESTING

### 8.1 ABI Checker Tool

```bash
# Compare ABI compatibility between versions
flame abi check --old v2.0.0 --new v2.1.0

# Output:
# ✅ Function signatures: Compatible
# ✅ Type layouts: No changes
# ✅ Symbol mangling: Consistent
# ⚠️  New functions added (additive change)
# 📊 ABI Level: 1 → 1 (compatible)
```

### 8.2 ABI Test Suite

```flamelang
// Test ABI stability
#[test]
fn test_dna_sequence_layout() {
    assert_eq!(size_of::<DNASequence>(), 24);
    assert_eq!(align_of::<DNASequence>(), 8);
    
    // Ensure layout matches C struct
    assert_c_compatible!(DNASequence);
}
```

---

## 9. PLATFORM-SPECIFIC CONSIDERATIONS

### 9.1 x86_64 (Linux, macOS, Windows)
- 16-byte stack alignment
- System V ABI (Linux/macOS)
- Microsoft x64 ABI (Windows)

### 9.2 ARM64 (Apple Silicon, Linux ARM)
- 16-byte stack alignment
- AAPCS64 calling convention
- Vector registers for quantum states

### 9.3 RISC-V (Future Support)
- 16-byte stack alignment
- RISC-V calling convention
- Custom extensions for DNA operations

---

## 10. DOCUMENTATION

### 10.1 ABI Reference Manual

```
flamelang-abi-reference/
├── 01-calling-convention.md
├── 02-symbol-mangling.md
├── 03-type-layouts.md
├── 04-versioning.md
├── 05-c-interop.md
├── 06-dynamic-linking.md
├── 07-exceptions.md
└── 08-platform-specifics.md
```

### 10.2 Examples

```
flamelang-abi-examples/
├── c-interop/
│   ├── call-c-from-flame/
│   └── call-flame-from-c/
├── cpp-interop/
│   └── mixed-language-project/
└── dynamic-linking/
    ├── shared-library/
    └── plugin-system/
```

---

## 11. FUTURE EXTENSIONS

- WebAssembly ABI compatibility
- GPU kernel ABI (CUDA/ROCm)
- Quantum computer ABI (when hardware available)
- Neuromorphic chip ABI

---

🔥 **"Stable interfaces, sovereign execution."** 🔥
