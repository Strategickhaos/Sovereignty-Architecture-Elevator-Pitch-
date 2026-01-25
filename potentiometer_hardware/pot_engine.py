#!/usr/bin/env python3
"""
POTENTIOMETER PROOF ENGINE - Python TRIG6 Interface

Connects to Arduino-based potentiometer hardware and computes
TRIG6 fitness metrics for material science validation.

Author: Dominic Thibodeau (StrategicKhaos)
Date: 2026-01-25
License: Prior Art for Patent Protection

Requirements:
    pip install pyserial numpy

Usage:
    python pot_engine.py --port /dev/ttyUSB0 --process papyrus
"""

import serial
import math
import time
import argparse
import sys
from typing import Dict, Tuple, Optional
import json

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class PotentiometerProofEngine:
    """
    Main engine for converting potentiometer input to TRIG6 fitness metrics.
    """
    
    def __init__(self, port: str = '/dev/ttyUSB0', baud: int = 9600):
        """
        Initialize connection to Arduino potentiometer.
        
        Args:
            port: Serial port path (e.g., '/dev/ttyUSB0', 'COM3')
            baud: Baud rate (default: 9600)
        """
        self.port = port
        self.baud = baud
        self.serial = None
        self.theta_min = 0
        self.theta_max = math.pi / 2  # Maximum complexity (danger zone)
        
        # Try to connect
        self.connect()
    
    def connect(self):
        """Establish serial connection to Arduino."""
        try:
            self.serial = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)  # Wait for Arduino reset
            print(f"{Colors.GREEN}✓ Connected to potentiometer on {self.port}{Colors.END}")
            
            # Read and display startup message
            for _ in range(5):
                line = self.serial.readline().decode('utf-8').strip()
                if line.startswith('#'):
                    print(f"{Colors.BLUE}{line}{Colors.END}")
        except serial.SerialException as e:
            print(f"{Colors.RED}✗ Failed to connect: {e}{Colors.END}")
            print(f"{Colors.YELLOW}Available ports:{Colors.END}")
            self.list_ports()
            sys.exit(1)
    
    @staticmethod
    def list_ports():
        """List available serial ports."""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            for port in ports:
                print(f"  - {port.device}: {port.description}")
        except ImportError:
            print("  (Install 'pyserial' to list ports)")
    
    def read_potentiometer(self) -> Tuple[Optional[float], Optional[float]]:
        """
        Read position and noise from potentiometer.
        
        Returns:
            (position, noise) tuple, or (None, None) if read failed
        """
        try:
            line = self.serial.readline().decode('utf-8').strip()
            
            # Skip comment lines
            if line.startswith('#') or not line:
                return None, None
            
            # Parse CSV format: position,noise
            if ',' in line:
                parts = line.split(',')
                position = float(parts[0])
                noise = float(parts[1])
                return position, noise
            
            return None, None
        except (ValueError, UnicodeDecodeError, serial.SerialException):
            return None, None
    
    def compute_trig6(self, position: float, noise: float, 
                      R: float, D: float, alpha: float) -> Dict:
        """
        Compute TRIG6 fitness from potentiometer input.
        
        Args:
            position: Potentiometer position (0.0-1.0)
            noise: Voltage fluctuation standard deviation
            R: Resource efficiency (0-1)
            D: Drift (0-1)
            alpha: Damping (0-1)
        
        Returns:
            Dictionary with TRIG6 parameters and fitness
        """
        # Map position to phase angle (0 to π/2)
        theta = position * self.theta_max
        
        # Map noise to TRIG6 noise parameter
        # Scale noise (typically 0.001-0.05) to meaningful range (0-0.5)
        N = min(noise * 10, 0.5)
        
        # Calculate fitness
        fitness = R * (1 - D) * (1 - N) * math.exp(-alpha)
        
        return {
            'theta': theta,
            'theta_deg': math.degrees(theta),
            'R': R,
            'D': D,
            'N': N,
            'alpha': alpha,
            'fitness': fitness,
            'position': position,
            'noise': noise
        }
    
    def get_fitness_status(self, fitness: float) -> Tuple[str, str]:
        """
        Get color-coded status based on fitness value.
        
        Returns:
            (status_text, color_code) tuple
        """
        if fitness >= 0.70:
            return "✓ EXCEPTIONAL", Colors.GREEN
        elif fitness >= 0.55:
            return "✓ ARCHIVAL", Colors.GREEN
        elif fitness >= 0.44:
            return "⚠ DURABLE", Colors.YELLOW
        elif fitness >= 0.33:
            return "⚠ FUNCTIONAL", Colors.ORANGE
        else:
            return "✗ UNSTABLE", Colors.RED
    
    def prove_process(self, process_name: str, R: float, D: float, 
                      alpha: float, threshold: float = 0.55,
                      duration: Optional[int] = None,
                      log_file: Optional[str] = None):
        """
        Interactive proof of process stability.
        
        Args:
            process_name: Name of process being tested
            R: Resource efficiency
            D: Drift
            alpha: Damping
            threshold: Minimum fitness for stability
            duration: Optional time limit (seconds)
            log_file: Optional file to log results
        """
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}POTENTIOMETER PROOF: {process_name}{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"Threshold: f ≥ {threshold:.2f}")
        print(f"Parameters: R={R:.2f}, D={D:.2f}, α={alpha:.2f}")
        print(f"{Colors.YELLOW}Turn potentiometer to explore fitness landscape...{Colors.END}")
        print(f"{Colors.YELLOW}Press Ctrl+C to end session{Colors.END}\n")
        
        start_time = time.time()
        log_data = []
        
        try:
            while True:
                # Check duration limit
                if duration and (time.time() - start_time) > duration:
                    print(f"\n{Colors.YELLOW}Session duration limit reached.{Colors.END}")
                    break
                
                # Read potentiometer
                position, noise = self.read_potentiometer()
                
                if position is not None:
                    # Compute TRIG6
                    result = self.compute_trig6(position, noise, R, D, alpha)
                    
                    # Get status
                    status, color = self.get_fitness_status(result['fitness'])
                    
                    # Display result
                    print(f"{color}"
                          f"Pos: {position:5.3f} | "
                          f"θ: {result['theta_deg']:5.1f}° | "
                          f"N: {result['N']:5.3f} | "
                          f"f: {result['fitness']:5.3f} | "
                          f"{status}"
                          f"{Colors.END}")
                    
                    # Log data
                    if log_file:
                        log_data.append({
                            'timestamp': time.time() - start_time,
                            'process': process_name,
                            **result
                        })
                
                time.sleep(0.1)  # Match Arduino sample rate
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BOLD}Proof session ended.{Colors.END}")
        
        # Save log if requested
        if log_file and log_data:
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            print(f"{Colors.GREEN}✓ Session logged to {log_file}{Colors.END}")
    
    def calibrate(self, duration: int = 10):
        """
        Calibrate potentiometer by measuring noise floor.
        
        Args:
            duration: Calibration duration in seconds
        """
        print(f"\n{Colors.BOLD}CALIBRATION MODE{Colors.END}")
        print(f"Keep potentiometer stationary for {duration} seconds...")
        
        noises = []
        start = time.time()
        
        while time.time() - start < duration:
            _, noise = self.read_potentiometer()
            if noise is not None:
                noises.append(noise)
            time.sleep(0.1)
        
        if noises:
            avg_noise = sum(noises) / len(noises)
            max_noise = max(noises)
            min_noise = min(noises)
            
            print(f"\n{Colors.BOLD}Calibration Results:{Colors.END}")
            print(f"  Average noise: {avg_noise:.4f}")
            print(f"  Min noise: {min_noise:.4f}")
            print(f"  Max noise: {max_noise:.4f}")
            
            # Evaluate quality
            if avg_noise < 0.005:
                quality = f"{Colors.GREEN}Excellent (high-quality potentiometer){Colors.END}"
            elif avg_noise < 0.015:
                quality = f"{Colors.YELLOW}Good (standard potentiometer){Colors.END}"
            else:
                quality = f"{Colors.RED}Poor (consider replacement){Colors.END}"
            
            print(f"  Quality: {quality}")
        else:
            print(f"{Colors.RED}✗ No data received during calibration{Colors.END}")
    
    def close(self):
        """Close serial connection."""
        if self.serial:
            self.serial.close()
            print(f"{Colors.GREEN}✓ Connection closed{Colors.END}")


