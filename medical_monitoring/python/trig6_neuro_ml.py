#!/usr/bin/env python3
"""
TRIG6 Machine Learning Detection System
Isolation Forest anomaly detection for neurological monitoring

Purpose: ML-powered pattern recognition for early warning
Creator: Dom
For: Sister

This module uses scikit-learn's Isolation Forest algorithm
to detect anomalous patterns in multi-dimensional feature space.
"""

from typing import List, Tuple, Optional
import numpy as np

# Check if sklearn is available
try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available. Install with: pip install scikit-learn")


class MLAnomalyDetector:
    """
    Machine Learning-based anomaly detection using Isolation Forest.
    
    Isolation Forest works by isolating anomalies through random partitioning.
    Anomalies are isolated more quickly than normal points.
    """
    
    def __init__(self, contamination: float = 0.05, random_state: int = 42):
        """
        Initialize ML anomaly detector.
        
        Args:
            contamination: Expected proportion of outliers (0.01 to 0.5)
            random_state: Random seed for reproducibility
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for ML detection")
        
        self.contamination = contamination
        self.random_state = random_state
        self.model = None
        self.is_trained = False
        self.feature_names = ['theta', 'slope', 'risk']
    
    def prepare_features(self, theta_values: List[float], 
                        slope_values: List[float],
                        risk_values: List[float]) -> np.ndarray:
        """
        Prepare feature matrix from raw values.
        
        Args:
            theta_values: List of theta readings
            slope_values: List of slope readings
            risk_values: List of risk readings
        
        Returns:
            X: Feature matrix (n_samples, 3 features)
        """
        if not (len(theta_values) == len(slope_values) == len(risk_values)):
            raise ValueError("All value lists must have same length")
        
        X = np.column_stack([theta_values, slope_values, risk_values])
        return X
    
    def train(self, theta_values: List[float], 
             slope_values: List[float],
             risk_values: List[float]) -> None:
        """
        Train Isolation Forest on baseline data.
        
        Should be trained on "normal" data to learn what's typical.
        
        Args:
            theta_values: Baseline theta readings
            slope_values: Baseline slope readings
            risk_values: Baseline risk readings
        """
        X = self.prepare_features(theta_values, slope_values, risk_values)
        
        if len(X) < 10:
            raise ValueError("Need at least 10 samples for training")
        
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=100,
            max_samples='auto',
            max_features=1.0
        )
        
        self.model.fit(X)
        self.is_trained = True
        
        print(f"✓ Model trained on {len(X)} baseline samples")
        print(f"  Contamination: {self.contamination}")
        print(f"  Expected outlier rate: {self.contamination * 100:.1f}%")
    
    def predict_anomaly(self, theta: float, slope: float, risk: float) -> Tuple[bool, float]:
        """
        Predict if current reading is anomalous.
        
        Args:
            theta: Current theta value
            slope: Current slope value
            risk: Current risk value
        
        Returns:
            tuple: (is_anomaly, anomaly_score)
                  - is_anomaly: True if classified as anomaly
                  - anomaly_score: Lower = more anomalous (range: roughly -0.5 to 0.5)
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction")
        
        X = self.prepare_features([theta], [slope], [risk])
        
        # Predict: -1 = anomaly, 1 = normal
        prediction = self.model.predict(X)[0]
        
        # Score: lower = more anomalous
        score = self.model.score_samples(X)[0]
        
        is_anomaly = (prediction == -1)
        
        return is_anomaly, score
    
    def predict_batch(self, theta_values: List[float],
                     slope_values: List[float],
                     risk_values: List[float]) -> Tuple[List[bool], List[float]]:
        """
        Predict anomalies for multiple readings.
        
        Args:
            theta_values: List of theta readings
            slope_values: List of slope readings
            risk_values: List of risk readings
        
        Returns:
            tuple: (anomaly_flags, anomaly_scores)
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction")
        
        X = self.prepare_features(theta_values, slope_values, risk_values)
        
        predictions = self.model.predict(X)
        scores = self.model.score_samples(X)
        
        anomaly_flags = [p == -1 for p in predictions]
        
        return anomaly_flags, scores.tolist()


def combined_detection(z_score_flag: bool, ml_flag: bool, 
                       risk: float, risk_threshold: float = 0.8) -> dict:
    """
    Combined detection using multiple independent methods.
    
    Triple confirmation approach:
    1. Z-score statistical anomaly
    2. ML-detected anomaly
    3. High absolute risk value
    
    Args:
        z_score_flag: True if Z-score detected anomaly
        ml_flag: True if ML detected anomaly
        risk: Current risk value (0-1)
        risk_threshold: Threshold for high risk
    
    Returns:
        dict: Detection results with confidence levels
    """
    high_risk = risk > risk_threshold
    
    # Count independent confirmations
    confirmations = sum([z_score_flag, ml_flag, high_risk])
    
    # Confidence levels
    if confirmations == 3:
        level = "CRITICAL"
        confidence = "HIGH"
        action = "🔴 IMMEDIATE ALERT"
    elif confirmations == 2:
        level = "ELEVATED"
        confidence = "MEDIUM"
        action = "🟡 WATCHFUL"
    elif confirmations == 1:
        level = "CAUTION"
        confidence = "LOW"
        action = "🟢 MONITOR"
    else:
        level = "NORMAL"
        confidence = "N/A"
        action = "🟢 STABLE"
    
    return {
        'level': level,
        'confidence': confidence,
        'action': action,
        'confirmations': confirmations,
        'z_score_flag': z_score_flag,
        'ml_flag': ml_flag,
        'high_risk': high_risk
    }


class AdaptiveSensitivity:
    """
    Adaptive sensitivity adjustment based on false positive rate.
    
    If too many false positives, increase threshold.
    If missing events, decrease threshold.
    """
    
    def __init__(self, initial_contamination: float = 0.05,
                 min_contamination: float = 0.01,
                 max_contamination: float = 0.15):
        """
        Initialize adaptive sensitivity controller.
        
        Args:
            initial_contamination: Starting contamination level
            min_contamination: Minimum sensitivity (fewer detections)
            max_contamination: Maximum sensitivity (more detections)
        """
        self.contamination = initial_contamination
        self.min_contamination = min_contamination
        self.max_contamination = max_contamination
        
        self.false_positive_count = 0
        self.true_positive_count = 0
        self.adjustment_interval = 50  # Adjust every N readings
        self.reading_count = 0
    
    def record_result(self, was_true_event: bool):
        """
        Record whether detection was true positive or false positive.
        
        Args:
            was_true_event: True if detection was confirmed as real event
        """
        self.reading_count += 1
        
        if was_true_event:
            self.true_positive_count += 1
        else:
            self.false_positive_count += 1
    
    def adjust_sensitivity(self) -> float:
        """
        Adjust contamination parameter based on recorded results.
        
        Returns:
            New contamination level
        """
        if self.reading_count < self.adjustment_interval:
            return self.contamination
        
        # Calculate false positive rate
        total = self.false_positive_count + self.true_positive_count
        if total == 0:
            return self.contamination
        
        fp_rate = self.false_positive_count / total
        
        # Adjust: high FP rate → decrease sensitivity (lower contamination)
        # Low FP rate → can increase sensitivity (higher contamination)
        if fp_rate > 0.2:  # Too many false positives
            self.contamination = max(self.min_contamination, 
                                    self.contamination * 0.8)
            print(f"⚙️ Reducing sensitivity: contamination={self.contamination:.3f}")
        elif fp_rate < 0.05:  # Very few false positives
            self.contamination = min(self.max_contamination,
                                    self.contamination * 1.2)
            print(f"⚙️ Increasing sensitivity: contamination={self.contamination:.3f}")
        
        # Reset counters
        self.false_positive_count = 0
        self.true_positive_count = 0
        self.reading_count = 0
        
        return self.contamination


if __name__ == "__main__":
    """
    Demonstration of ML anomaly detection system.
    """
    print("=" * 60)
    print("TRIG6 MACHINE LEARNING DETECTION SYSTEM")
    print("Isolation Forest Anomaly Detection")
    print("=" * 60)
    print()
    
    if not SKLEARN_AVAILABLE:
        print("ERROR: scikit-learn not installed")
        print("Install with: pip install scikit-learn")
        exit(1)
    
    # Generate synthetic baseline data (normal operation)
    np.random.seed(42)
    n_baseline = 100
    
    baseline_theta = np.random.normal(45, 5, n_baseline).tolist()
    baseline_slope = np.random.normal(1.0, 0.5, n_baseline).tolist()
    baseline_risk = np.random.normal(0.3, 0.1, n_baseline).clip(0, 1).tolist()
    
    # Create and train detector
    detector = MLAnomalyDetector(contamination=0.05)
    detector.train(baseline_theta, baseline_slope, baseline_risk)
    print()
    
    # Test on normal and anomalous readings
    print("Testing on sample readings:")
    print("-" * 60)
    
    test_cases = [
        (46, 1.2, 0.32, "Normal baseline"),
        (48, 1.5, 0.35, "Normal variation"),
        (75, 5.0, 0.65, "Elevated but gradual"),
        (85, 12.0, 0.89, "Sudden spike - ANOMALY"),
        (88, 15.0, 0.95, "Critical - ANOMALY"),
    ]
    
    for theta, slope, risk, description in test_cases:
        is_anomaly, score = detector.predict_anomaly(theta, slope, risk)
        
        # Simulate Z-score flag (would come from trig6_neuro_patterns.py)
        z_score_flag = theta > 80 or risk > 0.8
        
        # Combined detection
        result = combined_detection(z_score_flag, is_anomaly, risk)
        
        print(f"{description}:")
        print(f"  Values: θ={theta:.1f}° slope={slope:.1f}°/s risk={risk:.2f}")
        print(f"  ML Score: {score:.3f} (lower = more anomalous)")
        print(f"  ML Flag: {'🔴 ANOMALY' if is_anomaly else '🟢 NORMAL'}")
        print(f"  Combined: {result['action']} ({result['confidence']} confidence)")
        print(f"  Confirmations: {result['confirmations']}/3")
        print()
    
    print("=" * 60)
    print("Triple confirmation reduces false positives.")
    print("Z-score + ML + High Risk = High confidence alert.")
    print("Built with machine learning for Sister 💜")
    print("=" * 60)
