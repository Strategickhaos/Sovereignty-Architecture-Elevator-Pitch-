# Interactive Demos

This directory contains interactive demonstration tools for the Sovereignty Architecture project.

## Knot Efficiency Calculator

**File:** `knot-efficiency-calculator.html`

An interactive web-based calculator for rope mechanics analysis using the TRIG6 system. This tool helps calculate effective rope strength based on knot type, Maximum Breaking Strength (MBS), and anchor angle.

### Features

- **6 Common Knots:** Figure 8, Bowline, Alpine Butterfly, Double Fisherman's, Clove Hitch, and Prusik Hitch
- **Real-time Calculations:** Instant calculation of effective rope strength
- **Interactive Visualizations:** Click any knot to see detailed strength analysis
- **Angle Compensation:** Accounts for anchor angle deviations from vertical
- **Field Guidance:** Efficiency thresholds for different use cases
- **Professional UI:** Dark theme with responsive design

### Usage

1. Open `knot-efficiency-calculator.html` in a web browser
2. Adjust the Rope MBS (kN) value (default: 22 kN)
3. Set the Anchor Angle in degrees from vertical (0-90°)
4. Click on any knot card to see the effective strength calculation
5. Review the detailed formula breakdown and field guidance

### Formula

```
Effective Strength = MBS × Knot Efficiency × cos(Anchor Angle)
```

### Efficiency Thresholds

- **Under 65%:** Rescue only if backed up
- **65-75%:** Workhorse anchors
- **Over 75%:** Primary life support

### Technical Details

- Pure HTML/CSS/JavaScript - no dependencies
- Runs entirely in the browser
- Uses standard trigonometric calculations
- Includes kN to lbf conversion

### Reference

Part of the TRIG6 Rope Mechanics System | StrategicKhaos DAO LLC | INV-011
