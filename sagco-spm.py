#!/usr/bin/env python3
"""
SAGCO Provisioning Manifest (SPM) Runner
Reads SPM YAML and provisions SAGCO OS on Kali/Debian systems.
Run as: sudo python3 sagco-spm.py spm.yml
"""
import yaml
import subprocess
import os
import shutil
import json
import sys
from pathlib import Path

# Try to import rich, install if missing
try:
    from rich.console import Console
    from rich.progress import track
except ImportError:
    print("Installing required dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich.console import Console
    from rich.progress import track

console = Console()


def run_command(cmd, desc):
    """Execute a shell command with status output."""
    console.print(f"[bold green]Running:[/bold green] {desc}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            console.print(f"[dim]{result.stdout}[/dim]")
        return result
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if e.stderr:
            console.print(f"[bold red]STDERR:[/bold red] {e.stderr}")
        raise


def main(yaml_file):
    """Main provisioning logic."""
    console.print(f"[bold blue]SAGCO SPM Runner v1.0[/bold blue]")
    console.print(f"[dim]Loading manifest: {yaml_file}[/dim]\n")
    
    # Load YAML
    with open(yaml_file, 'r') as f:
        spm = yaml.safe_load(f)
    
    # Display identity
    identity = spm.get('identity', {})
    console.print(f"[bold cyan]Identity:[/bold cyan] {identity.get('name', 'Unknown')}")
    console.print(f"[bold cyan]Codename:[/bold cyan] {identity.get('codename', 'Unknown')}")
    console.print(f"[bold cyan]Version:[/bold cyan] {identity.get('version', 'Unknown')}")
    console.print(f"[bold cyan]Motto:[/bold cyan] {identity.get('motto', 'Unknown')}\n")
    
    # Setup directories
    console.print("[bold yellow]Setting up directories...[/bold yellow]")
    os.makedirs("/opt/sagco/assets", exist_ok=True)
    if 'artifacts' in spm:
        os.makedirs(spm['artifacts'].get('log_dir', '/var/log/sagco'), exist_ok=True)
        os.makedirs(spm['artifacts'].get('state_dir', '/var/lib/sagco'), exist_ok=True)
    
    # Update repos
    if 'repos' in spm and 'apt' in spm['repos']:
        console.print("\n[bold yellow]Updating APT repositories...[/bold yellow]")
        run_command("apt update", "Updating APT repos")
    
    # Install APT packages
    if 'packages' in spm and 'apt' in spm['packages']:
        console.print("\n[bold yellow]Installing APT packages...[/bold yellow]")
        all_apt = []
        for group, packages in spm['packages']['apt'].items():
            if isinstance(packages, list):
                all_apt.extend(packages)
                console.print(f"[dim]  Group '{group}': {len(packages)} packages[/dim]")
        
        if all_apt:
            run_command(
                f"DEBIAN_FRONTEND=noninteractive apt install -y {' '.join(all_apt)}", 
                f"Installing {len(all_apt)} APT packages"
            )
    
    # Install PIP packages
    if 'packages' in spm and 'pip' in spm['packages']:
        console.print("\n[bold yellow]Installing PIP packages...[/bold yellow]")
        pip_packages = spm['packages']['pip'].get('global', [])
        if pip_packages:
            run_command(
                f"pip3 install {' '.join(pip_packages)}", 
                f"Installing {len(pip_packages)} PIP packages"
            )
    
    # Copy files
    if 'files' in spm and 'copy' in spm['files']:
        console.print("\n[bold yellow]Copying files...[/bold yellow]")
        for file_spec in track(spm['files']['copy'], description="Copying files..."):
            src = file_spec.get('src')
            dst = file_spec.get('dst')
            mode = file_spec.get('mode', '0644')
            
            dst_dir = os.path.dirname(dst)
            os.makedirs(dst_dir, exist_ok=True)
            
            try:
                if '*' in src:  # Handle wildcards (e.g., theme dir)
                    src_base = src.replace('/*', '')
                    if os.path.exists(src_base):
                        shutil.copytree(src_base, dst, dirs_exist_ok=True)
                else:
                    if os.path.exists(src):
                        shutil.copy(src, dst)
                        os.chmod(dst, int(mode, 8))
                    else:
                        console.print(f"[yellow]Warning:[/yellow] Source file not found: {src}")
            except Exception as e:
                console.print(f"[yellow]Warning:[/yellow] Failed to copy {src} -> {dst}: {e}")
    
    # Setup services
    if 'services' in spm and 'systemd' in spm['services']:
        console.print("\n[bold yellow]Setting up systemd services...[/bold yellow]")
        service_files = spm['services']['systemd'].get('files', {})
        for service_name, service_path in service_files.items():
            if os.path.exists(service_path):
                shutil.copy(service_path, f"/etc/systemd/system/{service_name}")
                os.chmod(f"/etc/systemd/system/{service_name}", 0o644)
                console.print(f"[dim]  Installed: {service_name}[/dim]")
            else:
                console.print(f"[yellow]Warning:[/yellow] Service file not found: {service_path}")
    
    # Run post-install commands
    if 'commands' in spm and 'post_install' in spm['commands']:
        console.print("\n[bold yellow]Running post-install commands...[/bold yellow]")
        for cmd in track(spm['commands']['post_install'], description="Post-install..."):
            try:
                run_command(cmd, cmd)
            except Exception as e:
                console.print(f"[yellow]Warning:[/yellow] Command failed (continuing): {cmd}")
    
    # Verification
    if 'verification' in spm:
        console.print("\n[bold yellow]Running verification...[/bold yellow]")
        verify_results = {}
        verify_commands = spm['verification'].get('commands', [])
        
        for cmd in verify_commands:
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
                verify_results[cmd] = output
                console.print(f"[green]✓[/green] {cmd}")
            except Exception as e:
                verify_results[cmd] = "FAILED"
                console.print(f"[red]✗[/red] {cmd}")
        
        # Save manifest
        if 'output' in spm['verification']:
            manifest_path = spm['verification']['output'].get('manifest', '/var/lib/sagco/spm_installed.json')
            os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
            with open(manifest_path, 'w') as f:
                json.dump(verify_results, f, indent=4)
            console.print(f"\n[bold green]Verification complete. Manifest at:[/bold green] {manifest_path}")
    
    console.print("\n[bold blue]═══════════════════════════════════════════[/bold blue]")
    console.print("[bold blue]  SAGCO OS Provisioned Successfully!  [/bold blue]")
    console.print("[bold blue]═══════════════════════════════════════════[/bold blue]")
    console.print("[dim]Reboot to see boot identity and services.[/dim]\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("[bold red]Usage:[/bold red] sudo python3 sagco-spm.py spm.yml")
        console.print("[dim]Example: sudo python3 sagco-spm.py spm.yml[/dim]")
        sys.exit(1)
    
    if os.geteuid() != 0:
        console.print("[bold red]Error:[/bold red] This script must be run as root (use sudo)")
        sys.exit(1)
    
    main(sys.argv[1])
