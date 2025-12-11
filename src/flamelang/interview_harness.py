#!/usr/bin/env python3
"""
FlameLang Interview Test Harness
Testing framework for evaluating candidates on K8s → FlameLang transformation skills

This module provides:
1. Test cases with expected outputs
2. Scoring system for candidate submissions
3. Interactive challenges
4. Automated grading
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json

from .codon_mapping import (
    get_codon_for_method,
    extract_method_from_proto_payload,
    INTERVIEW_MAPPINGS,
    CodonCategory
)
from .dna_extraction import DNAExtractor, BehavioralDNA
from .transformation_pipeline import TransformationPipeline


@dataclass
class TestCase:
    """Represents a single test case"""
    id: str
    name: str
    description: str
    input_events: List[Dict]
    expected_codons: List[str]
    expected_pattern: str
    related_questions: List[str]
    difficulty: str  # "easy", "medium", "hard"


@dataclass
class TestResult:
    """Results from running a test case"""
    test_id: str
    passed: bool
    score: float  # 0.0 to 1.0
    candidate_output: Dict
    expected_output: Dict
    feedback: List[str]


class InterviewHarness:
    """
    Test harness for FlameLang interview challenges
    
    Evaluates candidates on:
    1. Codon mapping accuracy
    2. DNA extraction correctness
    3. Pattern recognition
    4. Anomaly detection
    """
    
    def __init__(self):
        self.test_cases = self._initialize_test_cases()
    
    def _initialize_test_cases(self) -> List[TestCase]:
        """Initialize standard test cases"""
        return [
            # Test Case 1: Basic heartbeat pattern
            TestCase(
                id="TC001",
                name="Controller Heartbeat Recognition",
                description="Identify repeated lease updates as heartbeat pattern",
                input_events=[
                    {
                        'timestamp': '2024-01-01T10:00:00Z',
                        'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
                        'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_lease'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:15Z',
                        'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
                        'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_lease'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:30Z',
                        'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
                        'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_lease'
                    },
                ],
                expected_codons=['UUA', 'UUA', 'UUA'],
                expected_pattern='heartbeat',
                related_questions=['Q2', 'Q21'],
                difficulty='easy'
            ),
            
            # Test Case 2: Configuration mutation
            TestCase(
                id="TC002",
                name="Configuration Mutation Detection",
                description="Detect configmap updates as mutation pattern",
                input_events=[
                    {
                        'timestamp': '2024-01-01T10:00:00Z',
                        'protoPayload.authenticationInfo.principalEmail': 'admin@example.com',
                        'protoPayload.methodName': 'io.k8s.core.v1.configmaps.get',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_configmap'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:15Z',
                        'protoPayload.authenticationInfo.principalEmail': 'admin@example.com',
                        'protoPayload.methodName': 'io.k8s.core.v1.configmaps.update',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_configmap'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:30Z',
                        'protoPayload.authenticationInfo.principalEmail': 'admin@example.com',
                        'protoPayload.methodName': 'io.k8s.core.v1.configmaps.update',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_configmap'
                    },
                ],
                expected_codons=['GCC', 'GCU', 'GCU'],
                expected_pattern='mutation',
                related_questions=['Q5', 'Q7', 'Q18'],
                difficulty='medium'
            ),
            
            # Test Case 3: Scaling operation (pod lifecycle)
            TestCase(
                id="TC003",
                name="Pod Scaling Pattern",
                description="Recognize pod creation/deletion as scaling pattern",
                input_events=[
                    {
                        'timestamp': '2024-01-01T10:00:00Z',
                        'protoPayload.authenticationInfo.principalEmail': 'scheduler@k8s.io',
                        'protoPayload.methodName': 'io.k8s.core.v1.pods.create',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_pod'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:15Z',
                        'protoPayload.authenticationInfo.principalEmail': 'scheduler@k8s.io',
                        'protoPayload.methodName': 'io.k8s.core.v1.pods.update',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_pod'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:30Z',
                        'protoPayload.authenticationInfo.principalEmail': 'chaos@k8s.io',
                        'protoPayload.methodName': 'io.k8s.core.v1.pods.delete',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_pod'
                    },
                ],
                expected_codons=['AUG', 'CCU', 'UAA'],
                expected_pattern='scaling',
                related_questions=['Q16'],
                difficulty='medium'
            ),
            
            # Test Case 4: Anomalous access attempts
            TestCase(
                id="TC004",
                name="Anomaly Detection - Unauthorized Access",
                description="Detect anomalous RBAC denial patterns",
                input_events=[
                    {
                        'timestamp': '2024-01-01T10:00:00Z',
                        'protoPayload.authenticationInfo.principalEmail': 'attacker@external.com',
                        'protoPayload.methodName': 'io.k8s.core.v1.secrets.get',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_secret',
                        'labels.authorization.k8s.io/reason': 'RBAC: denied'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:05Z',
                        'protoPayload.authenticationInfo.principalEmail': 'attacker@external.com',
                        'protoPayload.methodName': 'io.k8s.core.v1.secrets.get',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_secret',
                        'labels.authorization.k8s.io/reason': 'RBAC: denied'
                    },
                    {
                        'timestamp': '2024-01-01T10:00:10Z',
                        'protoPayload.authenticationInfo.principalEmail': 'attacker@external.com',
                        'protoPayload.methodName': 'io.k8s.core.v1.secrets.get',
                        'resource.labels.cluster_name': 'test-cluster',
                        'resource.type': 'k8s_secret',
                        'labels.authorization.k8s.io/reason': 'RBAC: denied'
                    },
                ],
                expected_codons=['UCU', 'UCU', 'UCU'],
                expected_pattern='unknown',  # Anomalous pattern
                related_questions=['Q9', 'Q29'],
                difficulty='hard'
            ),
        ]
    
    def run_test(self, test_case: TestCase, 
                 candidate_pipeline: TransformationPipeline) -> TestResult:
        """
        Run a single test case against candidate's implementation
        
        Args:
            test_case: Test case to run
            candidate_pipeline: Candidate's transformation pipeline
            
        Returns:
            TestResult with score and feedback
        """
        feedback = []
        score = 0.0
        
        # Load test events into candidate's pipeline
        candidate_pipeline.extractor.add_events_from_dict(test_case.input_events)
        
        # Get principal from first event
        principal = test_case.input_events[0]['protoPayload.authenticationInfo.principalEmail']
        
        # Extract DNA profile
        try:
            dna_profile = candidate_pipeline.extractor.extract_dna_profile(principal)
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                passed=False,
                score=0.0,
                candidate_output={},
                expected_output={
                    'codons': test_case.expected_codons,
                    'pattern': test_case.expected_pattern
                },
                feedback=[f"❌ Error extracting DNA profile: {str(e)}"]
            )
        
        # Extract candidate's codons from genes
        candidate_codons = []
        if dna_profile.genes:
            # Get codons from first gene
            gene_sequence = dna_profile.genes[0].sequence
            candidate_codons = gene_sequence.split('-')
        
        # Test 1: Codon mapping accuracy (40% of score)
        codon_score = self._score_codons(test_case.expected_codons, candidate_codons)
        if codon_score == 1.0:
            feedback.append("✅ Codon mapping: Perfect")
        elif codon_score > 0.5:
            feedback.append(f"⚠️  Codon mapping: Partial ({codon_score*100:.0f}%)")
            feedback.append(f"   Expected: {test_case.expected_codons}")
            feedback.append(f"   Got: {candidate_codons}")
        else:
            feedback.append(f"❌ Codon mapping: Incorrect")
            feedback.append(f"   Expected: {test_case.expected_codons}")
            feedback.append(f"   Got: {candidate_codons}")
        
        score += codon_score * 0.4
        
        # Test 2: Pattern recognition (40% of score)
        candidate_pattern = dna_profile.genes[0].pattern_type if dna_profile.genes else 'unknown'
        pattern_score = 1.0 if candidate_pattern == test_case.expected_pattern else 0.0
        
        if pattern_score == 1.0:
            feedback.append(f"✅ Pattern recognition: Correct ({candidate_pattern})")
        else:
            feedback.append(f"❌ Pattern recognition: Incorrect")
            feedback.append(f"   Expected: {test_case.expected_pattern}")
            feedback.append(f"   Got: {candidate_pattern}")
        
        score += pattern_score * 0.4
        
        # Test 3: DNA extraction completeness (20% of score)
        completeness_score = min(len(dna_profile.genes) / 1.0, 1.0)  # At least 1 gene
        
        if completeness_score == 1.0:
            feedback.append("✅ DNA extraction: Complete")
        else:
            feedback.append("⚠️  DNA extraction: Incomplete")
        
        score += completeness_score * 0.2
        
        # Overall result
        passed = score >= 0.7  # 70% passing score
        
        return TestResult(
            test_id=test_case.id,
            passed=passed,
            score=score,
            candidate_output={
                'codons': candidate_codons,
                'pattern': candidate_pattern,
                'genes_count': len(dna_profile.genes),
                'anomaly_score': dna_profile.anomaly_score
            },
            expected_output={
                'codons': test_case.expected_codons,
                'pattern': test_case.expected_pattern
            },
            feedback=feedback
        )
    
    def _score_codons(self, expected: List[str], actual: List[str]) -> float:
        """
        Score codon sequence accuracy
        
        Uses sequence alignment scoring:
        - Exact match: 1.0
        - Partial match: proportional to matches
        """
        if not expected or not actual:
            return 0.0
        
        # Simple matching score
        matches = sum(1 for e, a in zip(expected, actual) if e == a)
        max_length = max(len(expected), len(actual))
        
        return matches / max_length if max_length > 0 else 0.0
    
    def run_all_tests(self, candidate_pipeline: TransformationPipeline = None) -> Dict:
        """
        Run all test cases
        
        Args:
            candidate_pipeline: Optional pipeline, creates new one if None
            
        Returns:
            Dict with overall results and individual test results
        """
        if candidate_pipeline is None:
            candidate_pipeline = TransformationPipeline()
        
        results = []
        total_score = 0.0
        passed_count = 0
        
        for test_case in self.test_cases:
            # Create fresh pipeline for each test
            test_pipeline = TransformationPipeline()
            result = self.run_test(test_case, test_pipeline)
            results.append(result)
            
            total_score += result.score
            if result.passed:
                passed_count += 1
        
        avg_score = total_score / len(self.test_cases) if self.test_cases else 0.0
        
        return {
            'total_tests': len(self.test_cases),
            'passed': passed_count,
            'failed': len(self.test_cases) - passed_count,
            'average_score': avg_score,
            'results': results
        }
    
    def print_results(self, overall_results: Dict) -> None:
        """Print formatted test results"""
        print("=" * 80)
        print("🔥 FLAMELANG INTERVIEW TEST RESULTS")
        print("=" * 80)
        print(f"\nTotal Tests: {overall_results['total_tests']}")
        print(f"Passed: {overall_results['passed']}")
        print(f"Failed: {overall_results['failed']}")
        print(f"Average Score: {overall_results['average_score']*100:.1f}%")
        
        print("\n" + "-" * 80)
        print("Individual Test Results:")
        print("-" * 80)
        
        for result in overall_results['results']:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"\n{result.test_id}: {status} (Score: {result.score*100:.1f}%)")
            for feedback_line in result.feedback:
                print(f"  {feedback_line}")
        
        print("\n" + "=" * 80)
        
        # Final grade
        avg_score = overall_results['average_score']
        if avg_score >= 0.9:
            grade = "A (Excellent)"
        elif avg_score >= 0.8:
            grade = "B (Good)"
        elif avg_score >= 0.7:
            grade = "C (Passing)"
        else:
            grade = "F (Failing)"
        
        print(f"Final Grade: {grade}")
        print("=" * 80)
    
    def generate_challenge_file(self, output_path: Path) -> None:
        """
        Generate a challenge file for candidates
        
        Includes:
        - Instructions
        - Sample data
        - Expected output format
        """
        challenge = {
            "flamelang_interview_challenge": {
                "version": "1.0.0",
                "instructions": (
                    "Transform the provided K8s audit events into FlameLang behavioral DNA.\n"
                    "Your solution must:\n"
                    "1. Map K8s API methods to correct FlameLang codons\n"
                    "2. Extract behavioral patterns (heartbeat, mutation, scaling, etc.)\n"
                    "3. Generate valid DNA gene sequences\n"
                    "4. Calculate anomaly scores"
                ),
                "test_cases": [
                    {
                        "id": tc.id,
                        "name": tc.name,
                        "description": tc.description,
                        "difficulty": tc.difficulty,
                        "related_questions": tc.related_questions,
                        "input_events": tc.input_events
                    }
                    for tc in self.test_cases
                ],
                "submission_format": {
                    "principal": "email@example.com",
                    "codons": ["UUA", "GCU", "..."],
                    "pattern": "heartbeat|mutation|scaling|control_loop|unknown",
                    "genes_count": 1,
                    "anomaly_score": 0.0
                }
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(challenge, f, indent=2)
        
        print(f"✅ Generated challenge file: {output_path}")


if __name__ == "__main__":
    # Run test harness demo
    print("🔥 FlameLang Interview Test Harness Demo\n")
    
    harness = InterviewHarness()
    
    # Run all tests
    results = harness.run_all_tests()
    
    # Print results
    harness.print_results(results)
    
    # Generate challenge file
    challenge_path = Path("output/flamelang_interview_challenge.json")
    challenge_path.parent.mkdir(parents=True, exist_ok=True)
    harness.generate_challenge_file(challenge_path)
