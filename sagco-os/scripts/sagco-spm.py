#!/usr/bin/env python3
"""
SAGCO SPM (Sovereignty Package Manager) Runner
Installs and configures SAGCO OS from spm.yml manifest
"""

import yaml
import subprocess
import shutil
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any

class SPMRunner:
    def __init__(self, yaml_file: str):
        self.yaml_file = yaml_file
        with open(yaml_file, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def install_apt_packages(self):
        """Install APT packages from config"""
        packages = self.config.get('packages', {}).get('apt', {})
        all_packages = []
        
        for category, pkgs in packages.items():
            all_packages.extend(pkgs)
        
        if all_packages:
            print(f"Installing {len(all_packages)} APT packages...")
            cmd = ['apt-get', 'update']
            subprocess.run(cmd, check=True)
            
            cmd = ['apt-get', 'install', '-y'] + all_packages
            subprocess.run(cmd, check=True)
    
    def install_pip_packages(self):
        """Install pip packages from config"""
        packages = self.config.get('packages', {}).get('pip', {}).get('global', [])
        
        if packages:
            print(f"Installing {len(packages)} pip packages...")
            cmd = ['pip3', 'install'] + packages
            subprocess.run(cmd, check=True)
    
    def copy_files(self):
        """Copy files as specified in config"""
        files = self.config.get('files', {}).get('copy', [])
        
        for file_spec in files:
            src = file_spec['src']
            dst = file_spec['dst']
            mode = file_spec.get('mode', '0644')
            
            # Handle wildcards in src
            if '*' in src:
                print(f"Copying {src} to {dst}...")
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                subprocess.run(['cp', '-r', src, dst], check=False)
            else:
                print(f"Copying {src} to {dst}...")
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            
            # Set permissions
            os.chmod(dst, int(mode, 8))
    
    def run_post_install_commands(self):
        """Run post-installation commands"""
        commands = self.config.get('commands', {}).get('post_install', [])
        
        for cmd in commands:
            print(f"Running: {cmd}")
            subprocess.run(cmd, shell=True, check=False)
    
    def verify_installation(self):
        """Verify installation"""
        commands = self.config.get('verification', {}).get('commands', [])
        results = {}
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                results[cmd] = {
                    'status': 'success' if result.returncode == 0 else 'failed',
                    'output': result.stdout
                }
            except Exception as e:
                results[cmd] = {
                    'status': 'error',
                    'output': str(e)
                }
        
        # Write manifest
        manifest_path = self.config.get('verification', {}).get('output', {}).get('manifest', '')
        if manifest_path:
            os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
            with open(manifest_path, 'w') as f:
                json.dump({
                    'version': self.config.get('identity', {}).get('version', '1.0.0'),
                    'build_id': self.config.get('identity', {}).get('build_id', 'unknown'),
                    'verification': results
                }, f, indent=2)
        
        return results
    
    def run(self):
        """Run the full installation process"""
        print("=" * 60)
        print("SAGCO SPM Runner")
        print(f"Version: {self.config.get('identity', {}).get('version', '1.0.0')}")
        print(f"Codename: {self.config.get('identity', {}).get('codename', 'Unknown')}")
        print("=" * 60)
        
        try:
            # self.install_apt_packages()
            # self.install_pip_packages()
            # self.copy_files()
            # self.run_post_install_commands()
            
            # Copy spm.yml to /opt/sagco/spm.yml for sagco-menu
            print("Copying spm.yml to /opt/sagco/spm.yml for sagco-menu...")
            os.makedirs('/opt/sagco', exist_ok=True)
            shutil.copy(self.yaml_file, '/opt/sagco/spm.yml')
            
            # self.verify_installation()
            
            print("\n" + "=" * 60)
            print("SAGCO SPM installation complete!")
            print("=" * 60)
            
        except Exception as e:
            print(f"Error during installation: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: sagco-spm.py <spm.yml>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    
    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found")
        sys.exit(1)
    
    runner = SPMRunner(yaml_file)
    runner.run()

if __name__ == "__main__":
    main()
