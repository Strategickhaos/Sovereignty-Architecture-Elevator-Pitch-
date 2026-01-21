"""
Unit tests for SAGCO Kernel

Test suite covers all major components of the SAGCO system including:
- Kernel initialization and lifecycle
- Node registration and management
- Task submission and processing
- Dopamine reward system
- Academic context integration
- Event handling
- Health monitoring
"""

import pytest
import asyncio
from datetime import datetime
from src.core.sagco import (
    SAGCOKernel,
    ProcessingNode,
    Task,
    AcademicContext,
    DopamineEngine,
    LayerType,
    DopamineLevel,
    create_sagco_kernel
)


@pytest.fixture
def kernel():
    """Create a fresh SAGCO kernel for each test"""
    return SAGCOKernel()


@pytest.fixture
def populated_kernel():
    """Create a kernel with nodes already registered"""
    kernel = SAGCOKernel()
    for layer in LayerType:
        for i in range(2):
            node = ProcessingNode(
                node_id=f"{layer.value}-node-{i}",
                layer=layer,
                capacity=10
            )
            kernel.register_node(node)
    return kernel


@pytest.fixture
def dopamine_engine():
    """Create a fresh dopamine engine"""
    return DopamineEngine()


@pytest.fixture
def sample_task():
    """Create a sample task for testing"""
    return Task(
        task_id="test-task-1",
        task_type="cognitive_processing",
        payload={"data": "test data"},
        priority=1
    )


@pytest.fixture
def academic_context():
    """Create a sample academic context"""
    return AcademicContext(
        course_code="CYBER-PSY-620",
        module="Cognitive Architecture",
        learning_objectives=[
            "Understand distributed systems",
            "Implement reward-based learning"
        ]
    )


# ===== Kernel Tests =====

def test_kernel_initialization(kernel):
    """Test that kernel initializes correctly"""
    assert kernel is not None
    assert kernel.running is False
    assert len(kernel.nodes) == 0
    assert len(kernel.tasks) == 0
    assert kernel.dopamine_engine is not None


def test_kernel_config_initialization():
    """Test kernel initialization with config"""
    config = {
        "max_nodes": 100,
        "dopamine_learning_rate": 0.2
    }
    kernel = SAGCOKernel(config)
    assert kernel.config == config


# ===== Node Management Tests =====

def test_node_registration(kernel):
    """Test registering a processing node"""
    node = ProcessingNode(
        node_id="test-node-1",
        layer=LayerType.COGNITIVE,
        capacity=10
    )
    kernel.register_node(node)
    
    assert "test-node-1" in kernel.nodes
    assert kernel.nodes["test-node-1"].layer == LayerType.COGNITIVE


def test_node_unregistration(kernel):
    """Test unregistering a processing node"""
    node = ProcessingNode(
        node_id="test-node-1",
        layer=LayerType.COGNITIVE
    )
    kernel.register_node(node)
    assert "test-node-1" in kernel.nodes
    
    kernel.unregister_node("test-node-1")
    assert "test-node-1" not in kernel.nodes


def test_node_availability():
    """Test node availability checks"""
    node = ProcessingNode(
        node_id="test-node",
        layer=LayerType.SENSORY,
        capacity=10,
        current_load=5
    )
    assert node.is_available() is True
    
    node.current_load = 10
    assert node.is_available() is False
    
    node.current_load = 5
    node.health_score = 0.3
    assert node.is_available() is False


def test_node_utilization():
    """Test node utilization calculation"""
    node = ProcessingNode(
        node_id="test-node",
        layer=LayerType.COGNITIVE,
        capacity=100,
        current_load=50
    )
    assert node.get_utilization() == 50.0
    
    node.current_load = 0
    assert node.get_utilization() == 0.0
    
    node.current_load = 100
    assert node.get_utilization() == 100.0


# ===== Task Management Tests =====

def test_task_creation(sample_task):
    """Test task creation and properties"""
    assert sample_task.task_id == "test-task-1"
    assert sample_task.status == "pending"
    assert sample_task.priority == 1
    assert sample_task.result is None


def test_task_hash_calculation(sample_task):
    """Test task hash calculation"""
    hash1 = sample_task.calculate_hash()
    assert hash1 is not None
    assert len(hash1) == 64  # SHA256 hash length
    
    # Same task should produce same hash
    hash2 = sample_task.calculate_hash()
    assert hash1 == hash2


def test_task_submission(kernel, sample_task):
    """Test submitting a task to the kernel"""
    task_id = kernel.submit_task(sample_task)
    
    assert task_id == sample_task.task_id
    assert task_id in kernel.tasks
    assert sample_task in kernel.task_queue


