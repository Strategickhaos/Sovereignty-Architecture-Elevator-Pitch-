#!/usr/bin/env python3
"""
Sister Protocol - Immune-Aware Process Scheduler

Implements biological scheduling policies based on NEURO-36 classifications.
This is a proof-of-concept showing how immune dynamics translate to OS policies.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class ProcessClass(Enum):
    """Process classification based on immune system behavior"""
    RAIL = "RAIL"              # Critical, non-negotiable safety rails
    CHAMPION = "CHAMPION"       # High-performance core services
    GATE = "GATE"              # Structural holders with controlled exploration
    EVOLVING = "EVOLVING"      # Standard processes, homeostatic equilibrium
    SANDBOX = "SANDBOX"        # Experimental periphery, never trusted
    MUTANT = "MUTANT"          # Unstable/failing processes
    CULL = "CULL"              # Dead/failed processes


class Priority(Enum):
    """Process priority levels"""
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    MINIMAL = 4


class TRIG6Threshold(Enum):
    """TRIG6 geometry threshold tightness"""
    VERY_TIGHT = "very_tight"   # RAIL: ±5° from safe zones
    TIGHT = "tight"             # CHAMPION: ±10°
    MODERATE = "moderate"       # GATE: ±15°
    STANDARD = "standard"       # EVOLVING: ±20°
    LOOSE = "loose"             # SANDBOX/MUTANT: ±30°


class CoreAccess(Enum):
    """Level of access to core system resources"""
    ALWAYS = "always"           # Unrestricted access
    CONTROLLED = "controlled"   # Mediated through gates
    LIMITED = "limited"         # Minimal access
    NEVER = "never"            # Completely sandboxed


@dataclass
class SchedulingPolicy:
    """Scheduling policy for a process"""
    priority: Priority
    mutation_rate: float        # 0.0 - 1.0
    trig6_threshold: TRIG6Threshold
    core_access: CoreAccess
    cpu_share: float           # 0.0 - 1.0
    memory_limit_mb: Optional[int]
    restart_on_failure: bool
    protection_halo: bool      # Creates protection zone around this process
    
    def __str__(self):
        return (f"Priority: {self.priority.name}, "
                f"Mutation: {self.mutation_rate:.0%}, "
                f"Threshold: {self.trig6_threshold.value}, "
                f"Core: {self.core_access.value}, "
                f"CPU: {self.cpu_share:.0%}")


class SisterProtocol:
    """
    Immune-aware process scheduler based on NEURO-36 architecture.
    
    Maps biological immune classifications to OS scheduling policies.
    """
    
    # Policy matrix based on classification
    POLICIES: Dict[ProcessClass, SchedulingPolicy] = {
        ProcessClass.RAIL: SchedulingPolicy(
            priority=Priority.CRITICAL,
            mutation_rate=0.0,           # DNA locked
            trig6_threshold=TRIG6Threshold.VERY_TIGHT,
            core_access=CoreAccess.ALWAYS,
            cpu_share=1.0,               # Max resources
            memory_limit_mb=None,        # No limit
            restart_on_failure=True,
            protection_halo=True         # Protect neighbors
        ),
        
        ProcessClass.CHAMPION: SchedulingPolicy(
            priority=Priority.HIGH,
            mutation_rate=0.05,          # Minimal mutation
            trig6_threshold=TRIG6Threshold.TIGHT,
            core_access=CoreAccess.ALWAYS,
            cpu_share=0.8,
            memory_limit_mb=None,
            restart_on_failure=True,
            protection_halo=False
        ),
        
        ProcessClass.GATE: SchedulingPolicy(
            priority=Priority.MEDIUM,
            mutation_rate=0.15,          # Controlled exploration
            trig6_threshold=TRIG6Threshold.MODERATE,
            core_access=CoreAccess.CONTROLLED,
            cpu_share=0.5,
            memory_limit_mb=2048,
            restart_on_failure=True,
            protection_halo=False
        ),
        
        ProcessClass.EVOLVING: SchedulingPolicy(
            priority=Priority.MEDIUM,
            mutation_rate=0.25,          # Standard evolution
            trig6_threshold=TRIG6Threshold.STANDARD,
            core_access=CoreAccess.CONTROLLED,
            cpu_share=0.4,
            memory_limit_mb=1024,
            restart_on_failure=False,
            protection_halo=False
        ),
        
        ProcessClass.SANDBOX: SchedulingPolicy(
            priority=Priority.LOW,
            mutation_rate=0.50,          # Wild exploration
            trig6_threshold=TRIG6Threshold.LOOSE,
            core_access=CoreAccess.NEVER,
            cpu_share=0.2,
            memory_limit_mb=512,
            restart_on_failure=False,
            protection_halo=False
        ),
        
        ProcessClass.MUTANT: SchedulingPolicy(
            priority=Priority.LOW,
            mutation_rate=0.75,          # High mutation or reset
            trig6_threshold=TRIG6Threshold.LOOSE,
            core_access=CoreAccess.NEVER,
            cpu_share=0.1,
            memory_limit_mb=256,
            restart_on_failure=False,
            protection_halo=False
        ),
        
        ProcessClass.CULL: SchedulingPolicy(
            priority=Priority.MINIMAL,
            mutation_rate=0.0,           # N/A
            trig6_threshold=TRIG6Threshold.LOOSE,
            core_access=CoreAccess.NEVER,
            cpu_share=0.0,
            memory_limit_mb=0,
            restart_on_failure=False,
            protection_halo=False
        ),
    }
    
    @classmethod
    def get_policy(cls, process_class: ProcessClass) -> SchedulingPolicy:
        """Get scheduling policy for a process classification"""
        return cls.POLICIES[process_class]
    
    @classmethod
    def should_restart(cls, process_class: ProcessClass) -> bool:
        """Determine if a failed process should be restarted"""
        policy = cls.get_policy(process_class)
        return policy.restart_on_failure
    
    @classmethod
    def get_mutation_rate(cls, process_class: ProcessClass, 
                         fitness: float, H: float) -> float:
        """
        Calculate adaptive mutation rate based on classification and metrics.
        
        Lower fitness → higher mutation (explore more)
        Lower H → higher mutation (less valuable to preserve)
        """
        base_rate = cls.get_policy(process_class).mutation_rate
        
        # Adjust based on fitness (inverse relationship)
        fitness_factor = 1.0 - fitness
        
        # Adjust based on H (inverse relationship)
        h_factor = 1.0 - H
        
        # Combined adjustment (weighted)
        adjusted_rate = base_rate * (0.5 + 0.3 * fitness_factor + 0.2 * h_factor)
        
        return min(1.0, adjusted_rate)
    
    @classmethod
    def apply_protection_halo(cls, rail_processes: list, 
                            neighbor_processes: list) -> None:
        """
        Apply protection halo around RAIL processes.
        
        Neighbors of RAIL processes get:
        - Tighter TRIG6 thresholds
        - Reduced mutation rates
        - Increased monitoring
        """
        for neighbor in neighbor_processes:
            # Tighten thresholds
            if neighbor.trig6_threshold == TRIG6Threshold.LOOSE:
                neighbor.trig6_threshold = TRIG6Threshold.STANDARD
            elif neighbor.trig6_threshold == TRIG6Threshold.STANDARD:
                neighbor.trig6_threshold = TRIG6Threshold.MODERATE
            
            # Reduce mutation
            neighbor.mutation_rate *= 0.5
            
            # Note: In real implementation, would also increase watchdog coverage


def demonstrate_policies():
    """Demonstrate Sister Protocol policies for each classification"""
    print("=" * 80)
    print("SISTER PROTOCOL - IMMUNE-AWARE SCHEDULING POLICIES")
    print("=" * 80)
    print()
    
    # Show policy for each classification
    for process_class in ProcessClass:
        policy = SisterProtocol.get_policy(process_class)
        print(f"{process_class.value:12s}: {policy}")
    
    print()
    print("=" * 80)
    print("ADAPTIVE MUTATION RATES (based on fitness & H)")
    print("=" * 80)
    print()
    
    # Example: Show how mutation rate adapts
    test_cases = [
        (ProcessClass.GATE, 0.8, 0.7, "High fitness, high H"),
        (ProcessClass.GATE, 0.4, 0.5, "Mid fitness, mid H"),
        (ProcessClass.GATE, 0.2, 0.3, "Low fitness, low H"),
        (ProcessClass.SANDBOX, 0.8, 0.7, "High fitness, high H"),
        (ProcessClass.SANDBOX, 0.4, 0.5, "Mid fitness, mid H"),
        (ProcessClass.SANDBOX, 0.2, 0.3, "Low fitness, low H"),
    ]
    
    for process_class, fitness, H, description in test_cases:
        base_rate = SisterProtocol.get_policy(process_class).mutation_rate
        adjusted_rate = SisterProtocol.get_mutation_rate(process_class, fitness, H)
        print(f"{process_class.value:12s} | f={fitness:.1f}, H={H:.1f} ({description:20s}) | "
              f"Base: {base_rate:.0%} → Adjusted: {adjusted_rate:.0%}")
    
    print()
    print("=" * 80)
    print("NEURO-36 IMMUNE COMPONENTS MAPPED TO POLICIES")
    print("=" * 80)
    print()
    
    # Example mappings from actual NEURO-36 data
    examples = [
        ("Coughing", ProcessClass.RAIL, 0.477, 0.52),
        ("Stem Cells", ProcessClass.RAIL, 0.494, 0.52),
        ("Skin", ProcessClass.GATE, 0.458, 0.50),
        ("Bacteria", ProcessClass.GATE, 0.449, 0.54),
        ("Bone Marrow", ProcessClass.EVOLVING, 0.496, 0.47),
        ("Neutrophil", ProcessClass.SANDBOX, 0.374, 0.06),
        ("Toxins", ProcessClass.SANDBOX, 0.365, 0.25),
    ]
    
    for component, process_class, fitness, H in examples:
        policy = SisterProtocol.get_policy(process_class)
        mutation = SisterProtocol.get_mutation_rate(process_class, fitness, H)
        print(f"{component:20s} ({process_class.value:8s}) | f={fitness:.3f}, H={H:.2f}")
        print(f"  → {policy.priority.name:8s} priority, "
              f"{mutation:.0%} mutation, "
              f"{policy.core_access.value:10s} core access, "
              f"{policy.cpu_share:.0%} CPU")
        print()


if __name__ == '__main__':
    demonstrate_policies()
