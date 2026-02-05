# ReflexShell Agent (v1)

## Purpose

The ReflexShell Agent is a deterministic failover orchestrator that:
- Polls network layer health detectors
- Applies debounce and confirmation logic to avoid flapping
- Executes failover actions based on the trigger matrix
- Logs all state transitions for audit and troubleshooting

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ReflexShell Agent v1                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Detector   │────▶│ State Logic  │────▶│   Actions   │ │
│  │   Modules    │     │  (debounce)  │     │  Executor   │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│         │                     │                     │        │
│         ▼                     ▼                     ▼        │
│  • ping checks         • confirm_fail        • Android SIM  │
│  • android_radio       • hysteresis          • Cluster mesh │
│  • k8s health          • escalation          • Alerts       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## v1 Implementation Status

### ✅ Implemented (v1)
- **Cluster-side detectors**: Ping-based WAN health checks
- **State machine core**: Load YAML configuration
- **Cluster actions**: Mesh mode enable/disable (placeholder for kubectl)
- **Logging**: Simple console logging for audit trail

### 🚧 Manual (v1)
- **Android actions**: Manual SIM switching via device UI
- **Satellite detection**: Visual confirmation of satellite indicator
- **State persistence**: In-memory only (no database)

### 🔮 Planned (v2)
- **ADB automation**: Programmatic Android SIM switching
- **Kubernetes operator**: Native k8s CRD for mesh transitions
- **UI probing**: Automated screenshot analysis for satellite indicators
- **Distributed consensus**: Multi-node state agreement
- **Persistent state**: Database or etcd backend

## Usage

### Running the Agent

```bash
# From the 05_cross_layer_failover directory
python3 reflexshell_agent/reflex_agent.py
```

### Configuration

The agent reads from `trigger_matrix.yaml` in the parent directory. Key parameters:

- `poll_interval_seconds`: How often to check layer health (default: 15s)
- `debounce_seconds`: Minimum time before confirming failure (default: 30s)
- `confirm_fail_count`: Consecutive failures needed to trigger action (default: 3)
- `recover_confirm_count`: Consecutive successes needed to recover (default: 4)

### v1 Workflow

1. **Agent starts** and loads configuration
2. **Polls WAN health** using ping to public DNS servers
3. **Detects WAN failure** after consecutive failures
4. **Logs action** to enable mesh mode (manual kubectl apply)
5. **Continues monitoring** for recovery
6. **Logs recovery** when WAN is restored

### Manual Actions (v1)

When the agent logs a required action, perform manually:

**Enable mesh mode:**
```bash
kubectl apply -f ../mesh-mode-config.yaml
# Or follow your cluster-specific mesh enablement procedure
```

**Switch Android SIM:**
1. Open Settings → Network & Internet → SIMs
2. Select the target SIM for data
3. Confirm the switch

**Verify satellite mode:**
1. Check notification bar for satellite indicator
2. Confirm message capability with test SMS
3. Log results for audit

## Log Format

All transitions are logged with timestamps for audit:

```
[2026-02-05 01:30:15] [REFLEX] WAN health check: 1.1.1.1 FAIL, 8.8.8.8 FAIL
[2026-02-05 01:30:45] [REFLEX] WAN down (confirmed) -> enabling mesh mode (v1)
[2026-02-05 01:35:00] [REFLEX] WAN health check: 1.1.1.1 OK
[2026-02-05 01:35:30] [REFLEX] WAN restored (confirmed) -> normal mode (v1)
```

## Dependencies

**Python 3.8+** with:
- `pyyaml` for configuration parsing
- Standard library only (subprocess, time)

Install dependencies:
```bash
pip install pyyaml
```

## Testing

### Unit Test Detector Logic

```python
from reflex_agent import ping, detector_ping

# Test single host ping
assert ping("1.1.1.1") in [True, False]

# Test detector with multiple targets
detector_config = {"targets": ["1.1.1.1", "8.8.8.8"]}
result = detector_ping(detector_config)
```

### Integration Test (Manual)

1. Run agent with normal network
2. Disconnect WAN (unplug ethernet or disable Wi-Fi)
3. Observe agent logs showing WAN failure detection
4. Verify mesh mode action is logged
5. Reconnect WAN
6. Observe recovery detection and normal mode restore

## Security Considerations

- Agent runs with **minimal privileges** for cluster nodes
- No credential storage (uses ambient cluster auth)
- All actions are **logged and auditable**
- Fail-closed policy prevents unsafe fallbacks
- Rate limiting prevents log spam

## Future Enhancements (v2+)

- **Android automation via ADB**: Eliminate manual SIM switching
- **OCR-based UI probing**: Detect satellite indicators programmatically
- **Multi-node coordination**: Distributed state machine for cluster consensus
- **Web dashboard**: Real-time visualization of layer health and transitions
- **Alert integration**: PagerDuty, Slack, or SMS notifications
- **Metrics export**: Prometheus metrics for monitoring integration

## Contributing

This is v1 (semi-automated). Contributions welcome for:
- ADB integration for Android automation
- Kubernetes operator implementation
- Enhanced detector modules (signal strength, latency, etc.)
- Test coverage and CI/CD integration

---

**Status**: Production-ready for cluster-side failover with manual Android actions  
**Version**: 1.0  
**License**: See repository LICENSE file
