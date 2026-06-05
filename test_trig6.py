#!/usr/bin/env python3
"""
Unit tests for TRIG6 simulator mathematics.
Validates theta, R, D, N calculations and danger zone detection.
"""

import unittest
import math
from trig6_simulator import TRIG6Simulator, Recipe


class TestTRIG6Mathematics(unittest.TestCase):
    """Test TRIG6 mathematical functions."""
    
    def setUp(self):
        """Set up test simulator."""
        self.sim = TRIG6Simulator(steps_per_run=100)
    
    def test_theta_computation(self):
        """Test theta phase angle calculation."""
        # At s=0, theta should be 0
        theta_0 = self.sim.compute_theta(0.0)
        self.assertAlmostEqual(theta_0, 0.0)
        
        # At s=0.5, theta should be π
        theta_half = self.sim.compute_theta(0.5)
        self.assertAlmostEqual(theta_half, math.pi)
        
        # At s=1, theta should be 2π
        theta_1 = self.sim.compute_theta(1.0)
        self.assertAlmostEqual(theta_1, 2 * math.pi)
    
    def test_danger_zone_detection(self):
        """Test danger zone detection: |tan(θ)| > 10."""
        # At θ = π/2, tan is undefined → danger
        theta_danger = math.pi / 2
        self.assertTrue(self.sim.is_danger_zone(theta_danger))
        
        # At θ = 0, tan(0) = 0 → safe
        theta_safe = 0.0
        self.assertFalse(self.sim.is_danger_zone(theta_safe))
        
        # Near π/2 but tan < 10 → safe
        theta_near = math.atan(9.5)  # tan^-1(9.5)
        self.assertFalse(self.sim.is_danger_zone(theta_near))
        
        # tan(θ) > 10 → danger
        theta_high_tan = math.atan(11)
        self.assertTrue(self.sim.is_danger_zone(theta_high_tan))
    
    def test_resonance_computation(self):
        """Test resonance R calculation."""
        ingredients = {
            'embedding_dim': 256,
            'min_cluster_size': 15,
            'max_clusters': 120
        }
        
        # Early in process (s=0), R should be lower
        R_early = self.sim.compute_resonance(ingredients, 0.0)
        
        # Late in process (s=1), R should be higher
        R_late = self.sim.compute_resonance(ingredients, 1.0)
        
        self.assertGreater(R_late, R_early)
        self.assertGreaterEqual(R_early, 0.0)
        self.assertLessEqual(R_late, 1.0)
    
    def test_drift_computation(self):
        """Test drift D calculation."""
        ingredients = {
            'embedding_dim': 256,
            'min_cluster_size': 15,
            'max_clusters': 120
        }
        
        # LOW hazard should have lower drift
        D_low = self.sim.compute_drift(ingredients, 'LOW')
        
        # HIGH hazard should have higher drift
        D_high = self.sim.compute_drift(ingredients, 'HIGH')
        
        self.assertGreater(D_high, D_low)
        self.assertGreaterEqual(D_low, 0.0)
        self.assertLessEqual(D_high, 1.0)
    
    def test_noise_computation(self):
        """Test noise N calculation."""
        ingredients = {
            'embedding_dim': 256,
            'min_cluster_size': 15
        }
        
        # Early in process, N should be higher
        N_early = self.sim.compute_noise(0.0, ingredients)
        
        # Late in process, N should be lower
        N_late = self.sim.compute_noise(1.0, ingredients)
        
        self.assertGreater(N_early, N_late)
        
        # Higher embedding dim should reduce N
        ingredients_high_dim = ingredients.copy()
        ingredients_high_dim['embedding_dim'] = 500
        N_high_dim = self.sim.compute_noise(0.5, ingredients_high_dim)
        
        ingredients_low_dim = ingredients.copy()
        ingredients_low_dim['embedding_dim'] = 100
        N_low_dim = self.sim.compute_noise(0.5, ingredients_low_dim)
        
        self.assertGreater(N_low_dim, N_high_dim)
    
    def test_fitness_computation(self):
        """Test fitness function: f = R × (1-D) × (1-N) × eq."""
        # Perfect conditions
        R, D, N, eq = 1.0, 0.0, 0.0, 1.0
        f_perfect = self.sim.compute_fitness(R, D, N, eq)
        self.assertAlmostEqual(f_perfect, 1.0)
        
        # Zero resonance
        R, D, N, eq = 0.0, 0.5, 0.5, 1.0
        f_zero = self.sim.compute_fitness(R, D, N, eq)
        self.assertAlmostEqual(f_zero, 0.0)
        
        # Moderate conditions
        R, D, N, eq = 0.6, 0.3, 0.2, 1.0
        f_moderate = self.sim.compute_fitness(R, D, N, eq)
        expected = 0.6 * (1 - 0.3) * (1 - 0.2) * 1.0
        self.assertAlmostEqual(f_moderate, expected)
    
    def test_recipe_simulation(self):
        """Test full recipe simulation."""
        recipe = Recipe(
            id='TEST-001',
            name='Test Recipe',
            hazard_level='MEDIUM',
            ingredients={
                'embedding_dim': 256,
                'min_cluster_size': 15,
                'max_clusters': 120,
                'image_dpi': 300,
                'glyph_min_size': 30
            }
        )
        
        result = self.sim.simulate_recipe(recipe)
        
        # Check result fields exist
        self.assertIsNotNone(result.fitness)
        self.assertIsNotNone(result.danger_count)
        self.assertIsNotNone(result.R)
        self.assertIsNotNone(result.D)
        self.assertIsNotNone(result.N)
        
        # Check bounds
        self.assertGreaterEqual(result.fitness, 0.0)
        self.assertLessEqual(result.fitness, 1.0)
        self.assertGreaterEqual(result.danger_count, 0)
        self.assertLessEqual(result.danger_count, self.sim.steps_per_run)
    
    def test_monte_carlo_simulation(self):
        """Test Monte Carlo simulation."""
        recipe = Recipe(
            id='TEST-002',
            name='Monte Carlo Test',
            hazard_level='LOW',
            ingredients={
                'embedding_dim': 200,
                'min_cluster_size': 10,
                'max_clusters': 100,
                'image_dpi': 300,
                'glyph_min_size': 25
            }
        )
        
        results = self.sim.monte_carlo_simulation(recipe, num_runs=100)
        
        # Check results structure
        self.assertIn('mean_fitness', results)
        self.assertIn('std_fitness', results)
        self.assertIn('mean_danger_rate', results)
        self.assertIn('fitness_values', results)
        
        # Check we got 100 runs
        self.assertEqual(len(results['fitness_values']), 100)
        
        # Fitness should be in valid range
        self.assertGreaterEqual(results['mean_fitness'], 0.0)
        self.assertLessEqual(results['mean_fitness'], 1.0)
    
    def test_evolution(self):
        """Test Darwinian evolution."""
        recipe = Recipe(
            id='TEST-003',
            name='Evolution Test',
            hazard_level='MEDIUM',
            ingredients={
                'embedding_dim': 150,
                'min_cluster_size': 5,
                'max_clusters': 80,
                'image_dpi': 250,
                'glyph_min_size': 20
            }
        )
        
        champion, fitness, dangers = self.sim.evolve_recipe(
            recipe, 
            generations=10, 
            population_size=10
        )
        
        # Champion should be a valid recipe
        self.assertIsInstance(champion, Recipe)
        self.assertEqual(champion.id, recipe.id)
        
        # Fitness should be valid
        self.assertGreaterEqual(fitness, 0.0)
        self.assertLessEqual(fitness, 1.0)
        
        # Evolved ingredients should be different (mutation)
        # Note: Due to randomness, might be the same, but very unlikely
        # Just check they're still valid floats
        for key, value in champion.ingredients.items():
            self.assertIsInstance(value, float)
            self.assertGreater(value, 0.0)


class TestRecipeValidation(unittest.TestCase):
    """Test recipe structure and validation."""
    
    def test_recipe_creation(self):
        """Test Recipe object creation."""
        recipe = Recipe(
            id='VAL-001',
            name='Validation Test',
            hazard_level='HIGH',
            ingredients={'param1': 100.0, 'param2': 200.0}
        )
        
        self.assertEqual(recipe.id, 'VAL-001')
        self.assertEqual(recipe.name, 'Validation Test')
        self.assertEqual(recipe.hazard_level, 'HIGH')
        self.assertEqual(recipe.ingredients['param1'], 100.0)
    
    def test_custom_hooks(self):
        """Test recipe with custom hooks."""
        def custom_R(ingredients, s):
            return 0.5
        
        recipe = Recipe(
            id='HOOK-001',
            name='Hook Test',
            hazard_level='LOW',
            ingredients={'param': 100.0},
            custom_hooks={'R': custom_R}
        )
        
        self.assertIn('R', recipe.custom_hooks)
        self.assertTrue(callable(recipe.custom_hooks['R']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
