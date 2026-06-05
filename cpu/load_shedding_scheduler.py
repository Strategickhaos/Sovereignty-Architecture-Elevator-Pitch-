#!/usr/bin/env python3
"""
Load Shedding Scheduler - Resource Management
Part of SAGCO OS CPU Architecture

This module implements intelligent load shedding and resource
scheduling to prevent system overload. When resources are scarce,
it gracefully degrades functionality while maintaining critical
operations.

Inspired by electrical grid load shedding - when power is limited,
shed non-critical loads to keep essential services running.
"""

import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from heapq import heappush, heappop


class Priority(Enum):
    """Task priority levels"""
    CRITICAL = 5    # System survival
    HIGH = 4        # Core functionality
    NORMAL = 3      # Standard operations
    LOW = 2         # Nice-to-have features
    DEFERRABLE = 1  # Can be postponed indefinitely


class ResourceType(Enum):
    """Types of resources to manage"""
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK = "network"
    STORAGE = "storage"
    ENERGY = "energy"


@dataclass
class Task:
    """Represents a scheduled task"""
    id: str
    priority: Priority
    resource_requirements: Dict[ResourceType, float]
    execution_time: float
    deadline: Optional[float]
    callback: Optional[Callable]
    created: float = None
    
    def __post_init__(self):
        if self.created is None:
            self.created = time.time()
    
    def __lt__(self, other):
        """Tasks are ordered by priority (higher first), then deadline"""
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        if self.deadline and other.deadline:
            return self.deadline < other.deadline
        return self.created < other.created


@dataclass
class ResourceState:
    """Current state of system resources"""
    available: Dict[ResourceType, float]
    capacity: Dict[ResourceType, float]
    utilization: Dict[ResourceType, float]
    
    def is_sufficient_for(self, requirements: Dict[ResourceType, float]) -> bool:
        """Check if available resources meet requirements"""
        return all(
            self.available.get(rtype, 0) >= amount
            for rtype, amount in requirements.items()
        )
    
    def allocate(self, requirements: Dict[ResourceType, float]) -> bool:
        """Attempt to allocate resources"""
        if not self.is_sufficient_for(requirements):
            return False
        
        for rtype, amount in requirements.items():
            self.available[rtype] -= amount
            self.utilization[rtype] = 1.0 - (self.available[rtype] / self.capacity[rtype])
        
        return True
    
    def deallocate(self, requirements: Dict[ResourceType, float]):
        """Return resources to available pool"""
        for rtype, amount in requirements.items():
            self.available[rtype] = min(
                self.available[rtype] + amount,
                self.capacity[rtype]
            )
            self.utilization[rtype] = 1.0 - (self.available[rtype] / self.capacity[rtype])


class LoadSheddingScheduler:
    """
    Intelligent Load Shedding and Resource Scheduler
    
    Manages system resources and gracefully degrades functionality
    when resources are constrained.
    """
    
    # Load shedding thresholds
    THRESHOLD_WARNING = 0.75    # 75% utilization - start monitoring
    THRESHOLD_CRITICAL = 0.90   # 90% utilization - begin shedding
    THRESHOLD_EMERGENCY = 0.95  # 95% utilization - aggressive shedding
    
    def __init__(self, capacity: Dict[ResourceType, float]):
        """
        Initialize scheduler with resource capacity
        
        Args:
            capacity: Maximum capacity for each resource type
        """
        self.resources = ResourceState(
            available=capacity.copy(),
            capacity=capacity.copy(),
            utilization={rtype: 0.0 for rtype in capacity}
        )
        
        self.task_queue = []  # Priority queue of tasks
        self.running_tasks: Dict[str, Task] = {}
        self.shed_tasks: List[Task] = []
        self.completed_tasks = 0
        self.shed_count = 0
        
    def schedule_task(self, task: Task) -> bool:
        """
        Schedule a task for execution
        
        Args:
            task: Task to schedule
            
        Returns:
            True if task was scheduled, False if immediately shed
        """
        # Check if we should shed this task immediately
        if self._should_shed_task(task):
            self.shed_tasks.append(task)
            self.shed_count += 1
            return False
        
        # Add to priority queue
        heappush(self.task_queue, task)
        return True
    
    def execute_next(self) -> Optional[Task]:
        """
        Execute the next highest priority task if resources allow
        
        Returns:
            The executed task, or None if no task could execute
        """
        if not self.task_queue:
            return None
        
        # Get highest priority task
        task = heappop(self.task_queue)
        
        # Try to allocate resources
        if self.resources.allocate(task.resource_requirements):
            self.running_tasks[task.id] = task
            return task
        else:
            # Not enough resources - check if we should shed or requeue
            if self._should_shed_task(task):
                self.shed_tasks.append(task)
                self.shed_count += 1
                return None
            else:
                # Requeue for later
                heappush(self.task_queue, task)
                return None
    
    def complete_task(self, task_id: str):
        """Mark a task as complete and release its resources"""
        if task_id in self.running_tasks:
            task = self.running_tasks.pop(task_id)
            self.resources.deallocate(task.resource_requirements)
            self.completed_tasks += 1
    
    def _should_shed_task(self, task: Task) -> bool:
        """Determine if a task should be shed based on priority and load"""
        # Never shed critical tasks
        if task.priority == Priority.CRITICAL:
            return False
        
        # Calculate current maximum utilization
        max_utilization = max(self.resources.utilization.values())
        
        # Emergency: shed everything except critical and high
        if max_utilization >= self.THRESHOLD_EMERGENCY:
            return task.priority.value < Priority.HIGH.value
        
        # Critical: shed low and deferrable
        if max_utilization >= self.THRESHOLD_CRITICAL:
            return task.priority.value < Priority.NORMAL.value
        
        # Normal operation: only shed deferrable if at warning threshold
        if max_utilization >= self.THRESHOLD_WARNING:
            return task.priority == Priority.DEFERRABLE
        
        return False
    
    def get_load_level(self) -> str:
        """Get current load level description"""
        max_utilization = max(self.resources.utilization.values())
        
        if max_utilization >= self.THRESHOLD_EMERGENCY:
            return "EMERGENCY"
        elif max_utilization >= self.THRESHOLD_CRITICAL:
            return "CRITICAL"
        elif max_utilization >= self.THRESHOLD_WARNING:
            return "WARNING"
        else:
            return "NORMAL"
    
    def get_statistics(self) -> Dict:
        """Return scheduler statistics"""
        return {
            "queued_tasks": len(self.task_queue),
            "running_tasks": len(self.running_tasks),
            "completed_tasks": self.completed_tasks,
            "shed_tasks": self.shed_count,
            "load_level": self.get_load_level(),
            "resource_utilization": self.resources.utilization.copy(),
            "shed_rate": self.shed_count / max(1, self.completed_tasks + self.shed_count),
        }


