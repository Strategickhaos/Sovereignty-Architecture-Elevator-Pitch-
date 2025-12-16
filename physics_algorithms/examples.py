"""
Example usage of physics-based optimization algorithms for cyber defense.
Demonstrates each algorithm with practical security scenarios.
"""

import numpy as np
from physics_algorithms import *


def network_topology_optimization():
    """
    Example: Use GSA to optimize network node placement.
    Objective: Minimize average latency between nodes.
    """
    print("=" * 70)
    print("EXAMPLE 1: Network Topology Optimization with GSA")
    print("=" * 70)
    
    # Define objective function (minimize total distance between nodes)
    def network_latency(positions):
        """Calculate total network latency based on node positions."""
        # positions: [node1_x, node1_y, node2_x, node2_y, ...]
        n_nodes = len(positions) // 2
        total_latency = 0
        
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                x1, y1 = positions[i*2], positions[i*2+1]
                x2, y2 = positions[j*2], positions[j*2+1]
                distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                total_latency += distance
        
        return total_latency
    
    # Define bounds (2D space for 4 nodes)
    bounds = np.array([[0, 100]] * 8)  # 4 nodes in 100x100 grid
    
    # Run GSA
    gsa = GravitationalSearchAlgorithm(
        objective_func=network_latency,
        bounds=bounds,
        population_size=30,
        max_iterations=50,
        minimize=True,
        verbose=True
    )
    
    results = gsa.run()
    print(f"\nBest network layout found:")
    print(f"Positions: {results['best_solution']}")
    print(f"Total latency: {results['best_fitness']:.2f}")
    print(f"Execution time: {results['execution_time']:.2f} seconds\n")


def cryptographic_analysis():
    """
    Example: Use Simulated Annealing for cryptographic pattern analysis.
    Objective: Find optimal parameters for encryption strength testing.
    """
    print("=" * 70)
    print("EXAMPLE 2: Cryptographic Analysis with Simulated Annealing")
    print("=" * 70)
    
    # Define objective function (maximize entropy)
    def encryption_strength(params):
        """Calculate encryption strength metric."""
        # Simulated encryption strength based on key parameters
        key_length, rounds, salt_bits = params
        strength = key_length * np.log(rounds + 1) + salt_bits * 0.5
        return -strength  # Minimize (we want to maximize strength)
    
    # Define bounds
    bounds = np.array([
        [128, 256],    # Key length
        [10, 50],      # Encryption rounds
        [64, 256]      # Salt bits
    ])
    
    # Run SA
    sa = SimulatedAnnealing(
        objective_func=encryption_strength,
        bounds=bounds,
        T0=1000.0,
        cooling_rate=0.95,
        max_iterations=200,
        minimize=True,
        verbose=True
    )
    
    results = sa.run()
    print(f"\nOptimal encryption parameters:")
    print(f"Key length: {results['best_solution'][0]:.0f} bits")
    print(f"Rounds: {results['best_solution'][1]:.0f}")
    print(f"Salt bits: {results['best_solution'][2]:.0f}")
    print(f"Strength score: {-results['best_fitness']:.2f}")
    print(f"Execution time: {results['execution_time']:.2f} seconds\n")


def vulnerability_scanner_optimization():
    """
    Example: Use EMA for feature selection in vulnerability scanning.
    Objective: Select optimal features for maximum detection accuracy.
    """
    print("=" * 70)
    print("EXAMPLE 3: Vulnerability Scanner Feature Selection with EMA")
    print("=" * 70)
    
    # Simulated vulnerability features (binary selection: 0 or 1)
    feature_names = [
        "port_scan", "service_version", "ssl_check", "headers_analysis",
        "path_traversal", "sql_injection", "xss_detection", "csrf_check",
        "auth_bypass", "file_inclusion"
    ]
    
    # Define objective function
    def detection_accuracy(feature_vector):
        """Calculate detection accuracy based on selected features."""
        # Simulated: some features are more important
        weights = np.array([0.9, 0.8, 0.95, 0.7, 0.85, 0.9, 0.75, 0.6, 0.8, 0.7])
        
        # Round to binary selection
        binary_selection = (feature_vector > 0.5).astype(int)
        
        # Calculate accuracy (weighted sum)
        accuracy = np.sum(binary_selection * weights) / len(weights)
        
        # Penalize for using too many features (overhead)
        n_selected = np.sum(binary_selection)
        penalty = 0.02 * n_selected if n_selected > 7 else 0
        
        return -(accuracy - penalty)  # Minimize (maximize accuracy - penalty)
    
    # Define bounds
    bounds = np.array([[0, 1]] * 10)
    
    # Run EMA
    ema = ElectromagnetismAlgorithm(
        objective_func=detection_accuracy,
        bounds=bounds,
        population_size=25,
        max_iterations=30,
        minimize=True,
        verbose=True
    )
    
    results = ema.run()
    
    # Convert to binary selection
    binary_selection = (results['best_solution'] > 0.5).astype(int)
    selected_features = [feature_names[i] for i, sel in enumerate(binary_selection) if sel == 1]
    
    print(f"\nOptimal feature selection:")
    print(f"Selected features: {', '.join(selected_features)}")
    print(f"Number of features: {len(selected_features)}")
    print(f"Detection accuracy: {-results['best_fitness']:.2%}")
    print(f"Execution time: {results['execution_time']:.2f} seconds\n")


