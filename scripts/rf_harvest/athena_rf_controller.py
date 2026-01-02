#!/usr/bin/env python3
"""
Athena RF Orchestrator
Manages spectrum scanning, WiFi hunting, LoRa mesh, and auto-failover

Usage: sudo python3 athena_rf_controller.py
"""
import subprocess
import time
import json
import os
from datetime import datetime
import signal
import sys

class RFOrchestrator:
    def __init__(self):
        self.interfaces = {
            'sdr': '/dev/rtl_sdr',
            'wifi': 'wlan1',
            'lora': '/dev/ttyUSB0',
            'cellular': 'usb0'
        }
        self.active_connection = None
        self.running = True
        self.scan_interval = 3600  # Spectrum scan every hour
        self.wifi_hunt_interval = 900  # WiFi hunt every 15 minutes
        self.last_spectrum_scan = 0
        self.last_wifi_hunt = 0
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n[*] Shutting down RF Orchestrator...")
        self.running = False
    
    def check_interface_status(self, interface):
        """Check if network interface is up and has connectivity"""
        try:
            result = subprocess.run(['ip', 'addr', 'show', interface], 
                                  capture_output=True, text=True, timeout=5)
            if 'UP' in result.stdout:
                # Test connectivity
                ping = subprocess.run(['ping', '-c', '1', '-W', '2', '-I', interface, '8.8.8.8'],
                                    capture_output=True, timeout=5)
                return ping.returncode == 0
        except Exception as e:
            return False
        return False
    
    def check_sdr(self):
        """Check if RTL-SDR is available"""
        try:
            result = subprocess.run(['rtl_test', '-t'], 
                                  capture_output=True, text=True, timeout=5)
            return 'Found' in result.stdout
        except:
            return False
    
    def scan_spectrum(self):
        """Trigger spectrum scan"""
        if not self.check_sdr():
            print("[!] RTL-SDR not detected. Skipping spectrum scan.")
            return
        
        print("[*] Initiating spectrum scan...")
        timestamp = int(time.time())
        output_file = f'/tmp/spectrum_{timestamp}.csv'
        
        try:
            # Run rtl_power in background (10 minute scan)
            process = subprocess.Popen(['rtl_power', '-f', '100M:1.7G:1M', '-g', '50', 
                             '-i', '10m', output_file],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE)
            
            # Check if process started successfully
            time.sleep(1)
            if process.poll() is not None:
                stderr = process.stderr.read().decode('utf-8')
                print(f"[!] rtl_power failed to start: {stderr}")
                return
            
            print(f"[+] Spectrum scan started. Output: {output_file}")
            self.last_spectrum_scan = time.time()
        except FileNotFoundError:
            print("[!] rtl_power not found. Install with: sudo apt install rtl-sdr")
        except Exception as e:
            print(f"[!] Failed to start spectrum scan: {e}")
    
    def hunt_wifi(self):
        """Auto-hunt for best open WiFi"""
        print("[*] Hunting for open WiFi networks...")
        
        # Check if wifi_hunter.py exists and is executable
        script_path = 'scripts/rf_harvest/wifi_hunter.py'
        if not os.path.exists(script_path):
            print(f"[!] WiFi hunter script not found at {script_path}")
            return
        
        if not os.access(script_path, os.X_OK):
            print(f"[!] WiFi hunter script is not executable. Run: chmod +x {script_path}")
            return
        
        try:
            subprocess.run(['python3', script_path, self.interfaces['wifi'], '30'],
                         timeout=60)
        except subprocess.TimeoutExpired:
            print("[!] WiFi hunt timed out")
        except Exception as e:
            print(f"[!] WiFi hunt error: {e}")
        
        self.last_wifi_hunt = time.time()
    
    def monitor_lora_mesh(self):
        """Check LoRa mesh status"""
        try:
            # Check if meshtastic is installed
            subprocess.run(['which', 'meshtastic'], check=True, capture_output=True)
            
            # Check if device exists
            if not os.path.exists(self.interfaces['lora']):
                return False
            
            result = subprocess.run(['meshtastic', '--info', '--port', self.interfaces['lora']],
                                  capture_output=True, text=True, timeout=10)
            return 'Connected' in result.stdout or 'Owner' in result.stdout
        except:
            return False
    
    def auto_failover(self):
        """Automatically switch to best available connection"""
        priority = ['wifi', 'cellular', 'lora']
        
        for conn_type in priority:
            interface = self.interfaces.get(conn_type)
            if not interface:
                continue
            
            # Special handling for LoRa (not a network interface)
            if conn_type == 'lora':
                if self.monitor_lora_mesh():
                    if self.active_connection != conn_type:
                        print(f"[+] LoRa mesh available")
                        self.active_connection = conn_type
                    return True
                continue
            
            # Check network interfaces
            if self.check_interface_status(interface):
                if self.active_connection != conn_type:
                    print(f"[+] Switching to {conn_type} ({interface})")
                    self.active_connection = conn_type
                return True
        
        if self.active_connection is not None:
            print("[!] No active connections available")
            self.active_connection = None
        return False
    
    def print_status(self):
        """Print current system status"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] RF Sovereignty Status")
        print("=" * 60)
        
        # SDR status
        sdr_status = "Online" if self.check_sdr() else "Offline"
        print(f"  RTL-SDR:     {sdr_status}")
        
        # Network interfaces
        for name, interface in self.interfaces.items():
            if name in ['sdr', 'lora']:
                continue
            status = "Online" if self.check_interface_status(interface) else "Offline"
            active = " [ACTIVE]" if name == self.active_connection else ""
            print(f"  {name.capitalize():<12} {interface:<10} {status}{active}")
        
        # LoRa mesh
        lora_status = "Online" if self.monitor_lora_mesh() else "Offline"
        active = " [ACTIVE]" if 'lora' == self.active_connection else ""
        print(f"  LoRa Mesh:   {lora_status}{active}")
        
        print("=" * 60)
    
    def run(self):
        """Main orchestration loop"""
        print("=" * 60)
        print("  🔥 ATHENA RF ORCHESTRATOR - INV-086")
        print("  Spectrum Sovereignty Control System")
        print("=" * 60)
        print(f"[*] Started: {datetime.now().isoformat()}")
        print(f"[*] Press Ctrl+C to stop\n")
        
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Initial scan
        self.scan_spectrum()
        
        while self.running:
            # Print status
            self.print_status()
            
            # Auto-failover to best connection
            self.auto_failover()
            
            # Periodic spectrum scan
            if time.time() - self.last_spectrum_scan > self.scan_interval:
                self.scan_spectrum()
            
            # Periodic WiFi hunt
            if time.time() - self.last_wifi_hunt > self.wifi_hunt_interval:
                self.hunt_wifi()
            
            # Sleep before next check (60 seconds)
            for _ in range(60):
                if not self.running:
                    break
                time.sleep(1)
        
        print("\n[*] RF Orchestrator stopped")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] This script requires root privileges")
        print("[!] Run with: sudo python3 athena_rf_controller.py")
        sys.exit(1)
    
    orchestrator = RFOrchestrator()
    orchestrator.run()
