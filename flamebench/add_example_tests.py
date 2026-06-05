#!/usr/bin/env python3
"""
Example: Add test gists with varied success rates to demonstrate Guardian risk levels
"""

import json
import os

# Create a more comprehensive test suite with varying success rates
expanded_gists = [
    # High success - should be Safe
    {
        "slug": "zyb-it145-loops-for-basic",
        "gist_id": "example-gist-loops",
        "files": {
            "manifest.flame-test.json": {
                "id": "zyb-it145-loops-for-basic",
                "concept_tags": ["for-loop", "iteration"],
                "inputs": [5, 10, 3, 8, 12, 15],
                "expected_outputs": [15, 55, 6, 36, 78, 120]
            }
        }
    },
    # Medium success - should be Caution
    {
        "slug": "zyb-it145-ch4-4_2-nested-if",
        "gist_id": "example-gist-nested",
        "files": {
            "manifest.flame-test.json": {
                "id": "zyb-it145-ch4-4_2-nested-if",
                "concept_tags": ["if-else", "nested-conditions"],
                "inputs": [[10, 20], [5, 5], [30, 15], [0, 0]],
                "expected_outputs": ["max:20", "equal", "max:30", "zero"]
            }
        }
    },
    # Low success - should be Warning or Critical
    {
        "slug": "zyb-it145-ch5-5_1-recursion",
        "gist_id": "example-gist-recursion",
        "files": {
            "manifest.flame-test.json": {
                "id": "zyb-it145-ch5-5_1-recursion",
                "concept_tags": ["recursion", "functions"],
                "inputs": [5, 3, 7, 10],
                "expected_outputs": [120, 6, 5040, 3628800]
            }
        }
    },
    # Existing tests
    {
        "slug": "zyb-it145-ch3-3_2_5-even-odd",
        "gist_id": "sample-gist-id-1",
        "files": {
            "manifest.flame-test.json": {
                "id": "zyb-it145-ch3-3_2_5-even-odd",
                "concept_tags": ["if-else", "modulo"],
                "inputs": [2, 3, 10, 15],
                "expected_outputs": ["even", "odd", "even", "odd"]
            }
        }
    },
    {
        "slug": "zyb-it145-ch3-3_1-max-of-two",
        "gist_id": "sample-gist-id-2",
        "files": {
            "manifest.flame-test.json": {
                "id": "zyb-it145-ch3-3_1-max-of-two",
                "concept_tags": ["if-else", "comparison", "max"],
                "inputs": [[5, 3], [10, 20], [7, 7]],
                "expected_outputs": [5, 20, 7]
            }
        }
    },
]

# Write to flame_gists.json
gist_file = os.path.join(os.path.dirname(__file__), "flame_gists.json")
with open(gist_file, 'w', encoding='utf-8') as f:
    json.dump(expanded_gists, f, indent=2)

print(f"✓ Updated {gist_file} with {len(expanded_gists)} test gists")
print("\nTest suite includes:")
for gist in expanded_gists:
    tags = gist["files"]["manifest.flame-test.json"]["concept_tags"]
    print(f"  - {gist['slug']}: {', '.join(tags)}")