def malware_detection_evolution():
    """
    Example: Use Black Hole Algorithm for malware signature evolution.
    Objective: Evolve detection patterns that catch more malware variants.
    """
    print("=" * 70)
    print("EXAMPLE 4: Malware Signature Evolution with Black Hole Algorithm")
    print("=" * 70)
    
    # Define objective function
    def detection_rate(signature_params):
        """Calculate malware detection rate for given signature parameters."""
        # Simulated: signature characteristics
        sensitivity, specificity, threshold = signature_params
        
        # Higher sensitivity = more detections but more false positives
        # Higher specificity = fewer false positives
        detection = sensitivity * 0.6 + specificity * 0.4 - abs(threshold - 0.5) * 0.2
        
        return -detection  # Minimize (maximize detection)
    
    # Define bounds
    bounds = np.array([
        [0.5, 1.0],    # Sensitivity
        [0.7, 1.0],    # Specificity
        [0.3, 0.7]     # Threshold
    ])
    
    # Run BHA
    bha = BlackHoleAlgorithm(
        objective_func=detection_rate,
        bounds=bounds,
        population_size=40,
        max_iterations=50,
        minimize=True,
        verbose=True
    )
    
    results = bha.run()
    print(f"\nEvolved signature parameters:")
    print(f"Sensitivity: {results['best_solution'][0]:.3f}")
    print(f"Specificity: {results['best_solution'][1]:.3f}")
    print(f"Threshold: {results['best_solution'][2]:.3f}")
    print(f"Detection rate: {-results['best_fitness']:.2%}")
    print(f"Execution time: {results['execution_time']:.2f} seconds\n")


def parallel_threat_simulation():
    """
    Example: Use Multiverse Optimizer for parallel threat scenario simulation.
    Objective: Find worst-case attack scenarios.
    """
    print("=" * 70)
    print("EXAMPLE 5: Parallel Threat Simulation with Multiverse Optimizer")
    print("=" * 70)
    
    # Define objective function
    def threat_impact(attack_vector):
        """Calculate impact of attack vector."""
        # Attack parameters: [entry_point, lateral_movement, persistence, exfiltration]
        entry, lateral, persist, exfil = attack_vector
        
        # Calculate total impact
        impact = (entry * 0.3 + lateral * 0.25 + persist * 0.25 + exfil * 0.2) * 100
        
        return -impact  # Minimize (find maximum impact scenario)
    
    # Define bounds
    bounds = np.array([[0, 1]] * 4)
    
    # Run MVO
    mvo = MultiverseOptimizer(
        objective_func=threat_impact,
        bounds=bounds,
        population_size=30,
        max_iterations=40,
        minimize=True,
        verbose=True
    )
    
    results = mvo.run()
    print(f"\nWorst-case attack scenario identified:")
    print(f"Entry point difficulty: {results['best_solution'][0]:.2f}")
    print(f"Lateral movement ease: {results['best_solution'][1]:.2f}")
    print(f"Persistence strength: {results['best_solution'][2]:.2f}")
    print(f"Exfiltration capability: {results['best_solution'][3]:.2f}")
    print(f"Total impact score: {-results['best_fitness']:.2f}/100")
    print(f"Execution time: {results['execution_time']:.2f} seconds\n")


def antivirus_heuristic_evolution():
    """
    Example: Use IGIO for evolving antivirus heuristics.
    Objective: Create adaptive detection patterns.
    """
    print("=" * 70)
    print("EXAMPLE 6: Antivirus Heuristic Evolution with IGIO")
    print("=" * 70)
    
    # Define objective function
    def heuristic_performance(heuristic_weights):
        """Calculate heuristic detection performance."""
        # Weights for different behavioral indicators
        file_ops, network_ops, registry_ops, process_ops, memory_ops = heuristic_weights
        
        # Simulated malware samples with different characteristics
        malware_profiles = np.array([
            [0.9, 0.7, 0.5, 0.8, 0.6],  # Ransomware
            [0.6, 0.9, 0.4, 0.7, 0.5],  # Trojan
            [0.5, 0.8, 0.9, 0.6, 0.7],  # Rootkit
            [0.7, 0.6, 0.3, 0.9, 0.8],  # Worm
        ])
        
        # Calculate detection scores
        detection_scores = malware_profiles @ heuristic_weights
        detection_rate = np.mean(detection_scores > 0.7)
        
        # False positive penalty (prefer balanced weights)
        balance_penalty = np.std(heuristic_weights) * 0.1
        
        return -(detection_rate - balance_penalty)  # Minimize (maximize detection)
    
    # Define bounds
    bounds = np.array([[0, 1]] * 5)
    
    # Run IGIO
    igio = ImmuneGravitationOptimizer(
        objective_func=heuristic_performance,
        bounds=bounds,
        population_size=35,
        max_iterations=60,
        clone_rate=0.2,
        mutation_rate=0.15,
        minimize=True,
        verbose=True
    )
    
    results = igio.run()
    
    indicators = ["File Ops", "Network Ops", "Registry Ops", "Process Ops", "Memory Ops"]
    print(f"\nEvolved heuristic weights:")
    for i, indicator in enumerate(indicators):
        print(f"  {indicator}: {results['best_solution'][i]:.3f}")
    print(f"Detection rate: {-results['best_fitness']:.2%}")
    print(f"Memory cells stored: {results['info']['memory_cells_count']}")
    print(f"Execution time: {results['execution_time']:.2f} seconds\n")


if __name__ == "__main__":
    print("\n")
    print("🔥" * 35)
    print("PHYSICS-BASED CYBER DEFENSE OPTIMIZATION")
    print("Sovereignty Architecture Enhancement v1.0")
    print("🔥" * 35)
    print("\n")
    
    # Run all examples
    network_topology_optimization()
    cryptographic_analysis()
    vulnerability_scanner_optimization()
    malware_detection_evolution()
    parallel_threat_simulation()
    antivirus_heuristic_evolution()
    
    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
