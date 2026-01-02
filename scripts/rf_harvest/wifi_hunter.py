#!/usr/bin/env python3
"""
WiFi Auto-Hunter: Scans for open WiFi networks and ranks by signal strength

Usage: python3 wifi_hunter.py [interface] [duration_seconds]
Example: python3 wifi_hunter.py wlan1 30
"""
import subprocess
import re
import time
import os
from datetime import datetime
import sys

def scan_wifi(interface='wlan1', duration=30):
    """Scan for WiFi networks using airodump-ng"""
    # Validate interface name (alphanumeric and common chars only)
    if not re.match(r'^[a-zA-Z0-9_-]+$', interface):
        print(f"[!] Invalid interface name: {interface}")
        return []
    
    # Validate duration
    try:
        duration = int(duration)
        if duration < 1 or duration > 600:
            print(f"[!] Duration must be between 1 and 600 seconds")
            return []
    except ValueError:
        print(f"[!] Invalid duration: {duration}")
        return []
    
    print(f"[*] Scanning WiFi on {interface} for {duration} seconds...")
    print(f"[*] Ensure {interface} is in monitor mode:")
    print(f"    sudo ip link set {interface} down")
    print(f"    sudo iw dev {interface} set monitor none")
    print(f"    sudo ip link set {interface} up")
    
    # Create output file
    output_file = f"/tmp/wifi_scan_{int(time.time())}"
    
    # Run airodump-ng with validated parameters (no shell=True)
    cmd = ['sudo', 'timeout', str(duration), 'airodump-ng', interface, 
           '-w', output_file, '--output-format', 'csv']
    
    print(f"[*] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    if result.returncode != 0 and result.returncode != 124:  # 124 = timeout (expected)
        stderr = result.stderr.decode('utf-8')
        print(f"[!] airodump-ng failed. Error: {stderr}")
        print(f"[!] Ensure airodump-ng is installed: sudo apt install aircrack-ng")
        return []
    
    # Parse CSV output
    csv_file = f"{output_file}-01.csv"
    try:
        with open(csv_file, 'r', errors='ignore') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[!] No scan data found. Ensure {interface} is in monitor mode.")
        return []
    
    networks = []
    in_ap_section = False
    
    for line in lines:
        # Skip until we reach AP section
        if 'BSSID' in line and 'Station' not in line:
            in_ap_section = True
            continue
        
        # Stop at station section
        if 'Station' in line:
            break
        
        if not in_ap_section:
            continue
        
        # Skip empty lines
        if not line.strip():
            continue
        
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 14:
            continue
        
        bssid = parts[0]
        power = parts[8]
        encryption = parts[5]
        essid = parts[13]
        
        # Filter for open networks or guest networks
        if 'OPN' in encryption or not encryption or encryption == ' ':
            try:
                power_int = int(power) if power and power.strip() != '' else -100
                networks.append({
                    'bssid': bssid,
                    'essid': essid if essid else '(Hidden)',
                    'power': power_int,
                    'encryption': 'Open'
                })
            except ValueError:
                continue
    
    # Sort by signal strength (higher = better, closer to 0)
    networks.sort(key=lambda x: x['power'], reverse=True)
    
    # Clean up temporary files
    try:
        os.remove(csv_file)
        for ext in ['-01.cap', '-01.kismet.csv', '-01.kismet.netxml', '-01.log.csv']:
            temp_file = output_file + ext
            if os.path.exists(temp_file):
                os.remove(temp_file)
    except:
        pass
    
    return networks

def print_results(networks):
    """Display scan results"""
    print(f"\n[+] Found {len(networks)} open WiFi networks:")
    print("=" * 85)
    print(f"{'RANK':<6} {'SIGNAL':<8} {'BSSID':<20} {'ESSID':<35} {'QUALITY'}")
    print("=" * 85)
    
    for i, net in enumerate(networks, 1):
        if net['power'] > -50:
            quality = "Excellent"
        elif net['power'] > -70:
            quality = "Good"
        elif net['power'] > -80:
            quality = "Weak"
        else:
            quality = "Very Weak"
        
        print(f"{i:<6} {net['power']:<8} {net['bssid']:<20} {net['essid']:<35} {quality}")
    
    if networks:
        best_ssid = networks[0]['essid']
        # Escape single quotes in SSID for shell safety
        safe_ssid = best_ssid.replace("'", "'\\''")
        
        print(f"\n[+] Best target: {best_ssid} ({networks[0]['power']} dBm)")
        print(f"[+] BSSID: {networks[0]['bssid']}")
        print(f"\n[*] To connect:")
        print(f"    # Exit monitor mode first:")
        print(f"    sudo ip link set {interface} down")
        print(f"    sudo iw dev {interface} set type managed")
        print(f"    sudo ip link set {interface} up")
        print(f"    # Connect (use nmcli to safely handle special characters):")
        print(f"    sudo nmcli device wifi connect '{safe_ssid}'")
    else:
        print("\n[!] No open networks found. Try:")
        print("    - Moving to a different location")
        print("    - Using a directional antenna")
        print("    - Scanning for longer duration")

def check_requirements():
    """Check if required tools are installed"""
    try:
        subprocess.run(['which', 'airodump-ng'], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("[!] airodump-ng not found. Install with:")
        print("    sudo apt install aircrack-ng")
        return False
    
    return True

if __name__ == "__main__":
    if not check_requirements():
        sys.exit(1)
    
    interface = sys.argv[1] if len(sys.argv) > 1 else 'wlan1'
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    print(f"\n[*] WiFi Auto-Hunter - INV-086 RF Sovereignty")
    print(f"[*] Interface: {interface}")
    print(f"[*] Duration: {duration} seconds")
    print(f"[*] Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    networks = scan_wifi(interface, duration)
    print_results(networks)
    
    print(f"\n[*] Scan complete. Results valid as of {datetime.now().strftime('%H:%M:%S')}")
    print(f"[*] Remember: Only connect to legitimately open/public networks.")
    print(f"[*] Cracking WPA passwords is illegal under CFAA.")
