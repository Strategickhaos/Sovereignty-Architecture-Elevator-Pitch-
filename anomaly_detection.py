#!/usr/bin/env python3
"""
Kubernetes Log Anomaly Detection Module
Strategickhaos DAO LLC - KHAOS Methodology Implementation
Phase 2: Statistical Anomaly Detection via Z-score Analysis

Converts potential energy (raw logs) into kinetic actions through
hierarchical autonomous orchestration.
"""

try:
    import numpy as np
except ImportError:
    raise ImportError(
        "numpy is required for anomaly detection. Install with: pip install numpy>=1.24.0"
    )

try:
    import pandas as pd
except ImportError:
    raise ImportError(
        "pandas is required for anomaly detection. Install with: pip install pandas>=2.0.0"
    )

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError(
        "matplotlib is required for visualization. Install with: pip install matplotlib>=3.7.0"
    )

from typing import Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime


class KubernetesAnomalyDetector:
    """
    Detects anomalies in Kubernetes log volumes using Z-score statistical method.
    
    Part of the KHAOS (Kinetic Hierarchical Autonomous Orchestration System) methodology,
    this detector transforms static log data (potential energy) into actionable insights
    (kinetic energy) for autonomous system responses.
    """
    
    def __init__(self, threshold: float = 3.0):
        """
        Initialize the anomaly detector.
        
        Parameters:
        - threshold: float, Z-score threshold for flagging anomalies (default 3.0 for ~99.7% confidence)
        """
        self.threshold = threshold
        self.mean = None
        self.std = None
        
    def detect_anomalies(self, log_data: pd.DataFrame) -> pd.DataFrame:
        """
        Detects anomalies in log counts using Z-score analysis.
        
        Note: This function creates a copy of the input DataFrame to avoid side effects.
        
        Parameters:
        - log_data: pd.DataFrame with 'timestamp' (datetime) and 'log_count' (float/int) columns
        
        Returns:
        - pd.DataFrame with added 'z_score' and 'anomaly' columns
        
        Raises:
        - ValueError: If log data is empty or standard deviation is zero
        """
        if log_data.empty:
            raise ValueError("Log data is empty.")
        
        # Create a copy to avoid modifying the input DataFrame
        log_data = log_data.copy()
        
        # Calculate mean and standard deviation
        self.mean = log_data['log_count'].mean()
        self.std = log_data['log_count'].std()
        
        if self.std == 0:
            raise ValueError("Standard deviation is zero; cannot compute Z-scores.")
        
        # Compute Z-scores
        log_data['z_score'] = (log_data['log_count'] - self.mean) / self.std
        
        # Flag anomalies
        log_data['anomaly'] = np.abs(log_data['z_score']) > self.threshold
        
        return log_data
    
    def get_anomaly_summary(self, log_data: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for anomaly detection results.
        
        Parameters:
        - log_data: pd.DataFrame with anomaly detection results
        
        Returns:
        - Dict with summary statistics
        """
        if 'anomaly' not in log_data.columns:
            raise ValueError("Data must be processed with detect_anomalies first")
        
        anomalies = log_data[log_data['anomaly']]
        
        return {
            'total_records': len(log_data),
            'anomaly_count': len(anomalies),
            'anomaly_rate': len(anomalies) / len(log_data) if len(log_data) > 0 else 0,
            'mean_log_count': self.mean,
            'std_log_count': self.std,
            'threshold': self.threshold,
            'max_z_score': log_data['z_score'].abs().max() if len(log_data) > 0 else 0,
            'anomaly_timestamps': anomalies['timestamp'].tolist() if len(anomalies) > 0 else []
        }
    
    def visualize_anomalies(
        self, 
        log_data: pd.DataFrame, 
        title: str = "Kubernetes Log Volume with Detected Anomalies",
        save_path: Optional[str] = None,
        show: bool = False
    ) -> None:
        """
        Visualize log counts with anomalies highlighted.
        
        Parameters:
        - log_data: pd.DataFrame with anomaly detection results
        - title: str, plot title
        - save_path: Optional[str], path to save the figure (if None, uses default)
        - show: bool, whether to display the plot (default False for production)
        """
        if 'anomaly' not in log_data.columns:
            raise ValueError("Data must be processed with detect_anomalies first")
        
        plt.figure(figsize=(12, 6))
        
        # Plot log counts
        plt.plot(log_data['timestamp'], log_data['log_count'], label='Log Count', color='blue', linewidth=1.5)
        
        # Highlight anomalies
        anomalies = log_data[log_data['anomaly']]
        if len(anomalies) > 0:
            plt.scatter(
                anomalies['timestamp'], 
                anomalies['log_count'], 
                color='red', 
                label='Anomalies', 
                s=100, 
                zorder=5,
                edgecolors='darkred',
                linewidth=2
            )
        
        # Add mean line
        plt.axhline(y=self.mean, color='green', linestyle='--', label='Mean', linewidth=1.5)
        
        # Labels and formatting
        plt.xlabel('Timestamp', fontsize=12)
        plt.ylabel('Log Count', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save or show
        if save_path:
            try:
                # Ensure directory exists
                save_dir = Path(save_path).parent
                if save_dir and not save_dir.exists():
                    save_dir.mkdir(parents=True, exist_ok=True)
                plt.savefig(save_path, dpi=150, bbox_inches='tight')
                print(f"✅ Visualization saved to: {save_path}")
            except (OSError, IOError) as e:
                print(f"⚠️ Failed to save visualization to {save_path}: {e}")
        elif not show:
            # Default save path
            default_path = f"anomalies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            try:
                plt.savefig(default_path, dpi=150, bbox_inches='tight')
                print(f"✅ Visualization saved to: {default_path}")
            except (OSError, IOError) as e:
                print(f"⚠️ Failed to save visualization to {default_path}: {e}")
        
        if show:
            plt.show()
        
        plt.close()


def generate_simulated_data(
    periods: int = 100,
    mean: float = 100.0,
    std: float = 10.0,
    anomaly_points: Optional[Dict[int, float]] = None,
    freq: str = 'h'
) -> pd.DataFrame:
    """
    Generate simulated log data for testing and demonstration.
    
    Parameters:
    - periods: int, number of time periods
    - mean: float, mean log count
    - std: float, standard deviation for normal distribution
    - anomaly_points: Optional[Dict[int, float]], dict mapping indices to anomalous values
    - freq: str, pandas frequency string ('h' for hourly, 'D' for daily, etc.)
    
    Returns:
    - pd.DataFrame with 'timestamp' and 'log_count' columns
    """
    # Generate timestamps
    timestamps = pd.date_range(start='2025-12-01', periods=periods, freq=freq)
    
    # Generate normal log counts
    log_counts = np.random.normal(mean, std, periods)
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'log_count': log_counts
    })
    
    # Inject anomalies if specified
    if anomaly_points:
        for idx, value in anomaly_points.items():
            if 0 <= idx < periods:
                df.loc[idx, 'log_count'] = value
    
    return df


def cross_cluster_analysis(
    cluster_data: Dict[str, pd.DataFrame],
    threshold: float = 3.0
) -> Tuple[pd.DataFrame, Dict]:
    """
    Perform cross-cluster anomaly detection and correlation.
    
    Parameters:
    - cluster_data: Dict[str, pd.DataFrame], mapping cluster names to log data
    - threshold: float, Z-score threshold
    
    Returns:
    - Tuple of (combined_anomalies, cluster_summaries)
    """
    detector = KubernetesAnomalyDetector(threshold=threshold)
    cluster_summaries = {}
    all_anomalies = []
    
    for cluster_name, data in cluster_data.items():
        # Detect anomalies for this cluster
        processed_data = detector.detect_anomalies(data.copy())
        summary = detector.get_anomaly_summary(processed_data)
        
        # Add cluster identifier
        anomalies = processed_data[processed_data['anomaly']].copy()
        anomalies['cluster'] = cluster_name
        
        cluster_summaries[cluster_name] = summary
        all_anomalies.append(anomalies)
    
    # Combine all anomalies (sort=False for better performance)
    combined_anomalies = pd.concat(all_anomalies, ignore_index=True, sort=False) if all_anomalies else pd.DataFrame()
    
    return combined_anomalies, cluster_summaries


def main():
    """
    Example usage demonstrating anomaly detection on simulated Kubernetes log data.
    """
    print("=" * 80)
    print("Kubernetes Log Anomaly Detection - KHAOS Methodology")
    print("Strategickhaos DAO LLC")
    print("=" * 80)
    print()
    
    # Generate simulated data with injected anomalies
    print("📊 Generating simulated log data (100 hours)...")
    anomaly_points = {
        20: 150,   # Moderate high (potential scheduling spike)
        40: 50,    # Moderate low (possible health check failure)
        60: 200,   # Extreme high (anomaly like API overload)
        80: 30     # Extreme low (downtime indicator)
    }
    
    df = generate_simulated_data(
        periods=100,
        mean=100.0,
        std=10.0,
        anomaly_points=anomaly_points,
        freq='h'
    )
    
    print(f"✅ Generated {len(df)} data points")
    print()
    
    # Initialize detector and run analysis
    print("🔍 Running anomaly detection (Z-score threshold: 3.0)...")
    detector = KubernetesAnomalyDetector(threshold=3.0)
    
    try:
        anomaly_df = detector.detect_anomalies(df)
        print("✅ Anomaly detection complete")
        print()
        
        # Display detected anomalies
        anomalies = anomaly_df[anomaly_df['anomaly']]
        print(f"🚨 Detected {len(anomalies)} Anomalies:")
        print("-" * 80)
        
        if len(anomalies) > 0:
            for idx, row in anomalies.iterrows():
                timestamp = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                log_count = row['log_count']
                z_score = row['z_score']
                print(f"  [{timestamp}] Log Count: {log_count:.2f} | Z-score: {z_score:.2f}")
        else:
            print("  No anomalies detected")
        
        print()
        
        # Display summary statistics
        summary = detector.get_anomaly_summary(anomaly_df)
        print("📈 Summary Statistics:")
        print("-" * 80)
        print(f"  Total Records: {summary['total_records']}")
        print(f"  Anomaly Count: {summary['anomaly_count']}")
        print(f"  Anomaly Rate: {summary['anomaly_rate']:.2%}")
        print(f"  Mean Log Count: {summary['mean_log_count']:.2f}")
        print(f"  Std Deviation: {summary['std_log_count']:.2f}")
        print(f"  Max Z-score: {summary['max_z_score']:.2f}")
        print()
        
        # Generate visualization
        print("📊 Generating visualization...")
        detector.visualize_anomalies(
            anomaly_df,
            title="Kubernetes Log Volume with Detected Anomalies (Simulated Data)"
        )
        print()
        
        # Cross-cluster example
        print("🌐 Cross-Cluster Analysis Example:")
        print("-" * 80)
        
        # Simulate data from multiple clusters
        cluster_data = {
            'red-team': generate_simulated_data(50, mean=120, std=15, anomaly_points={10: 200, 30: 40}),
            'jarvis-swarm-personal-001': generate_simulated_data(50, mean=80, std=12, anomaly_points={15: 150, 35: 20})
        }
        
        combined_anomalies, cluster_summaries = cross_cluster_analysis(cluster_data, threshold=3.0)
        
        for cluster_name, summary in cluster_summaries.items():
            print(f"\n  {cluster_name}:")
            print(f"    Anomalies: {summary['anomaly_count']}/{summary['total_records']} ({summary['anomaly_rate']:.2%})")
            print(f"    Mean: {summary['mean_log_count']:.2f} ± {summary['std_log_count']:.2f}")
        
        print()
        print("=" * 80)
        print("✅ Analysis Complete - Ready for SynapseBus Integration")
        print("=" * 80)
        
    except ValueError as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