# Predefined process profiles from Chapter 16
PROCESSES = {
    'papyrus': {
        'name': 'Classic Reed Papyrus',
        'R': 0.82, 'D': 0.18, 'alpha': 0.15,
        'threshold': 0.55,
        'variable': 'Water quality (hydration variability)'
    },
    'papyrus_lime': {
        'name': 'Lime-Infused Papyrus',
        'R': 0.86, 'D': 0.14, 'alpha': 0.18,
        'threshold': 0.50,
        'variable': 'Lime concentration drift'
    },
    'bamboo': {
        'name': 'Bamboo Paper',
        'R': 0.88, 'D': 0.12, 'alpha': 0.10,
        'threshold': 0.55,
        'variable': 'Lime cooking temperature'
    },
    'cotton_rag': {
        'name': 'Cotton Rag Paper',
        'R': 0.92, 'D': 0.08, 'alpha': 0.12,
        'threshold': 0.60,
        'variable': 'Fermentation time'
    },
    'washi': {
        'name': 'Mulberry Paper (Japanese Washi)',
        'R': 0.94, 'D': 0.06, 'alpha': 0.10,
        'threshold': 0.60,
        'variable': 'Neri (mucilage) concentration'
    },
    'coptic': {
        'name': 'Coptic Sew Binding',
        'R': 0.75, 'D': 0.25, 'alpha': 0.12,
        'threshold': 0.44,
        'variable': 'Thread tension variability'
    },
    'nag_hammadi': {
        'name': 'Nag Hammadi Replica',
        'R': 0.78, 'D': 0.22, 'alpha': 0.16,
        'threshold': 0.44,
        'variable': 'Spine crease load distribution'
    },
    'wheat_starch': {
        'name': 'Wheat Starch Glue',
        'R': 0.86, 'D': 0.14, 'alpha': 0.15,
        'threshold': 0.55,
        'variable': 'Cooking temperature variability'
    },
    'hide_glue': {
        'name': 'Hide Glue (Collagen)',
        'R': 0.82, 'D': 0.18, 'alpha': 0.16,
        'threshold': 0.50,
        'variable': 'Working temperature'
    },
    'veg_tan': {
        'name': 'Veg-Tanned Leather',
        'R': 0.72, 'D': 0.28, 'alpha': 0.18,
        'threshold': 0.38,
        'variable': 'Curing humidity variability'
    },
    'chrome_tan': {
        'name': 'Chrome-Tanned Leather (DANGER)',
        'R': 0.65, 'D': 0.35, 'alpha': 0.30,
        'threshold': 0.25,
        'variable': 'Chemical volatility (UNSAFE)'
    }
}


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Potentiometer Proof Engine - TRIG6 Material Science Validator'
    )
    parser.add_argument('--port', default='/dev/ttyUSB0',
                        help='Serial port (default: /dev/ttyUSB0)')
    parser.add_argument('--baud', type=int, default=9600,
                        help='Baud rate (default: 9600)')
    parser.add_argument('--process', choices=list(PROCESSES.keys()),
                        help='Predefined process to test')
    parser.add_argument('--list-processes', action='store_true',
                        help='List available process profiles')
    parser.add_argument('--calibrate', action='store_true',
                        help='Run calibration mode')
    parser.add_argument('--duration', type=int,
                        help='Session duration in seconds')
    parser.add_argument('--log', help='Log file path for session data')
    parser.add_argument('--custom', nargs=4, metavar=('NAME', 'R', 'D', 'ALPHA'),
                        help='Test custom process (name R D alpha)')
    
    args = parser.parse_args()
    
    # List processes
    if args.list_processes:
        print(f"\n{Colors.BOLD}Available Process Profiles:{Colors.END}\n")
        for key, process in PROCESSES.items():
            print(f"{Colors.BLUE}{key:15s}{Colors.END} - {process['name']}")
            print(f"                  Variable: {process['variable']}")
            print(f"                  Params: R={process['R']:.2f}, "
                  f"D={process['D']:.2f}, α={process['alpha']:.2f}, "
                  f"threshold={process['threshold']:.2f}\n")
        return
    
    # Initialize engine
    engine = PotentiometerProofEngine(port=args.port, baud=args.baud)
    
    try:
        # Calibration mode
        if args.calibrate:
            engine.calibrate(duration=args.duration or 10)
        
        # Test predefined process
        elif args.process:
            process = PROCESSES[args.process]
            print(f"\n{Colors.BOLD}Testing Process:{Colors.END} {process['name']}")
            print(f"{Colors.BOLD}Variable Mapped:{Colors.END} {process['variable']}")
            
            engine.prove_process(
                process_name=process['name'],
                R=process['R'],
                D=process['D'],
                alpha=process['alpha'],
                threshold=process['threshold'],
                duration=args.duration,
                log_file=args.log
            )
        
        # Test custom process
        elif args.custom:
            name, R, D, alpha = args.custom
            R, D, alpha = float(R), float(D), float(alpha)
            
            engine.prove_process(
                process_name=name,
                R=R, D=D, alpha=alpha,
                threshold=0.50,
                duration=args.duration,
                log_file=args.log
            )
        
        # No action specified
        else:
            print(f"\n{Colors.YELLOW}No action specified. Use --help for options.{Colors.END}")
            print(f"{Colors.YELLOW}Example: python pot_engine.py --process papyrus{Colors.END}\n")
    
    finally:
        engine.close()


if __name__ == '__main__':
    main()
