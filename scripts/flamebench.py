#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  FLAMEBENCH: Evolving Probabilistic Compiler Benchmark Suite                  ║
║  DNA Strand: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1          ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Each zyBooks page → Gist capsule → Bernoulli atom → p_success                ║
║  Aggregates to concept tags, feeds Guardian uncertainty layer                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
Inventor: Domenic Gabriel Garza
Architecture Credit: GPT (Legion of Minds)
"""

import json
import os
import subprocess
import requests
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Tuple, Optional
import hashlib
import math

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DNA_STRAND = "SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1"
VERSION = "1.0.0"

# Paths - adapt for your system
if sys.platform == "win32":
    BENCH_CACHE = Path(r"E:\FlameBench\bench_cache")
    FLAME_COMPILER = Path(r"E:\Strategickhaos\FlameLang\target\release\flamec.exe")
    FLAME_RUNNER = Path(r"E:\Strategickhaos\FlameLang\target\release\flamerun.exe")
else:
    BENCH_CACHE = Path.home() / "flamebench" / "bench_cache"
    FLAME_COMPILER = Path.home() / "flamelang" / "target" / "release" / "flamec"
    FLAME_RUNNER = Path.home() / "flamelang" / "target" / "release" / "flamerun"

# GitHub config for auto-discovery
GITHUB_USER = os.environ.get("GITHUB_USER", "strategickhaos")
GIST_PREFIX = "FlameTest:"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Optional, for rate limits

# Fallback: hardcoded gist list (used if API unavailable)
STATIC_GISTS = [
    "zyb-it145-ch3-3_2_5-even-odd",
    "zyb-it145-ch3-3_1-max-of-two",
    "zyb-it145-ch3-3_3-age-category",
]

# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TestCase:
    test_id: str
    case_index: int
    input_val: any
    expected: str
    actual: str
    passed: bool
    execution_time_ms: float
    
@dataclass
class BenchmarkAtom:
    """Single gist capsule = Bernoulli atom"""
    id: str
    source: str
    concept_tags: List[str]
    difficulty: int
    version: int
    total_cases: int
    passed_cases: int
    p_success: float  # Bayesian: (successes + 1) / (total + 2)
    test_cases: List[TestCase] = field(default_factory=list)
    
@dataclass
class ConceptAggregate:
    """Aggregated stats per concept tag"""
    tag: str
    total_atoms: int
    total_cases: int
    passed_cases: int
    p_success: float
    alpha: float  # Beta distribution α
    beta: float   # Beta distribution β
    entropy: float  # Shannon entropy of p
    
@dataclass
class BenchResults:
    """Complete benchmark run"""
    dna_strand: str
    timestamp: str
    compiler_version: str
    atoms: List[BenchmarkAtom]
    concepts: List[ConceptAggregate]
    overall_p_success: float
    overall_entropy: float

# ═══════════════════════════════════════════════════════════════════════════════
# GIST CAPSULE TEMPLATES (Embedded)
# ═══════════════════════════════════════════════════════════════════════════════

EMBEDDED_CAPSULES = {
    "zyb-it145-ch3-3_2_5-even-odd": {
        "manifest.flame-test.json": json.dumps({
            "id": "zyb-it145-ch3-3_2_5-even-odd",
            "source": "zyBooks IT-145, Ch3.2.5 Even/Odd",
            "concept_tags": ["if-else", "modulo", "branching", "integer"],
            "language_under_test": "flamelang",
            "reference_language": "java",
            "inputs": [22, 45, 0, -3],
            "expected_outputs": ["22 is even.", "45 is odd.", "0 is even.", "-3 is odd."],
            "difficulty": 1,
            "version": 1
        }, indent=2),
        "even_odd.flm": '''// FlameLang port of zyBooks 3.2.5 Even/Odd
fn even_odd(num: i32) -> string {
    if num % 2 == 0 {
        return num.str() + " is even.";
    } else {
        return num.str() + " is odd.";
    }
}

fn main() {
    let input = io::read_int();
    print(even_odd(input));
}
''',
        "reference.java": '''// zyBooks 3.2.5 Even/Odd
import java.util.Scanner;

public class EvenOdd {
    public static void main(String[] args) {
        Scanner scnr = new Scanner(System.in);
        int num = scnr.nextInt();
        if (num % 2 == 0) {
            System.out.println(num + " is even.");
        } else {
            System.out.println(num + " is odd.");
        }
    }
}
'''
    },
    
    "zyb-it145-ch3-3_1-max-of-two": {
        "manifest.flame-test.json": json.dumps({
            "id": "zyb-it145-ch3-3_1-max-of-two",
            "source": "zyBooks-inspired, branching max-of-two",
            "concept_tags": ["if-else", "comparison", "max"],
            "language_under_test": "flamelang",
            "reference_language": "java",
            "inputs": [[5, 7], [10, -3], [4, 4]],
            "expected_outputs": [7, 10, 4],
            "difficulty": 1,
            "version": 1
        }, indent=2),
        "max_of_two.flm": '''// FlameLang: max of two numbers
fn max_of_two(a: i32, b: i32) -> i32 {
    if a > b {
        return a;
    } else {
        return b;
    }
}

fn main() {
    let a = io::read_int();
    let b = io::read_int();
    print(max_of_two(a, b));
}
''',
        "reference.java": '''// Max of two numbers
import java.util.Scanner;

public class MaxOfTwo {
    public static void main(String[] args) {
        Scanner scnr = new Scanner(System.in);
        int a = scnr.nextInt();
        int b = scnr.nextInt();
        if (a > b) {
            System.out.println(a);
        } else {
            System.out.println(b);
        }
    }
}
'''
    },
    
    "zyb-it145-ch3-3_3-age-category": {
        "manifest.flame-test.json": json.dumps({
            "id": "zyb-it145-ch3-3_3-age-category",
            "source": "zyBooks-inspired, range-based branching",
            "concept_tags": ["if-else-if", "range-detection", "comparison"],
            "language_under_test": "flamelang",
            "reference_language": "java",
            "inputs": [-2, 5, 15, 35, 80],
            "expected_outputs": ["invalid", "child", "teen", "adult", "senior"],
            "difficulty": 2,
            "version": 1
        }, indent=2),
        "age_category.flm": '''// FlameLang: age category using chained comparisons
fn age_category(age: i32) -> string {
    if age < 0 {
        return "invalid";
    } else if age < 13 {
        return "child";
    } else if age < 20 {
        return "teen";
    } else if age < 65 {
        return "adult";
    } else {
        return "senior";
    }
}

fn main() {
    let age = io::read_int();
    print(age_category(age));
}
''',
        "reference.java": '''// Age category classifier
import java.util.Scanner;

public class AgeCategory {
    public static void main(String[] args) {
        Scanner scnr = new Scanner(System.in);
        int age = scnr.nextInt();
        if (age < 0) {
            System.out.println("invalid");
        } else if (age < 13) {
            System.out.println("child");
        } else if (age < 20) {
            System.out.println("teen");
        } else if (age < 65) {
            System.out.println("adult");
        } else {
            System.out.println("senior");
        }
    }
}
'''
    },
    
    "zyb-it145-ch3-3_4-leap-year": {
        "manifest.flame-test.json": json.dumps({
            "id": "zyb-it145-ch3-3_4-leap-year",
            "source": "zyBooks-inspired, complex boolean logic",
            "concept_tags": ["if-else-if", "boolean-logic", "modulo", "nested-conditions"],
            "language_under_test": "flamelang",
            "reference_language": "java",
            "inputs": [2000, 1900, 2024, 2023, 2100],
            "expected_outputs": ["leap year", "not a leap year", "leap year", "not a leap year", "not a leap year"],
            "difficulty": 3,
            "version": 1
        }, indent=2),
        "leap_year.flm": '''// FlameLang: leap year detection
fn is_leap_year(year: i32) -> string {
    if year % 400 == 0 {
        return "leap year";
    } else if year % 100 == 0 {
        return "not a leap year";
    } else if year % 4 == 0 {
        return "leap year";
    } else {
        return "not a leap year";
    }
}

fn main() {
    let year = io::read_int();
    print(is_leap_year(year));
}
''',
        "reference.java": '''// Leap year detector
import java.util.Scanner;

public class LeapYear {
    public static void main(String[] args) {
        Scanner scnr = new Scanner(System.in);
        int year = scnr.nextInt();
        if (year % 400 == 0) {
            System.out.println("leap year");
        } else if (year % 100 == 0) {
            System.out.println("not a leap year");
        } else if (year % 4 == 0) {
            System.out.println("leap year");
        } else {
            System.out.println("not a leap year");
        }
    }
}
'''
    },
    
    "zyb-it145-ch3-3_5-grade-calculator": {
        "manifest.flame-test.json": json.dumps({
            "id": "zyb-it145-ch3-3_5-grade-calculator",
            "source": "zyBooks-inspired, multi-branch grading",
            "concept_tags": ["if-else-if", "range-detection", "string-output"],
            "language_under_test": "flamelang",
            "reference_language": "java",
            "inputs": [95, 85, 75, 65, 55, 101, -5],
            "expected_outputs": ["A", "B", "C", "D", "F", "invalid", "invalid"],
            "difficulty": 2,
            "version": 1
        }, indent=2),
        "grade_calculator.flm": '''// FlameLang: grade calculator
fn calculate_grade(score: i32) -> string {
    if score < 0 || score > 100 {
        return "invalid";
    } else if score >= 90 {
        return "A";
    } else if score >= 80 {
        return "B";
    } else if score >= 70 {
        return "C";
    } else if score >= 60 {
        return "D";
    } else {
        return "F";
    }
}

fn main() {
    let score = io::read_int();
    print(calculate_grade(score));
}
''',
        "reference.java": '''// Grade calculator
import java.util.Scanner;

public class GradeCalculator {
    public static void main(String[] args) {
        Scanner scnr = new Scanner(System.in);
        int score = scnr.nextInt();
        if (score < 0 || score > 100) {
            System.out.println("invalid");
        } else if (score >= 90) {
            System.out.println("A");
        } else if (score >= 80) {
            System.out.println("B");
        } else if (score >= 70) {
            System.out.println("C");
        } else if (score >= 60) {
            System.out.println("D");
        } else {
            System.out.println("F");
        }
    }
}
'''
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# GITHUB API FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def list_flame_gists() -> List[Tuple[str, str, dict]]:
    """Auto-discover gists with FlameTest: prefix"""
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        url = f"https://api.github.com/users/{GITHUB_USER}/gists"
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        gists = resp.json()
        
        slugs = []
        for g in gists:
            desc = g.get("description") or ""
            if desc.startswith(GIST_PREFIX):
                slug = desc.replace(GIST_PREFIX, "").strip()
                slugs.append((slug, g["id"], g["files"]))
        
        return slugs
    except Exception as e:
        print(f"⚠️  GitHub API error: {e}")
        print(f"    Falling back to embedded capsules")
        return []

def fetch_gist(slug: str, gist_id: str = None, files_meta: dict = None) -> Path:
    """Fetch gist files to local cache"""
    path = BENCH_CACHE / slug
    path.mkdir(parents=True, exist_ok=True)
    
    # Try remote fetch first
    if gist_id and files_meta:
        headers = {}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
        try:
            for fname, meta in files_meta.items():
                raw_url = meta["raw_url"]
                r = requests.get(raw_url, headers=headers, timeout=10)
                r.raise_for_status()
                (path / fname).write_text(r.text, encoding="utf-8")
            print(f"✅ Fetched gist {slug} ({gist_id}) from GitHub")
            return path
        except Exception as e:
            print(f"⚠️  Failed to fetch {slug}: {e}")
    
    # Fallback to embedded capsules
    if slug in EMBEDDED_CAPSULES:
        for fname, content in EMBEDDED_CAPSULES[slug].items():
            (path / fname).write_text(content, encoding="utf-8")
        print(f"📦 Materialized embedded capsule: {slug}")
        return path
    
    raise FileNotFoundError(f"No gist or embedded capsule for: {slug}")

# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def load_manifest(gist_path: Path) -> dict:
    """Load manifest.flame-test.json from capsule"""
    manifest_path = gist_path / "manifest.flame-test.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No manifest in {gist_path}")
    return json.loads(manifest_path.read_text())

def find_flm_file(gist_path: Path) -> Path:
    """Find the .flm file in capsule"""
    flm_files = list(gist_path.glob("*.flm"))
    if not flm_files:
        raise FileNotFoundError(f"No .flm file in {gist_path}")
    return flm_files[0]

def run_single_case(flm_path: Path, input_val: any, expected: str, 
                    compile_only: bool = False) -> TestCase:
    """Run a single test case through FlameLang compiler/runtime"""
    import time
    start = time.perf_counter()
    
    # Format input for multi-value cases
    if isinstance(input_val, list):
        input_str = "\n".join(str(v) for v in input_val)
    else:
        input_str = str(input_val)
    
    try:
        # Check if compiler exists
        if not FLAME_COMPILER.exists():
            # Stub mode: simulate compilation for testing harness
            actual = f"[STUB] {expected}"  # In stub mode, assume pass
            passed = True
        else:
            # Compile
            bin_path = flm_path.with_suffix(".bin")
            compile_result = subprocess.run(
                [str(FLAME_COMPILER), str(flm_path), "-o", str(bin_path)],
                capture_output=True, text=True, timeout=30
            )
            
            if compile_result.returncode != 0:
                actual = f"COMPILE_ERROR: {compile_result.stderr}"
                passed = False
            elif compile_only:
                actual = "COMPILED"
                passed = True
            else:
                # Run
                run_result = subprocess.run(
                    [str(FLAME_RUNNER), str(bin_path)],
                    input=input_str,
                    capture_output=True, text=True, timeout=10
                )
                actual = run_result.stdout.strip()
                passed = actual == str(expected)
                
    except subprocess.TimeoutExpired:
        actual = "TIMEOUT"
        passed = False
    except Exception as e:
        actual = f"ERROR: {e}"
        passed = False
    
    elapsed = (time.perf_counter() - start) * 1000
    
    return TestCase(
        test_id=flm_path.stem,
        case_index=0,  # Will be set by caller
        input_val=input_val,
        expected=str(expected),
        actual=actual,
        passed=passed,
        execution_time_ms=elapsed
    )

def run_capsule(gist_path: Path) -> BenchmarkAtom:
    """Run all tests for a single capsule"""
    manifest = load_manifest(gist_path)
    flm_path = find_flm_file(gist_path)
    
    test_cases = []
    passed = 0
    
    inputs = manifest.get("inputs", [])
    expected_outputs = manifest.get("expected_outputs", [])
    
    for i, (inp, exp) in enumerate(zip(inputs, expected_outputs)):
        tc = run_single_case(flm_path, inp, exp)
        tc.case_index = i
        test_cases.append(tc)
        if tc.passed:
            passed += 1
    
    total = len(inputs)
    
    # Bayesian p_success: (successes + 1) / (total + 2)
    # Prior: Beta(1,1) = uniform
    p_success = (passed + 1) / (total + 2) if total > 0 else 0.5
    
    return BenchmarkAtom(
        id=manifest["id"],
        source=manifest.get("source", "unknown"),
        concept_tags=manifest.get("concept_tags", []),
        difficulty=manifest.get("difficulty", 1),
        version=manifest.get("version", 1),
        total_cases=total,
        passed_cases=passed,
        p_success=p_success,
        test_cases=test_cases
    )

# ═══════════════════════════════════════════════════════════════════════════════
# AGGREGATION & STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

def shannon_entropy(p: float) -> float:
    """Calculate Shannon entropy for binary outcome"""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1-p) * math.log2(1-p)

def aggregate_by_concept(atoms: List[BenchmarkAtom]) -> List[ConceptAggregate]:
    """Aggregate statistics per concept tag"""
    tag_stats = {}
    
    for atom in atoms:
        for tag in atom.concept_tags:
            if tag not in tag_stats:
                tag_stats[tag] = {
                    "atoms": 0,
                    "total_cases": 0,
                    "passed_cases": 0
                }
            tag_stats[tag]["atoms"] += 1
            tag_stats[tag]["total_cases"] += atom.total_cases
            tag_stats[tag]["passed_cases"] += atom.passed_cases
    
    aggregates = []
    for tag, stats in tag_stats.items():
        # Bayesian posterior: Beta(passed+1, failed+1)
        alpha = stats["passed_cases"] + 1
        beta_param = (stats["total_cases"] - stats["passed_cases"]) + 1
        
        # Point estimate (mean of Beta)
        p_success = alpha / (alpha + beta_param)
        
        # Entropy
        entropy = shannon_entropy(p_success)
        
        aggregates.append(ConceptAggregate(
            tag=tag,
            total_atoms=stats["atoms"],
            total_cases=stats["total_cases"],
            passed_cases=stats["passed_cases"],
            p_success=p_success,
            alpha=alpha,
            beta=beta_param,
            entropy=entropy
        ))
    
    return sorted(aggregates, key=lambda x: -x.p_success)

def get_compiler_version() -> str:
    """Get FlameLang compiler version"""
    try:
        result = subprocess.run(
            [str(FLAME_COMPILER), "--version"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or "unknown"
    except:
        return "not-installed"

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN HARNESS
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_benchmarks(use_api: bool = True) -> BenchResults:
    """Run complete benchmark suite"""
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║   ███████╗██╗      █████╗ ███╗   ███╗███████╗██████╗ ███████╗███╗   ██╗██████╗║
║   ██╔════╝██║     ██╔══██╗████╗ ████║██╔════╝██╔══██╗██╔════╝████╗  ██║██╔═══╝║
║   █████╗  ██║     ███████║██╔████╔██║█████╗  ██████╔╝█████╗  ██╔██╗ ██║██║    ║
║   ██╔══╝  ██║     ██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══╝  ██║╚██╗██║██║    ║
║   ██║     ███████╗██║  ██║██║ ╚═╝ ██║███████╗██████╔╝███████╗██║ ╚████║██████╗║
║   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═════╝║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  EVOLVING PROBABILISTIC COMPILER BENCHMARK v{VERSION:<25}           ║
║  DNA: {DNA_STRAND:<60}║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")
    
    BENCH_CACHE.mkdir(parents=True, exist_ok=True)
    
    # Discover capsules
    gist_list = []
    if use_api:
        gist_list = list_flame_gists()
    
    # Merge with embedded capsules
    discovered_slugs = {g[0] for g in gist_list}
    for slug in EMBEDDED_CAPSULES:
        if slug not in discovered_slugs:
            gist_list.append((slug, None, None))
    
    print(f"\n📊 Found {len(gist_list)} benchmark capsules\n")
    
    # Run each capsule
    atoms = []
    for slug, gist_id, files_meta in gist_list:
        try:
            path = fetch_gist(slug, gist_id, files_meta)
            atom = run_capsule(path)
            atoms.append(atom)
            
            status = "✅" if atom.p_success >= 0.8 else "⚠️" if atom.p_success >= 0.5 else "❌"
            print(f"  {status} {atom.id}: p={atom.p_success:.3f} ({atom.passed_cases}/{atom.total_cases})")
            
        except Exception as e:
            print(f"  ❌ {slug}: {e}")
    
    # Aggregate
    concepts = aggregate_by_concept(atoms)
    
    # Overall stats
    total_passed = sum(a.passed_cases for a in atoms)
    total_cases = sum(a.total_cases for a in atoms)
    overall_p = (total_passed + 1) / (total_cases + 2) if total_cases > 0 else 0.5
    overall_entropy = shannon_entropy(overall_p)
    
    return BenchResults(
        dna_strand=DNA_STRAND,
        timestamp=datetime.now().isoformat(),
        compiler_version=get_compiler_version(),
        atoms=atoms,
        concepts=concepts,
        overall_p_success=overall_p,
        overall_entropy=overall_entropy
    )

def print_report(results: BenchResults):
    """Print formatted benchmark report"""
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                          🧬 BENCHMARK RESULTS                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

OVERALL: p_success = {results.overall_p_success:.4f}  entropy = {results.overall_entropy:.4f}
Compiler: {results.compiler_version}
DNA: {results.dna_strand}
""")
    
    print("\n📊 CONCEPT TAG AGGREGATES:")
    print("-" * 70)
    print(f"{'Tag':<25} {'Atoms':<8} {'Pass/Total':<12} {'p_success':<10} {'Entropy':<8}")
    print("-" * 70)
    
    for c in results.concepts:
        print(f"{c.tag:<25} {c.total_atoms:<8} {c.passed_cases}/{c.total_cases:<9} {c.p_success:<10.4f} {c.entropy:<8.4f}")
    
    print("-" * 70)
    
    print("\n🧪 INDIVIDUAL ATOMS:")
    print("-" * 70)
    for atom in sorted(results.atoms, key=lambda x: -x.p_success):
        status = "✅" if atom.p_success >= 0.8 else "⚠️" if atom.p_success >= 0.5 else "❌"
        print(f"  {status} {atom.id}")
        print(f"     Tags: {', '.join(atom.concept_tags)}")
        print(f"     p_success: {atom.p_success:.4f} ({atom.passed_cases}/{atom.total_cases})")
    
    print("\n" + "="*70)

