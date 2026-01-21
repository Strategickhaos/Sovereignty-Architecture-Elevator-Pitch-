#!/usr/bin/env python3
"""
SAGCO Kernel Test Suite
Comprehensive unit tests for the SAGCO operating system
"""

import unittest
import asyncio
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'core'))

from sagco import (
    SAGCOKernel,
    CognitiveLayer,
    DopamineLevel,
    TaskPriority
)


class TestSAGCOKernel(unittest.TestCase):
    """Test suite for SAGCO kernel initialization"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.kernel = SAGCOKernel()
    
    def test_kernel_initialization(self):
        """Test kernel initializes correctly"""
        self.assertIsNotNone(self.kernel)
        self.assertEqual(self.kernel.version, "0.1.0")
        self.assertEqual(self.kernel.dopamine_level, DopamineLevel.BASELINE)
        self.assertEqual(self.kernel.active_layer, CognitiveLayer.TACTICAL)
    
    def test_config_loading(self):
        """Test configuration loading"""
        self.assertIsNotNone(self.kernel.config)
        self.assertIn('layers', self.kernel.config)
        self.assertIn('dopamine', self.kernel.config)
        self.assertIn('academic', self.kernel.config)
    
    def test_initial_state(self):
        """Test initial state is correct"""
        self.assertEqual(len(self.kernel.tasks), 0)
        self.assertEqual(self.kernel.optimization_cycles, 0)
        self.assertEqual(self.kernel.academic_metrics['assignments_completed'], 0)


class TestTaskManagement(unittest.TestCase):
    """Test suite for task management"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.kernel = SAGCOKernel()
    
    def test_add_task(self):
        """Test adding a task"""
        task = self.kernel.add_task(
            "Test Task",
            priority=TaskPriority.HIGH,
            effort=3
        )
        
        self.assertIsNotNone(task)
        self.assertEqual(task['title'], "Test Task")
        self.assertEqual(task['priority'], TaskPriority.HIGH)
        self.assertEqual(task['effort'], 3)
        self.assertEqual(len(self.kernel.tasks), 1)
    
    def test_complete_task(self):
        """Test completing a task"""
        task = self.kernel.add_task("Test Task")
        task_id = task['id']
        
        result = self.kernel.complete_task(task_id)
        self.assertTrue(result)
        self.assertEqual(task['status'], 'completed')
        self.assertIn('completed_at', task)
    
    def test_complete_nonexistent_task(self):
        """Test completing a task that doesn't exist"""
        result = self.kernel.complete_task(999)
        self.assertFalse(result)
    
    def test_task_prioritization(self):
        """Test tasks are prioritized correctly"""
        self.kernel.add_task("Low Priority", priority=TaskPriority.LOW)
        self.kernel.add_task("High Priority", priority=TaskPriority.HIGH)
        self.kernel.add_task("Critical Priority", priority=TaskPriority.CRITICAL)
        
        asyncio.run(self.kernel._optimize_tasks())
        
        # After optimization, highest priority should be first
        self.assertEqual(
            self.kernel.tasks[0]['priority'],
            TaskPriority.CRITICAL
        )


class TestAcademicTracking(unittest.TestCase):
    """Test suite for academic performance tracking"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.kernel = SAGCOKernel()
    
    def test_log_study_session(self):
        """Test logging study sessions"""
        initial_hours = self.kernel.academic_metrics['study_hours']
        self.kernel.log_study_session(2.5, "Mathematics")
        
        self.assertEqual(
            self.kernel.academic_metrics['study_hours'],
            initial_hours + 2.5
        )
    
    def test_record_quiz_score(self):
        """Test recording quiz scores"""
        self.kernel.record_quiz_score(95.0)
        self.kernel.record_quiz_score(88.0)
        
        self.assertEqual(len(self.kernel.academic_metrics['quiz_scores']), 2)
        self.assertIn(95.0, self.kernel.academic_metrics['quiz_scores'])
        self.assertIn(88.0, self.kernel.academic_metrics['quiz_scores'])
    
    def test_gpa_calculation(self):
        """Test GPA calculation"""
        self.kernel.record_quiz_score(100.0)
        self.kernel.record_quiz_score(90.0)
        
        asyncio.run(self.kernel._update_academic_metrics())
        
        # Average of 100 and 90 is 95, which should give 3.8 GPA
        expected_gpa = (95.0 / 100) * 4.0
        self.assertAlmostEqual(
            self.kernel.academic_metrics['current_gpa'],
            expected_gpa,
            places=2
        )
    
    def test_record_discussion_post(self):
        """Test recording discussion posts"""
        initial_count = self.kernel.academic_metrics['discussion_posts']
        self.kernel.record_discussion_post()
        
        self.assertEqual(
            self.kernel.academic_metrics['discussion_posts'],
            initial_count + 1
        )
    
    def test_complete_academic_task(self):
        """Test completing an academic task updates metrics"""
        task = self.kernel.add_task(
            "Complete Assignment",
            metadata={'type': 'academic'}
        )
        
        initial_count = self.kernel.academic_metrics['assignments_completed']
        self.kernel.complete_task(task['id'])
        
        self.assertEqual(
            self.kernel.academic_metrics['assignments_completed'],
            initial_count + 1
        )


class TestCognitiveLayers(unittest.TestCase):
    """Test suite for cognitive layer management"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.kernel = SAGCOKernel()
    
    def test_switch_layer(self):
        """Test switching cognitive layers"""
        self.kernel.switch_layer(CognitiveLayer.STRATEGIC)
        self.assertEqual(self.kernel.active_layer, CognitiveLayer.STRATEGIC)
        
        self.kernel.switch_layer(CognitiveLayer.REFLEXIVE)
        self.assertEqual(self.kernel.active_layer, CognitiveLayer.REFLEXIVE)
    
    def test_all_layers_exist(self):
        """Test all cognitive layers are defined"""
        layers = [layer.value for layer in CognitiveLayer]
        self.assertIn('reflexive', layers)
        self.assertIn('tactical', layers)
        self.assertIn('strategic', layers)
        self.assertIn('sovereign', layers)


