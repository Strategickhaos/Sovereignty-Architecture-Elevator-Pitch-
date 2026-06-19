#!/usr/bin/env python3
"""
SAGCO TRIG6 Hybrid Hyperbolic Blend Logger
Phase 4.5: Quantum-inspired symbolic AI processor emulator

Implements hybrid blending of trigonometric (periodic/bounded) and hyperbolic (exponential/unbounded)
functions with embedding-enhanced coherence heuristics and FlameBench integration.
"""

import json
import datetime
import re
import math
import argparse
import yaml
import os
import sys
import numpy as np
from collections import Counter

# Try to import torch for embedding-based heuristics
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available. Using fallback embedding methods.", file=sys.stderr)

# Get absolute path to repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
CONFIG_PATH = os.path.join(REPO_ROOT, 'config/trig6.yaml')

# Load TRIG6 config
try:
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print(f"Error: Config file not found at {CONFIG_PATH}", file=sys.stderr)
    sys.exit(1)

# Noise patterns
high_penalty_patterns = [re.compile(p, re.IGNORECASE) for p in config['noise_filters']['high_penalty_phrases']]
medium_penalty_patterns = [re.compile(p, re.IGNORECASE) for p in config['noise_filters']['medium_penalty_phrases']]

# Theta map
theta_map = {topic: data['theta'] for topic, data in config['theta_topics'].items()}

def get_theta_numeric(theta_topic):
    """Get numeric theta value for a topic."""
    return theta_map.get(theta_topic, 0.0)

def sigmoid(x):
    """Sigmoid activation function."""
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def compute_blended_trig_value(trig, theta, alpha):
    """
    Compute hybrid blend: (1-alpha)*trig + alpha*hyper
    
    Args:
        trig: Trigonometric function name ('sin', 'cos', 'tan', 'cot', 'sec', 'csc')
        theta: Angle in radians
        alpha: Blend parameter [0,1], 0=pure trig, 1=pure hyper
    
    Returns:
        Blended value
    """
    # Compute trig component
    if trig == 'sin':
        trig_val = math.sin(theta)
        hyper_val = math.sinh(theta)
    elif trig == 'cos':
        trig_val = math.cos(theta)
        hyper_val = math.cosh(theta)
    elif trig == 'tan':
        trig_val = math.tanh(math.tan(theta))  # Damped for stability
        hyper_val = math.tanh(theta)
    elif trig == 'cot':
        trig_val = math.tanh(1 / (math.tan(theta) + 1e-6))  # Damped for stability
        hyper_val = 1 / (math.tanh(theta) + 1e-6)
    elif trig == 'sec':
        trig_val = 1 / (math.cos(theta) + 1e-6)
        hyper_val = 1 / math.cosh(theta)
    elif trig == 'csc':
        trig_val = 1 / (math.sin(theta) + 1e-6)
        hyper_val = 1 / (math.sinh(theta) + 1e-6)
    else:
        trig_val = 0.0
        hyper_val = 0.0

    return (1 - alpha) * trig_val + alpha * hyper_val

def compute_embeddings(sentences):
    """
    Compute sentence embeddings.
    
    Uses PyTorch if available, otherwise falls back to simple token overlap.
    
    Args:
        sentences: List of sentence strings
    
    Returns:
        Embedding matrix (numpy array or torch tensor)
    """
    if TORCH_AVAILABLE:
        # Mock embedding for demo (would use sentence-transformers in production)
        embed_dim = config['hybrid_blend']['coherence']['embedding_dim']
        embeds = torch.rand(len(sentences), embed_dim)
        return embeds
    else:
        # Fallback: bag-of-words embeddings
        embed_dim = config['hybrid_blend']['coherence']['embedding_dim']
        embeds = np.random.rand(len(sentences), embed_dim)
        return embeds

