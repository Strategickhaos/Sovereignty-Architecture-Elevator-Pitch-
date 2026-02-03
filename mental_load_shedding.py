#!/usr/bin/env python3
"""
Mental Load-Shedding Scheduler
Strategickhaos DAO LLC | Node 137

Real-time cognitive load balancing system that routes, buffers, and processes
inputs without emotional overhead or identity attachment.

"You route." — Not absorb everything. Not block everything. Route.
"""

import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, field
from collections import deque


class InputClassification(Enum):
    """Classification of incoming inputs"""
    IMMEDIATE = "immediate"  # Process now
    BUFFER = "buffer"        # Store for later
    NOISE = "noise"          # Discard
    THREAT = "threat"        # Escalate


class CoreState(Enum):
    """State of core execution system"""
    INTACT = "intact"
    PROCESSING = "processing"
    RECOVERING = "recovering"
    COMPROMISED = "compromised"


@dataclass
class InputData:
    """Wrapper for input data with metadata"""
    content: Any
    source: str
    timestamp: float = field(default_factory=time.time)
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BufferedItem:
    """Item stored in buffer with context"""
    data: InputData
    reason: str
    buffered_at: float
    priority: int
    retry_count: int = 0


class InputClassifier:
    """Classifies incoming inputs based on timing, framing, and actionability"""
    
    def __init__(self, threat_keywords: Optional[List[str]] = None,
                 noise_keywords: Optional[List[str]] = None):
        self.threat_keywords = threat_keywords or ['critical', 'emergency', 'security']
        self.noise_keywords = noise_keywords or ['spam', 'irrelevant']
        
    def classify(self, input_data: InputData, current_context: Dict[str, Any]) -> InputClassification:
        """
        Classify input based on threat level, noise detection, and timing.
        
        Args:
            input_data: The input to classify
            current_context: Current system state and focus
            
        Returns:
            Classification result
        """
        # Quick threat check
        if self._is_threat(input_data):
            return InputClassification.THREAT
        
        # Noise detection
        if self._is_noise(input_data):
            return InputClassification.NOISE
        
        # Timing and framing check
        if not self._is_good_timing(input_data, current_context):
            return InputClassification.BUFFER
        
        # Actionability check
        if not self._is_actionable(input_data, current_context):
            return InputClassification.BUFFER
        
        return InputClassification.IMMEDIATE
    
    def _is_threat(self, input_data: InputData) -> bool:
        """Quick threat detection"""
        content_str = str(input_data.content).lower()
        return any(keyword in content_str for keyword in self.threat_keywords)
    
    def _is_noise(self, input_data: InputData) -> bool:
        """Noise detection - poorly framed or irrelevant"""
        content_str = str(input_data.content).lower()
        return any(keyword in content_str for keyword in self.noise_keywords)
    
    def _is_good_timing(self, input_data: InputData, current_context: Dict[str, Any]) -> bool:
        """Check if timing is appropriate for processing"""
        # If core is busy with high-priority task, timing is wrong
        if current_context.get('focus_level', 0) > 7 and input_data.priority < 8:
            return False
        
        # If input requires context that's not currently loaded
        required_context = input_data.metadata.get('required_context', [])
        loaded_context = current_context.get('loaded_modules', [])
        
        if required_context and not all(ctx in loaded_context for ctx in required_context):
            return False
        
        return True
    
    def _is_actionable(self, input_data: InputData, current_context: Dict[str, Any]) -> bool:
        """Check if input is actionable in current moment"""
        # If input requires resources we don't have, it's not actionable
        required_resources = input_data.metadata.get('required_resources', [])
        available_resources = current_context.get('available_resources', [])
        
        if required_resources and not all(res in available_resources for res in required_resources):
            return False
        
        return True


