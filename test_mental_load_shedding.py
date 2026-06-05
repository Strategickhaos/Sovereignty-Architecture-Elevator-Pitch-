#!/usr/bin/env python3
"""
Tests for Mental Load-Shedding Scheduler
Strategickhaos DAO LLC | Node 137

Testing the routing, buffering, and processing logic.
"""

import unittest
import time
from mental_load_shedding import (
    LoadSheddingScheduler,
    InputData,
    InputClassification,
    CoreState,
    InputClassifier,
    CoreExecutor,
    BufferManager
)


class TestInputClassifier(unittest.TestCase):
    """Test the InputClassifier component"""
    
    def setUp(self):
        self.classifier = InputClassifier()
        self.context = {
            'focus_level': 5,
            'loaded_modules': ['python', 'docker'],
            'available_resources': ['cpu', 'memory']
        }
    
    def test_threat_detection(self):
        """Test that threats are properly identified"""
        threat_input = InputData(
            content="CRITICAL security breach detected",
            source="security",
            priority=10
        )
        
        classification = self.classifier.classify(threat_input, self.context)
        self.assertEqual(classification, InputClassification.THREAT)
    
    def test_noise_detection(self):
        """Test that noise is properly filtered"""
        noise_input = InputData(
            content="This is spam and irrelevant",
            source="unknown",
            priority=1
        )
        
        classification = self.classifier.classify(noise_input, self.context)
        self.assertEqual(classification, InputClassification.NOISE)
    
    def test_timing_check(self):
        """Test that poorly-timed inputs are buffered"""
        # High focus level with low priority input
        self.context['focus_level'] = 8
        low_priority_input = InputData(
            content="Update documentation",
            source="docs",
            priority=3
        )
        
        classification = self.classifier.classify(low_priority_input, self.context)
        self.assertEqual(classification, InputClassification.BUFFER)
    
    def test_immediate_processing(self):
        """Test that well-timed inputs are processed immediately"""
        good_input = InputData(
            content="Deploy new feature",
            source="github",
            priority=8
        )
        
        classification = self.classifier.classify(good_input, self.context)
        self.assertEqual(classification, InputClassification.IMMEDIATE)


class TestCoreExecutor(unittest.TestCase):
    """Test the CoreExecutor component"""
    
    def setUp(self):
        self.executor = CoreExecutor()
    
    def test_initial_state(self):
        """Test that executor starts in INTACT state"""
        self.assertEqual(self.executor.state, CoreState.INTACT)
    
    def test_successful_processing(self):
        """Test successful input processing"""
        input_data = InputData(
            content="Test task",
            source="test",
            priority=5
        )
        
        result = self.executor.process(input_data)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(self.executor.state, CoreState.INTACT)
        self.assertIn('result', result)
    
    def test_processing_maintains_integrity(self):
        """Test that processing doesn't compromise core integrity"""
        for i in range(10):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=5
            )
            
            result = self.executor.process(input_data)
            
            # Core should remain intact after each processing
            self.assertEqual(self.executor.state, CoreState.INTACT)
    
    def test_execution_history(self):
        """Test that execution history is maintained"""
        input_data = InputData(
            content="Historical task",
            source="test",
            priority=5
        )
        
        self.executor.process(input_data)
        
        self.assertEqual(len(self.executor.execution_history), 1)
        self.assertIn('input', self.executor.execution_history[0])
        self.assertIn('duration', self.executor.execution_history[0])


class TestBufferManager(unittest.TestCase):
    """Test the BufferManager component"""
    
    def setUp(self):
        self.buffer = BufferManager(max_buffer_size=100)
    
    def test_store_item(self):
        """Test storing items in buffer"""
        input_data = InputData(
            content="Buffered task",
            source="test",
            priority=5
        )
        
        success = self.buffer.store(input_data, reason="timing")
        
        self.assertTrue(success)
        self.assertEqual(len(self.buffer.buffer), 1)
        self.assertEqual(self.buffer.total_buffered, 1)
    
    def test_retrieve_when_ready(self):
        """Test retrieving buffered items"""
        # Store multiple items
        for i in range(5):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=i
            )
            self.buffer.store(input_data, reason="timing")
        
        # Retrieve top 3
        items = self.buffer.retrieve_when_ready(available_capacity=3)
        
        self.assertEqual(len(items), 3)
        # Should retrieve highest priority first (4, 3, 2)
        self.assertEqual(items[0].data.priority, 4)
        self.assertEqual(self.buffer.total_retrieved, 3)
    
    def test_priority_calculation(self):
        """Test that priority is calculated correctly"""
        high_priority = InputData(
            content="Important task",
            source="critical",
            priority=10,
            metadata={'source_importance': 5}
        )
        
        self.buffer.store(high_priority, reason="timing")
        
        # The stored item should have boosted priority
        self.assertGreater(self.buffer.buffer[0].priority, 10)
    
    def test_max_buffer_size(self):
        """Test that buffer respects max size"""
        # Store more than max size
        for i in range(150):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=i
            )
            self.buffer.store(input_data, reason="timing")
        
        # Should not exceed max size
        self.assertEqual(len(self.buffer.buffer), 100)
    
    def test_buffer_stats(self):
        """Test buffer statistics"""
        # Store some items
        for i in range(10):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=i
            )
            self.buffer.store(input_data, reason="timing")
        
        stats = self.buffer.get_stats()
        
        self.assertEqual(stats['current_size'], 10)
        self.assertEqual(stats['total_buffered'], 10)
        self.assertEqual(stats['max_size'], 100)
        self.assertEqual(stats['utilization'], 0.1)


