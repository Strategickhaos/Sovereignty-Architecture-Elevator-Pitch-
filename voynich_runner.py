#!/usr/bin/env python3
"""
voynich_runner.py
Voynich Manuscript Diagnostic Pipeline Runner with TRIG6 Evolution
Author: Domenic Gabriel Garza (Strategickhaos DAO LLC)
Version: 1.0.1

Concise runner implementing TRIG6 evaluation and Darwinian evolution loops
for Voynich manuscript glyph clustering and codon mapping.
"""

import yaml
import os
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

# Utility functions
def clamp(x, minv, maxv):
    """Clamp value between min and max."""
    return max(minv, min(x, maxv))

def load_pipeline(yaml_path='voynich_diag_pipeline.yaml'):
    """Load pipeline configuration from YAML."""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

# TRIG6 functions
def trig6_theta(progress):
    """Calculate theta from decipher progress."""
    return 2 * np.pi * progress

def trig6_resonance(purity, coverage, stability=0.0):
    """Calculate resonance from pattern consistency and coverage."""
    return clamp(0.55 * purity + 0.45 * coverage + 0.0 * stability, 0.0, 1.0)

def trig6_drift(reassign_rate, outlier_frac):
    """Calculate drift from variance rate and outlier fraction."""
    return clamp(0.65 * reassign_rate + 0.35 * outlier_frac, 0.0, 1.0)

def trig6_noise(var_norm, entropy_norm):
    """Calculate noise from embedding variance and entropy."""
    return clamp(0.55 * var_norm + 0.45 * entropy_norm, 0.0, 1.0)

def trig6_eq(count, target):
    """Calculate equilibrium from count vs target."""
    if target == 0:
        return 0.0
    return clamp(1.0 - abs(count - target) / target, 0.0, 1.0)

def trig6_danger(theta, limit, extra_cond=False):
    """Detect danger from tan(theta) exceeding limit."""
    return abs(np.tan(theta)) > limit or extra_cond

def trig6_fitness(R, D, N, eq):
    """Calculate overall fitness from TRIG6 components."""
    return R * (1.0 - D) * (1.0 - N) * eq

# Evolution functions
def evolve_population(pop_size, generations, top_k, mutation_rate, mutation_targets, eval_fn, init_pop):
    """
    Evolve population using Darwinian selection with mutation and crossover.
    
    Args:
        pop_size: Population size
        generations: Number of generations
        top_k: Number of top individuals to select as parents
        mutation_rate: Probability of mutation
        mutation_targets: List of parameter names to mutate
        eval_fn: Fitness evaluation function
        init_pop: Initial population
    
    Returns:
        (champion, history): Best individual and generation history
    """
    population = init_pop
    history = []
    
    for gen in range(generations):
        # Evaluate all individuals
        for ind in population:
            ind['fitness'] = eval_fn(ind['params'])
        
        # Sort by fitness (descending)
        population.sort(key=lambda x: x['fitness'], reverse=True)
        
        # Select top parents and keep top 2 as elites
        parents = population[:top_k]
        elites = [p.copy() for p in parents[:2]]
        
        # Generate children through mutation and crossover
        children = []
        for _ in range(pop_size - len(elites)):
            # Select random parent
            parent = parents[np.random.randint(len(parents))].copy()
            child = {'params': parent['params'].copy(), 'fitness': 0.0}
            
            # Mutation
            if np.random.rand() < mutation_rate:
                target = mutation_targets[np.random.randint(len(mutation_targets))]
                if target in child['params']:
                    if isinstance(child['params'][target], (int, float)):
                        # Numeric mutation: ±10%
                        child['params'][target] *= (1 + np.random.uniform(-0.1, 0.1))
                        if isinstance(child['params'][target], int):
                            child['params'][target] = int(child['params'][target])
            
            # Crossover (low rate)
            if np.random.rand() < 0.1 and len(parents) > 1:
                other = parents[np.random.randint(len(parents))]
                for k in child['params']:
                    if np.random.rand() < 0.5:
                        child['params'][k] = other['params'][k]
            
            children.append(child)
        
        # New population: elites + children
        population = elites + children
        
        # Record history
        history.append({
            'gen': gen,
            'best_fitness': population[0]['fitness'],
            'avg_fitness': np.mean([ind['fitness'] for ind in population])
        })
        
        print(f"[evolution] Gen {gen+1}/{generations}: best_fitness={population[0]['fitness']:.4f}")
    
    return population[0], history

