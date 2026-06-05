#!/usr/bin/env python3
"""
ReflexShell Agent v1
Deterministic failover orchestrator for multi-layer network architecture
"""

import time
import yaml
import subprocess
from typing import Dict, List, Any, Optional

STATE_OK = "OK"
STATE_FAIL = "FAIL"


def ping(host: str) -> bool:
    """
    Ping a single host to check reachability.
    
    Args:
        host: IP address or hostname to ping
        
    Returns:
        True if ping succeeds, False otherwise
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )
        return result.returncode == 0
    except Exception:
        return False


def load_cfg(path: str = "trigger_matrix.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        path: Path to the trigger matrix YAML configuration
        
    Returns:
        Parsed configuration dictionary
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def detector_ping(detector: Dict[str, Any]) -> bool:
    """
    Execute ping-based detector.
    
    Args:
        detector: Detector configuration with 'targets' list
        
    Returns:
        True if ANY target is reachable (OR logic), False otherwise
    """
    targets = detector.get("targets", [])
    results = [ping(target) for target in targets]
    # Pass if ANY target responds
    return any(results) if results else True


def eval_layer(layer_cfg: Dict[str, Any]) -> bool:
    """
    Evaluate layer health based on all detectors.
    
    v1: Only evaluates ping-based detectors (cluster-side)
    Other detector methods are reserved for v2 implementation
    
    Args:
        layer_cfg: Layer configuration with detectors list
        
    Returns:
        True if all applicable detectors pass, False otherwise
    """
    detectors = layer_cfg.get("detectors", [])
    results = []
    
    for detector in detectors:
        method = detector.get("method")
        if method == "ping":
            results.append(detector_ping(detector))
        # Other methods (android_radio, android_ui_probe, k8s, manual_attestation)
        # are reserved for v2 implementation
    
    # All detectors must pass
    return all(results) if results else True


def log_event(message: str) -> None:
    """
    Log an event with timestamp for audit trail.
    
    Args:
        message: Event message to log
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [REFLEX] {message}")


def main() -> None:
    """
    Main agent loop.
    
    v1 Behavior:
    - Monitors WAN health via ping to public DNS
    - Logs actions to enable mesh mode on WAN failure
    - Continues monitoring for recovery
    - Human operator performs manual actions based on logs
    """
    # Load configuration
    try:
        cfg = load_cfg()
    except FileNotFoundError:
        # Try parent directory if running from reflexshell_agent/
        cfg = load_cfg("../trigger_matrix.yaml")
    
    poll_interval = cfg["globals"]["poll_interval_seconds"]
    escalation_order = cfg["policies"]["escalation_order"]
    
    log_event("ReflexShell Agent v1 starting")
    log_event(f"Poll interval: {poll_interval}s")
    log_event(f"Escalation order: {' → '.join(escalation_order)}")
    
    # v1: Focus on WAN (L1/L2) vs LAN (L4) decision
    # This is the most actionable automation for cluster nodes
    
    current_state = "WAN_ACTIVE"
    
    while True:
        # Check WAN health using external connectivity
        wan_ok = ping("1.1.1.1") or ping("8.8.8.8")
        
        if not wan_ok and current_state == "WAN_ACTIVE":
            log_event("WAN health check: FAILED (both 1.1.1.1 and 8.8.8.8 unreachable)")
            log_event("WAN down -> enabling mesh mode (v1 - manual action required)")
            log_event("ACTION REQUIRED: kubectl apply -f mesh-mode-config.yaml")
            current_state = "MESH_MODE"
            
        elif wan_ok and current_state == "MESH_MODE":
            log_event("WAN health check: OK")
            log_event("WAN restored -> normal mode (v1 - manual action required)")
            log_event("ACTION REQUIRED: kubectl delete -f mesh-mode-config.yaml")
            current_state = "WAN_ACTIVE"
            
        elif wan_ok and current_state == "WAN_ACTIVE":
            # Healthy state, log periodically (every 5 cycles to reduce noise)
            if int(time.time()) % (poll_interval * 5) < poll_interval:
                log_event("WAN health check: OK (normal operation)")
        
        time.sleep(poll_interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_event("Agent stopped by user")
    except Exception as e:
        log_event(f"Agent error: {e}")
        raise
