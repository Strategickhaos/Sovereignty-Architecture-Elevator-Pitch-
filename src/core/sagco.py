"""
SAGCO (Sovereignty Architecture Governance Cognitive OS) - The Kernel

A distributed cognitive operating system for sovereign architecture management,
featuring layered processing (dopamine rewards), academic integration, and 
multi-agent orchestration.

Version: 0.1.0
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import json
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LayerType(Enum):
    """SAGCO processing layers"""
    SENSORY = "sensory"  # Input reception layer
    COGNITIVE = "cognitive"  # Processing and reasoning layer
    EXECUTIVE = "executive"  # Decision making layer
    MOTOR = "motor"  # Action execution layer


class DopamineLevel(Enum):
    """Reward levels for dopamine-driven learning"""
    CRITICAL_LOW = -2
    LOW = -1
    NEUTRAL = 0
    HIGH = 1
    CRITICAL_HIGH = 2


@dataclass
class ProcessingNode:
    """A node in the SAGCO processing network"""
    node_id: str
    layer: LayerType
    capacity: int = 100
    current_load: int = 0
    health_score: float = 1.0
    last_heartbeat: datetime = field(default_factory=datetime.now)
    
    def is_available(self) -> bool:
        """Check if node can accept more work"""
        return self.current_load < self.capacity and self.health_score > 0.5
    
    def get_utilization(self) -> float:
        """Get current utilization percentage"""
        return (self.current_load / self.capacity) * 100 if self.capacity > 0 else 0


@dataclass
class Task:
    """A task to be processed by SAGCO"""
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    assigned_node: Optional[str] = None
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    dopamine_reward: float = 0.0
    
    def calculate_hash(self) -> str:
        """Calculate unique hash for task"""
        data = f"{self.task_id}{self.task_type}{json.dumps(self.payload, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class AcademicContext:
    """Academic integration context for research and learning"""
    course_code: str
    module: str
    learning_objectives: List[str]
    research_questions: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)
    
    def validate_learning_alignment(self, task: Task) -> bool:
        """Validate if task aligns with learning objectives"""
        # Simple keyword matching for demonstration
        task_str = json.dumps(task.payload).lower()
        return any(obj.lower() in task_str for obj in self.learning_objectives)


class DopamineEngine:
    """
    Dopamine-driven reward system for SAGCO
    Implements reinforcement learning principles for task optimization
    """
    
    def __init__(self):
        self.reward_history: Dict[str, List[float]] = defaultdict(list)
        self.baseline_reward = 0.0
        self.learning_rate = 0.1
        
    def calculate_reward(self, task: Task, execution_time: float, 
                        success: bool, quality_score: float = 1.0) -> float:
        """
        Calculate dopamine reward based on task performance
        
        Args:
            task: The completed task
            execution_time: Time taken to execute (seconds)
            success: Whether task succeeded
            quality_score: Quality of output (0-1)
        
        Returns:
            Dopamine reward value
        """
        base_reward = 1.0 if success else -1.0
        
        # Time efficiency factor (faster is better, up to a point)
        time_factor = max(0.1, 1.0 - (execution_time / 10.0))
        
        # Quality multiplier
        quality_factor = quality_score
        
        # Priority bonus
        priority_bonus = task.priority * 0.1
        
        reward = base_reward * time_factor * quality_factor + priority_bonus
        
        # Update history
        self.reward_history[task.task_type].append(reward)
        
        # Update baseline (moving average)
        self.baseline_reward = (
            self.baseline_reward * 0.9 + reward * 0.1
        )
        
        logger.info(f"Dopamine reward for {task.task_id}: {reward:.2f}")
        return reward
    
    def get_dopamine_level(self, reward: float) -> DopamineLevel:
        """Convert reward value to dopamine level"""
        if reward >= 2.0:
            return DopamineLevel.CRITICAL_HIGH
        elif reward >= 0.5:
            return DopamineLevel.HIGH
        elif reward >= -0.5:
            return DopamineLevel.NEUTRAL
        elif reward >= -2.0:
            return DopamineLevel.LOW
        else:
            return DopamineLevel.CRITICAL_LOW
    
    def get_task_priority_adjustment(self, task_type: str) -> float:
        """
        Adjust task priority based on historical rewards
        Tasks with higher average rewards get higher priority
        """
        if task_type not in self.reward_history:
            return 0.0
        
        avg_reward = sum(self.reward_history[task_type]) / len(self.reward_history[task_type])
        return avg_reward - self.baseline_reward


class SAGCOKernel:
    """
    The main SAGCO Kernel - orchestrates all cognitive operations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.nodes: Dict[str, ProcessingNode] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[Task] = []
        self.dopamine_engine = DopamineEngine()
        self.academic_contexts: Dict[str, AcademicContext] = {}
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.running = False
        
        logger.info("SAGCO Kernel initialized")
    
    def register_node(self, node: ProcessingNode) -> None:
        """Register a processing node with the kernel"""
        self.nodes[node.node_id] = node
        logger.info(f"Registered node {node.node_id} on layer {node.layer.value}")
    
    def unregister_node(self, node_id: str) -> None:
        """Unregister a processing node"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            logger.info(f"Unregistered node {node_id}")
    
    def add_academic_context(self, context_id: str, context: AcademicContext) -> None:
        """Add academic context for learning alignment"""
        self.academic_contexts[context_id] = context
        logger.info(f"Added academic context: {context.course_code} - {context.module}")
    
    def submit_task(self, task: Task) -> str:
        """Submit a task for processing"""
        self.tasks[task.task_id] = task
        self.task_queue.append(task)
        
        # Adjust priority based on dopamine history
        priority_adjustment = self.dopamine_engine.get_task_priority_adjustment(task.task_type)
        task.priority += int(priority_adjustment)
        
        # Sort queue by priority
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        
        logger.info(f"Submitted task {task.task_id} with priority {task.priority}")
        return task.task_id
    
    def _select_node_for_task(self, task: Task, layer: LayerType) -> Optional[ProcessingNode]:
        """Select the best available node for a task"""
        available_nodes = [
            node for node in self.nodes.values()
            if node.layer == layer and node.is_available()
        ]
        
        if not available_nodes:
            return None
        
        # Select node with lowest utilization
        return min(available_nodes, key=lambda n: n.get_utilization())
    
    async def _execute_task_on_node(self, task: Task, node: ProcessingNode) -> bool:
        """Execute a task on a specific node"""
        start_time = datetime.now()
        task.assigned_node = node.node_id
        task.status = "running"
        node.current_load += 1
        
        try:
            # Simulate task execution
            logger.info(f"Executing task {task.task_id} on node {node.node_id}")
            await asyncio.sleep(0.1)  # Simulate processing time
            
            # Simulate result
            task.result = {
                "status": "success",
                "node": node.node_id,
                "layer": node.layer.value,
                "output": f"Processed by {node.node_id}"
            }
            task.status = "completed"
            
            # Calculate dopamine reward
            execution_time = (datetime.now() - start_time).total_seconds()
            reward = self.dopamine_engine.calculate_reward(
                task, execution_time, True, quality_score=0.9
            )
            task.dopamine_reward = reward
            
            # Emit completion event
            await self._emit_event("task_completed", {
                "task_id": task.task_id,
                "node_id": node.node_id,
                "reward": reward,
                "dopamine_level": self.dopamine_engine.get_dopamine_level(reward).value
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Task {task.task_id} failed: {e}")
            task.status = "failed"
            task.result = {"status": "error", "error": str(e)}
            
            # Negative reward for failure
            execution_time = (datetime.now() - start_time).total_seconds()
            reward = self.dopamine_engine.calculate_reward(
                task, execution_time, False, quality_score=0.0
            )
            task.dopamine_reward = reward
            
            return False
            
        finally:
            node.current_load -= 1
    
    async def _process_layer(self, layer: LayerType) -> None:
        """Process all tasks in a specific layer"""
        tasks_to_process = [t for t in self.task_queue if t.status == "pending"]
        
        for task in tasks_to_process:
            node = self._select_node_for_task(task, layer)
            if node:
                await self._execute_task_on_node(task, node)
    
    async def _processing_loop(self) -> None:
        """Main processing loop - processes tasks through all layers"""
        while self.running:
            try:
                # Process through layers in order
                for layer in LayerType:
                    await self._process_layer(layer)
                
                # Clean up completed tasks from queue
                self.task_queue = [t for t in self.task_queue if t.status == "pending"]
                
                # Brief sleep to prevent tight loop
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                await asyncio.sleep(1)
    
    def on(self, event_name: str, handler: Callable) -> None:
        """Register an event handler"""
        self.event_handlers[event_name].append(handler)
    
    async def _emit_event(self, event_name: str, data: Dict[str, Any]) -> None:
        """Emit an event to all registered handlers"""
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event_name}: {e}")
    
    async def start(self) -> None:
        """Start the SAGCO kernel"""
        if self.running:
            logger.warning("Kernel is already running")
            return
        
        self.running = True
        logger.info("SAGCO Kernel starting...")
        
        # Start processing loop
        asyncio.create_task(self._processing_loop())
        
        logger.info("SAGCO Kernel started successfully")
    
    async def stop(self) -> None:
        """Stop the SAGCO kernel"""
        self.running = False
        logger.info("SAGCO Kernel stopping...")
        
        # Wait for pending tasks to complete (with timeout)
        timeout = 10
        start = datetime.now()
        while self.task_queue and (datetime.now() - start).seconds < timeout:
            await asyncio.sleep(0.1)
        
        logger.info("SAGCO Kernel stopped")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get kernel statistics"""
        total_tasks = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t.status == "completed")
        failed = sum(1 for t in self.tasks.values() if t.status == "failed")
        pending = sum(1 for t in self.tasks.values() if t.status == "pending")
        running = sum(1 for t in self.tasks.values() if t.status == "running")
        
        return {
            "total_nodes": len(self.nodes),
            "nodes_by_layer": {
                layer.value: len([n for n in self.nodes.values() if n.layer == layer])
                for layer in LayerType
            },
            "total_tasks": total_tasks,
            "completed_tasks": completed,
            "failed_tasks": failed,
            "pending_tasks": pending,
            "running_tasks": running,
            "average_reward": self.dopamine_engine.baseline_reward,
            "queue_length": len(self.task_queue)
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        unhealthy_nodes = [
            n.node_id for n in self.nodes.values() 
            if n.health_score < 0.5
        ]
        
        avg_utilization = sum(
            n.get_utilization() for n in self.nodes.values()
        ) / len(self.nodes) if self.nodes else 0
        
        return {
            "status": "healthy" if not unhealthy_nodes and avg_utilization < 80 else "degraded",
            "unhealthy_nodes": unhealthy_nodes,
            "average_utilization": avg_utilization,
            "kernel_running": self.running
        }


# Factory function for easy instantiation
def create_sagco_kernel(config_path: Optional[str] = None) -> SAGCOKernel:
    """
    Factory function to create and configure a SAGCO kernel
    
    Args:
        config_path: Optional path to configuration file
    
    Returns:
        Configured SAGCOKernel instance
    """
    config = {}
    if config_path:
        try:
            with open(config_path, 'r') as f:
                import yaml
                config = yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
    
    kernel = SAGCOKernel(config)
    
    # Register default nodes if specified in config
    if "nodes" in config:
        for node_config in config["nodes"]:
            node = ProcessingNode(
                node_id=node_config["id"],
                layer=LayerType(node_config["layer"]),
                capacity=node_config.get("capacity", 100)
            )
            kernel.register_node(node)
    
    return kernel


if __name__ == "__main__":
    # Example usage
    async def main():
        # Create kernel
        kernel = SAGCOKernel()
        
        # Register nodes
        for layer in LayerType:
            for i in range(2):
                node = ProcessingNode(
                    node_id=f"{layer.value}-node-{i}",
                    layer=layer,
                    capacity=10
                )
                kernel.register_node(node)
        
        # Add academic context
        context = AcademicContext(
            course_code="CYBER-PSY-620",
            module="Cognitive Architecture",
            learning_objectives=[
                "Understand distributed cognitive systems",
                "Implement reward-based learning",
                "Design layered processing architectures"
            ]
        )
        kernel.add_academic_context("cyber-psy-620", context)
        
        # Start kernel
        await kernel.start()
        
        # Submit some tasks
        for i in range(5):
            task = Task(
                task_id=f"task-{i}",
                task_type="cognitive_processing",
                payload={"data": f"test data {i}"},
                priority=i
            )
            kernel.submit_task(task)
        
        # Let it run for a bit
        await asyncio.sleep(2)
        
        # Get statistics
        stats = kernel.get_statistics()
        health = kernel.get_health_status()
        
        print("\n=== SAGCO Kernel Statistics ===")
        print(json.dumps(stats, indent=2))
        print("\n=== Health Status ===")
        print(json.dumps(health, indent=2))
        
        # Stop kernel
        await kernel.stop()
    
    # Run the example
    asyncio.run(main())
