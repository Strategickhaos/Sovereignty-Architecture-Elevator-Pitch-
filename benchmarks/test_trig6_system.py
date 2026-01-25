#!/usr/bin/env python3
"""
TRIG6 Calibration & BCI Gate Test Suite
Strategickhaos DAO LLC - TRIG6 Calibration System
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from trig6_calibration import ClaimMetrics, Trig6Calibrator
from bci_trig6_gate import BCITrig6, bci_gate


class TestTrig6Calibration:
    """Test suite for TRIG6 Calibration System"""
    
    def test_claim_metrics_score_calculation(self):
        """Test ClaimMetrics score calculation formula"""
        # Test perfect score
        perfect = ClaimMetrics(R=1.0, D=0.0, N=0.0, eq=1.0)
        assert perfect.score() == 1.0, "Perfect metrics should yield score of 1.0"
        
        # Test zero score
        zero = ClaimMetrics(R=0.0, D=0.0, N=0.0, eq=0.0)
        assert zero.score() == 0.0, "All zero metrics should yield score of 0.0"
        
        # Test known value
        known = ClaimMetrics(R=0.8, D=0.2, N=0.3, eq=0.7)
        expected = 0.8 * (1 - 0.2) * (1 - 0.3) * 0.7
        assert abs(known.score() - expected) < 0.0001, f"Expected {expected}, got {known.score()}"
    
    def test_calibrator_initialization(self):
        """Test Trig6Calibrator initialization"""
        calibrator = Trig6Calibrator()
        assert not calibrator.calibrated, "Calibrator should start uncalibrated"
        assert calibrator._model is not None, "Model should be initialized"
    
    def test_calibrator_fit_and_predict(self):
        """Test calibrator fitting and prediction"""
        calibrator = Trig6Calibrator()
        
        # Create training data
        data = [
            (ClaimMetrics(0.95, 0.05, 0.05, 0.95), 1.0),  # High quality -> True
            (ClaimMetrics(0.90, 0.10, 0.10, 0.90), 1.0),
            (ClaimMetrics(0.85, 0.15, 0.15, 0.85), 1.0),
            (ClaimMetrics(0.80, 0.20, 0.20, 0.80), 1.0),
            (ClaimMetrics(0.75, 0.25, 0.25, 0.75), 1.0),
            (ClaimMetrics(0.30, 0.70, 0.60, 0.20), 0.0),  # Low quality -> False
            (ClaimMetrics(0.25, 0.75, 0.65, 0.15), 0.0),
            (ClaimMetrics(0.20, 0.80, 0.70, 0.10), 0.0),
            (ClaimMetrics(0.15, 0.85, 0.75, 0.05), 0.0),
            (ClaimMetrics(0.10, 0.90, 0.80, 0.00), 0.0),
        ]
        
        # Fit calibrator
        calibrator.fit(data)
        assert calibrator.calibrated, "Calibrator should be calibrated after fit"
        
        # Test predictions
        high_quality = ClaimMetrics(0.9, 0.1, 0.1, 0.9)
        low_quality = ClaimMetrics(0.2, 0.8, 0.7, 0.1)
        
        high_prob = calibrator.predict_proba(high_quality)
        low_prob = calibrator.predict_proba(low_quality)
        
        assert 0.0 <= high_prob <= 1.0, "Probability should be in [0, 1]"
        assert 0.0 <= low_prob <= 1.0, "Probability should be in [0, 1]"
        assert high_prob > low_prob, "High quality should have higher probability"
    
    def test_calibrator_predict_without_fit_raises_error(self):
        """Test that predicting before fitting raises ValueError"""
        calibrator = Trig6Calibrator()
        test_metrics = ClaimMetrics(0.8, 0.2, 0.2, 0.8)
        
        with pytest.raises(ValueError, match="Calibrator not fitted"):
            calibrator.predict_proba(test_metrics)
    
    def test_calibrator_monotonicity(self):
        """Test that calibrator maintains monotonic relationship"""
        calibrator = Trig6Calibrator()
        
        # Training data with clear monotonic pattern
        data = [
            (ClaimMetrics(0.9, 0.1, 0.1, 0.9), 1.0),
            (ClaimMetrics(0.7, 0.3, 0.3, 0.7), 0.8),
            (ClaimMetrics(0.5, 0.5, 0.5, 0.5), 0.5),
            (ClaimMetrics(0.3, 0.7, 0.7, 0.3), 0.2),
            (ClaimMetrics(0.1, 0.9, 0.9, 0.1), 0.0),
        ]
        
        calibrator.fit(data)
        
        # Test points in increasing order
        test_points = [
            ClaimMetrics(0.2, 0.8, 0.8, 0.2),
            ClaimMetrics(0.4, 0.6, 0.6, 0.4),
            ClaimMetrics(0.6, 0.4, 0.4, 0.6),
            ClaimMetrics(0.8, 0.2, 0.2, 0.8),
        ]
        
        predictions = [calibrator.predict_proba(m) for m in test_points]
        
        # Check monotonicity
        for i in range(len(predictions) - 1):
            assert predictions[i] <= predictions[i + 1], \
                f"Predictions not monotonic: {predictions[i]} > {predictions[i + 1]}"


class TestBCITrig6Gate:
    """Test suite for BCI TRIG6 Gate System"""
    
    def test_bci_trig6_score_calculation(self):
        """Test BCITrig6 score calculation formula"""
        # Test perfect score
        perfect = BCITrig6(R=1.0, D=0.0, N=0.0, eq=1.0)
        assert perfect.score() == 1.0, "Perfect metrics should yield score of 1.0"
        
        # Test known value from example
        burst = BCITrig6(R=0.85, D=0.15, N=0.25, eq=0.9)
        expected = 0.85 * (1 - 0.15) * (1 - 0.25) * 0.9
        assert abs(burst.score() - expected) < 0.0001, \
            f"Expected {expected}, got {burst.score()}"
    
    def test_bci_gate_normal_mode(self):
        """Test BCI gate returns NORMAL for high scores"""
        # Score above warning threshold (0.6)
        high_quality = BCITrig6(R=0.9, D=0.1, N=0.1, eq=0.9)
        verdict = bci_gate(high_quality)
        assert verdict == "NORMAL", f"Expected NORMAL, got {verdict}"
        
        # Score well above warning threshold
        very_high = BCITrig6(R=0.95, D=0.05, N=0.1, eq=0.95)  # score > 0.7
        verdict = bci_gate(very_high)
        assert verdict == "NORMAL", f"Expected NORMAL for high quality, got {verdict}"
    
    def test_bci_gate_degraded_mode(self):
        """Test BCI gate returns DEGRADED_MODE for medium scores"""
        # Score between abort (0.4) and warn (0.6)
        medium_quality = BCITrig6(R=0.85, D=0.15, N=0.25, eq=0.9)
        verdict = bci_gate(medium_quality)
        assert verdict == "DEGRADED_MODE", f"Expected DEGRADED_MODE, got {verdict}"
        
        # Score just above abort threshold  
        near_abort = BCITrig6(R=0.8, D=0.2, N=0.3, eq=0.93)  # score ≈ 0.416
        verdict = bci_gate(near_abort)
        assert verdict == "DEGRADED_MODE", f"Expected DEGRADED_MODE near abort, got {verdict}"
    
    def test_bci_gate_abort_session(self):
        """Test BCI gate returns ABORT_SESSION for low scores"""
        # Score below abort threshold (0.4)
        low_quality = BCITrig6(R=0.3, D=0.7, N=0.6, eq=0.5)
        verdict = bci_gate(low_quality)
        assert verdict == "ABORT_SESSION", f"Expected ABORT_SESSION, got {verdict}"
        
        # Score at zero
        zero_quality = BCITrig6(R=0.0, D=1.0, N=1.0, eq=0.0)
        verdict = bci_gate(zero_quality)
        assert verdict == "ABORT_SESSION", f"Expected ABORT_SESSION for zero, got {verdict}"
    
    def test_bci_gate_custom_thresholds(self):
        """Test BCI gate with custom threshold values"""
        # Use metrics with score around 0.5 for clearer testing
        metrics = BCITrig6(R=0.85, D=0.15, N=0.25, eq=0.95)  # score ≈ 0.514
        
        # With default thresholds (warn=0.6, abort=0.4), should be DEGRADED_MODE
        verdict_default = bci_gate(metrics)
        assert verdict_default == "DEGRADED_MODE"
        
        # With higher thresholds (warn=0.7, abort=0.6), should be ABORT_SESSION
        verdict_custom = bci_gate(metrics, warn=0.7, abort=0.6)
        assert verdict_custom == "ABORT_SESSION"
        
        # With lower thresholds, should be NORMAL
        verdict_low = bci_gate(metrics, warn=0.4, abort=0.2)
        assert verdict_low == "NORMAL"
    
    def test_bci_gate_boundary_conditions(self):
        """Test BCI gate at exact threshold boundaries"""
        # Score exactly at warn threshold (0.6) should be NORMAL (>= check)
        # R * (1-D) * (1-N) * eq = 0.6
        # Using R=0.9, D=0.1, N=0.25: 0.9 * 0.9 * 0.75 * eq = 0.6 => eq = 0.9877
        at_warn = BCITrig6(R=0.9, D=0.1, N=0.25, eq=0.9877)
        at_warn_score = at_warn.score()
        assert abs(at_warn_score - 0.6) < 0.001, f"Expected score ~0.6, got {at_warn_score}"
        assert bci_gate(at_warn) == "NORMAL", "Score at warn threshold should be NORMAL"
        
        # Just below warn threshold
        below_warn = BCITrig6(R=0.85, D=0.15, N=0.3, eq=0.95)  # score ≈ 0.48
        assert bci_gate(below_warn) == "DEGRADED_MODE", "Score below warn should be DEGRADED_MODE"
        
        # Exactly at abort threshold (0.4) should be DEGRADED_MODE (>= check)
        at_abort = BCITrig6(R=0.8, D=0.2, N=0.375, eq=1.0)
        at_abort_score = at_abort.score()
        assert abs(at_abort_score - 0.4) < 0.001, f"Expected score ~0.4, got {at_abort_score}"
        result = bci_gate(at_abort)
        assert result == "DEGRADED_MODE", \
            f"Score at abort threshold should be DEGRADED_MODE, got {result}"


class TestIntegration:
    """Integration tests for TRIG6 system"""
    
    def test_calibrator_with_bci_data(self):
        """Test using calibrator with BCI-style data"""
        calibrator = Trig6Calibrator()
        
        # BCI data: high coherence with low drift/noise = good outcome
        bci_data = [
            (ClaimMetrics(0.9, 0.1, 0.1, 0.9), 1.0),   # Good BCI signal
            (ClaimMetrics(0.85, 0.15, 0.2, 0.85), 1.0),
            (ClaimMetrics(0.8, 0.2, 0.25, 0.8), 0.8),  # Medium BCI signal
            (ClaimMetrics(0.6, 0.4, 0.5, 0.6), 0.5),
            (ClaimMetrics(0.3, 0.7, 0.6, 0.3), 0.0),   # Poor BCI signal
            (ClaimMetrics(0.2, 0.8, 0.7, 0.2), 0.0),
        ]
        
        calibrator.fit(bci_data)
        
        # Test prediction on new BCI metrics
        test_signal = ClaimMetrics(0.75, 0.25, 0.3, 0.7)
        probability = calibrator.predict_proba(test_signal)
        
        assert 0.0 <= probability <= 1.0, "Probability should be in valid range"
        assert probability > 0.4, "Medium signal should have reasonable probability"
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from raw metrics to decision"""
        # Step 1: Train calibrator
        calibrator = Trig6Calibrator()
        training_data = [
            (ClaimMetrics(0.95, 0.05, 0.05, 0.95), 1.0),
            (ClaimMetrics(0.90, 0.10, 0.10, 0.90), 1.0),
            (ClaimMetrics(0.70, 0.30, 0.30, 0.70), 0.7),
            (ClaimMetrics(0.50, 0.50, 0.50, 0.50), 0.3),
            (ClaimMetrics(0.30, 0.70, 0.60, 0.20), 0.0),
            (ClaimMetrics(0.20, 0.80, 0.70, 0.10), 0.0),
        ]
        calibrator.fit(training_data)
        
        # Step 2: Get new BCI metrics
        bci_metrics = BCITrig6(R=0.8, D=0.2, N=0.25, eq=0.85)
        
        # Step 3: Get BCI gate verdict
        gate_verdict = bci_gate(bci_metrics)
        
        # Step 4: Convert BCI metrics to ClaimMetrics and get probability
        claim_metrics = ClaimMetrics(
            R=bci_metrics.R,
            D=bci_metrics.D,
            N=bci_metrics.N,
            eq=bci_metrics.eq
        )
        probability = calibrator.predict_proba(claim_metrics)
        
        # Verify workflow consistency
        assert gate_verdict in ["NORMAL", "DEGRADED_MODE", "ABORT_SESSION"]
        assert 0.0 <= probability <= 1.0
        
        # High probability should correlate with NORMAL or DEGRADED_MODE
        if probability > 0.7:
            assert gate_verdict in ["NORMAL", "DEGRADED_MODE"], \
                "High probability should not trigger ABORT"


def run_all_tests():
    """Run all TRIG6 tests and print results"""
    import json
    from datetime import datetime
    
    # Create results directory
    results_dir = Path(__file__).parent / "reports"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Run tests using pytest
    pytest_args = [
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    result = pytest.main(pytest_args)
    
    # Generate report
    report = {
        "test_suite": "TRIG6 Calibration & BCI Gate",
        "timestamp": datetime.now().isoformat(),
        "exit_code": result,
        "status": "PASS" if result == 0 else "FAIL"
    }
    
    # Save report
    report_file = results_dir / "trig6_test_results.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nTest report saved to: {report_file}")
    return result


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
