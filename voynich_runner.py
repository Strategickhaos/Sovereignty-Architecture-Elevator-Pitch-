#!/usr/bin/env python3
# voynich_runner.py
# Voynich Diagnostic → TRIG6 → Evolution Loop
# Drop in same directory as voynich_diag_pipeline.yaml

import os
import json
import copy
import yaml
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

# ---- Utility ---------------------------------------------------------------

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def load_pipeline(yaml_path="voynich_diag_pipeline.yaml"):
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

# ---- TRIG6 primitives (Voynich flavor) ------------------------------------

def trig6_theta(progress: float) -> float:
    # progress in [0,1]
    return 2.0 * np.pi * clamp(progress, 0.0, 1.0)

def trig6_resonance(pattern_consistency, coverage, stability=0.0):
    return clamp(0.55 * pattern_consistency + 0.35 * coverage + 0.10 * stability, 0.0, 1.0)

def trig6_drift(variance_rate, outlier_frac):
    return clamp(0.65 * variance_rate + 0.35 * outlier_frac, 0.0, 1.0)

def trig6_noise(embed_variance, entropy_norm):
    return clamp(0.55 * embed_variance + 0.45 * entropy_norm, 0.0, 1.0)

def trig6_eq(count, target):
    return clamp(1.0 - abs(count - target) / float(target), 0.0, 1.0)

def trig6_danger(theta, tan_limit, extra_cond=False):
    return abs(np.tan(theta)) > tan_limit or extra_cond

def trig6_fitness(R, D, N, eq):
    return R * (1.0 - D) * (1.0 - N) * eq

# ---- Evolution core --------------------------------------------------------

def mutate_params(params: dict, target: str):
    """In-place mutation rule for a single param key.
    
    Args:
        params (dict): Parameter dictionary to mutate
        target (str): Parameter name to mutate. Supported values:
            - "n_clusters": Integer cluster count mutation (±4, bounds [8, inf))
            - "glyph_variance_threshold": Float threshold mutation (±0.02, bounds [0.01, 0.5])
            - "strategy": Categorical strategy selection from predefined choices
    """
    if target == "n_clusters":
        new_val = int(round(params.get("n_clusters", 48)))
        new_val += np.random.randint(-4, 5)  # -4..+4
        params["n_clusters"] = max(8, new_val)

    elif target == "glyph_variance_threshold":
        val = params.get("glyph_variance_threshold", 0.15)
        val += np.random.uniform(-0.02, 0.02)
        params["glyph_variance_threshold"] = clamp(val, 0.01, 0.5)

    elif target == "strategy":
        choices = ["entropy_weighted", "frequency_weighted", "uniform"]
        # pick anything except current when possible
        current = params.get("strategy", choices[0])
        options = [c for c in choices if c != current] or choices
        params["strategy"] = np.random.choice(options)

    # Add more branches later (e.g. thresholds) as needed.


def evolve_population(pop_size, generations, top_k, mutation_rate,
                      mutation_targets, eval_fn, init_params):
    """Evolve population using genetic algorithm with elitism.
    
    Args:
        pop_size (int): Population size (must be > 0)
        generations (int): Number of generations to evolve
        top_k (int): Number of top individuals to use as parents (must be > 0)
        mutation_rate (float): Probability of mutation [0.0, 1.0]
        mutation_targets (list[str]): List of parameter names that can be mutated
        eval_fn (callable): Fitness evaluation function. Takes params dict, returns float fitness.
        init_params (dict): Initial parameter dictionary to seed population
    
    Returns:
        tuple: (champion, history) where
            - champion: dict with 'params' and 'fitness' keys for best individual
            - history: list of dicts with 'gen' and 'best_fitness' for each generation
    """
    if top_k <= 0:
        raise ValueError(f"top_k must be positive, got {top_k}")
    if pop_size <= 0:
        raise ValueError(f"pop_size must be positive, got {pop_size}")
    population = []
    for _ in range(pop_size):
        population.append({"params": copy.deepcopy(init_params), "fitness": 0.0})

    history = []

    for gen in range(generations):
        # Evaluate
        for ind in population:
            ind["fitness"] = float(eval_fn(ind["params"]))

        population.sort(key=lambda x: x["fitness"], reverse=True)
        best = population[0]
        history.append({"gen": gen, "best_fitness": best["fitness"]})
        print(f"[evo] gen={gen:03d} best_fitness={best['fitness']:.4f}")

        # Select parents
        parents = population[:max(1, top_k)]
        elites = [copy.deepcopy(p) for p in parents[:2]]

        # Reproduce
        children = []
        while len(elites) + len(children) < pop_size:
            parent = copy.deepcopy(np.random.choice(parents))
            # mutation
            if np.random.rand() < mutation_rate:
                target = np.random.choice(mutation_targets)
                mutate_params(parent["params"], target)

            # light crossover
            if np.random.rand() < 0.10:
                other = np.random.choice(parents)
                for k in parent["params"].keys():
                    if np.random.rand() < 0.5:
                        parent["params"][k] = other["params"].get(k, parent["params"][k])

            children.append(parent)

        population = elites + children

    # final champion
    population.sort(key=lambda x: x["fitness"], reverse=True)
    return population[0], history