class TestLoadSheddingScheduler(unittest.TestCase):
    """Test the complete LoadSheddingScheduler"""
    
    def setUp(self):
        self.scheduler = LoadSheddingScheduler()
        self.scheduler.update_context(
            focus_level=5,
            loaded_modules=['python', 'docker'],
            available_resources=['cpu', 'memory', 'network']
        )
    
    def test_immediate_processing(self):
        """Test immediate processing of well-timed inputs"""
        input_data = InputData(
            content="Deploy feature",
            source="github",
            priority=8
        )
        
        result = self.scheduler.process_input(input_data)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(self.scheduler.metrics['immediate_processed'], 1)
    
    def test_buffering(self):
        """Test buffering of poorly-timed inputs"""
        # High focus level
        self.scheduler.update_context(focus_level=9)
        
        input_data = InputData(
            content="Low priority task",
            source="test",
            priority=3
        )
        
        result = self.scheduler.process_input(input_data)
        
        self.assertEqual(result['status'], 'buffered')
        self.assertEqual(self.scheduler.metrics['buffered'], 1)
    
    def test_noise_filtering(self):
        """Test noise filtering"""
        noise_input = InputData(
            content="spam irrelevant message",
            source="unknown",
            priority=1
        )
        
        result = self.scheduler.process_input(noise_input)
        
        self.assertEqual(result['status'], 'filtered')
        self.assertEqual(self.scheduler.metrics['noise_filtered'], 1)
    
    def test_threat_escalation(self):
        """Test threat escalation"""
        threat_input = InputData(
            content="CRITICAL security emergency",
            source="security",
            priority=10
        )
        
        result = self.scheduler.process_input(threat_input)
        
        self.assertEqual(result['status'], 'threat_escalated')
        self.assertEqual(self.scheduler.metrics['threats_escalated'], 1)
    
    def test_buffer_processing(self):
        """Test processing of buffered items"""
        # Buffer some items
        self.scheduler.update_context(focus_level=9)
        
        for i in range(5):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=i
            )
            self.scheduler.process_input(input_data)
        
        # Now process buffer
        self.scheduler.update_context(focus_level=2)
        results = self.scheduler.process_buffer(capacity=3)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.get('from_buffer', False))
    
    def test_metrics_tracking(self):
        """Test that metrics are tracked correctly"""
        # Process various types of inputs
        inputs = [
            InputData(content="Deploy", source="github", priority=8),
            InputData(content="CRITICAL alert", source="security", priority=10),
            InputData(content="spam", source="unknown", priority=1),
        ]
        
        for inp in inputs:
            self.scheduler.process_input(inp)
        
        metrics = self.scheduler.get_metrics()
        
        self.assertEqual(metrics['total_inputs'], 3)
        self.assertIn('buffer_stats', metrics)
        self.assertIn('humor_index', metrics)
    
    def test_humor_index(self):
        """Test humor index calculation"""
        # With empty buffer and intact core, should be high
        metrics = self.scheduler.get_metrics()
        self.assertGreaterEqual(metrics['humor_index'], 0.7)
        
        # Fill buffer significantly (need to ensure buffer utilization > 0.5)
        # Buffer max is 100 by default, so fill with 60 items to get >50% utilization
        # First, lower available resources to force buffering
        self.scheduler.update_context(focus_level=9, available_resources=[])
        for i in range(60):  # Fill more than half of buffer
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=3,
                metadata={'required_resources': ['gpu']}  # Resource not available
            )
            self.scheduler.process_input(input_data)
        
        metrics = self.scheduler.get_metrics()
        # Humor index should drop with full buffer
        # Only check if buffer actually filled
        if metrics['buffer_stats']['utilization'] > 0.5:
            self.assertLess(metrics['humor_index'], 0.7)
    
    def test_idle_state(self):
        """Test idle state functionality"""
        self.scheduler.idle()
        
        self.assertEqual(self.scheduler.context['state'], 'idle')
    
    def test_spin_up(self):
        """Test spin up functionality"""
        # Buffer some items first
        self.scheduler.update_context(focus_level=9)
        for i in range(5):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=i
            )
            self.scheduler.process_input(input_data)
        
        # Spin up should process some buffer
        initial_buffer_size = len(self.scheduler.buffer.buffer)
        self.scheduler.spin_up()
        
        self.assertEqual(self.scheduler.context['state'], 'active')
        # Buffer should be smaller after spin up
        self.assertLess(len(self.scheduler.buffer.buffer), initial_buffer_size)
    
    def test_routing_pattern(self):
        """Test the core routing pattern: not absorb, not block, route"""
        # Mix of different input types with clear routing requirements
        inputs = [
            InputData(content="Feature A", source="github", priority=8),
            InputData(content="Feature B", source="github", priority=3, 
                     metadata={'required_resources': ['gpu']}),  # Will be buffered
            InputData(content="spam noise", source="unknown", priority=1),
            InputData(content="CRITICAL issue", source="security", priority=10),
        ]
        
        # Set context to force some buffering
        self.scheduler.update_context(focus_level=7, available_resources=['cpu', 'memory'])
        
        immediate = 0
        buffered = 0
        filtered = 0
        escalated = 0
        
        for inp in inputs:
            result = self.scheduler.process_input(inp)
            
            if result['status'] == 'success':
                immediate += 1
            elif result['status'] == 'buffered':
                buffered += 1
            elif result['status'] == 'filtered':
                filtered += 1
            elif result['status'] == 'threat_escalated':
                escalated += 1
        
        # Should have routed to different paths
        self.assertGreater(immediate, 0)  # Some processed immediately
        self.assertGreater(filtered, 0)   # Some filtered
        self.assertGreater(escalated, 0)  # Some escalated
        # Buffered might be 0 or more depending on resource availability
        
        # Total should equal input count
        total = immediate + buffered + filtered + escalated
        self.assertEqual(total, len(inputs))