class CoreExecutor:
    """
    Maintains execution integrity while processing inputs.
    Never compromised by poorly-timed inputs.
    """
    
    def __init__(self):
        self.state = CoreState.INTACT
        self.current_focus: Optional[str] = None
        self.execution_history: List[Dict[str, Any]] = []
    
    def process(self, input_data: InputData) -> Dict[str, Any]:
        """
        Process input while maintaining core integrity.
        
        Args:
            input_data: Input to process
            
        Returns:
            Processing result with status
        """
        if self.state == CoreState.COMPROMISED:
            return {
                'status': 'error',
                'message': 'Core integrity compromised, cannot process',
                'input': input_data
            }
        
        # Begin processing
        self.state = CoreState.PROCESSING
        start_time = time.time()
        
        try:
            # Execute with integrity maintained
            result = self._execute(input_data)
            
            # Record in history
            self.execution_history.append({
                'input': input_data,
                'result': result,
                'timestamp': start_time,
                'duration': time.time() - start_time
            })
            
            # Return to intact state
            self.state = CoreState.INTACT
            
            return {
                'status': 'success',
                'result': result,
                'duration': time.time() - start_time
            }
            
        except Exception as e:
            # Handle error without compromising core
            self.state = CoreState.RECOVERING
            
            return {
                'status': 'error',
                'message': str(e),
                'input': input_data
            }
    
    def _execute(self, input_data: InputData) -> Any:
        """
        Internal execution logic.
        Override this in subclasses for specific behavior.
        """
        # Placeholder - actual implementation depends on use case
        return {
            'processed': True,
            'content': input_data.content,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def recover(self) -> bool:
        """Attempt to recover from error state"""
        if self.state == CoreState.RECOVERING:
            # Simple recovery - in production, this would be more sophisticated
            self.state = CoreState.INTACT
            return True
        return False


class BufferManager:
    """
    Stores poorly-timed inputs for later processing.
    Implements intelligent retrieval based on priority and context.
    """
    
    def __init__(self, max_buffer_size: int = 1000):
        self.buffer: deque[BufferedItem] = deque(maxlen=max_buffer_size)
        self.max_buffer_size = max_buffer_size
        self.total_buffered = 0
        self.total_retrieved = 0
    
    def store(self, input_data: InputData, reason: str) -> bool:
        """
        Store input with context for later retrieval.
        
        Args:
            input_data: Input to buffer
            reason: Reason for buffering
            
        Returns:
            True if stored successfully
        """
        priority = self._calculate_priority(input_data)
        
        item = BufferedItem(
            data=input_data,
            reason=reason,
            buffered_at=time.time(),
            priority=priority
        )
        
        self.buffer.append(item)
        self.total_buffered += 1
        
        return True
    
    def retrieve_when_ready(self, available_capacity: int = 5,
                           current_context: Optional[Dict[str, Any]] = None) -> List[BufferedItem]:
        """
        Return buffered items when resources are available.
        
        Args:
            available_capacity: Number of items that can be processed
            current_context: Current system state for filtering
            
        Returns:
            List of buffered items to process
        """
        if not self.buffer:
            return []
        
        # Filter items that are now actionable
        actionable_items = []
        for item in self.buffer:
            if self._is_now_actionable(item, current_context):
                actionable_items.append(item)
        
        # Sort by priority
        sorted_items = sorted(actionable_items, key=lambda x: x.priority, reverse=True)
        
        # Return top N items
        items_to_return = sorted_items[:available_capacity]
        
        # Remove from buffer
        for item in items_to_return:
            self.buffer.remove(item)
            self.total_retrieved += 1
        
        return items_to_return
    
    def _calculate_priority(self, input_data: InputData) -> int:
        """Calculate priority score for buffered item"""
        # Base priority from input
        priority = input_data.priority
        
        # Boost priority based on source importance
        source_boost = input_data.metadata.get('source_importance', 0)
        priority += source_boost
        
        # Age factor - older items get slight priority boost
        age_boost = int((time.time() - input_data.timestamp) / 3600)  # +1 per hour
        priority += min(age_boost, 5)  # Cap age boost at 5
        
        return priority
    
    def _is_now_actionable(self, item: BufferedItem,
                          current_context: Optional[Dict[str, Any]]) -> bool:
        """Check if a buffered item is now actionable"""
        if not current_context:
            return True  # If no context provided, assume actionable
        
        # Check if required resources are now available
        required_resources = item.data.metadata.get('required_resources', [])
        available_resources = current_context.get('available_resources', [])
        
        if required_resources:
            return all(res in available_resources for res in required_resources)
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get buffer statistics"""
        return {
            'current_size': len(self.buffer),
            'max_size': self.max_buffer_size,
            'total_buffered': self.total_buffered,
            'total_retrieved': self.total_retrieved,
            'utilization': len(self.buffer) / self.max_buffer_size if self.max_buffer_size > 0 else 0
        }


class LoadSheddingScheduler:
    """
    Main scheduler that orchestrates the mental load-shedding system.
    
    "You route." — Self-correction without self-destruction.
    """
    
    def __init__(self):
        self.classifier = InputClassifier()
        self.executor = CoreExecutor()
        self.buffer = BufferManager()
        self.context = {
            'focus_level': 0,
            'loaded_modules': [],
            'available_resources': [],
            'state': 'idle'
        }
        self.metrics = {
            'total_inputs': 0,
            'immediate_processed': 0,
            'buffered': 0,
            'noise_filtered': 0,
            'threats_escalated': 0
        }
    
    def process_input(self, input_data: InputData) -> Dict[str, Any]:
        """
        Main entry point for processing inputs.
        
        Args:
            input_data: Input to process
            
        Returns:
            Processing result
        """
        self.metrics['total_inputs'] += 1
        
        # Classify input
        classification = self.classifier.classify(input_data, self.context)
        
        # Route based on classification
        if classification == InputClassification.IMMEDIATE:
            self.metrics['immediate_processed'] += 1
            return self.executor.process(input_data)
        
        elif classification == InputClassification.BUFFER:
            self.metrics['buffered'] += 1
            self.buffer.store(input_data, reason="timing_or_framing")
            return {
                'status': 'buffered',
                'message': 'Stored for later processing',
                'buffer_size': len(self.buffer.buffer)
            }
        
        elif classification == InputClassification.NOISE:
            self.metrics['noise_filtered'] += 1
            return {
                'status': 'filtered',
                'message': 'Classified as noise, discarded'
            }
        
        elif classification == InputClassification.THREAT:
            self.metrics['threats_escalated'] += 1
            return self._escalate_threat(input_data)
        
        return {'status': 'error', 'message': 'Unknown classification'}
    
    def process_buffer(self, capacity: int = 5) -> List[Dict[str, Any]]:
        """
        Process buffered items when resources are available.
        
        Args:
            capacity: Number of items to process
            
        Returns:
            List of processing results
        """
        items = self.buffer.retrieve_when_ready(capacity, self.context)
        results = []
        
        for item in items:
            result = self.executor.process(item.data)
            result['from_buffer'] = True
            result['buffer_reason'] = item.reason
            result['buffer_duration'] = time.time() - item.buffered_at
            results.append(result)
        
        return results
    
    def update_context(self, **kwargs) -> None:
        """Update system context"""
        self.context.update(kwargs)
    
    def _escalate_threat(self, input_data: InputData) -> Dict[str, Any]:
        """Handle threat escalation"""
        return {
            'status': 'threat_escalated',
            'message': 'Input classified as threat, escalating',
            'input': input_data,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        buffer_stats = self.buffer.get_stats()
        
        return {
            **self.metrics,
            'buffer_stats': buffer_stats,
            'core_state': self.executor.state.value,
            'context': self.context,
            'humor_index': self._calculate_humor_index()
        }
    
    def _calculate_humor_index(self) -> float:
        """
        Calculate humor index - sign of integration.
        Higher is better (can laugh at the system).
        """
        # If buffer is manageable and core is intact, humor index is high
        buffer_util = len(self.buffer.buffer) / self.buffer.max_buffer_size
        
        if self.executor.state == CoreState.INTACT:
            if buffer_util < 0.5:
                return 1.0  # Everything's good, can laugh
            elif buffer_util < 0.8:
                return 0.7  # Getting busy but still okay
            else:
                return 0.4  # Buffer filling up, less funny
        elif self.executor.state == CoreState.RECOVERING:
            return 0.3  # In recovery, not that funny
        else:
            return 0.1  # Compromised, heavy not funny
    
    def idle(self) -> None:
        """Let the system idle - recovery happens naturally"""
        self.context['state'] = 'idle'
        
        # Attempt recovery if needed
        if self.executor.state == CoreState.RECOVERING:
            self.executor.recover()
    
    def spin_up(self) -> None:
        """Spin system back up - cleaner, not louder"""
        self.context['state'] = 'active'
        
        # Process some buffered items
        if len(self.buffer.buffer) > 0:
            self.process_buffer(capacity=3)


if __name__ == "__main__":
    # Example usage
    print("🧠 Mental Load-Shedding Scheduler")
    print("=" * 50)
    
    # Create scheduler
    scheduler = LoadSheddingScheduler()
    
    # Update context
    scheduler.update_context(
        focus_level=5,
        loaded_modules=['python', 'docker', 'kubernetes'],
        available_resources=['cpu', 'memory', 'network']
    )
    
    # Process some inputs
    inputs = [
        InputData(content="Deploy new feature", source="github", priority=8),
        InputData(content="CRITICAL: Security breach", source="security", priority=10),
        InputData(content="Spam message", source="unknown", priority=1),
        InputData(content="Review PR #123", source="github", priority=5),
        InputData(content="Update docs", source="docs", priority=3),
    ]
    
    print("\n📥 Processing inputs...")
    for inp in inputs:
        result = scheduler.process_input(inp)
        print(f"  • {inp.content[:30]:30} → {result['status']}")
    
    # Get metrics
    print("\n📊 Metrics:")
    metrics = scheduler.get_metrics()
    print(f"  Total inputs: {metrics['total_inputs']}")
    print(f"  Immediate: {metrics['immediate_processed']}")
    print(f"  Buffered: {metrics['buffered']}")
    print(f"  Noise filtered: {metrics['noise_filtered']}")
    print(f"  Threats: {metrics['threats_escalated']}")
    print(f"  Buffer size: {metrics['buffer_stats']['current_size']}")
    print(f"  Humor index: {metrics['humor_index']:.2f}")
    
    # Process buffer
    print("\n🔄 Processing buffer...")
    scheduler.update_context(focus_level=2)  # Lower focus, more capacity
    buffered_results = scheduler.process_buffer(capacity=5)
    print(f"  Processed {len(buffered_results)} buffered items")
    
    # Idle state
    print("\n💤 Idling...")
    scheduler.idle()
    print("  System in idle state, ready for next cycle")
    
    print("\n✅ That's just the scheduler. 💜")
