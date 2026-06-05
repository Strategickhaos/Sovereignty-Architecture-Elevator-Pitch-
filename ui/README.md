# Event Horizon UI v0

SynapseBus Nervous System Visualization - A real-time visualization dashboard for the StrategicKhaos Swarm Intelligence system.

## Overview

Event Horizon UI provides three interactive views for monitoring and analyzing system behavior:

### 🧠 Trace Graph — Dendrite View
- **Visual trace graph** showing the flow of system events (spikes)
- **Interactive nodes** with color-coded event types:
  - 🔵 Blue: Process events (`proc.*`)
  - 🟢 Green: File system events (`fs.*`)
  - 🟠 Orange: Network events (`net.*`)
  - 🔴 Red: Network anomalies (`net.flow.anomaly`)
  - 🟣 Purple: Security events (`sec.*`)
- **Animated connections** showing causal relationships
- **Click nodes** to view detailed information (ID, hash, timestamp)
- **Pulsing animation** on anomaly nodes for immediate attention

### 🔥 Field Map — Heat Map
- **Physics fields** monitoring with real-time metrics:
  - **Entropy**: System disorder/unpredictability
  - **Mass**: System load/activity
  - **Trust**: Security confidence level
- **Color-coded heat map**:
  - Red zones indicate high entropy or low trust
  - Green zones indicate stable/trusted state
- **Velocity indicators** showing rate of change
- **Reflex proposals** from optimizers (Simulated Annealing, Black Hole)

### ⚡ Reflexes — Spinal Cord
- **Active reflexes** with priority levels
- **Activation counters** showing how many times each reflex fired
- **Ratification status** indicating approved autonomous responses
- **Recent activations** timeline with trigger sources
- **Enable/disable status** indicators

## Running the UI

### Development Mode
```bash
npm run ui:dev
```
Then open http://localhost:3000

### Production Build
```bash
npm run ui:build
```
The built files will be in `dist-ui/`

### Preview Production Build
```bash
npm run ui:preview
```

## Architecture

- **Framework**: React 18
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3
- **Visualization**: SVG-based custom graphics
- **State Management**: React Hooks (useState, useEffect)
- **Animation**: CSS transitions + SVG animations

## Features

### Real-time Updates
- 50ms animation loop for smooth transitions
- Live data updates (ready for WebSocket integration)
- Animated edge flows showing data propagation

### Interactive Elements
- Click nodes to inspect details
- Tab navigation between views
- Responsive hover states
- Smooth transitions

### Visual Design
- Dark theme optimized for long monitoring sessions
- Purple/blue gradient branding
- Color-coded event types for quick recognition
- Heat map visualization for field metrics

## Data Structure

The UI expects data in the following format:

```javascript
{
  trace: {
    nodes: [{ id, kind, label, timestamp, hash }],
    edges: [{ source, target, relationship }]
  },
  fields: {
    fields: [{ key, namespace, type, value, velocity }],
    proposals: [{ optimizer, pattern, action, confidence }]
  },
  reflexes: {
    reflexes: [{ id, name, priority, enabled, ratified, activation_count }],
    recent_activations: [{ reflex, trigger, timestamp }]
  },
  stats: { spikes_processed, reflexes_activated }
}
```

## Integration

Currently using demo data. To integrate with live system:

1. **WebSocket Connection**: Connect to SynapseBus event stream
2. **Update Data State**: Replace demo data with real-time updates
3. **Event Handlers**: Add callbacks for user actions (pause, filter, etc.)

## Future Enhancements

- WebSocket integration for real-time data
- Historical data playback
- Event filtering and search
- Export capabilities
- Customizable dashboards
- Multi-system monitoring

## License

Part of the StrategicKhaos Sovereignty Architecture project.
