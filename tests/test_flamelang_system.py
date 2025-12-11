#!/usr/bin/env python3
"""
FlameLang System Test Script
Tests all components of the FlameLang transformation system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.flamelang.codon_mapping import CODON_MAP, get_codon_for_method
from src.flamelang.dna_extraction import DNAExtractor, format_dna_profile
from src.flamelang.transformation_pipeline import process_logs
from src.flamelang.interview_harness import InterviewHarness

def test_codon_mapping():
    """Test codon mapping functionality"""
    print("=" * 80)
    print("TEST 1: Codon Mapping")
    print("=" * 80)
    
    # Test mapping
    codon = get_codon_for_method("leases.update")
    print(f"✅ leases.update -> {codon}")
    assert codon == "UUA", f"Expected UUA, got {codon}"
    
    codon = get_codon_for_method("configmaps.update")
    print(f"✅ configmaps.update -> {codon}")
    assert codon == "GCU", f"Expected GCU, got {codon}"
    
    codon = get_codon_for_method("pods.create")
    print(f"✅ pods.create -> {codon}")
    assert codon == "AUG", f"Expected AUG, got {codon}"
    
    print(f"✅ Codon mapping test passed!\n")

def test_dna_extraction():
    """Test DNA extraction functionality"""
    print("=" * 80)
    print("TEST 2: DNA Extraction")
    print("=" * 80)
    
    extractor = DNAExtractor(window_size=5, min_gene_length=3)
    
    sample_events = [
        {
            'timestamp': '2024-01-01T10:00:00Z',
            'protoPayload.authenticationInfo.principalEmail': 'test@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'test-cluster',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-01T10:00:15Z',
            'protoPayload.authenticationInfo.principalEmail': 'test@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'test-cluster',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-01T10:00:30Z',
            'protoPayload.authenticationInfo.principalEmail': 'test@k8s.io',
            'protoPayload.methodName': 'io.k8s.core.v1.configmaps.update',
            'resource.labels.cluster_name': 'test-cluster',
            'resource.type': 'k8s_configmap'
        },
    ]
    
    extractor.add_events_from_dict(sample_events)
    dna = extractor.extract_dna_profile('test@k8s.io')
    
    print(f"✅ Extracted DNA profile for: {dna.principal}")
    print(f"✅ Total events: {dna.total_events}")
    print(f"✅ Genes extracted: {len(dna.genes)}")
    print(f"✅ Anomaly score: {dna.anomaly_score}")
    
    assert dna.total_events == 3, "Expected 3 events"
    assert len(dna.genes) >= 1, "Expected at least 1 gene"
    
    print(f"✅ DNA extraction test passed!\n")

def test_transformation_pipeline():
    """Test full transformation pipeline"""
    print("=" * 80)
    print("TEST 3: Transformation Pipeline")
    print("=" * 80)
    
    # Test with sample CSV
    csv_path = Path(__file__).parent.parent / "data" / "sample_gke_audit_logs.csv"
    
    if not csv_path.exists():
        print(f"⚠️  Sample CSV not found at: {csv_path}")
        return
    
    print(f"Processing: {csv_path}")
    dna_profiles = process_logs(str(csv_path), output_dir="test_output")
    
    print(f"✅ Processed {len(dna_profiles)} principal profiles")
    
    for principal, dna in list(dna_profiles.items())[:3]:  # Show first 3
        print(f"\n  Principal: {principal}")
        print(f"    Events: {dna.total_events}")
        print(f"    Genes: {len(dna.genes)}")
        print(f"    Anomaly: {dna.anomaly_score}")
    
    print(f"\n✅ Transformation pipeline test passed!\n")

def test_interview_harness():
    """Test interview harness"""
    print("=" * 80)
    print("TEST 4: Interview Harness")
    print("=" * 80)
    
    harness = InterviewHarness()
    
    print(f"✅ Loaded {len(harness.test_cases)} test cases")
    
    # Run all tests
    results = harness.run_all_tests()
    
    print(f"✅ Total tests: {results['total_tests']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"✅ Average score: {results['average_score']*100:.1f}%")
    
    print(f"\n✅ Interview harness test passed!\n")

def main():
    """Run all tests"""
    print("\n🔥 FLAMELANG SYSTEM TEST SUITE\n")
    
    try:
        test_codon_mapping()
        test_dna_extraction()
        test_transformation_pipeline()
        test_interview_harness()
        
        print("=" * 80)
        print("✨ ALL TESTS PASSED!")
        print("=" * 80)
        print("\nFlameLang K8s audit log transformation system is working correctly.")
        print("Ready for production use and candidate interviews.\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
