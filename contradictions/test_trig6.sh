#!/bin/bash
# Test script for TRIG6 Contradiction Detector

echo "🧪 TRIG6 Contradiction Detector Test Suite"
echo "================================================"
echo ""

# Test 1: List all triggers
echo "Test 1: Listing all trigger words"
echo "-----------------------------------"
python3 trig6_detector.py --list
echo ""

# Test 2: High-trigger text (should be FLIP LIKELY)
echo "Test 2: High-trigger text analysis"
echo "-----------------------------------"
echo "Input: 'The legion member council uses baby bonds'"
python3 trig6_detector.py "The legion member council uses baby bonds"
echo ""

# Test 3: Low-trigger text (should be SAFE or borderline)
echo "Test 3: Low-trigger text analysis"
echo "-----------------------------------"
echo "Input: 'The signal shows alignment with mode'"
python3 trig6_detector.py "The signal shows alignment with mode"
echo ""

# Test 4: No triggers (should be SAFE)
echo "Test 4: No-trigger text analysis"
echo "-----------------------------------"
echo "Input: 'The system processes data efficiently'"
python3 trig6_detector.py "The system processes data efficiently"
echo ""

# Test 5: Python API test
echo "Test 5: Python API functionality"
echo "-----------------------------------"
python3 << 'PYEOF'
from trig6_detector import TRIG6Detector, predict_flip

print("Testing simple predict_flip function:")
prob, status = predict_flip("council legion baby heart love")
print(f"  Probability: {prob:.3f}")
print(f"  Status: {status}")
print("")

print("Testing TRIG6Detector class:")
detector = TRIG6Detector()
result = detector.analyze_text("The baby shows love in heart mode")
print(f"  Probability: {result['probability']:.3f}")
print(f"  Status: {result['status']}")
print(f"  Triggers found: {list(result['triggers_found'].keys())}")
print(f"  Total tokens: {result['total_tokens']}")
print("")

print("Testing safer text generation:")
original = "The legion member uses baby heart"
safer, changes = detector.suggest_replacement(original)
print(f"  Original: {original}")
print(f"  Safer: {safer}")
print(f"  Changes made: {len(changes)}")
PYEOF
echo ""

# Test 6: YAML validation
echo "Test 6: YAML file validation"
echo "-----------------------------------"
python3 << 'PYEOF'
import yaml

with open('gpt_contradiction_analysis.yaml', 'r') as f:
    data = yaml.safe_load(f)

print(f"✅ YAML is valid and parseable")
print(f"  API Version: {data['apiVersion']}")
print(f"  Kind: {data['kind']}")
print(f"  Analysis Name: {data['metadata']['name']}")
print(f"  Method: {data['metadata']['method']}")
print(f"  Total ranked triggers: {len(data['spec']['ranked_triggers'])}")
print(f"  Total contradictions: {len(data['spec']['contradictions'])}")
print(f"  Highest trigger: {data['spec']['ranked_triggers'][0]['word']} (P={data['spec']['ranked_triggers'][0]['P']})")
PYEOF
echo ""

echo "================================================"
echo "✅ All tests completed!"
echo "================================================"