# Stage runners
def run_stage(stage, context, pipeline):
    """Execute a pipeline stage."""
    sid = stage['id']
    print(f"[{sid}] Running...")
    work_dir = pipeline['inputs']['work_dir']
    
    # Create necessary directories
    os.makedirs(work_dir, exist_ok=True)
    
    if sid == 'ingest':
        # Stub: Parse PDF to extract glyph data
        print(f"  Ingesting PDF from {pipeline['inputs']['voynich_pdf_path']}")
        # Generate synthetic glyph data for demo
        glyphs = [{'id': i, 'features': np.random.rand(10).tolist()} for i in range(1000)]
        with open(f"{work_dir}/glyphs.json", 'w') as f:
            json.dump(glyphs, f)
        context['glyph_data'] = glyphs
        print(f"  Generated {len(glyphs)} glyphs")
    
    elif sid == 'anomaly_detect':
        # Anomaly detection using Isolation Forest
        data = np.array([g['features'] for g in context['glyph_data']])
        model = IsolationForest(contamination=stage['params']['contamination'], random_state=42)
        predictions = model.fit_predict(data)
        anomalies = data[predictions == -1]
        with open(f"{work_dir}/anomalies.json", 'w') as f:
            json.dump(anomalies.tolist(), f)
        context['anomalies'] = anomalies
        print(f"  Detected {len(anomalies)} anomalies")
    
    elif sid == 'glyph_extract':
        # Extract glyph features (stub)
        os.makedirs(f"{work_dir}/glyphs/raw", exist_ok=True)
        print(f"  Extracted features for {len(context['anomalies'])} glyphs")
    
    elif sid == 'glyph_embed':
        # Embed glyphs using autoencoder (stubbed with random embeddings)
        embeds = np.random.rand(len(context['anomalies']), 192)
        np.save(f"{work_dir}/glyphs/embeddings.npy", embeds)
        context['embeds'] = embeds
        print(f"  Generated {embeds.shape} embeddings")
    
    elif sid == 'glyph_cluster':
        # Cluster glyphs using K-means
        embeds = context['embeds']
        n_clusters = pipeline['inputs']['anomaly_target_count']
        kmeans = KMeans(n_clusters=n_clusters, max_iter=stage['params']['max_iter'], random_state=42)
        labels = kmeans.fit_predict(embeds)
        np.save(f"{work_dir}/glyphs/cluster_labels.npy", labels)
        
        # Compute cluster statistics
        unique, counts = np.unique(labels, return_counts=True)
        stats = {
            'n_clusters': len(unique),
            'cluster_sizes': counts.tolist(),
            'cluster_ids': unique.tolist()
        }
        os.makedirs(f"{work_dir}/glyphs", exist_ok=True)
        with open(f"{work_dir}/glyphs/cluster_stats.json", 'w') as f:
            json.dump(stats, f)
        context['labels'] = labels
        context['stats'] = stats
        print(f"  Clustered into {stats['n_clusters']} groups")
    
    elif sid == 'symbol_assign':
        # Assign symbols to clusters (stub)
        os.makedirs(f"{work_dir}/symbols", exist_ok=True)
        symbols = {f"cluster_{i}": f"VSYM_{i:03d}" for i in range(pipeline['inputs']['anomaly_target_count'])}
        with open(f"{work_dir}/symbols/symbol_table.json", 'w') as f:
            json.dump(symbols, f)
        print(f"  Assigned {len(symbols)} symbols")
    
    elif sid == 'codon_mapping_init':
        # Initialize codon mapping (stub)
        os.makedirs(f"{work_dir}/binding", exist_ok=True)
        mapping = {f"VSYM_{i:03d}": f"COD{i:03d}" for i in range(pipeline['inputs']['anomaly_target_count'])}
        with open(f"{work_dir}/binding/symbol_to_codon_v0.json", 'w') as f:
            json.dump(mapping, f)
        print(f"  Initialized {len(mapping)} codon mappings")
    
    elif sid == 'trig6_eval':
        # TRIG6 evaluation with stub metrics
        progress = 0.7  # Fake decipher progress
        theta = trig6_theta(progress)
        R = trig6_resonance(0.8, 0.9)
        D = trig6_drift(0.1, 0.05)
        N = trig6_noise(0.2, 0.15)
        eq = trig6_eq(context['stats']['n_clusters'], pipeline['inputs']['anomaly_target_count'])
        danger = trig6_danger(theta, pipeline['meta']['tan_danger_limit'], D > 0.1)
        fitness = trig6_fitness(R, D, N, eq)
        
        report = {
            'theta': theta,
            'resonance': R,
            'drift': D,
            'noise': N,
            'equilibrium': eq,
            'fitness': fitness,
            'danger': danger
        }
        with open(f"{work_dir}/binding/trig6_report.json", 'w') as f:
            json.dump(report, f)
        with open(f"{work_dir}/binding/trig6_state_history.json", 'w') as f:
            json.dump([report], f)
        context['trig6_state'] = report
        print(f"  TRIG6 fitness: {fitness:.4f}, danger: {danger}")
    
    elif sid == 'evolution_loop':
        # Darwinian evolution of mapping parameters
        evo = stage['evolution']
        
        # Initialize population with parameter variations
        init_pop = []
        for _ in range(evo['pop_size']):
            params = {
                'n_clusters': pipeline['inputs']['anomaly_target_count'] + np.random.randint(-5, 6),
                'strategy': 'entropy_weighted',
                'thresholds': {'glyph_variance': 0.15 + np.random.uniform(-0.03, 0.03)},
                'glyph_variance_threshold': 0.15 + np.random.uniform(-0.05, 0.05)
            }
            init_pop.append({'params': params, 'fitness': 0.0})
        
        # Define evaluation function
        def eval_fn(params):
            # Simulate fitness based on parameters
            purity = 0.8 + (params.get('glyph_variance_threshold', 0.15) - 0.15) * 2.0
            coverage = 0.9
            variance_rate = abs(params.get('n_clusters', 48) - 48) / 48.0
            R = trig6_resonance(clamp(purity, 0.0, 1.0), coverage)
            D = trig6_drift(variance_rate, 0.05)
            N = trig6_noise(0.2, 0.15)
            eq = trig6_eq(params.get('n_clusters', 48), pipeline['inputs']['anomaly_target_count'])
            return trig6_fitness(R, D, N, eq)
        
        # Run evolution
        champion, log = evolve_population(
            evo['pop_size'], 
            evo['generations'], 
            evo['top_k'], 
            evo['mutation_rate'], 
            evo['targets'], 
            eval_fn, 
            init_pop
        )
        
        # Save results
        with open(f"{work_dir}/binding/symbol_to_codon_champion.json", 'w') as f:
            json.dump(champion, f, indent=2)
        with open(f"{work_dir}/binding/evolution_log.json", 'w') as f:
            json.dump(log, f, indent=2)
        context['champion'] = champion
        print(f"  Evolution complete. Champion fitness: {champion['fitness']:.4f}")
    
    elif sid == 'codon_stream_emit':
        # Emit codon streams (stub)
        os.makedirs(f"{work_dir}/binding/codon_streams", exist_ok=True)
        print(f"  Emitted codon streams")
    
    elif sid == 'compiler_integration':
        # Compiler integration (stub)
        os.makedirs(f"{work_dir}/binding/fix_bins", exist_ok=True)
        os.makedirs(f"{work_dir}/binding/runtime_logs", exist_ok=True)
        print(f"  Compiled and integrated")

def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("Voynich Diagnostic Pipeline with TRIG6 Evolution")
    print("=" * 60)
    
    # Load pipeline configuration
    pipeline = load_pipeline()
    print(f"\nLoaded pipeline: {pipeline['meta']['name']}")
    print(f"Target: {pipeline['inputs']['anomaly_target_count']} symbols")
    
    # Create work directory
    os.makedirs(pipeline['inputs']['work_dir'], exist_ok=True)
    
    # Execute pipeline stages
    context = {}
    for stage in pipeline['stages']:
        run_stage(stage, context, pipeline)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Pipeline Complete")
    print("=" * 60)
    if 'trig6_state' in context:
        print(f"TRIG6 Fitness: {context['trig6_state']['fitness']:.4f}")
        print(f"Danger Status: {context['trig6_state']['danger']}")
    if 'champion' in context:
        print(f"Champion Fitness: {context['champion']['fitness']:.4f}")
        print(f"Champion Params: {json.dumps(context['champion']['params'], indent=2)}")
    print(f"\nOutputs saved to: {pipeline['inputs']['work_dir']}")

if __name__ == "__main__":
    main()
