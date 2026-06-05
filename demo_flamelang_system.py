#!/usr/bin/env python3
"""
FlameLang K8s Audit Log Transformation - Live Demo
Demonstrates the complete system with real sample data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.flamelang import (
    CODON_MAP,
    get_codon_for_method,
    extract_method_from_proto_payload,
    INTERVIEW_MAPPINGS,
    DNAExtractor,
    format_dna_profile,
)
from src.flamelang.transformation_pipeline import TransformationPipeline
from src.flamelang.interview_harness import InterviewHarness


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"🔥 {title}")
    print("=" * 80 + "\n")


def demo_codon_mapping():
    """Demonstrate codon mapping functionality"""
    print_section("DEMO 1: Codon Mapping - K8s Operations → Genetic Codons")
    
    test_methods = [
        ("io.k8s.coordination.v1.leases.update", "Controller heartbeat"),
        ("io.k8s.core.v1.configmaps.update", "Configuration change"),
        ("io.k8s.core.v1.pods.create", "Pod creation (START)"),
        ("io.k8s.core.v1.pods.delete", "Pod deletion (STOP)"),
        ("io.k8s.apps.v1.deployments.update", "Deployment scaling"),
        ("io.k8s.core.v1.secrets.get", "Secret access"),
    ]
    
    print("K8s API Method → FlameLang Codon Mapping:\n")
    for full_method, description in test_methods:
        simplified = extract_method_from_proto_payload(full_method)
        codon = get_codon_for_method(simplified)
        
        if codon:
            print(f"  ✅ {simplified:25s} → {codon:5s} | {description}")
        else:
            print(f"  ⚠️  {simplified:25s} → None  | {description}")
    
    print(f"\n📊 Total Codons Defined: {len(CODON_MAP)}")
    print(f"📋 Interview Questions Mapped: {len(INTERVIEW_MAPPINGS)}")


def demo_dna_extraction():
    """Demonstrate DNA extraction from audit events"""
    print_section("DEMO 2: Behavioral DNA Extraction")
    
    print("Processing sample controller behavior...\n")
    
    # Simulate a controller's behavior pattern
    controller_events = [
        {
            'timestamp': '2024-01-15T08:00:00Z',
            'protoPayload.authenticationInfo.principalEmail': 'kube-controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'demo-cluster',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-15T08:00:15Z',
            'protoPayload.authenticationInfo.principalEmail': 'kube-controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'demo-cluster',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-15T08:00:30Z',
            'protoPayload.authenticationInfo.principalEmail': 'kube-controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'demo-cluster',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-15T08:00:45Z',
            'protoPayload.authenticationInfo.principalEmail': 'kube-controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.core.v1.configmaps.update',
            'resource.labels.cluster_name': 'demo-cluster',
            'resource.type': 'k8s_configmap'
        },
        {
            'timestamp': '2024-01-15T08:01:00Z',
            'protoPayload.authenticationInfo.principalEmail': 'kube-controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'demo-cluster',
            'resource.type': 'k8s_lease'
        },
    ]
    
    extractor = DNAExtractor(window_size=5, min_gene_length=3)
    extractor.add_events_from_dict(controller_events)
    
    dna = extractor.extract_dna_profile('kube-controller@k8s.io')
    
    print(f"Principal: {dna.principal}")
    print(f"Events Analyzed: {dna.total_events}")
    print(f"Genes Extracted: {len(dna.genes)}")
    print(f"Anomaly Score: {dna.anomaly_score} (0.0 = normal, 1.0 = highly anomalous)")
    
    if dna.genes:
        gene = dna.genes[0]
        print(f"\nFirst Gene Sequence:")
        print(f"  DNA: {gene.sequence}")
        print(f"  Pattern: {gene.pattern_type}")
        print(f"  Categories: {[c.value for c in gene.categories]}")
    
    print(f"\nCodon Frequency:")
    for codon, count in sorted(dna.codon_frequency.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / dna.total_events) * 100
        print(f"  {codon}: {count} ({percentage:.1f}%)")


def demo_transformation_pipeline():
    """Demonstrate full transformation pipeline"""
    print_section("DEMO 3: Full Transformation Pipeline")
    
    csv_file = Path("data/sample_gke_audit_logs.csv")
    
    if not csv_file.exists():
        print("⚠️  Sample CSV file not found. Skipping this demo.")
        return
    
    print(f"Loading audit logs from: {csv_file}\n")
    
    pipeline = TransformationPipeline(window_size=10, min_gene_length=3)
    event_count = pipeline.load_logs(csv_file)
    
    print(f"✅ Loaded {event_count} events")
    
    summary = pipeline.get_summary()
    print(f"\nPrincipal Summary:")
    for principal, count in list(summary['events_by_principal'].items())[:5]:
        print(f"  {principal}: {count} events")
    
    print(f"\n🧬 Extracting DNA profiles...")
    dna_profiles = pipeline.transform()
    
    print(f"✅ Extracted {len(dna_profiles)} DNA profiles")
    
    # Show top 3 by event count
    top_principals = sorted(
        dna_profiles.items(),
        key=lambda x: x[1].total_events,
        reverse=True
    )[:3]
    
    print(f"\nTop 3 Most Active Principals:")
    for i, (principal, dna) in enumerate(top_principals, 1):
        print(f"\n  {i}. {principal}")
        print(f"     Events: {dna.total_events}")
        print(f"     Genes: {len(dna.genes)}")
        print(f"     Anomaly: {dna.anomaly_score}")
        print(f"     Dominant: {[c.value for c in dna.dominant_categories[:2]]}")


def demo_interview_harness():
    """Demonstrate interview test harness"""
    print_section("DEMO 4: Interview Test Harness")
    
    print("Running automated test suite for candidate evaluation...\n")
    
    harness = InterviewHarness()
    
    print(f"📋 Test Cases Loaded: {len(harness.test_cases)}")
    
    # Show test case details
    for tc in harness.test_cases[:2]:  # Show first 2
        print(f"\n  Test Case: {tc.id} - {tc.name}")
        print(f"  Difficulty: {tc.difficulty}")
        print(f"  Related Questions: {tc.related_questions}")
        print(f"  Expected Pattern: {tc.expected_pattern}")
    
    print("\n" + "-" * 80)
    print("Running all test cases...\n")
    
    results = harness.run_all_tests()
    
    print(f"✅ Tests Completed:")
    print(f"   Total: {results['total_tests']}")
    print(f"   Passed: {results['passed']}")
    print(f"   Failed: {results['failed']}")
    print(f"   Average Score: {results['average_score']*100:.1f}%")
    
    # Show individual results
    print(f"\nDetailed Results:")
    for result in results['results']:
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"  {result.test_id}: {status} ({result.score*100:.1f}%)")


def demo_interview_questions():
    """Show interview question mappings"""
    print_section("DEMO 5: Interview Question Mappings")
    
    print("How K8s audit logs map to FlameLang interview questions:\n")
    
    for q_id, details in list(INTERVIEW_MAPPINGS.items())[:5]:
        print(f"{q_id}: {details['question']}")
        print(f"   Log Pattern: {details['log_pattern']}")
        print(f"   Codon Categories: {[c.value for c in details['codon_categories']]}")
        print(f"   Example: {details['example']}")
        print()


def main():
    """Run complete demo"""
    print("\n" + "=" * 80)
    print("🔥 FLAMELANG K8S AUDIT LOG TRANSFORMATION SYSTEM")
    print("   Live Demonstration")
    print("=" * 80)
    
    try:
        demo_codon_mapping()
        demo_dna_extraction()
        demo_transformation_pipeline()
        demo_interview_harness()
        demo_interview_questions()
        
        print_section("DEMO COMPLETE")
        print("The FlameLang system successfully transforms K8s audit logs into")
        print("behavioral DNA sequences, enabling:")
        print("  • Pattern recognition (heartbeat, mutation, scaling)")
        print("  • Anomaly detection for security analysis")
        print("  • Interview candidate evaluation")
        print("  • AI-driven operational insights")
        print("\n✨ Ready for production use and candidate interviews!\n")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
