# Quick Start Guide: Physics-Based Cyber Defense Framework

## Introduction

This guide will get you started with the physics-based cyber defense framework in under 5 minutes.

## Installation

No external dependencies required beyond NumPy!

```bash
# Install NumPy (if not already installed)
pip install numpy

# Navigate to the repository
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-
```

## Your First Optimization

### Example 1: Basic Algorithm Usage

```python
import numpy as np
from physics_algorithms import GravitationalSearchAlgorithm

# Define a simple optimization problem
def sphere_function(x):
    """Simple sphere function: minimize sum of squares"""
    return np.sum(x**2)

# Set search space bounds (10 dimensions, range [-100, 100])
bounds = np.array([[-100, 100]] * 10)

# Create optimizer
gsa = GravitationalSearchAlgorithm(
    objective_func=sphere_function,
    bounds=bounds,
    population_size=30,
    max_iterations=50,
    minimize=True,
    verbose=True
)

# Run optimization
results = gsa.run()

# Display results
print(f"\n{'='*60}")
print(f"Best Solution: {results['best_solution']}")
print(f"Best Fitness: {results['best_fitness']:.6f}")
print(f"Execution Time: {results['execution_time']:.2f}s")
print(f"{'='*60}\n")
```

Save this as `test_basic.py` and run:
```bash
python test_basic.py
```

### Example 2: FlameLang Interface

```python
from physics_algorithms.flamelang_integration import flame_executor, register_all_algorithms
import numpy as np

# Register all algorithms
register_all_algorithms()

# Define your optimization problem
def network_cost(positions):
    return np.sum(positions**2)  # Simplified cost function

# Execute using FlameLang syntax
results = flame_executor.execute_command(
    "⚛{gsa⟐network_topology}",
    context={
        'objective_func': network_cost,
        'bounds': np.array([[-10, 10]] * 5),
        'config': {
            'population_size': 20,
            'max_iterations': 30,
            'verbose': True
        }
    }
)

print(f"Optimization complete!")
print(f"Best fitness: {results['best_fitness']:.6f}")

# View execution history
history = flame_executor.get_history()
print(f"\nExecuted {len(history)} operations")
```

### Example 3: Cyber Defense Application

```python
import numpy as np
from physics_algorithms import (
    ElectromagnetismAlgorithm,  # For vulnerability scanning
    BlackHoleAlgorithm,          # For malware detection
    MultiverseOptimizer          # For threat simulation
)

# Example: Optimize vulnerability scanner parameters
def scanner_accuracy(params):
    """
    Optimize scanner for maximum detection with minimum false positives
    params: [sensitivity, timeout, thread_count]
    """
    sensitivity, timeout, thread_count = params
    
    # Simulate detection accuracy (higher sensitivity = more detections)
    detection = sensitivity * 0.8
    
    # Penalize slow scans
    speed_penalty = timeout / 100.0
    
    # Optimal thread count is around 8
    thread_penalty = abs(thread_count - 8) * 0.02
    
    accuracy = detection - speed_penalty - thread_penalty
    return -accuracy  # Minimize (we want to maximize accuracy)

# Define realistic bounds
bounds = np.array([
    [0.5, 1.0],    # Sensitivity: 50% to 100%
    [10, 60],      # Timeout: 10 to 60 seconds
    [1, 16]        # Thread count: 1 to 16
])

# Use Electromagnetism Algorithm for feature selection
ema = ElectromagnetismAlgorithm(
    objective_func=scanner_accuracy,
    bounds=bounds,
    population_size=25,
    max_iterations=30,
    minimize=True,
    verbose=True
)

results = ema.run()

print(f"\n{'='*60}")
print(f"Optimal Scanner Configuration:")
print(f"  Sensitivity: {results['best_solution'][0]:.2%}")
print(f"  Timeout: {results['best_solution'][1]:.1f} seconds")
print(f"  Threads: {int(results['best_solution'][2])}")
print(f"  Accuracy Score: {-results['best_fitness']:.4f}")
print(f"{'='*60}\n")
```

