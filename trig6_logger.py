#!/usr/bin/env python3
"""
trig6_logger.py

SAGCO-OS TRIG6 Logging System

Provides structured logging for the TRIG6 trigonometric multi-agent
orchestration system with metrics tracking and event recording.

Part of: Self-Amplifying Generative Cognitive Operating System
DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1-LOM1-TRIG6-WAVE1-HYBRID1-NEURO1-OPS1-BOOT1

Copyright (c) 2026 Strategickhaos DAO LLC
Inventor: Dom Garza
"""

import json
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class EventType(Enum):
    """TRIG6 event types"""
    ORCHESTRATION = "orchestration"
    MODE_SWITCH = "mode_switch"
    DANGER_ZONE = "danger_zone"
    METRIC_UPDATE = "metric_update"
    AGENT_WEIGHT = "agent_weight"
    CORRECTIVE_ACTION = "corrective_action"
    THETA_UPDATE = "theta_update"


class Severity(Enum):
    """Event severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class TRIG6Event:
    """TRIG6 event record"""
    event_type: EventType
    severity: Severity
    timestamp: float
    theta: float
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['severity'] = self.severity.value
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())


class TRIG6Logger:
    """
    Structured logger for TRIG6 system events
    
    Provides:
    - Structured event logging with JSON format
    - File and console output
    - Event filtering by severity
    - Metrics aggregation
    - Historical event tracking
    """
    
    def __init__(self, log_dir: str = "/tmp/sagco_logs", 
                 console_level: Severity = Severity.INFO):
        """
        Initialize TRIG6 logger
        
        Args:
            log_dir: Directory for log files
            console_level: Minimum severity for console output
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.console_level = console_level
        self.events: List[TRIG6Event] = []
        
        # Setup standard Python logger
        self.logger = logging.getLogger("TRIG6")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler for all events
        log_file = self.log_dir / f"trig6_{int(time.time())}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler with configurable level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._severity_to_logging_level(console_level))
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"TRIG6 Logger initialized. Log file: {log_file}")
    
    def _severity_to_logging_level(self, severity: Severity) -> int:
        """Convert Severity enum to logging level"""
        mapping = {
            Severity.DEBUG: logging.DEBUG,
            Severity.INFO: logging.INFO,
            Severity.WARNING: logging.WARNING,
            Severity.ERROR: logging.ERROR,
            Severity.CRITICAL: logging.CRITICAL
        }
        return mapping.get(severity, logging.INFO)
    
    def log_event(self, event: TRIG6Event):
        """
        Log a TRIG6 event
        
        Args:
            event: TRIG6Event to log
        """
        # Store event
        self.events.append(event)
        
        # Log to standard logger
        level = self._severity_to_logging_level(event.severity)
        self.logger.log(level, f"[{event.event_type.value}] θ={event.theta:.4f} - {event.message}")
        
        # Write JSON to dedicated event log
        event_log_file = self.log_dir / "trig6_events.jsonl"
        with open(event_log_file, 'a') as f:
            f.write(event.to_json() + "\n")
    
    def log_orchestration(self, theta: float, mode: str, alpha: float,
                         agent_weights: Dict[str, float], metrics: Dict[str, float]):
        """
        Log an orchestration event
        
        Args:
            theta: Task angle
            mode: Projection mode
            alpha: Blend ratio
            agent_weights: Dictionary of agent weights
            metrics: Dictionary of metric scores
        """
        event = TRIG6Event(
            event_type=EventType.ORCHESTRATION,
            severity=Severity.INFO,
            timestamp=time.time(),
            theta=theta,
            message=f"Orchestration in {mode} mode (α={alpha:.3f})",
            metadata={
                "mode": mode,
                "alpha": alpha,
                "agent_weights": agent_weights,
                "metrics": metrics
            }
        )
        self.log_event(event)
    
    def log_mode_switch(self, theta: float, old_mode: str, new_mode: str,
                       trigger: str):
        """
        Log a mode switch event
        
        Args:
            theta: Current task angle
            old_mode: Previous mode
            new_mode: New mode
            trigger: Reason for switch
        """
        event = TRIG6Event(
            event_type=EventType.MODE_SWITCH,
            severity=Severity.WARNING,
            timestamp=time.time(),
            theta=theta,
            message=f"Mode switch: {old_mode} → {new_mode} ({trigger})",
            metadata={
                "old_mode": old_mode,
                "new_mode": new_mode,
                "trigger": trigger
            }
        )
        self.log_event(event)
    
    def log_danger_zone(self, theta: float, agents: List[str], 
                       singularities: List[str]):
        """
        Log a danger zone warning
        
        Args:
            theta: Current task angle
            agents: Affected agents
            singularities: Approaching singularities
        """
        event = TRIG6Event(
            event_type=EventType.DANGER_ZONE,
            severity=Severity.WARNING,
            timestamp=time.time(),
            theta=theta,
            message=f"Danger zone: {len(agents)} agent(s) near singularity",
            metadata={
                "affected_agents": agents,
                "singularities": singularities
            }
        )
        self.log_event(event)
    
    def log_metric_update(self, theta: float, metrics: Dict[str, float]):
        """
        Log metric update
        
        Args:
            theta: Current task angle
            metrics: Updated metrics
        """
        # Determine severity based on metric thresholds
        severity = Severity.DEBUG
        if metrics.get("drift", 0) > 0.3:
            severity = Severity.WARNING
        if metrics.get("resonance", 1.0) < 0.3:
            severity = Severity.WARNING
        
        event = TRIG6Event(
            event_type=EventType.METRIC_UPDATE,
            severity=severity,
            timestamp=time.time(),
            theta=theta,
            message=f"Metrics: R={metrics.get('resonance', 0):.3f}, "
                   f"D={metrics.get('drift', 0):.3f}, N={metrics.get('noise', 0):.3f}",
            metadata=metrics
        )
        self.log_event(event)
    
    def log_corrective_action(self, theta: float, action: str, reason: str):
        """
        Log a corrective action
        
        Args:
            theta: Current task angle
            action: Action taken
            reason: Reason for action
        """
        event = TRIG6Event(
            event_type=EventType.CORRECTIVE_ACTION,
            severity=Severity.INFO,
            timestamp=time.time(),
            theta=theta,
            message=f"Corrective action: {action}",
            metadata={
                "action": action,
                "reason": reason
            }
        )
        self.log_event(event)
    
    def log_theta_update(self, old_theta: float, new_theta: float, reason: str):
        """
        Log theta update
        
        Args:
            old_theta: Previous theta value
            new_theta: New theta value
            reason: Reason for update
        """
        event = TRIG6Event(
            event_type=EventType.THETA_UPDATE,
            severity=Severity.DEBUG,
            timestamp=time.time(),
            theta=new_theta,
            message=f"Theta updated: {old_theta:.4f} → {new_theta:.4f}",
            metadata={
                "old_theta": old_theta,
                "new_theta": new_theta,
                "delta": new_theta - old_theta,
                "reason": reason
            }
        )
        self.log_event(event)
    
    def get_events(self, event_type: Optional[EventType] = None,
                   severity: Optional[Severity] = None,
                   since: Optional[float] = None) -> List[TRIG6Event]:
        """
        Get filtered events
        
        Args:
            event_type: Filter by event type
            severity: Filter by minimum severity
            since: Filter by timestamp (events after this time)
            
        Returns:
            List of matching events
        """
        filtered = self.events
        
        if event_type is not None:
            filtered = [e for e in filtered if e.event_type == event_type]
        
        if severity is not None:
            severity_order = [Severity.DEBUG, Severity.INFO, Severity.WARNING, 
                            Severity.ERROR, Severity.CRITICAL]
            min_index = severity_order.index(severity)
            filtered = [e for e in filtered 
                       if severity_order.index(e.severity) >= min_index]
        
        if since is not None:
            filtered = [e for e in filtered if e.timestamp >= since]
        
        return filtered
    
    def get_metrics_summary(self) -> Dict:
        """
        Get summary of metrics over time
        
        Returns:
            Dictionary with metrics statistics
        """
        metric_events = self.get_events(event_type=EventType.METRIC_UPDATE)
        
        if not metric_events:
            return {}
        
        # Extract metrics
        resonance_values = []
        drift_values = []
        noise_values = []
        
        for event in metric_events:
            if "resonance" in event.metadata:
                resonance_values.append(event.metadata["resonance"])
            if "drift" in event.metadata:
                drift_values.append(event.metadata["drift"])
            if "noise" in event.metadata:
                noise_values.append(event.metadata["noise"])
        
        summary = {
            "sample_count": len(metric_events)
        }
        
        if resonance_values:
            summary["resonance"] = {
                "min": min(resonance_values),
                "max": max(resonance_values),
                "avg": sum(resonance_values) / len(resonance_values)
            }
        
        if drift_values:
            summary["drift"] = {
                "min": min(drift_values),
                "max": max(drift_values),
                "avg": sum(drift_values) / len(drift_values)
            }
        
        if noise_values:
            summary["noise"] = {
                "min": min(noise_values),
                "max": max(noise_values),
                "avg": sum(noise_values) / len(noise_values)
            }
        
        return summary
    
    def export_summary(self, output_file: Optional[str] = None) -> str:
        """
        Export summary report
        
        Args:
            output_file: Optional file to write summary to
            
        Returns:
            Summary text
        """
        lines = []
        lines.append("=" * 80)
        lines.append("TRIG6 System Log Summary")
        lines.append("=" * 80)
        lines.append(f"Total events: {len(self.events)}")
        lines.append("")
        
        # Event counts by type
        lines.append("Events by Type:")
        type_counts = {}
        for event in self.events:
            type_name = event.event_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        for event_type, count in sorted(type_counts.items()):
            lines.append(f"  {event_type:20s}: {count}")
        lines.append("")
        
        # Severity distribution
        lines.append("Events by Severity:")
        severity_counts = {}
        for event in self.events:
            sev_name = event.severity.value
            severity_counts[sev_name] = severity_counts.get(sev_name, 0) + 1
        
        for severity, count in sorted(severity_counts.items()):
            lines.append(f"  {severity:20s}: {count}")
        lines.append("")
        
        # Metrics summary
        metrics_summary = self.get_metrics_summary()
        if metrics_summary:
            lines.append("Metrics Summary:")
            for metric, stats in metrics_summary.items():
                if metric != "sample_count":
                    lines.append(f"  {metric.title()}:")
                    lines.append(f"    Min: {stats['min']:.4f}")
                    lines.append(f"    Max: {stats['max']:.4f}")
                    lines.append(f"    Avg: {stats['avg']:.4f}")
            lines.append("")
        
        lines.append("=" * 80)
        
        summary_text = "\n".join(lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(summary_text)
        
        return summary_text


def main():
    """Example usage and demonstration"""
    import math
    import random
    
    print("=" * 80)
    print("SAGCO-OS TRIG6 Logging System Demonstration")
    print("=" * 80)
    print()
    
    # Initialize logger
    logger = TRIG6Logger(log_dir="/tmp/sagco_logs", console_level=Severity.INFO)
    
    # Simulate orchestration events
    print("Simulating TRIG6 orchestration events...\n")
    
    thetas = [0.5, math.pi/4, math.pi/2 - 0.1, math.pi/2, 3*math.pi/4]
    modes = ["trigonometric", "hybrid", "hybrid", "hyperbolic", "hybrid"]
    
    for i, (theta, mode) in enumerate(zip(thetas, modes)):
        # Log orchestration
        agent_weights = {
            "GPT": abs(math.sin(theta)),
            "Claude": abs(math.cos(theta)),
            "Grok": random.uniform(0.3, 0.9),
            "Gemini": random.uniform(0.3, 0.9),
            "Web": random.uniform(0.2, 0.6),
            "SAGCO": 1.0
        }
        
        metrics = {
            "resonance": random.uniform(0.6, 0.95),
            "drift": random.uniform(0.1, 0.4),
            "noise": random.uniform(0.05, 0.2)
        }
        
        alpha = 0.0 if mode == "trigonometric" else \
                (1.0 if mode == "hyperbolic" else 0.5)
        
        logger.log_orchestration(theta, mode, alpha, agent_weights, metrics)
        logger.log_metric_update(theta, metrics)
        
        # Log mode switch if applicable
        if i > 0 and modes[i] != modes[i-1]:
            logger.log_mode_switch(theta, modes[i-1], modes[i], 
                                  f"drift={metrics['drift']:.3f}")
        
        # Log danger zone for certain thetas
        if abs(theta - math.pi/2) < 0.15:
            logger.log_danger_zone(theta, ["Grok", "Web"], 
                                  ["tan at π/2", "sec at π/2"])
        
        # Small delay to simulate time passing
        time.sleep(0.1)
    
    # Log some corrective actions
    logger.log_corrective_action(math.pi/2, "agent_muting", 
                                "Grok noise contribution too high")
    logger.log_theta_update(math.pi/2, math.pi/4, 
                           "FOCUS Router adjustment")
    
    # Print summary
    print("\n" + logger.export_summary())
    
    # Export to file
    summary_file = "/tmp/sagco_logs/trig6_summary.txt"
    logger.export_summary(summary_file)
    print(f"\nSummary exported to: {summary_file}")
    
    # Show recent warnings
    warnings = logger.get_events(severity=Severity.WARNING)
    print(f"\nTotal warnings: {len(warnings)}")
    if warnings:
        print("\nRecent warnings:")
        for event in warnings[-3:]:
            print(f"  - {event.message}")


if __name__ == "__main__":
    main()
