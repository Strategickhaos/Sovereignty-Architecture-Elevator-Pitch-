# FlameLang Evolutionary Gate - Documentation Index

Welcome to the FlameLang Evolutionary Gate documentation. This system implements Darwinian compiler evolution for the SAGCO/FlameLang project.

## 🎯 Quick Start

**New to the evolutionary gate?** Start here:

1. **[Implementation Summary](EVOLUTIONARY_GATE_SUMMARY.md)** - High-level overview of what was built and why
2. **[Integration Guide](EVOLUTIONARY_GATE_INTEGRATION.md)** - Step-by-step setup instructions
3. **[Architecture Diagram](EVOLUTIONARY_GATE_ARCHITECTURE.md)** - Visual system architecture and data flow

## 📚 Complete Documentation

### Core Guides

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[EVOLUTIONARY_GATE_SUMMARY.md](EVOLUTIONARY_GATE_SUMMARY.md)** | Implementation overview | First - understand what was built |
| **[EVOLUTIONARY_GATE_INTEGRATION.md](EVOLUTIONARY_GATE_INTEGRATION.md)** | Integration steps | Second - set up the system |
| **[EVOLUTIONARY_GATE.md](EVOLUTIONARY_GATE.md)** | Comprehensive reference | Third - deep dive into theory and usage |
| **[EVOLUTIONARY_GATE_ARCHITECTURE.md](EVOLUTIONARY_GATE_ARCHITECTURE.md)** | Visual diagrams | Anytime - visual reference |

### Quick References

| Document | Location | Purpose |
|----------|----------|---------|
| **Package README** | `src/emulator/wave_cores/trig6/evo_gate/README.md` | Command-line quick reference |
| **Main README** | `README.md` | System overview with evo gate section |

## 🔍 What You'll Learn

### Implementation Summary
- What problem the evolutionary gate solves
- How it transforms "vibes" into objective fitness
- Core innovation: multi-domain fitness evaluation
- Safety mechanisms and curriculum-driven evolution
- Complete file listing and testing verification

### Integration Guide
- Prerequisites and directory structure
- Manual testing instructions
- How to integrate with actual FlameBench and TRIG6
- Data format requirements
- CI/CD integration steps
- Troubleshooting common issues

### Comprehensive Reference
- Detailed fitness formula explanation
- Safety mechanism deep dive
- Usage examples and exit codes
- Input/output data formats
- Integration with zyBooks curriculum
- Extending the gate (custom fitness, metrics, constraints)
- Theoretical foundation
- Future enhancements

### Architecture Diagrams
- End-to-end system flow
- Fitness calculation breakdown
- Curriculum-driven evolution process
- Data flow and integration points

## 🚀 Recommended Reading Order

### For First-Time Users
1. [Implementation Summary](EVOLUTIONARY_GATE_SUMMARY.md) - 5 min read
2. [Architecture Diagram](EVOLUTIONARY_GATE_ARCHITECTURE.md) - Visual overview
3. [Integration Guide](EVOLUTIONARY_GATE_INTEGRATION.md) - Hands-on setup

### For Deep Understanding
1. [Comprehensive Reference](EVOLUTIONARY_GATE.md) - Complete theory
2. [Architecture Diagram](EVOLUTIONARY_GATE_ARCHITECTURE.md) - Visual reinforcement
3. Package source code - Implementation details

### For Quick Reference
- [Package README](../src/emulator/wave_cores/trig6/evo_gate/README.md) - Commands only
- [Architecture Diagram](EVOLUTIONARY_GATE_ARCHITECTURE.md) - Visual cheat sheet

## 🎓 Key Concepts

Before diving into the docs, understand these core concepts:

### Multi-Domain Fitness
The gate evaluates mutations across three domains:
1. **TRIG6** - Swarm behavior (resonance, drift, noise, invention, phase)
2. **FlameBench** - Compiler performance (p_success)
3. **Equivalence** - Behavioral correctness (hard gate ≥ 0.99)

### Safety-First Design
Three independent safety layers:
1. Equivalence hard gate (no "faster but wrong")
2. Strict improvement requirement (no regression)
3. TRIG6 behavioral clamps (drift/noise penalties)

### Curriculum-Driven Evolution
Your academic work (zyBooks labs) becomes evolutionary pressure:
- Labs → FlameBench test atoms
- Mutations must not break labs
- Every new lab constrains mutation space

## 📊 Documentation Stats

- **Total Documentation**: ~37KB across 4 comprehensive guides
- **Core Implementation**: ~370 lines of production Python
- **Test Coverage**: 4 critical scenarios validated
- **Example Data**: TRIG6 metrics + FlameBench results

## 🔗 External References

- **FlameLang Specification**: `../FLAMELANG_SPECIFICATION.md`
- **Main Project README**: `../README.md`
- **GitHub Workflow**: `../.github/workflows/flamelang-evolution.yml`
- **Source Code**: `../src/emulator/wave_cores/trig6/evo_gate/`

## 💡 Common Questions

**Q: Where do I start?**  
A: Read the [Implementation Summary](EVOLUTIONARY_GATE_SUMMARY.md) first.

**Q: How do I integrate this with my project?**  
A: Follow the [Integration Guide](EVOLUTIONARY_GATE_INTEGRATION.md) step-by-step.

**Q: How does the fitness formula work?**  
A: See the [Comprehensive Reference](EVOLUTIONARY_GATE.md) or [Architecture Diagrams](EVOLUTIONARY_GATE_ARCHITECTURE.md).

**Q: What data formats are required?**  
A: See "Data Format Requirements" in the [Integration Guide](EVOLUTIONARY_GATE_INTEGRATION.md).

**Q: Can I customize the fitness function?**  
A: Yes! See "Extending the Gate" in the [Comprehensive Reference](EVOLUTIONARY_GATE.md).

**Q: What if the gate keeps rejecting/accepting everything?**  
A: See "Troubleshooting" in the [Integration Guide](EVOLUTIONARY_GATE_INTEGRATION.md).

## 🎯 Next Steps

1. ✅ Read the [Implementation Summary](EVOLUTIONARY_GATE_SUMMARY.md)
2. 📖 Review the [Architecture Diagrams](EVOLUTIONARY_GATE_ARCHITECTURE.md)
3. 🚀 Follow the [Integration Guide](EVOLUTIONARY_GATE_INTEGRATION.md)
4. 🔬 Deep dive into the [Comprehensive Reference](EVOLUTIONARY_GATE.md)
5. 💻 Run your first evolution cycle!

## 📝 Feedback

If you find gaps in the documentation or have questions not covered here, please open an issue or submit a PR.

---

**Status**: Complete and ready for production integration ✅  
**Last Updated**: 2026-01-25  
**Version**: 1.0.0
