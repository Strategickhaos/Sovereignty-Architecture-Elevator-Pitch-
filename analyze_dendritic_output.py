#!/usr/bin/env python3
"""
Analysis utility for Proto-Elamite dendritic visualization probe output
Provides insights and statistics from the mutation edge data
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List


class DendriticAnalyzer:
    """Analyzer for dendritic visualization probe output"""
    
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load JSON data from file"""
        try:
            with open(self.json_path, 'r') as f:
                self.data = json.load(f)
            print(f"✓ Loaded: {self.json_path}")
            print(f"  Total edges: {len(self.data['edges'])}")
            print()
        except FileNotFoundError:
            print(f"❌ Error: File not found: {self.json_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON: {e}")
            sys.exit(1)
    
    def analyze_color_distribution(self):
        """Analyze edge color distribution"""
        print("📊 COLOR DISTRIBUTION")
        print("=" * 60)
        
        color_counts = defaultdict(int)
        for edge in self.data['edges']:
            color_counts[edge['color']] += 1
        
        total = len(self.data['edges'])
        for color in ['green', 'yellow', 'red']:
            count = color_counts[color]
            percentage = (count / total * 100) if total > 0 else 0
            bar = '█' * int(percentage / 2)
            print(f"  {color.upper():7} | {bar} {count:3} ({percentage:5.1f}%)")
        
        print()
    
    def analyze_acceptance_rate(self):
        """Analyze mutation acceptance rates"""
        print("🎯 ACCEPTANCE RATES")
        print("=" * 60)
        
        total_accepted = sum(1 for edge in self.data['edges'] if edge['accepted'])
        total_rejected = len(self.data['edges']) - total_accepted
        total = len(self.data['edges'])
        
        accept_pct = (total_accepted / total * 100) if total > 0 else 0
        reject_pct = (total_rejected / total * 100) if total > 0 else 0
        
        print(f"  Accepted:  {total_accepted:3} ({accept_pct:5.1f}%)")
        print(f"  Rejected:  {total_rejected:3} ({reject_pct:5.1f}%)")
        print()
    
    def analyze_per_symbol(self):
        """Analyze statistics per symbol"""
        print("🔬 PER-SYMBOL ANALYSIS")
        print("=" * 60)
        
        symbol_stats = defaultdict(lambda: {
            'total': 0,
            'accepted': 0,
            'colors': defaultdict(int),
            'avg_f_delta': 0.0,
            'avg_danger_delta': 0.0
        })
        
        for edge in self.data['edges']:
            symbol = edge['symbol']
            stats = symbol_stats[symbol]
            
            stats['total'] += 1
            if edge['accepted']:
                stats['accepted'] += 1
            stats['colors'][edge['color']] += 1
            
            f_delta = edge['f_new'] - edge['f_old']
            danger_delta = edge['danger_new'] - edge['danger_old']
            
            stats['avg_f_delta'] += f_delta
            stats['avg_danger_delta'] += danger_delta
        
        for symbol in sorted(symbol_stats.keys()):
            stats = symbol_stats[symbol]
            if stats['total'] > 0:
                stats['avg_f_delta'] /= stats['total']
                stats['avg_danger_delta'] /= stats['total']
            
            accept_rate = (stats['accepted'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
            print(f"\n  {symbol}")
            print(f"    Mutations: {stats['total']}")
            print(f"    Accepted:  {stats['accepted']} ({accept_rate:.1f}%)")
            print(f"    Colors:    G={stats['colors']['green']} Y={stats['colors']['yellow']} R={stats['colors']['red']}")
            print(f"    Avg Δf:    {stats['avg_f_delta']:+.4f}")
            print(f"    Avg Δdanger: {stats['avg_danger_delta']:+.4f}")
        
        print()
    
    def analyze_fitness_landscape(self):
        """Analyze fitness landscape"""
        print("🗺️  FITNESS LANDSCAPE")
        print("=" * 60)
        
        improvements = [edge for edge in self.data['edges'] if edge['f_new'] > edge['f_old']]
        degradations = [edge for edge in self.data['edges'] if edge['f_new'] < edge['f_old']]
        neutral = [edge for edge in self.data['edges'] if edge['f_new'] == edge['f_old']]
        
        total = len(self.data['edges'])
        imp_pct = (len(improvements) / total * 100) if total > 0 else 0
        deg_pct = (len(degradations) / total * 100) if total > 0 else 0
        neu_pct = (len(neutral) / total * 100) if total > 0 else 0
        
        print(f"  Improvements:  {len(improvements):3} ({imp_pct:5.1f}%)")
        print(f"  Degradations:  {len(degradations):3} ({deg_pct:5.1f}%)")
        print(f"  Neutral:       {len(neutral):3} ({neu_pct:5.1f}%)")
        
        if improvements:
            max_improvement = max(edge['f_new'] - edge['f_old'] for edge in improvements)
            print(f"\n  Max fitness gain: {max_improvement:+.4f}")
        
        if degradations:
            max_degradation = min(edge['f_new'] - edge['f_old'] for edge in degradations)
            print(f"  Max fitness loss: {max_degradation:+.4f}")
        
        print()
    
    def analyze_danger_zones(self):
        """Analyze danger zones and safe paths"""
        print("⚠️  DANGER ANALYSIS")
        print("=" * 60)
        
        safer = [edge for edge in self.data['edges'] if edge['danger_new'] < edge['danger_old']]
        riskier = [edge for edge in self.data['edges'] if edge['danger_new'] > edge['danger_old']]
        neutral = [edge for edge in self.data['edges'] if edge['danger_new'] == edge['danger_old']]
        
        total = len(self.data['edges'])
        safer_pct = (len(safer) / total * 100) if total > 0 else 0
        riskier_pct = (len(riskier) / total * 100) if total > 0 else 0
        neutral_pct = (len(neutral) / total * 100) if total > 0 else 0
        
        print(f"  Safer paths:   {len(safer):3} ({safer_pct:5.1f}%)")
        print(f"  Riskier paths: {len(riskier):3} ({riskier_pct:5.1f}%)")
        print(f"  Neutral:       {len(neutral):3} ({neutral_pct:5.1f}%)")
        
        # High danger increases
        high_danger = [edge for edge in riskier if edge['danger_new'] > edge['danger_old'] * 1.5]
        if high_danger:
            print(f"\n  ⚠️  High danger increases (>1.5x): {len(high_danger)}")
            print(f"      These were filtered by hard rails before visualization")
        
        print()
    
    def show_top_mutations(self, n: int = 5):
        """Show top N mutations by fitness improvement"""
        print(f"🏆 TOP {n} FITNESS IMPROVEMENTS")
        print("=" * 60)
        
        sorted_edges = sorted(
            self.data['edges'],
            key=lambda e: e['f_new'] - e['f_old'],
            reverse=True
        )
        
        for i, edge in enumerate(sorted_edges[:n], 1):
            f_delta = edge['f_new'] - edge['f_old']
            print(f"\n  {i}. {edge['symbol']}")
            print(f"     {edge['old_value']} → {edge['new_value']}")
            print(f"     Δf: {f_delta:+.4f} | Δdanger: {edge['danger_new'] - edge['danger_old']:+.4f}")
            print(f"     Color: {edge['color']} | Accepted: {edge['accepted']}")
        
        print()
    
    def generate_summary(self):
        """Generate complete summary"""
        print()
        print("╔" + "═" * 58 + "╗")
        print("║  PROTO-ELAMITE DENDRITIC VISUALIZATION ANALYSIS         ║")
        print("╚" + "═" * 58 + "╝")
        print()
        
        print(f"📁 File: {self.json_path}")
        print(f"🔬 Probe type: {self.data['metadata']['probe_type']}")
        print(f"🎯 Scope: {self.data['metadata']['scope']}")
        print(f"📊 Total edges: {self.data['metadata']['total_edges']}")
        print(f"⚠️  Warning: {self.data['metadata']['warning']}")
        print()
        
        self.analyze_color_distribution()
        self.analyze_acceptance_rate()
        self.analyze_per_symbol()
        self.analyze_fitness_landscape()
        self.analyze_danger_zones()
        self.show_top_mutations()
        
        print("=" * 60)
        print("✓ Analysis complete")
        print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_dendritic_output.py <path_to_json>")
        print()
        print("Example:")
        print("  python3 analyze_dendritic_output.py neurograph/proto_elamite_pelsim1_dendrites.json")
        sys.exit(1)
    
    json_path = sys.argv[1]
    analyzer = DendriticAnalyzer(json_path)
    analyzer.generate_summary()


if __name__ == "__main__":
    main()