def test_task_priority_sorting(kernel):
    """Test that tasks are sorted by priority"""
    low_priority = Task(
        task_id="low",
        task_type="test",
        payload={},
        priority=1
    )
    high_priority = Task(
        task_id="high",
        task_type="test",
        payload={},
        priority=10
    )
    
    kernel.submit_task(low_priority)
    kernel.submit_task(high_priority)
    
    assert kernel.task_queue[0].task_id == "high"
    assert kernel.task_queue[1].task_id == "low"


# ===== Dopamine Engine Tests =====

def test_dopamine_engine_initialization(dopamine_engine):
    """Test dopamine engine initialization"""
    assert dopamine_engine.baseline_reward == 0.0
    assert dopamine_engine.learning_rate == 0.1
    assert len(dopamine_engine.reward_history) == 0


def test_reward_calculation_success(dopamine_engine, sample_task):
    """Test reward calculation for successful task"""
    reward = dopamine_engine.calculate_reward(
        sample_task,
        execution_time=0.5,
        success=True,
        quality_score=0.9
    )
    
    assert reward > 0
    assert sample_task.task_type in dopamine_engine.reward_history


def test_reward_calculation_failure(dopamine_engine, sample_task):
    """Test reward calculation for failed task"""
    reward = dopamine_engine.calculate_reward(
        sample_task,
        execution_time=1.0,
        success=False,
        quality_score=0.0
    )
    
    assert reward < 0


def test_dopamine_level_conversion(dopamine_engine):
    """Test conversion of reward to dopamine level"""
    assert dopamine_engine.get_dopamine_level(3.0) == DopamineLevel.CRITICAL_HIGH
    assert dopamine_engine.get_dopamine_level(1.0) == DopamineLevel.HIGH
    assert dopamine_engine.get_dopamine_level(0.0) == DopamineLevel.NEUTRAL
    assert dopamine_engine.get_dopamine_level(-1.0) == DopamineLevel.LOW
    assert dopamine_engine.get_dopamine_level(-3.0) == DopamineLevel.CRITICAL_LOW


def test_priority_adjustment(dopamine_engine, sample_task):
    """Test task priority adjustment based on history"""
    # Build up history
    for i in range(5):
        dopamine_engine.calculate_reward(
            sample_task,
            execution_time=0.5,
            success=True,
            quality_score=0.9
        )
    
    adjustment = dopamine_engine.get_task_priority_adjustment("cognitive_processing")
    assert adjustment >= 0  # Should be positive given successful history


# ===== Academic Context Tests =====

def test_academic_context_creation(academic_context):
    """Test academic context creation"""
    assert academic_context.course_code == "CYBER-PSY-620"
    assert academic_context.module == "Cognitive Architecture"
    assert len(academic_context.learning_objectives) == 2


def test_academic_context_registration(kernel, academic_context):
    """Test registering academic context with kernel"""
    kernel.add_academic_context("cyber-psy-620", academic_context)
    
    assert "cyber-psy-620" in kernel.academic_contexts
    assert kernel.academic_contexts["cyber-psy-620"] == academic_context


def test_learning_alignment_validation(academic_context):
    """Test validation of task alignment with learning objectives"""
    aligned_task = Task(
        task_id="aligned",
        task_type="learning",
        payload={"topic": "distributed systems architecture"}
    )
    
    assert academic_context.validate_learning_alignment(aligned_task) is True
    
    unaligned_task = Task(
        task_id="unaligned",
        task_type="other",
        payload={"topic": "quantum mechanics"}
    )
    
    assert academic_context.validate_learning_alignment(unaligned_task) is False


# ===== Async Processing Tests =====

@pytest.mark.asyncio
async def test_kernel_start_stop(kernel):
    """Test starting and stopping the kernel"""
    assert kernel.running is False
    
    await kernel.start()
    assert kernel.running is True
    
    await kernel.stop()
    assert kernel.running is False


@pytest.mark.asyncio
async def test_task_execution(populated_kernel, sample_task):
    """Test executing a task on the kernel"""
    await populated_kernel.start()
    
    task_id = populated_kernel.submit_task(sample_task)
    
    # Wait for processing
    await asyncio.sleep(0.5)
    
    task = populated_kernel.tasks[task_id]
    assert task.status in ["completed", "running"]
    
    await populated_kernel.stop()


@pytest.mark.asyncio
async def test_multiple_task_execution(populated_kernel):
    """Test executing multiple tasks"""
    await populated_kernel.start()
    
    tasks = []
    for i in range(5):
        task = Task(
            task_id=f"task-{i}",
            task_type="test",
            payload={"index": i},
            priority=i
        )
        populated_kernel.submit_task(task)
        tasks.append(task)
    
    # Wait for processing
    await asyncio.sleep(1.0)
    
    # Check that some tasks completed
    completed_count = sum(
        1 for t in tasks if t.status == "completed"
    )
    assert completed_count > 0
    
    await populated_kernel.stop()