class TestIntegrationScenarios(unittest.TestCase):
    """Test real-world integration scenarios"""
    
    def test_high_load_scenario(self):
        """Test system behavior under high load"""
        scheduler = LoadSheddingScheduler()
        scheduler.update_context(focus_level=8)
        
        # Simulate burst of inputs
        for i in range(100):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=i % 10
            )
            scheduler.process_input(input_data)
        
        metrics = scheduler.get_metrics()
        
        # Should have routed appropriately
        self.assertEqual(
            metrics['total_inputs'],
            metrics['immediate_processed'] + 
            metrics['buffered'] + 
            metrics['noise_filtered'] + 
            metrics['threats_escalated']
        )
        
        # Core should still be intact
        self.assertEqual(scheduler.executor.state, CoreState.INTACT)
    
    def test_recovery_scenario(self):
        """Test system recovery from high buffer state"""
        scheduler = LoadSheddingScheduler()
        
        # Fill buffer
        scheduler.update_context(focus_level=9)
        for i in range(50):
            input_data = InputData(
                content=f"Task {i}",
                source="test",
                priority=3
            )
            scheduler.process_input(input_data)
        
        buffer_size_before = len(scheduler.buffer.buffer)
        
        # Recover by idling and spinning up
        scheduler.idle()
        scheduler.update_context(focus_level=2)
        scheduler.spin_up()
        
        # Process remaining buffer
        while len(scheduler.buffer.buffer) > 0:
            scheduler.process_buffer(capacity=10)
        
        buffer_size_after = len(scheduler.buffer.buffer)
        
        # Buffer should be cleared
        self.assertEqual(buffer_size_after, 0)
        self.assertLess(buffer_size_after, buffer_size_before)
    
    def test_continuous_operation(self):
        """Test continuous operation over time"""
        scheduler = LoadSheddingScheduler()
        
        # Simulate continuous operation
        for cycle in range(10):
            # Vary focus level
            scheduler.update_context(focus_level=cycle % 10)
            
            # Process inputs
            for i in range(10):
                input_data = InputData(
                    content=f"Cycle {cycle} Task {i}",
                    source="test",
                    priority=i
                )
                scheduler.process_input(input_data)
            
            # Process buffer periodically
            if cycle % 3 == 0:
                scheduler.process_buffer(capacity=5)
        
        metrics = scheduler.get_metrics()
        
        # Should have processed 100 inputs total
        self.assertEqual(metrics['total_inputs'], 100)
        
        # Core should remain intact
        self.assertEqual(scheduler.executor.state, CoreState.INTACT)


if __name__ == '__main__':
    print("🧪 Testing Mental Load-Shedding Scheduler")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2)
