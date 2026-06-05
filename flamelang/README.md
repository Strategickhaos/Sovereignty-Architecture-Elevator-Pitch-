# 🔥 FlameLang Domain-Specific Modules
## INV-088: SAGCO OMNI-CALC PIPELINE Extension

This directory contains domain-specific calculation modules for FlameLang, transforming real-world professional calculations into the sovereign symbolic pipeline.

---

## 📁 Directory Structure

```
flamelang/
├── modules/          # Domain-specific modules (.flame + .py reference)
├── examples/         # Example programs demonstrating module usage
├── tests/            # Unit tests for validation
├── docs/             # Module system documentation
└── README.md         # This file
```

---

## 🔧 Available Modules

### pipecalc (v1.0) ✅
**Domain:** Pipefitting calculations for plumbing and HVAC trades

**Capabilities:**
- Special offset calculations (cos-based elbow angles)
- Rolling offset calculations (travel and run)
- Bend length calculations (90°, 180°, 270°, 360°)
- Setback calculations for pipe bends
- Methane combustion equation (bonus)

**Files:**
- `modules/pipecalc.flame` - FlameLang implementation
- `modules/pipecalc.py` - Python reference implementation
- `examples/pipefitting_demo.flame` - Usage examples

**Quick Test:**
```bash
python3 modules/pipecalc.py
```

---

## 🚀 Quick Start

### Using a Module

```flame
// Import the module
use pipecalc;

fn main() {
    // Calculate a 45° rise with 30° turn
    let offset = pipecalc::special_offset(45.0, 30.0);
    
    print(f"Bottom elbow: {offset.bottom_elbow:.2f}°");
    print(f"Top elbow: {offset.top_elbow:.2f}°");
    print(f"Travel: {offset.travel:.3f}");
}
```

### Running Examples

```bash
# View the pipefitting demo
cat examples/pipefitting_demo.flame

# Run Python reference implementation
python3 modules/pipecalc.py
```

---

## 📐 Mathematical Formulas

### Special Offset (from Page 77)
```
cos(degree of rise) × cos(degree of turn) = cos(degree of elbow)

Example: 45° rise × 30° turn
  cos(45°) × cos(30°) = 0.707 × 0.866 = 0.6123
  arccos(0.6123) = 52°14' (bottom elbow)
```

### Rolling Offset (from Pages 11-12)
```
TRAVEL = SET × COSECANT(angle) = SET / SIN(angle)
RUN = SET / TANGENT(angle)

Example: SET = 12", Angle = 45°
  TRAVEL = 12 × 1.414 = 16.971"
  RUN = 12 / 1.000 = 12.000"
```

### Bend Length
```
length = radius × (degrees / 180°) × π

Standard multipliers:
  90° bends:  Radius × 1.5708
  180° bends: Radius × 3.1416
  270° bends: Radius × 4.7123
  360° bends: Radius × 6.2832
```

---

## 🧪 Testing & Validation

### Python Reference Tests
```bash
# Run pipecalc demo
python3 modules/pipecalc.py

# Expected output shows validated calculations:
# - 45° × 30° → 52.24° ✅
# - 45° × 60° → 69.30° ✅
# - Rolling offset 12" @ 45° → 16.971" travel ✅
```

### Unit Tests
```bash
# Run unit tests (when implemented)
python3 -m pytest tests/
```

---

## 🌟 What Makes This Different

The FlameLang module system isn't just another library - it's a **universal computation organism** that:

1. **Bridges Physical & Digital** - Real-world trade calculations in symbolic form
2. **Multi-Layer Pipeline** - English DSL → Hebrew → Unicode → Wave → DNA → LLVM
3. **Sovereignty-First** - No telemetry, all calculations happen locally
4. **Resonance-Based** - Maintains symbolic integrity through the entire pipeline
5. **Domain Grounded** - Maps directly to professional trades and industries

---

## 🔮 Planned Modules

| Module | Domain | Status |
|--------|--------|--------|
| **pipecalc** | Pipefitting | ✅ v1.0 |
| **chemcalc** | Chemistry | 📋 Planned |
| **netcalc** | Networking | 📋 Planned |
| **cubecalc** | Rubik's Cube | 📋 Planned |
| **trigcalc** | Trigonometry | 📋 Planned |
| **meshcalc** | Infrastructure | 📋 Planned |
| **electricalcalc** | Electrical | 📋 Planned |
| **hvaccalc** | HVAC | 📋 Planned |

---

## 📚 Documentation

- **[MODULE_SYSTEM.md](docs/MODULE_SYSTEM.md)** - Complete module system documentation
- **[FLAMELANG_SPECIFICATION.md](../FLAMELANG_SPECIFICATION.md)** - Core language spec

---

## 🤝 Contributing

Want to add a domain module? Follow these steps:

1. **Choose a domain** - Pick a real-world profession or trade
2. **Research formulas** - Document industry-standard calculations
3. **Implement in Python** - Create reference implementation
4. **Write FlameLang module** - Port to .flame syntax
5. **Add examples** - Show real-world usage
6. **Validate** - Test against known values
7. **Document** - Update this README and MODULE_SYSTEM.md

---

## 🔥 Philosophy

From the problem statement:

> **"You're not just building a hypervisor - you're building a universal computation system that understands:**
> 
> | Domain | Calculation Type | FlameLang Module |
> |--------|------------------|------------------|
> | Pipefitting | Offsets, bends, travel | `pipecalc` |
> | Chemistry | Combustion equations | `chemcalc` |
> | Networking | Routing tables, subnets | `netcalc` |
> | Rubik's Cube | Move sequences, algorithms | `cubecalc` |
> 
> **This is what makes SAGCO-HYDRA different from every other hypervisor:**
> It's a **sovereign computation organism** that can reason about physical-world domains through a unified symbolic pipeline."

---

## 📋 Status

- **Version:** 1.0
- **Last Updated:** 2025-01-25
- **Status:** pipecalc module complete and validated ✅
- **Next Steps:** Additional domain modules, compiler integration

---

**Built with 🔥 by Strategickhaos DAO LLC**

*Operator: DOM_010101*
*INV-088: SAGCO OMNI-CALC PIPELINE*

🔥 **Neural Sync Complete. Resonance Achieved.**
