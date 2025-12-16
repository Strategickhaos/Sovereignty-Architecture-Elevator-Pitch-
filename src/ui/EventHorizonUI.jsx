import React, { useState, useEffect, useRef, useCallback } from 'react';

// Event Horizon UI v0 - SynapseBus Visualization
// StrategicKhaos Swarm Intelligence

const EventHorizonUI = () => {
  // Demo data - in production, this would come from WebSocket/API
  const [data, setData] = useState({
    trace: {
      nodes: [
        { id: 'spike-001', kind: 'proc.spawn', label: 'nginx started', timestamp: Date.now() - 5000, hash: 'a1b2c3' },
        { id: 'spike-002', kind: 'proc.spawn', label: 'python3 app.py', timestamp: Date.now() - 4500, hash: 'd4e5f6' },
        { id: 'spike-003', kind: 'fs.read', label: '/etc/passwd', timestamp: Date.now() - 4000, hash: 'g7h8i9' },
        { id: 'spike-004', kind: 'fs.read', label: '/var/secrets/api_key', timestamp: Date.now() - 3500, hash: 'j0k1l2' },
        { id: 'spike-005', kind: 'net.flow.start', label: '10.0.0.5:5432', timestamp: Date.now() - 3000, hash: 'm3n4o5' },
        { id: 'spike-006', kind: 'net.flow.anomaly', label: 'Unusual outbound', timestamp: Date.now() - 2000, hash: 'p6q7r8' },
        { id: 'spike-007', kind: 'sec.quarantine', label: 'Process isolated', timestamp: Date.now() - 1000, hash: 's9t0u1' },
      ],
      edges: [
        { source: 'spike-001', target: 'spike-002', relationship: 'caused_by' },
        { source: 'spike-002', target: 'spike-003', relationship: 'triggered' },
        { source: 'spike-003', target: 'spike-004', relationship: 'triggered' },
        { source: 'spike-004', target: 'spike-005', relationship: 'triggered' },
        { source: 'spike-005', target: 'spike-006', relationship: 'caused_by' },
        { source: 'spike-006', target: 'spike-007', relationship: 'triggered' },
      ],
    },
    fields: {
      fields: [
        { key: 'kernel:Entropy', namespace: 'kernel', type: 'Entropy', value: 0.45, velocity: 0.02 },
        { key: 'kernel:Mass', namespace: 'kernel', type: 'Mass', value: 3.2, velocity: 0.1 },
        { key: 'net/monitor:Entropy', namespace: 'net/monitor', type: 'Entropy', value: 0.85, velocity: 0.15 },
        { key: 'net/monitor:Trust', namespace: 'net/monitor', type: 'Trust', value: 0.25, velocity: -0.1 },
        { key: 'fs/audit:Mass', namespace: 'fs/audit', type: 'Mass', value: 5.8, velocity: 0.5 },
      ],
      proposals: [
        { optimizer: 'Simulated Annealing', pattern: 'entropy > 0.8', action: 'cool_down_sandbox', confidence: 0.9 },
        { optimizer: 'Black Hole', pattern: 'trust < 0.3', action: 'absorb_and_quarantine', confidence: 0.95 },
      ],
    },
    reflexes: {
      reflexes: [
        { id: 'r1', name: 'entropy_mass_isolation', priority: 80, enabled: true, ratified: true, activation_count: 3 },
        { id: 'r2', name: 'low_trust_quarantine', priority: 90, enabled: true, ratified: true, activation_count: 1 },
        { id: 'r3', name: 'exfil_throttle', priority: 70, enabled: true, ratified: true, activation_count: 2 },
      ],
      recent_activations: [
        { reflex: 'low_trust_quarantine', trigger: 'spike-006', timestamp: Date.now() - 1500 },
        { reflex: 'entropy_mass_isolation', trigger: 'spike-006', timestamp: Date.now() - 1400 },
      ],
    },
    stats: { spikes_processed: 7, reflexes_activated: 2 },
  });

  const [selectedNode, setSelectedNode] = useState(null);
  const [viewMode, setViewMode] = useState('graph'); // 'graph', 'fields', 'reflexes'
  const canvasRef = useRef(null);
  const [time, setTime] = useState(Date.now());

  // Animation loop
  useEffect(() => {
    const interval = setInterval(() => setTime(Date.now()), 50);
    return () => clearInterval(interval);
  }, []);

  // Get color based on spike kind
  const getNodeColor = (kind) => {
    if (kind.startsWith('proc')) return '#3b82f6'; // Blue
    if (kind.startsWith('fs')) return '#22c55e'; // Green
    if (kind.startsWith('net.flow.anomaly')) return '#ef4444'; // Red
    if (kind.startsWith('net')) return '#f59e0b'; // Orange
    if (kind.startsWith('sec')) return '#a855f7'; // Purple
    return '#6b7280'; // Gray
  };

  // Get entropy heat color
  const getHeatColor = (value) => {
    const r = Math.floor(255 * Math.min(value * 2, 1));
    const g = Math.floor(255 * Math.max(0, 1 - value * 2));
    return `rgb(${r}, ${g}, 50)`;
  };

  // Render trace graph
  const renderGraph = () => {
    const nodes = data.trace.nodes;
    const edges = data.trace.edges;
    const width = 800;
    const height = 400;
    const nodeRadius = 25;

    // Layout nodes in a timeline
    const nodePositions = {};
    nodes.forEach((node, i) => {
      const x = 80 + (i * (width - 160) / Math.max(nodes.length - 1, 1));
      const y = height / 2 + Math.sin(i * 0.8) * 60;
      nodePositions[node.id] = { x, y };
    });

    return (
      <svg width={width} height={height} className="bg-gray-900 rounded-lg">
        {/* Edges */}
        {edges.map((edge, i) => {
          const source = nodePositions[edge.source];
          const target = nodePositions[edge.target];
          if (!source || !target) return null;
          
          // Animated dash offset
          const dashOffset = (time / 50) % 20;
          
          return (
            <g key={`edge-${i}`}>
              <line
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                stroke="#4b5563"
                strokeWidth="2"
                strokeDasharray="10,5"
                strokeDashoffset={dashOffset}
              />
              {/* Arrow */}
              <polygon
                points={`${target.x - 15},${target.y - 5} ${target.x - 15},${target.y + 5} ${target.x - 5},${target.y}`}
                fill="#4b5563"
                transform={`rotate(${Math.atan2(target.y - source.y, target.x - source.x) * 180 / Math.PI}, ${target.x - 10}, ${target.y})`}
              />
            </g>
          );
        })}

        {/* Nodes */}
        {nodes.map((node, i) => {
          const pos = nodePositions[node.id];
          const color = getNodeColor(node.kind);
          const isSelected = selectedNode === node.id;
          
          // Pulse animation for anomalies
          const pulse = node.kind.includes('anomaly') 
            ? 1 + Math.sin(time / 200) * 0.2 
            : 1;

          return (
            <g
              key={node.id}
              transform={`translate(${pos.x}, ${pos.y})`}
              onClick={() => setSelectedNode(isSelected ? null : node.id)}
              style={{ cursor: 'pointer' }}
            >
              {/* Glow for selected */}
              {isSelected && (
                <circle r={nodeRadius + 10} fill={color} opacity="0.3" />
              )}
              
              {/* Node circle */}
              <circle
                r={nodeRadius * pulse}
                fill={color}
                stroke={isSelected ? '#fff' : '#1f2937'}
                strokeWidth={isSelected ? 3 : 2}
              />
              
              {/* Icon based on type */}
              <text
                textAnchor="middle"
                dy="0.35em"
                fill="white"
                fontSize="16"
                fontWeight="bold"
              >
                {node.kind.startsWith('proc') ? '⚙' :
                 node.kind.startsWith('fs') ? '📁' :
                 node.kind.includes('anomaly') ? '⚠' :
                 node.kind.startsWith('net') ? '🌐' :
                 node.kind.startsWith('sec') ? '🛡' : '•'}
              </text>
              
              {/* Label */}
              <text
                y={nodeRadius + 15}
                textAnchor="middle"
                fill="#9ca3af"
                fontSize="10"
              >
                {node.kind.split('.').pop()}
              </text>
            </g>
          );
        })}

        {/* Title */}
        <text x="20" y="30" fill="#fff" fontSize="18" fontWeight="bold">
          Trace Graph — Dendrite View
        </text>
        <text x="20" y="50" fill="#6b7280" fontSize="12">
          {nodes.length} spikes • {edges.length} synapses
        </text>
      </svg>
    );
  };

  // Render field heatmap
  const renderFields = () => {
    const fields = data.fields.fields;
    const proposals = data.fields.proposals;

    return (
      <div className="bg-gray-900 rounded-lg p-4">
        <h3 className="text-white text-lg font-bold mb-4">Physics Fields — Heat Map</h3>
        
        {/* Field grid */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {fields.map((field, i) => (
            <div
              key={i}
              className="p-3 rounded-lg border"
              style={{
                backgroundColor: field.type === 'Entropy' 
                  ? getHeatColor(field.value) 
                  : field.type === 'Trust'
                    ? getHeatColor(1 - field.value)
                    : '#1f2937',
                borderColor: '#374151',
              }}
            >
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-white font-mono text-sm">{field.namespace}</div>
                  <div className="text-gray-400 text-xs">{field.type}</div>
                </div>
                <div className="text-right">
                  <div className="text-white text-xl font-bold">{field.value.toFixed(2)}</div>
                  <div className={`text-xs ${field.velocity > 0 ? 'text-red-400' : 'text-green-400'}`}>
                    {field.velocity > 0 ? '↑' : '↓'} {Math.abs(field.velocity).toFixed(2)}/s
                  </div>
                </div>
              </div>
              
              {/* Progress bar */}
              <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
                <div
                  className="h-full transition-all duration-300"
                  style={{
                    width: `${Math.min(field.value * 100, 100)}%`,
                    backgroundColor: field.type === 'Entropy' ? '#ef4444' :
                                    field.type === 'Mass' ? '#3b82f6' :
                                    field.type === 'Trust' ? '#22c55e' : '#f59e0b',
                  }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Proposals */}
        <h4 className="text-white font-bold mb-2">Reflex Proposals</h4>
        <div className="space-y-2">
          {proposals.map((prop, i) => (
            <div key={i} className="flex items-center justify-between bg-gray-800 p-2 rounded">
              <div>
                <span className="text-purple-400 font-mono text-sm">{prop.optimizer}</span>
                <span className="text-gray-500 mx-2">→</span>
                <span className="text-yellow-400 font-mono text-sm">{prop.action}</span>
              </div>
              <div className="text-green-400 font-bold">
                {(prop.confidence * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render reflex monitor
  const renderReflexes = () => {
    const reflexes = data.reflexes.reflexes;
    const activations = data.reflexes.recent_activations;

    return (
      <div className="bg-gray-900 rounded-lg p-4">
        <h3 className="text-white text-lg font-bold mb-4">Reflex Engine — Spinal Cord</h3>
        
        {/* Active reflexes */}
        <div className="space-y-2 mb-6">
          {reflexes.map((reflex, i) => (
            <div
              key={i}
              className="flex items-center justify-between p-3 rounded-lg"
              style={{
                backgroundColor: reflex.activation_count > 0 ? '#1e3a5f' : '#1f2937',
                borderLeft: `4px solid ${reflex.ratified ? '#22c55e' : '#f59e0b'}`,
              }}
            >
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${reflex.enabled ? 'bg-green-500' : 'bg-gray-500'}`} />
                <div>
                  <div className="text-white font-mono">{reflex.name}</div>
                  <div className="text-gray-500 text-xs">Priority: {reflex.priority}</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-blue-400 font-bold">{reflex.activation_count}x</div>
                <div className="text-gray-500 text-xs">
                  {reflex.ratified ? '✓ Ratified' : '⏳ Pending'}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Recent activations */}
        <h4 className="text-white font-bold mb-2">Recent Activations</h4>
        <div className="space-y-1">
          {activations.map((act, i) => {
            const age = Math.floor((Date.now() - act.timestamp) / 1000);
            return (
              <div key={i} className="flex items-center gap-2 text-sm">
                <span className="text-red-400">⚡</span>
                <span className="text-purple-400 font-mono">{act.reflex}</span>
                <span className="text-gray-500">←</span>
                <span className="text-gray-400 font-mono">{act.trigger}</span>
                <span className="text-gray-600 ml-auto">{age}s ago</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  // Node detail panel
  const renderNodeDetail = () => {
    if (!selectedNode) return null;
    const node = data.trace.nodes.find(n => n.id === selectedNode);
    if (!node) return null;

    return (
      <div className="bg-gray-800 rounded-lg p-4 mt-4">
        <div className="flex justify-between items-start">
          <div>
            <h4 className="text-white font-bold">{node.kind}</h4>
            <p className="text-gray-400">{node.label}</p>
          </div>
          <button
            onClick={() => setSelectedNode(null)}
            className="text-gray-500 hover:text-white"
          >
            ✕
          </button>
        </div>
        <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
          <div className="text-gray-500">ID:</div>
          <div className="text-gray-300 font-mono">{node.id}</div>
          <div className="text-gray-500">Hash:</div>
          <div className="text-gray-300 font-mono">{node.hash}</div>
          <div className="text-gray-500">Time:</div>
          <div className="text-gray-300">{new Date(node.timestamp).toLocaleTimeString()}</div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-black text-white p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            Event Horizon UI v0
          </h1>
          <p className="text-gray-500">SynapseBus Nervous System Visualization</p>
        </div>
        <div className="flex gap-2">
          <div className="px-3 py-1 bg-gray-800 rounded text-sm">
            <span className="text-gray-400">Spikes:</span>{' '}
            <span className="text-green-400 font-bold">{data.stats.spikes_processed}</span>
          </div>
          <div className="px-3 py-1 bg-gray-800 rounded text-sm">
            <span className="text-gray-400">Reflexes:</span>{' '}
            <span className="text-purple-400 font-bold">{data.stats.reflexes_activated}</span>
          </div>
        </div>
      </div>

      {/* View tabs */}
      <div className="flex gap-2 mb-4">
        {['graph', 'fields', 'reflexes'].map((mode) => (
          <button
            key={mode}
            onClick={() => setViewMode(mode)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              viewMode === mode
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {mode === 'graph' ? '🧠 Trace Graph' :
             mode === 'fields' ? '🔥 Field Map' :
             '⚡ Reflexes'}
          </button>
        ))}
      </div>

      {/* Main view */}
      <div className="mb-4">
        {viewMode === 'graph' && renderGraph()}
        {viewMode === 'fields' && renderFields()}
        {viewMode === 'reflexes' && renderReflexes()}
      </div>

      {/* Node detail */}
      {viewMode === 'graph' && renderNodeDetail()}

      {/* Footer */}
      <div className="mt-6 text-center text-gray-600 text-sm">
        StrategicKhaos Swarm Intelligence • SynapseBus v0.1.0
      </div>
    </div>
  );
};

export default EventHorizonUI;