# ===== Event Handling Tests =====

@pytest.mark.asyncio
async def test_event_registration(kernel):
    """Test registering event handlers"""
    events_received = []
    
    def handler(data):
        events_received.append(data)
    
    kernel.on("task_completed", handler)
    assert len(kernel.event_handlers["task_completed"]) == 1


@pytest.mark.asyncio
async def test_event_emission(populated_kernel):
    """Test event emission"""
    events_received = []
    
    async def async_handler(data):
        events_received.append(data)
    
    populated_kernel.on("task_completed", async_handler)
    
    await populated_kernel.start()
    
    task = Task(
        task_id="event-test",
        task_type="test",
        payload={}
    )
    populated_kernel.submit_task(task)
    
    # Wait for processing and event
    await asyncio.sleep(0.5)
    
    assert len(events_received) > 0
    
    await populated_kernel.stop()


# ===== Statistics Tests =====

def test_get_statistics_empty(kernel):
    """Test getting statistics from empty kernel"""
    stats = kernel.get_statistics()
    
    assert stats["total_nodes"] == 0
    assert stats["total_tasks"] == 0
    assert stats["queue_length"] == 0


def test_get_statistics_populated(populated_kernel):
    """Test getting statistics from populated kernel"""
    # Add some tasks
    for i in range(3):
        task = Task(
            task_id=f"task-{i}",
            task_type="test",
            payload={}
        )
        populated_kernel.submit_task(task)
    
    stats = populated_kernel.get_statistics()
    
    assert stats["total_nodes"] == 8  # 2 nodes per layer, 4 layers
    assert stats["total_tasks"] == 3
    assert stats["pending_tasks"] == 3
    assert stats["queue_length"] == 3


def test_nodes_by_layer_stats(populated_kernel):
    """Test node distribution by layer in statistics"""
    stats = populated_kernel.get_statistics()
    
    for layer in LayerType:
        assert stats["nodes_by_layer"][layer.value] == 2


# ===== Health Monitoring Tests =====

def test_health_status_healthy(populated_kernel):
    """Test health status for healthy kernel"""
    health = populated_kernel.get_health_status()
    
    assert health["status"] == "healthy"
    assert len(health["unhealthy_nodes"]) == 0
    assert health["kernel_running"] is False


def test_health_status_unhealthy():
    """Test health status with unhealthy nodes"""
    kernel = SAGCOKernel()
    
    unhealthy_node = ProcessingNode(
        node_id="unhealthy",
        layer=LayerType.COGNITIVE,
        health_score=0.3
    )
    kernel.register_node(unhealthy_node)
    
    health = kernel.get_health_status()
    
    assert "unhealthy" in health["unhealthy_nodes"]


# ===== Factory Function Tests =====

def test_create_sagco_kernel():
    """Test factory function for kernel creation"""
    kernel = create_sagco_kernel()
    
    assert kernel is not None
    assert isinstance(kernel, SAGCOKernel)


def test_create_sagco_kernel_with_invalid_config():
    """Test factory function with invalid config path"""
    kernel = create_sagco_kernel("/nonexistent/config.yaml")
    
    # Should still create kernel even if config fails to load
    assert kernel is not None
    assert isinstance(kernel, SAGCOKernel)


# ===== Integration Tests =====

@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete workflow from kernel creation to task execution"""
    # Create kernel
    kernel = SAGCOKernel()
    
    # Register nodes
    for layer in LayerType:
        node = ProcessingNode(
            node_id=f"{layer.value}-node",
            layer=layer,
            capacity=10
        )
        kernel.register_node(node)
    
    # Add academic context
    context = AcademicContext(
        course_code="TEST-101",
        module="Integration Testing",
        learning_objectives=["Test end-to-end workflows"]
    )
    kernel.add_academic_context("test-101", context)
    
    # Start kernel
    await kernel.start()
    
    # Submit tasks
    task_ids = []
    for i in range(3):
        task = Task(
            task_id=f"integration-task-{i}",
            task_type="integration_test",
            payload={"test_data": i},
            priority=i
        )
        task_id = kernel.submit_task(task)
        task_ids.append(task_id)
    
    # Wait for processing
    await asyncio.sleep(1.0)
    
    # Verify tasks were processed
    for task_id in task_ids:
        task = kernel.tasks[task_id]
        assert task.status in ["completed", "running"]
    
    # Check statistics
    stats = kernel.get_statistics()
    assert stats["total_nodes"] == 4
    assert stats["total_tasks"] == 3
    
    # Check health
    health = kernel.get_health_status()
    assert health["kernel_running"] is True
    
    # Stop kernel
    await kernel.stop()
    assert kernel.running is False