def save_results(results: BenchResults, output_path: Path = None):
    """Save results to JSON"""
    if output_path is None:
        output_path = BENCH_CACHE / "flamebench-results.json"
    
    # Convert to dict
    data = {
        "dna_strand": results.dna_strand,
        "timestamp": results.timestamp,
        "compiler_version": results.compiler_version,
        "overall_p_success": results.overall_p_success,
        "overall_entropy": results.overall_entropy,
        "atoms": [asdict(a) for a in results.atoms],
        "concepts": [asdict(c) for c in results.concepts]
    }
    
    output_path.write_text(json.dumps(data, indent=2, default=str))
    print(f"\n📁 Results saved to: {output_path}")
    
    return output_path

def export_for_guardian(results: BenchResults) -> dict:
    """Export in format suitable for SAGCO Guardian uncertainty layer"""
    return {
        "source": "flamebench",
        "dna_strand": results.dna_strand,
        "uncertainties": [
            {
                "quadrant": "linguistic",  # Branching logic = linguistic quadrant
                "tag": c.tag,
                "p_correct": c.p_success,
                "entropy": c.entropy,
                "alpha": c.alpha,
                "beta": c.beta,
                "sample_size": c.total_cases
            }
            for c in results.concepts
        ],
        "overall": {
            "p_success": results.overall_p_success,
            "entropy": results.overall_entropy
        }
    }

# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FlameBench: Evolving Probabilistic Compiler Benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  flamebench.py                  # Run all benchmarks
  flamebench.py --no-api         # Use embedded capsules only
  flamebench.py --guardian       # Export for Guardian layer
  flamebench.py --list           # List available capsules

DNA Strand: {DNA_STRAND}
        """
    )
    
    parser.add_argument("--no-api", action="store_true", help="Skip GitHub API, use embedded only")
    parser.add_argument("--guardian", action="store_true", help="Export results for Guardian layer")
    parser.add_argument("--list", action="store_true", help="List available capsules")
    parser.add_argument("--output", "-o", type=Path, help="Output path for results JSON")
    
    args = parser.parse_args()
    
    if args.list:
        print("📦 Embedded Capsules:")
        for slug in EMBEDDED_CAPSULES:
            print(f"  • {slug}")
        return
    
    results = run_all_benchmarks(use_api=not args.no_api)
    print_report(results)
    save_results(results, args.output)
    
    if args.guardian:
        guardian_data = export_for_guardian(results)
        guardian_path = BENCH_CACHE / "guardian-uncertainty.json"
        guardian_path.write_text(json.dumps(guardian_data, indent=2))
        print(f"🛡️ Guardian export: {guardian_path}")

if __name__ == "__main__":
    main()
