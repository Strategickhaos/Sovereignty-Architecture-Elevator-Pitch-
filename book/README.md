# Rope Access Rigging Book Content

This directory contains chapters and interactive diagrams for a rope access rigging manual featuring the TRIG6 trigonometric framework.

## Structure

### Chapters
- `chapter_17_dynamic_loading.md` - Complete chapter on dynamic forces, fall factors, impact calculations, and TRIG6 angle modifications

### Interactive Diagrams
Three HTML-based interactive diagrams with JavaScript functionality:

1. **mechanical_advantage_interactive.html**
   - Visual comparison of 1:1, 2:1, 3:1, and 4:1 mechanical advantage systems
   - Interactive features:
     - Hover over rope segments to see tension calculations
     - Click pulleys to highlight systems
     - Click loads to input custom weights
   - Calculates tension per strand and pull required

2. **deviation_angles_interactive.html**
   - Demonstrates tension multipliers at different deviation angles (30°, 60°, 90°, 120°, 150°, 170°)
   - Interactive features:
     - Hover over pulleys to see TRIG6 sec(θ/2) calculations
     - Color-coded warnings for high-tension configurations
     - Quick reference table showing multipliers
     - Click to input custom loads
   - Uses formula: Tension Multiplier = sec(θ/2) = 1/cos(θ/2)

3. **highline_sag_interactive.html**
   - Shows relationship between sag angle and rope tension in highline systems
   - Interactive features:
     - Multiple sag angles from 5° to 45° with visual comparison
     - Hover to calculate tension for each configuration
     - Status indicators (Critical/High/Optimal/Low tension zones)
     - Comparison table with recommendations
     - Click loads to change weight
   - Uses formula: T = W / (2 × sin(θ))

## Usage

### For Print
- The markdown chapter can be included in book compilation
- SVG paths from interactive diagrams can be extracted as static images

### For Digital/Interactive Use
- Open HTML files directly in any modern web browser
- No server or external dependencies required
- Can be embedded in EPUB with interactive support
- Can be hosted on a website alongside the book content

## Technical Details

All interactive diagrams use:
- Vanilla JavaScript (no external libraries required)
- SVG for scalable graphics
- Responsive design principles
- Hover and click event handlers
- Real-time mathematical calculations using TRIG6 principles

## Safety Disclaimer

Content is educational and demonstrates the TRIG6 framework. Always:
- Verify calculations with rated equipment and manufacturer data
- Follow applicable standards (SPRAT/IRATA)
- Consult professional training before field application
- Apply appropriate safety factors (10:1 for dynamics, 5:1 for statics)