## Algorithm Selection Guide

Choose the right algorithm for your problem:

### Network & Infrastructure
- **GSA** - Network topology, node placement
- **CFO** - Load balancing, resource distribution
- **CSS** - Path optimization, routing
- **APO** - Resource management under load
- **EO** - Traffic shaping, flow control

### Security Analysis
- **SA** - Cryptographic analysis, pattern finding
- **EMA** - Feature selection, parameter tuning
- **MOA** - Data stream synchronization
- **OIO** - Packet analysis, signal processing

### Threat Detection
- **BHA** - Malware signature evolution
- **IGIO** - Antivirus heuristics, adaptive learning
- **MVO** - Parallel threat scenarios
- **RAY** - Attack path backtracing

### Alert Management
- **CBO** - Alert consolidation, deduplication
- **GIO** - Tool orchestration, dependency management

## Common Patterns

### Pattern 1: Parameter Tuning
```python
def tune_security_tool(algorithm_class, objective_func, param_bounds):
    """Generic parameter tuning for any security tool"""
    optimizer = algorithm_class(
        objective_func=objective_func,
        bounds=param_bounds,
        population_size=30,
        max_iterations=50,
        minimize=True
    )
    return optimizer.run()
```

### Pattern 2: Multi-Objective Optimization
```python
def multi_objective_security(params):
    """Balance security, performance, and cost"""
    security_score = calculate_security(params)
    performance_cost = calculate_performance(params)
    financial_cost = calculate_cost(params)
    
    # Weighted sum (adjust weights based on priorities)
    return -(0.5 * security_score - 0.3 * performance_cost - 0.2 * financial_cost)
```

### Pattern 3: Constraint Handling
```python
from physics_algorithms.base import CyberDefenseOptimizer

class CustomOptimizer(CyberDefenseOptimizer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add security constraints
        self.add_defense_constraint(lambda x: x[0] > 0.5)  # Min security level
        self.add_defense_constraint(lambda x: np.sum(x) < 100)  # Resource limit
```

## Performance Tips

1. **Start Small**: Begin with `population_size=20` and `max_iterations=30`
2. **Tune Gradually**: Increase population and iterations if results aren't good enough
3. **Use Verbose Mode**: Set `verbose=True` to monitor progress
4. **Cache Results**: Store convergence curves for analysis
5. **Parallel Execution**: Run multiple algorithms in parallel for comparison

## Troubleshooting

### Problem: Slow convergence
**Solution**: Increase population size or adjust algorithm-specific parameters

### Problem: Stuck in local optima
**Solution**: Try different algorithms or increase exploration (temperature, mutation rate, etc.)

### Problem: Out of bounds errors
**Solution**: Check that bounds are correctly defined and objective function handles edge cases

### Problem: Poor results
**Solution**: 
- Verify objective function is correct
- Try multiple random seeds
- Use ensemble of algorithms
- Adjust algorithm parameters

## Next Steps

1. **Run Examples**: Execute `python physics_algorithms/examples.py`
2. **Read Documentation**: Review `docs/physics_framework/PHYSICS_CYBER_DEFENSE_ARCHITECTURE.md`
3. **Explore Security Tools**: Check `security_tools/SECURITY_TOOLS_FRAMEWORK.md`
4. **Integrate FlameLang**: Study `physics_algorithms/flamelang_integration.py`
5. **Build Your Application**: Adapt algorithms to your specific security needs

## Getting Help

- **Documentation**: See README.md in physics_algorithms/
- **Examples**: Check examples.py for comprehensive use cases
- **Architecture**: Review the main architecture document
- **Community**: Join the Strategickhaos Discord server

---

*🔥 Built with FlameLang • Powered by Physics • Defending with Sovereignty*
