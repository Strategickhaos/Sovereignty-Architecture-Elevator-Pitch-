# Usage Guide for Book Content

## Quick Start

### Viewing Interactive Diagrams
Simply open any HTML file in a web browser:
```bash
# From the book/diagrams directory
open mechanical_advantage_interactive.html
# or
firefox deviation_angles_interactive.html
# or
google-chrome highline_sag_interactive.html
```

No server, build process, or external dependencies required!

## Interactive Features

### Mechanical Advantage Diagram
- **Hover** over rope segments → See tension per strand
- **Click** on pulleys → Highlight and animate
- **Click** on loads → Input custom weight
- View real-time MA calculations

### Deviation Angles Diagram  
- **Hover** over pulleys → See TRIG6 sec(θ/2) calculation
- **Click** on pulleys → Input custom load weight
- See color-coded warnings for dangerous angles
- Quick reference table auto-generates

### Highline Sag Diagram
- **Hover** over rope lines → Calculate tension at each sag angle
- **Click** on load markers → Change weight
- **Hover** over anchors → See anchor requirements
- Comparison table shows optimal configurations

## Integration Options

### 1. For Digital Books (EPUB/Web)
```html
<!-- Link from your book -->
<a href="diagrams/mechanical_advantage_interactive.html">
  View Interactive MA Systems
</a>

<!-- Or embed in iframe -->
<iframe src="diagrams/mechanical_advantage_interactive.html" 
        width="900" height="600"></iframe>
```

### 2. For Print Books
- Extract SVG paths from HTML files
- Convert to high-resolution PNG/PDF
- Include QR codes linking to web-hosted versions

### 3. For Websites/Apps
- Upload HTML files to web server
- Link from course materials or app
- No backend required - pure client-side

### 4. For Course Materials
- Include in LMS (Canvas, Moodle, Blackboard)
- Use in PowerPoint/Google Slides (embed via web)
- Distribute as standalone files on USB drives

## Customization

### Changing Default Values
Edit the JavaScript variables at the top of each file:

```javascript
// In mechanical_advantage_interactive.html
let currentWeight = 100; // Change default weight

// In deviation_angles_interactive.html  
let currentLoad = 100; // Change default load

// In highline_sag_interactive.html
let currentWeight = 200; // Change default weight
```

### Adding More Scenarios
Add new SVG elements and data attributes:

```html
<!-- Add a new deviation angle -->
<circle id="pulley-45" cx="300" cy="150" r="12" 
        class="pulley" data-angle="45" data-load="100"/>
```

### Styling Changes
Modify CSS in the `<style>` section of each HTML file.

## Educational Use

### Classroom Demonstrations
1. Project on screen during lectures
2. Have students interact with live calculations
3. Compare theoretical vs. practical scenarios
4. Demonstrate danger zones interactively

### Self-Study
1. Students can download and explore offline
2. Practice calculations with custom values
3. Visual reinforcement of TRIG6 concepts
4. No login or subscription required

### Lab Exercises
1. Use as pre-lab preparation
2. Have students predict tensions before field work
3. Compare calculated vs. measured values
4. Build intuition before hands-on rigging

## Technical Requirements

### Browser Compatibility
- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

### System Requirements
- Any modern device (desktop, laptop, tablet, phone)
- JavaScript enabled
- No plugins or extensions needed
- Works offline once downloaded

### Accessibility
- Keyboard navigation supported
- Screen reader compatible (ARIA labels could be added)
- Color-blind safe (can be enhanced with patterns)
- Text can be enlarged via browser zoom

## Deployment Examples

### Example 1: GitHub Pages
```bash
# Host for free on GitHub Pages
git add book/
git commit -m "Add interactive diagrams"
git push origin main

# Enable GitHub Pages in repository settings
# Access at: https://yourusername.github.io/yourrepo/book/diagrams/
```

### Example 2: Simple Web Server
```bash
# Using Python's built-in server
cd book/diagrams
python3 -m http.server 8000
# Open browser to http://localhost:8000/
```

### Example 3: Cloud Storage
- Upload to Dropbox/Google Drive/OneDrive
- Share public links
- Users can view directly in browser

## Troubleshooting

### Diagrams Not Interactive
- Ensure JavaScript is enabled in browser
- Check browser console for errors (F12)
- Verify file wasn't corrupted during transfer

### Calculations Seem Wrong
- Check default weight/load values
- Ensure proper angle input (degrees, not radians)
- Formulas use standard TRIG6: sec(θ) = 1/cos(θ)

### Display Issues
- Try different browser
- Check zoom level (100% recommended)
- Ensure viewport width ≥ 800px for best experience

## License & Attribution

- Content is educational, per problem statement
- Always include SPRAT/IRATA disclaimers when redistributing
- Attribute TRIG6 framework to original author
- Verify calculations with professional equipment/training

## Support & Updates

For enhancements or bug fixes:
1. Check IMPLEMENTATION_SUMMARY.md for technical details
2. Modify HTML/JS/CSS as needed
3. Test in multiple browsers
4. Submit pull requests with improvements

## Next Steps

Consider adding:
- 📱 Mobile-optimized responsive layouts
- 🎨 Dark mode toggle
- 📊 More complex scenarios (compound systems)
- 💾 Save/export calculation results
- 🔊 Accessibility enhancements
- 🌐 Multi-language support