def main():
    """Demonstration of Load Shedding Scheduler"""
    
    # Initialize with limited resources
    scheduler = LoadSheddingScheduler({
        ResourceType.CPU: 100.0,
        ResourceType.MEMORY: 1000.0,
        ResourceType.NETWORK: 50.0,
    })
    
    print("⚡ LOAD SHEDDING SCHEDULER - Resource Management")
    print("=" * 70)
    
    # Create test tasks with varying priorities and requirements
    tasks = [
        Task("critical_1", Priority.CRITICAL, {ResourceType.CPU: 20, ResourceType.MEMORY: 100}, 1.0, None, None),
        Task("high_1", Priority.HIGH, {ResourceType.CPU: 30, ResourceType.MEMORY: 200}, 2.0, None, None),
        Task("normal_1", Priority.NORMAL, {ResourceType.CPU: 25, ResourceType.MEMORY: 150}, 1.5, None, None),
        Task("normal_2", Priority.NORMAL, {ResourceType.CPU: 25, ResourceType.MEMORY: 150}, 1.5, None, None),
        Task("low_1", Priority.LOW, {ResourceType.CPU: 15, ResourceType.MEMORY: 100}, 1.0, None, None),
        Task("defer_1", Priority.DEFERRABLE, {ResourceType.CPU: 10, ResourceType.MEMORY: 50}, 0.5, None, None),
    ]
    
    print("\n[Phase 1] Scheduling tasks...")
    for task in tasks:
        scheduled = scheduler.schedule_task(task)
        status = "✅ Scheduled" if scheduled else "⚠️  Shed immediately"
        print(f"  {task.id:12s} ({task.priority.name:12s}): {status}")
    
    print(f"\n[Phase 2] Executing tasks...")
    executed_tasks = []
    for _ in range(4):  # Try to execute 4 tasks
        task = scheduler.execute_next()
        if task:
            executed_tasks.append(task)
            print(f"  ✓ Executing: {task.id} ({task.priority.name})")
            # Simulate task completion after brief execution
            time.sleep(0.01)
        else:
            print(f"  ⚠️  No task could execute (insufficient resources)")
            break
    
    print(f"\n[Phase 3] Completing tasks...")
    for task in executed_tasks:
        scheduler.complete_task(task.id)
        print(f"  ✓ Completed: {task.id}")
    
    # Try to execute remaining
    remaining = scheduler.execute_next()
    if remaining:
        print(f"  ✓ Executing remaining: {remaining.id}")
        scheduler.complete_task(remaining.id)
    
    print("\n" + "=" * 70)
    stats = scheduler.get_statistics()
    print(f"Scheduler Statistics:")
    print(f"  Load Level: {stats['load_level']}")
    print(f"  Completed Tasks: {stats['completed_tasks']}")
    print(f"  Shed Tasks: {stats['shed_tasks']}")
    print(f"  Shed Rate: {stats['shed_rate']:.1%}")
    print(f"  Queued Tasks: {stats['queued_tasks']}")
    print(f"\nResource Utilization:")
    for rtype, util in stats['resource_utilization'].items():
        bar = "█" * int(util * 20)
        print(f"  {rtype.value:8s}: [{bar:20s}] {util:.1%}")


if __name__ == "__main__":
    main()