# ---- Pipeline stages (stubs wired to TRIG6/Evo) ---------------------------

def run_stage(stage, ctx, pipeline):
    sid = stage["id"]
    work_dir = pipeline["inputs"]["work_dir"]
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(os.path.join(work_dir, "glyphs"), exist_ok=True)
    os.makedirs(os.path.join(work_dir, "binding"), exist_ok=True)

    print(f"[stage] {sid}")

    if sid == "ingest":
        # TODO [P0, Sprint 2]: Replace with real glyph extraction from PDF
        # Expected integration: OmniCalc toolchain for PDF → image → glyph pipeline
        # For now, generate fake glyphs with simple feature vectors.
        glyphs = [{"id": i, "features": np.random.rand(10).tolist()}
                  for i in range(1200)]
        ctx["glyphs"] = glyphs
        with open(f"{work_dir}/glyphs.json", "w") as f:
            json.dump(glyphs, f)

    elif sid == "anomaly_detect":
        feats = np.array([g["features"] for g in ctx["glyphs"]])
        iso = IsolationForest(contamination=stage["params"]["contamination"],
                              random_state=pipeline["inputs"]["random_seed"])
        mask = iso.fit_predict(feats) == -1
        anomalies = feats[mask]
        ctx["anomalies"] = anomalies
        with open(f"{work_dir}/anomalies.json", "w") as f:
            json.dump(anomalies.tolist(), f)

    elif sid == "glyph_extract":
        # TODO [P0, Sprint 2]: Compute real feature vectors
        # Expected features and ranges:
        #   - shape_entropy: float [0.0, 1.0] - Shannon entropy of glyph shape
        #   - stroke_count: int [1, 20] - Number of distinct strokes
        #   - context_position: float [0.0, 1.0] - Relative position in line/page
        #   - aspect_ratio: float [0.1, 10.0] - Width/height ratio
        # For now we treat anomalies as already-featured.
        ctx["glyph_features"] = ctx["anomalies"]

    elif sid == "glyph_embed":
        # Stub: "autoencoder" = linear projection to desired dim.
        dim = stage["params"]["dim"]
        n = ctx["glyph_features"].shape[0]
        embeds = np.random.rand(n, dim)
        ctx["embeds"] = embeds
        np.save(f"{work_dir}/glyphs/embeddings.npy", embeds)

    elif sid == "glyph_cluster":
        embeds = ctx["embeds"]
        k = pipeline["inputs"]["anomaly_target_count"]
        km = KMeans(n_clusters=k,
                    max_iter=stage["params"]["max_iter"],
                    n_init=10,
                    random_state=pipeline["inputs"]["random_seed"])
        labels = km.fit_predict(embeds)
        ctx["labels"] = labels
        cluster_sizes = np.bincount(labels, minlength=k)
        stats = {"cluster_sizes": cluster_sizes.tolist()}
        ctx["cluster_stats"] = stats
        np.save(f"{work_dir}/glyphs/cluster_labels.npy", labels)
        with open(f"{work_dir}/glyphs/cluster_stats.json", "w") as f:
            json.dump(stats, f)

    elif sid == "symbol_assign":
        # simple VSYM_XXX assignment by cluster index
        k = pipeline["inputs"]["anomaly_target_count"]
        sizes = ctx["cluster_stats"]["cluster_sizes"]
        symbol_table = {}
        for idx in range(k):
            symbol_table[f"VSYM_{idx:03d}"] = {
                "cluster_id": idx,
                "size": sizes[idx]
            }
        symbol_table["VSYM_NOOP"] = {"cluster_id": -1, "size": 0}
        ctx["symbol_table"] = symbol_table
        os.makedirs(os.path.join(work_dir, "symbols"), exist_ok=True)
        with open(f"{work_dir}/symbols/symbol_table.json", "w") as f:
            json.dump(symbol_table, f, indent=2)

    elif sid == "codon_mapping_init":
        # Stub: 1-to-1 map VSYM_xxx to dummy codons from codon table
        mapping = {}
        for sym in ctx["symbol_table"].keys():
            mapping[sym] = {"codon": "NNN", "op": "NOOP"}
        ctx["mapping"] = mapping
        os.makedirs(os.path.join(work_dir, "binding"), exist_ok=True)
        with open(f"{work_dir}/binding/symbol_to_codon_v0.json", "w") as f:
            json.dump(mapping, f, indent=2)

    elif sid == "trig6_eval":
        # Example TRIG6 eval using aggregate stats
        sizes = np.array(ctx["cluster_stats"]["cluster_sizes"], dtype=float)
        coverage = float(sizes.sum()) / max(1.0, sizes.sum())  # ~1.0 here
        pattern_consistency = 0.8   # stub – from intra-cluster similarity
        variance_rate = np.var(sizes / sizes.sum()) if sizes.sum() > 0 else 0.0
        outlier_frac = 0.05         # stub – #tiny clusters / total
        embed_variance = 0.2        # stub – variance of embeddings
        entropy_norm = 0.3          # stub – normalized size entropy

        target = pipeline["inputs"]["anomaly_target_count"]
        count = target  # our cluster count

        theta = trig6_theta(progress=0.6)
        R = trig6_resonance(pattern_consistency, coverage)
        D = trig6_drift(variance_rate, outlier_frac)
        N = trig6_noise(embed_variance, entropy_norm)
        eq = trig6_eq(count, target)
        danger = trig6_danger(theta, pipeline["meta"]["tan_danger_limit"])
        fitness = trig6_fitness(R, D, N, eq)

        state = {
            "theta": theta,
            "R": R,
            "D": D,
            "N": N,
            "eq": eq,
            "danger": danger,
            "fitness": fitness,
        }
        ctx["trig6_state"] = state
        with open(f"{work_dir}/binding/trig6_report.json", "w") as f:
            json.dump(state, f, indent=2)

    elif sid == "evolution_loop":
        evo = stage["evolution"]
        targets = evo["targets"]

        init_params = {
            "n_clusters": pipeline["inputs"]["anomaly_target_count"],
            "strategy": "entropy_weighted",
            "glyph_variance_threshold": 0.15,
        }

        def eval_fn(params):
            # Here you'd re-run clustering/mapping with these params and recompute TRIG6.
            # For now, we build a shaped toy fitness landscape:
            purity = 0.80 + (0.15 - abs(params["glyph_variance_threshold"] - 0.15)) * 0.5
            coverage = 0.90
            variance_rate = 0.05 + abs(params["n_clusters"] - 48) * 0.002
            outlier_frac = 0.05
            embed_variance = 0.20
            entropy_norm = 0.30

            theta = trig6_theta(0.7)
            R = trig6_resonance(purity, coverage)
            D = trig6_drift(variance_rate, outlier_frac)
            N = trig6_noise(embed_variance, entropy_norm)
            eq = trig6_eq(params["n_clusters"], 48)
            return trig6_fitness(R, D, N, eq)

        champion, history = evolve_population(
            pop_size=evo["pop_size"],
            generations=evo["generations"],
            top_k=evo["top_k"],
            mutation_rate=evo["mutation_rate"],
            mutation_targets=targets,
            eval_fn=eval_fn,
            init_params=init_params,
        )

        with open(f"{work_dir}/binding/symbol_to_codon_champion.json", "w") as f:
            json.dump(champion, f, indent=2)
        with open(f"{work_dir}/binding/evolution_log.json", "w") as f:
            json.dump(history, f, indent=2)

        ctx["champion"] = champion

    elif sid == "codon_stream_emit":
        # Stub: turn champion mapping into .codon streams
        # Real version will take champion symbol→codon mapping and write stream files.
        streams_dir = os.path.join(work_dir, "binding", "codon_streams")
        os.makedirs(streams_dir, exist_ok=True)
        with open(os.path.join(streams_dir, "voynich_diag.codon"), "w") as f:
            f.write("// TODO: emit codon stream from champion mapping\n")

    elif sid == "compiler_integration":
        # TODO [P1, Sprint 3]: Hook FlameLang/SAGCO-OS compiler
        # Expected interface:
        #   flamelang_compile(
        #       input_dir: Path to codon_streams/,
        #       output_dir: Path for compiled artifacts,
        #       sandbox: bool = True,
        #       max_exec_time: int = 30
        #   ) -> CompilationReport
        print("[compiler] sandbox compile would run here.")
        # e.g., flamelang_compile(streams_dir, out_dir)

def main():
    pipeline = load_pipeline()
    ctx = {}
    for stage in pipeline["stages"]:
        run_stage(stage, ctx, pipeline)

    fitness = ctx.get("trig6_state", {}).get("fitness", None)
    print("\n=== Pipeline complete ===")
    print("TRIG6 fitness (initial mapping):", fitness)
    if "champion" in ctx:
        print("Champion params:", ctx["champion"]["params"])
        print("Champion fitness:", ctx["champion"]["fitness"])

if __name__ == "__main__":
    main()