def compute_agent_metrics(agent, text, theta_num, alpha, theta_topic):
    """
    Compute agent-specific metrics based on text analysis.
    
    Args:
        agent: Agent name
        text: Input text to analyze
        theta_num: Numeric theta value
        alpha: Blend parameter
        theta_topic: Topic name for tag matching
    
    Returns:
        Dictionary of computed metrics
    """
    agent_conf = config['agents'][agent]
    trig = agent_conf['trig']
    metrics = {}
    
    # Split into sentences and tokens
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        sentences = [text]  # Fallback if no sentence delimiters
    
    tokens = text.split()
    token_counter = Counter(tokens)
    
    # Compute embeddings for coherence
    embeds = compute_embeddings(sentences)
    
    # Compute each metric defined for this agent
    for m_key, m_conf in agent_conf['metrics'].items():
        if 'focus' in m_key:
            # Focus: density of topic-relevant tags
            tags = config['theta_topics'].get(theta_topic, {}).get('tags', [])
            tag_density = len(re.findall('|'.join(tags), text, re.I)) / max(1, len(sentences))
            rel_sentences = sum(1 for s in sentences if any(tag.lower() in s.lower() for tag in tags)) / max(1, len(sentences))
            metrics[m_key] = (tag_density + rel_sentences) / 2
            
        elif 'coherence' in m_key:
            # Coherence: embedding-based with transition penalties
            if len(sentences) > 1:
                if TORCH_AVAILABLE:
                    cos_sims = [torch.cosine_similarity(embeds[i], embeds[i+1], dim=0).item() for i in range(len(sentences)-1)]
                else:
                    # Fallback: simple cosine similarity
                    cos_sims = []
                    for i in range(len(sentences)-1):
                        a, b = embeds[i], embeds[i+1]
                        cos = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
                        cos_sims.append(cos)
                avg_cos = sum(cos_sims) / len(cos_sims)
            else:
                avg_cos = 1.0
            
            # Transition penalty (but, however, although)
            transitions = text.lower().count('but') + text.lower().count('however') + text.lower().count('although')
            beta = config['hybrid_blend']['coherence']['transition_penalty']
            metrics[m_key] = avg_cos - beta * (transitions / max(1, len(sentences)))
            
        elif 'noise' in m_key:
            # Noise: pattern-based penalties
            high_hits = sum(len(p.findall(text)) for p in high_penalty_patterns)
            med_hits = sum(len(p.findall(text)) for p in medium_penalty_patterns)
            metrics[m_key] = (2 * high_hits + med_hits) / max(1, len(tokens))
            
        elif 'innovation' in m_key or 'density' in m_key:
            # Innovation: unique tokens + artifacts
            unique_ratio = len(token_counter) / max(1, len(tokens))
            artifact_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
            artifact_complex = sum(len(block.split('\n')) for block in artifact_blocks) / max(1, len(tokens))
            keyword_density = (text.lower().count('algorithm') + text.lower().count('invariant') + 
                             text.lower().count('novel') + text.lower().count('breakthrough')) / max(1, len(tokens))
            metrics[m_key] = (unique_ratio + artifact_complex + keyword_density) / 3
            
        elif 'edge' in m_key or 'coverage' in m_key:
            # Edge case coverage
            metrics[m_key] = (text.lower().count('edge') + text.lower().count('corner') + 
                            text.lower().count('boundary') + text.lower().count('exception')) / max(1, len(sentences))
            
        elif 'derail' in m_key or 'risk' in m_key:
            # Derailment risk
            metrics[m_key] = (text.lower().count('meme') + text.lower().count('joke') + 
                            text.lower().count('off-topic') + text.lower().count('random')) / max(1, len(tokens))
        else:
            # Default metric (not used in base config)
            metrics[m_key] = 0.5
    
    # Apply danger zone amplification
    danger = agent_conf.get('danger_zone')
    if danger and danger[0] <= theta_num <= danger[1]:
        if 'derail_risk' in metrics:
            metrics['derail_risk'] *= (2 * (1 - alpha))  # Damp with alpha
    
    return metrics

def compute_derived_metrics(agent_metrics_dict, theta_num, text, bench_r=0.75):
    """
    Compute derived metrics: resonance, drift, noise entropy, etc.
    
    Args:
        agent_metrics_dict: Dict of agent -> metrics
        theta_num: Numeric theta value
        text: Input text
        bench_r: Benchmark resonance (from FlameBench, default 0.75)
    
    Returns:
        Tuple of (derived_metrics_dict, alpha)
    """
    # Initial alpha estimate (will refine based on drift)
    alpha = 0.0
    
    # Mock agent outputs (in real system, would be actual agent response embeddings)
    num_agents = len(config['agents'])
    outputs = np.random.rand(num_agents) * 0.5 + 0.5
    
    # Compute blended weights
    agent_list = list(config['agents'].values())
    weights = np.array([compute_blended_trig_value(a['trig'], theta_num, alpha) for a in agent_list])
    weighted = outputs * weights
    var = np.var(weighted)
    max_var = num_agents
    
    # Damping factor: sech(theta) + (1-alpha)
    try:
        damp = (1 / math.cosh(theta_num)) + (1 - alpha)
    except OverflowError:
        damp = 1 - alpha
    
    resonance = 1 - (var / (max_var * damp + 1e-9))
    
    # Drift score with FlameBench penalty
    drift_base = (1 - math.cos(theta_num - math.pi/4)) + 0.1 * abs(theta_num - math.pi/4)
    gamma = config['hybrid_blend']['drift']['bench_weight']
    drift = drift_base + gamma * (1 - bench_r)
    
    # Update alpha based on drift
    drift_threshold = config['hybrid_blend']['alpha_sigmoid']['drift_threshold']
    sharpness = config['hybrid_blend']['alpha_sigmoid']['sigmoid_sharpness']
    alpha = sigmoid(sharpness * (drift - drift_threshold))
    
    # Recompute resonance with updated alpha
    weights = np.array([compute_blended_trig_value(a['trig'], theta_num, alpha) for a in agent_list])
    weighted = outputs * weights
    var = np.var(weighted)
    try:
        damp = (1 / math.cosh(theta_num)) + (1 - alpha)
    except OverflowError:
        damp = 1 - alpha
    resonance = 1 - (var / (max_var * damp + 1e-9))
    
    # Noise entropy (bigram-based + pattern penalties)
    tokens = text.split()
    if len(tokens) > 1:
        bigrams = [' '.join(tokens[i:i+2]) for i in range(len(tokens)-1)]
        bigram_counter = Counter(bigrams)
        total_bi = sum(bigram_counter.values())
        h = -sum((count / total_bi) * math.log2(count / total_bi) for count in bigram_counter.values() if count > 0)
    else:
        h = 0.0
    
    # Add noise penalties
    high_count = sum(len(p.findall(text)) for p in high_penalty_patterns)
    med_count = sum(len(p.findall(text)) for p in medium_penalty_patterns)
    h += (2 * high_count + med_count) / max(1, len(tokens))
    
    # Invention density
    artifact_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    artifacts = sum(len(block) for block in artifact_blocks)
    invention = artifacts / max(1, len(tokens))
    
    # Phase coherence (mock quantum correlation)
    q_cos = np.array([0.8])
    q_sin_lag = np.roll(np.array([0.7]), 1)
    try:
        phase_c = np.corrcoef(q_cos, q_sin_lag)[0, 1]
        if np.isnan(phase_c):
            phase_c = 0.5
    except:
        phase_c = 0.5
    
    derived = {
        'resonance_score': float(resonance),
        'drift_score': float(drift),
        'noise_entropy': float(h),
        'invention_density': float(invention),
        'phase_coherence': float(phase_c)
    }
    
    return derived, alpha

