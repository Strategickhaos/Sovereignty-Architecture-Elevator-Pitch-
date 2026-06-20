"""
SAGCO NC — TCP socket layer for piping SAGCO signals between nodes.
Pure stdlib: socket, threading.

Server: listens for SAGCO command strings, runs them on the pathway,
        streams results back line by line.
Client: connects, sends commands typed by user, prints responses.

Protocol: UTF-8 line-delimited. Response ends with "\\x00\\n".
"""
import socket, threading, sys, os

HOST_DEFAULT = "0.0.0.0"
PORT_DEFAULT = 9944
TERMINATOR   = b"\x00\n"


# ── SERVER ─────────────────────────────────────────────────────────────────────

def _handle_client(conn, addr, pathway):
    print(f"[nc] connection from {addr[0]}:{addr[1]}")
    try:
        buf = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                cmd_str = line.decode("utf-8", errors="replace").strip()
                if not cmd_str:
                    continue
                print(f"[nc] ← {cmd_str}")
                response = _dispatch(pathway, cmd_str)
                print(f"[nc] → {response[:60]}...")
                payload = (response + "\n").encode("utf-8") + TERMINATOR
                conn.sendall(payload)
    except Exception as e:
        print(f"[nc] client error: {e}")
    finally:
        conn.close()
        print(f"[nc] {addr[0]} disconnected")


def _dispatch(pathway, cmd_str: str) -> str:
    """Run a SAGCO command string on the pathway. Returns string response."""
    parts = cmd_str.split()
    if not parts:
        return "EMPTY"
    cmd = parts[0].lower()

    try:
        if cmd in ("status", "eru", "transmit"):
            return pathway.sagco_command(cmd)
        elif cmd == "fire" and len(parts) >= 2:
            return pathway.sagco_command("fire", parts[1])
        elif cmd == "receive" and len(parts) >= 3:
            label    = " ".join(parts[2:]).strip('"')
            variance = 0.0
            return pathway.sagco_command("receive", parts[1], label, variance)
        elif cmd == "synapse" and len(parts) >= 3:
            return pathway.sagco_command("synapse", parts[1], parts[2])
        elif cmd == "dendrites" and len(parts) >= 2:
            n = pathway.neurons.get(parts[1])
            if not n:
                return f"No neuron: {parts[1]}"
            lines = [f"DENDRITES — {parts[1]}"]
            for d in n.dendrites:
                lines.append(f"  {'✓' if d.received else '○'} {d.signal_type} {d.label} w={d.weight}")
            return "\n".join(lines)
        elif cmd == "ping":
            return "PONG — organism alive"
        else:
            return f"UNKNOWN_COMMAND: {cmd_str}"
    except Exception as e:
        return f"ERROR: {e}"


def run_server(pathway, host: str = HOST_DEFAULT, port: int = PORT_DEFAULT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print(f"[nc] SAGCO server listening on {host}:{port}")
    print(f"[nc] connect with: python3 habebian_cli.py nc client <host> --port {port}")
    try:
        while True:
            conn, addr = sock.accept()
            t = threading.Thread(target=_handle_client, args=(conn, addr, pathway), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[nc] server shutdown")
    finally:
        sock.close()


# ── CLIENT ─────────────────────────────────────────────────────────────────────

def run_client(host: str, port: int = PORT_DEFAULT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except ConnectionRefusedError:
        print(f"[nc] connection refused — is server running on {host}:{port}?")
        return

    print(f"[nc] connected to SAGCO node {host}:{port}")
    print(f"[nc] type SAGCO commands. 'quit' to disconnect.\n")

    def _recv_loop():
        buf = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    print("[nc] server closed connection")
                    os._exit(0)
                buf += chunk
                while TERMINATOR in buf:
                    msg, buf = buf.split(TERMINATOR, 1)
                    print(msg.decode("utf-8", errors="replace"))
                    print()
            except Exception:
                break

    t = threading.Thread(target=_recv_loop, daemon=True)
    t.start()

    try:
        while True:
            cmd = input("sagco-nc › ").strip()
            if not cmd:
                continue
            if cmd.lower() in ("quit", "exit", "q"):
                break
            sock.sendall((cmd + "\n").encode("utf-8"))
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        sock.close()
        print("[nc] disconnected")
