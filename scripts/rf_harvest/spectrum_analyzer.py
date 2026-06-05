#!/usr/bin/env python3
"""
RTL-SDR Spectrum Analyzer and Visualization
Analyzes rtl_power CSV output and identifies active frequencies

Usage: python3 spectrum_analyzer.py <rtl_power_csv_file>
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import sys

def analyze_spectrum(csv_file):
    """Load and analyze spectrum CSV from rtl_power"""
    print(f"[*] Loading spectrum data from {csv_file}...")
    
    try:
        # rtl_power CSV format: date, time, Hz low, Hz high, Hz step, samples, dB values...
        df = pd.read_csv(csv_file, header=None)
    except FileNotFoundError:
        print(f"[!] Error: File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error reading CSV: {e}")
        sys.exit(1)
    
    # Extract frequency data (columns 2-5) and power levels (6+)
    freq_start = df.iloc[:, 2]
    freq_stop = df.iloc[:, 3]
    power_data = df.iloc[:, 6:]
    
    # Calculate center frequencies
    center_freqs = (freq_start + freq_stop) / 2 / 1e6  # Convert to MHz
    
    # Average power across time
    avg_power = power_data.mean(axis=1)
    max_power = power_data.max(axis=1)
    
    # Find peaks (active frequencies)
    threshold = avg_power.mean() + (avg_power.std() * 2)
    peaks = avg_power[avg_power > threshold]
    
    print(f"\n[+] Analysis Results:")
    print(f"    Frequency Range: {center_freqs.min():.2f} - {center_freqs.max():.2f} MHz")
    print(f"    Average Power: {avg_power.mean():.2f} dB")
    print(f"    Detected Peaks: {len(peaks)}")
    
    print(f"\n[+] Top 10 Active Frequencies:")
    peak_freqs = center_freqs[avg_power > threshold].values
    peak_powers = avg_power[avg_power > threshold].values
    
    if len(peak_freqs) > 0:
        sorted_idx = np.argsort(peak_powers)[::-1][:min(10, len(peak_freqs))]
        
        for idx in sorted_idx:
            freq = peak_freqs[idx]
            power = peak_powers[idx]
            band = identify_band(freq)
            print(f"    {freq:8.2f} MHz | {power:6.2f} dB | {band}")
    else:
        print("    No significant peaks detected above threshold")
    
    # Generate visualization
    plt.figure(figsize=(14, 6))
    plt.plot(center_freqs, avg_power, linewidth=0.5, alpha=0.7, label='Average Power')
    plt.plot(center_freqs, max_power, linewidth=0.3, alpha=0.5, label='Peak Power')
    plt.axhline(y=threshold, color='r', linestyle='--', alpha=0.5, label='Detection Threshold')
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Power (dB)')
    plt.title(f'Spectrum Analysis - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file = csv_file.replace('.csv', '_plot.png')
    plt.savefig(output_file, dpi=150)
    print(f"\n[+] Plot saved to {output_file}")
    
    return center_freqs, avg_power

def identify_band(freq_mhz):
    """Identify service/band for a given frequency"""
    if 88 <= freq_mhz <= 108:
        return "FM Radio"
    elif 162 <= freq_mhz <= 174:
        return "Marine VHF"
    elif 400 <= freq_mhz <= 512:
        return "UHF/Public Safety"
    elif 433.8 <= freq_mhz <= 434.0:
        return "ISM 433 MHz (IoT)"
    elif 862 <= freq_mhz <= 928:
        return "ISM 900 MHz (LoRa/Cellular)"
    elif 2400 <= freq_mhz <= 2500:
        return "2.4 GHz WiFi/Bluetooth"
    elif 5150 <= freq_mhz <= 5925:
        return "5 GHz WiFi"
    elif 5925 <= freq_mhz <= 7125:
        return "6 GHz WiFi 6E/7"
    else:
        return "Unknown/Other"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 spectrum_analyzer.py <rtl_power_csv_file>")
        print("\nExample:")
        print("  # First, capture spectrum data:")
        print("  rtl_power -f 100M:1.7G:1M -g 50 -i 10m spectrum_scan.csv")
        print("  # Then analyze it:")
        print("  python3 spectrum_analyzer.py spectrum_scan.csv")
        sys.exit(1)
    
    analyze_spectrum(sys.argv[1])
