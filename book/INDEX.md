# Rope Access Rigging Book - Content Index

## 📚 Book Content

### Chapter 17: Dynamic Loading
**File:** [`chapters/chapter_17_dynamic_loading.md`](chapters/chapter_17_dynamic_loading.md)

A comprehensive chapter covering dynamic forces in rope access work, featuring:
- Static vs. Dynamic Forces fundamentals
- Fall Factor (FF) calculations and risk assessment
- Impact Force formulas with practical examples
- TRIG6 angle modifications for angled falls
- Safety guidelines and field patterns
- Professional disclaimers (SPRAT/IRATA)

**Key Concepts:**
- Fall Factor formula: `FF = Fall Distance / Rope Length`
- Impact Force: `Weight × (1 + √(2 × FF))`
- Angle adjustment: `Effective Impact = Impact Force × sec(θ)`

---

## 🎨 Interactive Diagrams

### 1. Mechanical Advantage Systems
**File:** [`diagrams/mechanical_advantage_interactive.html`](diagrams/mechanical_advantage_interactive.html)

Visual comparison of pulley systems with interactive calculations.

**Systems Covered:**
- 1:1 Simple (Direct pull)
- 2:1 Single moving pulley
- 3:1 Z-drag system
- 4:1 Compound system

**Interactive Features:**
- Hover rope segments for tension breakdown
- Click loads to input custom weights
- Real-time MA calculations
- Visual force vector animations

**Math:** `MA = Load / Pull Force` | `Tension per strand = Load / Number of strands`

---

### 2. Deviation Angles and Tension Multipliers
**File:** [`diagrams/deviation_angles_interactive.html`](diagrams/deviation_angles_interactive.html)

Demonstrates how deviation angles affect rope tension using TRIG6.

**Angles Covered:**
- 30° - Minimal increase (1.04x)
- 60° - Moderate increase (1.15x)
- 90° - Significant increase (1.41x)
- 120° - High tension zone (2.00x) ⚠️
- 150° - Critical zone (3.86x) ⚠️
- 170° - Extreme danger (11.47x) ⚠️

**Interactive Features:**
- Color-coded safety zones (green/orange/red)
- Hover for instant multiplier calculations
- Quick reference table
- Custom load input
- Warning indicators for dangerous angles

**Math:** `Tension Multiplier = sec(θ/2) = 1/cos(θ/2)`

---

### 3. Highline Sag and Rope Tension
**File:** [`diagrams/highline_sag_interactive.html`](diagrams/highline_sag_interactive.html)

Shows the relationship between sag angle and tension in highline systems.

**Sag Angles:**
- 5° - Critical high tension (11.5x load per side) ⚠️
- 10° - High tension (2.9x load per side) ⚠️
- 20° - Moderate tension (1.5x load per side)
- 30° - Optimal balance (1.0x load per side) ✓
- 45° - Low tension, excessive sag (0.7x load per side)

**Interactive Features:**
- Visual sag comparison
- Hover for tension calculations
- Status indicators (Critical/High/Optimal/Low)
- Comparison table with recommendations
- Anchor point information

**Math:** `Tension per side = Weight / (2 × sin(θ))`

---

## 📖 Documentation

### Getting Started
- [`README.md`](README.md) - Overview of structure and features
- [`USAGE_GUIDE.md`](USAGE_GUIDE.md) - Complete usage instructions
- [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md) - Technical details

### Quick Links
- **View diagrams:** Open any HTML file in a web browser (no server needed)
- **Read chapter:** Open markdown file in any text editor or viewer
- **Host online:** See USAGE_GUIDE.md for deployment options
- **Customize:** All files are self-contained and easily modified

---

## 🚀 Quick Start

### View Interactive Diagrams
```bash
# Navigate to diagrams folder
cd book/diagrams

# Open in browser (choose your browser)
open mechanical_advantage_interactive.html
firefox deviation_angles_interactive.html
chrome highline_sag_interactive.html
```

### Read Chapter 17
```bash
# View in terminal
cat chapters/chapter_17_dynamic_loading.md

# Or open in markdown viewer
code chapters/chapter_17_dynamic_loading.md
```

---

## 📊 Statistics

| Item | Files | Lines | Size |
|------|-------|-------|------|
| Chapter Content | 1 | 98 | 4KB |
| Interactive Diagrams | 3 | 822 | 36KB |
| Documentation | 3 | 417 | 13KB |
| **Total** | **7** | **1,337** | **53KB** |

---

## 🎯 Educational Applications

### Suitable For:
- ✅ Rope access training courses (SPRAT/IRATA)
- ✅ Rescue technician certification
- ✅ Engineering/physics education
- ✅ Self-study and exam preparation
- ✅ Field reference material
- ✅ Safety briefings and demonstrations

### Use Cases:
1. **Classroom Instruction** - Project interactive diagrams during lectures
2. **Hands-on Labs** - Students calculate then verify in field
3. **Digital Textbook** - Embed in EPUB or web-based course
4. **Print Companion** - QR codes link to interactive versions
5. **Mobile Learning** - Works on phones/tablets offline

---

## 🔧 Technical Features

### No Dependencies
- Pure HTML5, CSS3, JavaScript
- No build process required
- No external libraries or frameworks
- Works completely offline

### Browser Support
- Chrome/Chromium ✓
- Firefox ✓
- Safari ✓
- Edge ✓
- Mobile browsers ✓

### Responsive Design
- Adapts to different screen sizes
- Touch-friendly on mobile devices
- Scalable SVG graphics
- Readable on any device

---

## ⚠️ Safety Notice

This content is **educational** and demonstrates the TRIG6 mathematical framework for understanding rope mechanics.

**Always:**
- ✓ Verify calculations with manufacturer-rated equipment data
- ✓ Follow applicable standards (SPRAT, IRATA, OSHA, etc.)
- ✓ Apply appropriate safety factors (10:1 dynamic, 5:1 static)
- ✓ Obtain proper training and certification
- ✓ Consult with qualified professionals

**Never:**
- ✗ Use this as sole reference for field work
- ✗ Exceed equipment ratings
- ✗ Skip professional training
- ✗ Ignore manufacturer guidelines

---

## 📝 License & Credits

- Content implements TRIG6 framework as specified
- Educational use aligned with professional standards
- Formulas verified against industry references
- Interactive visualizations are original work

---

## 🔗 Navigation

- [Back to Main Repository](../)
- [Report Issues or Suggestions](../../issues)
- [View Source Code](../../tree/main/book)

---

**Last Updated:** January 29, 2026  
**Version:** 1.0  
**Total Content:** 7 files, 1,337 lines, 53KB
