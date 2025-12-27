#!/usr/bin/env python3
"""
Test Suite for Kubernetes Log Anomaly Detection
Strategickhaos DAO LLC - KHAOS Methodology Tests
"""

import sys
import json
from pathlib import Path

# Import test infrastructure compatibility
try:
    import numpy as np
except ImportError:
    class np:
        @staticmethod
        def mean(x):
            return sum(x) / len(x) if x else 0
        @staticmethod
        def std(x):
            if not x: return 0
            mean = sum(x) / len(x)
            variance = sum((xi - mean) ** 2 for xi in x) / len(x)
            return variance ** 0.5
        @staticmethod
        def abs(x):
            return abs(x)

try:
    import pandas as pd
except ImportError:
    print("Warning: pandas not installed. Some tests may be skipped.")
    pd = None

# Import the module to test
sys.path.append('.')
from anomaly_detection import (
    KubernetesAnomalyDetector,
    generate_simulated_data,
    cross_cluster_analysis
)


class AnomalyDetectionTests:
    """Test suite for anomaly detection functionality"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def test_01_basic_anomaly_detection(self) -> dict:
        """Test 1: Basic Z-score anomaly detection on simulated data"""
        result = {"test_id": 1, "name": "Basic Anomaly Detection", "status": "PASS"}
        
        try:
            # Generate data with known anomalies
            df = generate_simulated_data(
                periods=50,
                mean=100.0,
                std=10.0,
                anomaly_points={10: 200, 30: 30},  # 2 clear anomalies
                freq='h'
            )
            
            # Run detection
            detector = KubernetesAnomalyDetector(threshold=3.0)
            results = detector.detect_anomalies(df)
            
            # Count anomalies
            anomaly_count = results['anomaly'].sum()
            
            result['data_points'] = len(df)
            result['anomalies_detected'] = int(anomaly_count)
            result['expected_min'] = 2
            
            # Verify we detected at least the injected anomalies
            if anomaly_count < 2:
                result['status'] = 'FAIL'
                result['reason'] = f'Expected at least 2 anomalies, found {anomaly_count}'
            
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Exception: {str(e)}'
            
        return result
    
    def test_02_empty_data_handling(self) -> dict:
        """Test 2: Verify proper error handling for empty datasets"""
        result = {"test_id": 2, "name": "Empty Data Handling", "status": "PASS"}
        
        try:
            if pd is None:
                result['status'] = 'SKIP'
                result['reason'] = 'pandas not available'
                return result
                
            # Create empty DataFrame
            empty_df = pd.DataFrame({'timestamp': [], 'log_count': []})
            
            detector = KubernetesAnomalyDetector(threshold=3.0)
            
            # Should raise ValueError
            try:
                detector.detect_anomalies(empty_df)
                result['status'] = 'FAIL'
                result['reason'] = 'Should have raised ValueError for empty data'
            except ValueError as e:
                result['error_message'] = str(e)
                result['expected_error'] = 'Log data is empty'
                if 'empty' not in str(e).lower():
                    result['status'] = 'FAIL'
                    result['reason'] = f'Unexpected error message: {str(e)}'
                    
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Unexpected exception: {str(e)}'
            
        return result
    
    def test_03_zero_variance_handling(self) -> dict:
        """Test 3: Handle datasets with zero variance (constant values)"""
        result = {"test_id": 3, "name": "Zero Variance Handling", "status": "PASS"}
        
        try:
            if pd is None:
                result['status'] = 'SKIP'
                result['reason'] = 'pandas not available'
                return result
                
            # Create data with constant values
            constant_df = pd.DataFrame({
                'timestamp': pd.date_range(start='2025-12-01', periods=20, freq='h'),
                'log_count': [100.0] * 20
            })
            
            detector = KubernetesAnomalyDetector(threshold=3.0)
            
            # Should raise ValueError for zero std
            try:
                detector.detect_anomalies(constant_df)
                result['status'] = 'FAIL'
                result['reason'] = 'Should have raised ValueError for zero variance'
            except ValueError as e:
                result['error_message'] = str(e)
                result['expected_error'] = 'Standard deviation is zero'
                if 'standard deviation' not in str(e).lower():
                    result['status'] = 'FAIL'
                    result['reason'] = f'Unexpected error message: {str(e)}'
                    
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Unexpected exception: {str(e)}'
            
        return result
    
    def test_04_threshold_sensitivity(self) -> dict:
        """Test 4: Verify threshold parameter affects detection sensitivity"""
        result = {"test_id": 4, "name": "Threshold Sensitivity", "status": "PASS"}
        
        try:
            # Generate data with moderate anomaly
            df = generate_simulated_data(
                periods=50,
                mean=100.0,
                std=10.0,
                anomaly_points={25: 135},  # Moderate anomaly (~3.5 sigma)
                freq='h'
            )
            
            # Test with strict threshold (should detect)
            detector_strict = KubernetesAnomalyDetector(threshold=3.0)
            results_strict = detector_strict.detect_anomalies(df.copy())
            anomalies_strict = results_strict['anomaly'].sum()
            
            # Test with loose threshold (may not detect)
            detector_loose = KubernetesAnomalyDetector(threshold=5.0)
            results_loose = detector_loose.detect_anomalies(df.copy())
            anomalies_loose = results_loose['anomaly'].sum()
            
            result['strict_threshold'] = 3.0
            result['loose_threshold'] = 5.0
            result['strict_anomalies'] = int(anomalies_strict)
            result['loose_anomalies'] = int(anomalies_loose)
            
            # Strict threshold should detect more or equal anomalies
            if anomalies_strict < anomalies_loose:
                result['status'] = 'FAIL'
                result['reason'] = 'Strict threshold detected fewer anomalies than loose'
                
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Exception: {str(e)}'
            
        return result
    
    def test_05_anomaly_summary_statistics(self) -> dict:
        """Test 5: Verify summary statistics generation"""
        result = {"test_id": 5, "name": "Summary Statistics", "status": "PASS"}
        
        try:
            # Generate data
            df = generate_simulated_data(
                periods=100,
                mean=100.0,
                std=10.0,
                anomaly_points={10: 150, 50: 50, 80: 180},
                freq='h'
            )
            
            # Run detection
            detector = KubernetesAnomalyDetector(threshold=3.0)
            results = detector.detect_anomalies(df)
            summary = detector.get_anomaly_summary(results)
            
            # Verify summary contains expected keys
            required_keys = [
                'total_records', 'anomaly_count', 'anomaly_rate',
                'mean_log_count', 'std_log_count', 'threshold',
                'max_z_score', 'anomaly_timestamps'
            ]
            
            missing_keys = [k for k in required_keys if k not in summary]
            if missing_keys:
                result['status'] = 'FAIL'
                result['reason'] = f'Missing keys in summary: {missing_keys}'
            else:
                result['summary_keys'] = list(summary.keys())
                result['total_records'] = summary['total_records']
                result['anomaly_count'] = summary['anomaly_count']
                result['anomaly_rate'] = summary['anomaly_rate']
                
                # Verify basic consistency
                if summary['total_records'] != len(df):
                    result['status'] = 'FAIL'
                    result['reason'] = 'Total records mismatch'
                    
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Exception: {str(e)}'
            
        return result
    
    def test_06_cross_cluster_analysis(self) -> dict:
        """Test 6: Cross-cluster anomaly correlation"""
        result = {"test_id": 6, "name": "Cross-Cluster Analysis", "status": "PASS"}
        
        try:
            # Simulate two clusters
            cluster_data = {
                'red-team': generate_simulated_data(
                    30, mean=120, std=15, 
                    anomaly_points={10: 200, 20: 40}
                ),
                'jarvis-swarm': generate_simulated_data(
                    30, mean=80, std=12,
                    anomaly_points={10: 150, 25: 30}
                )
            }
            
            # Run cross-cluster analysis
            combined_anomalies, summaries = cross_cluster_analysis(cluster_data, threshold=3.0)
            
            result['clusters_analyzed'] = len(summaries)
            result['total_anomalies'] = len(combined_anomalies) if len(combined_anomalies) > 0 else 0
            
            # Verify summaries for each cluster
            for cluster_name in ['red-team', 'jarvis-swarm']:
                if cluster_name not in summaries:
                    result['status'] = 'FAIL'
                    result['reason'] = f'Missing summary for {cluster_name}'
                    break
                    
                cluster_summary = summaries[cluster_name]
                result[f'{cluster_name}_anomalies'] = cluster_summary['anomaly_count']
                result[f'{cluster_name}_mean'] = cluster_summary['mean_log_count']
            
            # Verify combined anomalies have cluster identifier
            if len(combined_anomalies) > 0 and 'cluster' not in combined_anomalies.columns:
                result['status'] = 'FAIL'
                result['reason'] = 'Combined anomalies missing cluster identifier'
                
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Exception: {str(e)}'
            
        return result
    
    def test_07_simulated_data_generation(self) -> dict:
        """Test 7: Verify simulated data generation utility"""
        result = {"test_id": 7, "name": "Simulated Data Generation", "status": "PASS"}
        
        try:
            # Generate data with specific parameters
            periods = 50
            mean = 100.0
            std = 10.0
            
            df = generate_simulated_data(
                periods=periods,
                mean=mean,
                std=std,
                freq='h'
            )
            
            result['generated_records'] = len(df)
            result['expected_records'] = periods
            
            # Verify structure
            if len(df) != periods:
                result['status'] = 'FAIL'
                result['reason'] = f'Expected {periods} records, got {len(df)}'
            elif 'timestamp' not in df.columns or 'log_count' not in df.columns:
                result['status'] = 'FAIL'
                result['reason'] = 'Missing required columns'
            else:
                # Verify mean and std are roughly correct (within reason for small sample)
                actual_mean = df['log_count'].mean()
                actual_std = df['log_count'].std()
                
                result['actual_mean'] = actual_mean
                result['actual_std'] = actual_std
                result['expected_mean'] = mean
                result['expected_std'] = std
                
                # Allow 30% deviation due to random sampling
                if abs(actual_mean - mean) > mean * 0.3:
                    result['status'] = 'FAIL'
                    result['reason'] = f'Mean too far from expected: {actual_mean} vs {mean}'
                    
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Exception: {str(e)}'
            
        return result
    
    def test_08_z_score_calculation_accuracy(self) -> dict:
        """Test 8: Verify Z-score calculations are mathematically correct"""
        result = {"test_id": 8, "name": "Z-Score Accuracy", "status": "PASS"}
        
        try:
            if pd is None:
                result['status'] = 'SKIP'
                result['reason'] = 'pandas not available'
                return result
                
            # Create simple dataset with known statistics
            df = pd.DataFrame({
                'timestamp': pd.date_range(start='2025-12-01', periods=5, freq='h'),
                'log_count': [90.0, 95.0, 100.0, 105.0, 110.0]  # Mean=100, Std≈7.91
            })
            
            detector = KubernetesAnomalyDetector(threshold=3.0)
            results = detector.detect_anomalies(df)
            
            # Verify calculated mean and std
            expected_mean = 100.0
            expected_std = df['log_count'].std()  # Should be ~7.91
            
            result['calculated_mean'] = detector.mean
            result['calculated_std'] = detector.std
            result['expected_mean'] = expected_mean
            
            # Verify mean is exact
            if abs(detector.mean - expected_mean) > 0.001:
                result['status'] = 'FAIL'
                result['reason'] = f'Mean calculation incorrect: {detector.mean} vs {expected_mean}'
            
            # Verify Z-scores are calculated correctly
            # For value 110 with mean 100 and std ~7.91, Z ≈ 1.26
            z_score_110 = results[results['log_count'] == 110.0]['z_score'].iloc[0]
            expected_z = (110.0 - expected_mean) / expected_std
            
            result['z_score_for_110'] = z_score_110
            result['expected_z'] = expected_z
            
            if abs(z_score_110 - expected_z) > 0.01:
                result['status'] = 'FAIL'
                result['reason'] = f'Z-score calculation incorrect: {z_score_110} vs {expected_z}'
                
        except Exception as e:
            result['status'] = 'FAIL'
            result['reason'] = f'Exception: {str(e)}'
            
        return result
    
    def run_all_tests(self):
        """Execute all test cases"""
        print("=" * 80)
        print("🧪 Anomaly Detection Test Suite")
        print("Strategickhaos DAO LLC - KHAOS Methodology")
        print("=" * 80)
        print()
        
        # Run all tests
        test_methods = [
            self.test_01_basic_anomaly_detection,
            self.test_02_empty_data_handling,
            self.test_03_zero_variance_handling,
            self.test_04_threshold_sensitivity,
            self.test_05_anomaly_summary_statistics,
            self.test_06_cross_cluster_analysis,
            self.test_07_simulated_data_generation,
            self.test_08_z_score_calculation_accuracy
        ]
        
        for test_method in test_methods:
            result = test_method()
            self.results.append(result)
            
            # Update counters
            if result['status'] == 'PASS':
                self.passed += 1
                status_icon = '✅'
            elif result['status'] == 'SKIP':
                status_icon = '⏭️'
            else:
                self.failed += 1
                status_icon = '❌'
            
            print(f"{status_icon} Test {result['test_id']}: {result['name']} - {result['status']}")
            
            if result['status'] == 'FAIL':
                print(f"   Reason: {result.get('reason', 'Unknown')}")
        
        print()
        self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        total = len(self.results)
        skipped = sum(1 for r in self.results if r['status'] == 'SKIP')
        
        print("=" * 80)
        print("📊 Test Summary")
        print("=" * 80)
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Skipped: {skipped}")
        print(f"Pass Rate: {self.passed / (total - skipped) * 100:.1f}%" if (total - skipped) > 0 else "N/A")
        print("=" * 80)
        
        # Overall status
        if self.failed == 0:
            print("🎉 All tests passed!")
        else:
            print("⚠️ Some tests failed. Review output above.")
        print()
        
    def save_results(self, output_path: str = "benchmarks/reports/anomaly_detection_test_results.json"):
        """Save test results to JSON file"""
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        test_summary = {
            'total_tests': len(self.results),
            'passed': self.passed,
            'failed': self.failed,
            'pass_rate': self.passed / len(self.results) if self.results else 0,
            'test_results': self.results
        }
        
        with open(output_path, 'w') as f:
            json.dump(test_summary, f, indent=2)
        
        print(f"📁 Test results saved to: {output_path}")
        

def main():
    """Main test runner"""
    if pd is None:
        print("⚠️ Warning: pandas not installed. Some tests will be skipped.")
        print("   Install with: pip install pandas numpy matplotlib")
        print()
    
    # Run test suite
    test_suite = AnomalyDetectionTests()
    test_suite.run_all_tests()
    test_suite.save_results()
    
    # Exit code based on results
    exit_code = 0 if test_suite.failed == 0 else 1
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