class TestDopamineSystem(unittest.TestCase):
    """Test suite for dopamine-driven motivation system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.kernel = SAGCOKernel()
    
    def test_initial_dopamine_level(self):
        """Test initial dopamine level"""
        self.assertEqual(self.kernel.dopamine_level, DopamineLevel.BASELINE)
    
    def test_dopamine_depletion(self):
        """Test dopamine depletion with many tasks"""
        # Add many tasks to trigger depletion
        for i in range(15):
            self.kernel.add_task(f"Task {i}")
        
        asyncio.run(self.kernel._update_dopamine())
        self.assertEqual(self.kernel.dopamine_level, DopamineLevel.DEPLETED)
    
    def test_dopamine_levels_exist(self):
        """Test all dopamine levels are defined"""
        levels = [level.value for level in DopamineLevel]
        self.assertIn('depleted', levels)
        self.assertIn('baseline', levels)
        self.assertIn('elevated', levels)
        self.assertIn('flow', levels)


class TestSystemStatus(unittest.TestCase):
    """Test suite for system status and monitoring"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.kernel = SAGCOKernel()
    
    def test_get_status(self):
        """Test getting system status"""
        status = self.kernel.get_status()
        
        self.assertIsNotNone(status)
        self.assertIn('version', status)
        self.assertIn('uptime_seconds', status)
        self.assertIn('active_layer', status)
        self.assertIn('dopamine_level', status)
        self.assertIn('tasks', status)
        self.assertIn('academic_metrics', status)
    
    def test_status_task_counts(self):
        """Test status includes correct task counts"""
        self.kernel.add_task("Task 1")
        self.kernel.add_task("Task 2")
        task = self.kernel.add_task("Task 3")
        self.kernel.complete_task(task['id'])
        
        status = self.kernel.get_status()
        
        self.assertEqual(status['tasks']['total'], 3)
        self.assertEqual(status['tasks']['pending'], 2)
        self.assertEqual(status['tasks']['completed'], 1)
    
    def test_uptime_tracking(self):
        """Test uptime is tracked correctly"""
        import time
        time.sleep(0.1)
        
        status = self.kernel.get_status()
        self.assertGreater(status['uptime_seconds'], 0)


class TestTaskPriorities(unittest.TestCase):
    """Test suite for task priority system"""
    
    def test_all_priorities_exist(self):
        """Test all priority levels are defined"""
        priorities = [p.name for p in TaskPriority]
        self.assertIn('CRITICAL', priorities)
        self.assertIn('HIGH', priorities)
        self.assertIn('MEDIUM', priorities)
        self.assertIn('LOW', priorities)
        self.assertIn('BACKGROUND', priorities)
    
    def test_priority_values(self):
        """Test priority values are ordered correctly"""
        self.assertGreater(TaskPriority.CRITICAL.value, TaskPriority.HIGH.value)
        self.assertGreater(TaskPriority.HIGH.value, TaskPriority.MEDIUM.value)
        self.assertGreater(TaskPriority.MEDIUM.value, TaskPriority.LOW.value)
        self.assertGreater(TaskPriority.LOW.value, TaskPriority.BACKGROUND.value)


class TestConfigManagement(unittest.TestCase):
    """Test suite for configuration management"""
    
    def test_default_config(self):
        """Test default configuration is loaded"""
        kernel = SAGCOKernel()
        
        self.assertIn('layers', kernel.config)
        self.assertIn('dopamine', kernel.config)
        self.assertIn('academic', kernel.config)
    
    def test_layer_config(self):
        """Test layer configuration"""
        kernel = SAGCOKernel()
        
        self.assertIn('reflexive', kernel.config['layers'])
        self.assertIn('tactical', kernel.config['layers'])
        self.assertIn('strategic', kernel.config['layers'])
        self.assertIn('sovereign', kernel.config['layers'])
    
    def test_dopamine_config(self):
        """Test dopamine configuration"""
        kernel = SAGCOKernel()
        
        self.assertIn('baseline_threshold', kernel.config['dopamine'])
        self.assertIn('flow_threshold', kernel.config['dopamine'])
        self.assertIn('recovery_rate', kernel.config['dopamine'])
    
    def test_academic_config(self):
        """Test academic configuration"""
        kernel = SAGCOKernel()
        
        self.assertIn('target_gpa', kernel.config['academic'])
        self.assertIn('min_study_hours_per_day', kernel.config['academic'])
        self.assertIn('max_concurrent_tasks', kernel.config['academic'])


if __name__ == '__main__':
    unittest.main()