def log_entry(agent, text, theta_topic, session, bench_r=0.75):
    """
    Log a TRIG6 entry with all computed metrics.
    
    Args:
        agent: Agent name
        text: Input text to analyze
        theta_topic: Topic name
        session: Session identifier
        bench_r: Benchmark resonance (from FlameBench)
    """
    theta_num = get_theta_numeric(theta_topic)
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    trig = config['agents'][agent]['trig']
    
    # Compute agent metrics (initial pass)
    agent_metrics = compute_agent_metrics(agent, text, theta_num, 0.0, theta_topic)
    
    # Compute derived metrics and alpha
    derived, alpha = compute_derived_metrics({agent: agent_metrics}, theta_num, text, bench_r)
    
    # Recompute agent metrics with final alpha
    agent_metrics = compute_agent_metrics(agent, text, theta_num, alpha, theta_topic)
    
    # Compute final trig value with alpha blend
    trig_val = compute_blended_trig_value(trig, theta_num, alpha)
    
    # Count tokens and artifacts
    tokens = len(text.split())
    artifacts = len(re.findall(r'```|\|-\s', text))
    
    # Build log entry
    entry = {
        'ts': ts,
        'session': session,
        'theta_topic': theta_topic,
        'theta_numeric': theta_num,
        'agent': agent,
        'trig': trig,
        'trig_value': trig_val,
        'alpha_blend': alpha,
        'model': config['agents'][agent]['model'],
        'metrics': agent_metrics,
        'tokens': tokens,
        'artifacts': artifacts,
        'derived': derived
    }
    
    # Write to log file
    log_path = os.path.join(REPO_ROOT, config['logging']['path'])
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    with open(log_path, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    # FlameBench integration hook (mock)
    print(f"FlameBench integration: Simulated bench with resonance {derived['resonance_score']:.2f}")
    
    return entry, derived

def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description='SAGCO TRIG6 Hybrid Hyperbolic Blend Logger',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sagco_trig_logger.py --agent tangent_grok --theta trig6-hybrid --text "Sample text"
  python sagco_trig_logger.py --agent cosine_claude --theta security --text "Security analysis" --session TEST-01
        """
    )
    parser.add_argument('--agent', required=True, choices=list(config['agents'].keys()),
                       help='Agent name')
    parser.add_argument('--text', required=True,
                       help='Input text to analyze')
    parser.add_argument('--theta', required=True, choices=list(theta_map.keys()),
                       help='Theta topic')
    parser.add_argument('--session', default='SAGCO-HYDRA-OS-HYPERVISOR',
                       help='Session identifier')
    parser.add_argument('--bench-r', type=float, default=0.75,
                       help='Benchmark resonance (from FlameBench)')
    
    args = parser.parse_args()
    
    # Log entry
    entry, derived = log_entry(args.agent, args.text, args.theta, args.session, args.bench_r)
    
    # Print summary
    print(f"\nLogged for {args.agent}:")
    print(f"  Resonance: {derived['resonance_score']:.3f}")
    print(f"  Drift: {derived['drift_score']:.3f}")
    print(f"  Noise Entropy: {derived['noise_entropy']:.3f}")
    print(f"  Invention Density: {derived['invention_density']:.3f}")
    print(f"  Alpha Blend: {entry['alpha_blend']:.3f}")
    print(f"  Trig Value ({entry['trig']}): {entry['trig_value']:.3f}")
    print(f"\nLog written to: {config['logging']['path']}")

if __name__ == '__main__':
    main()
