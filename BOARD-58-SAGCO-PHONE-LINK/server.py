#!/usr/bin/env python3
"""
BOARD-58 — SAGCO Phone Link Server (runs on Termux / Z Fold)
Headless replacement for Microsoft Phone Link.

Start on phone:
  python3 server.py [--port 9944] [--secret SAGCO_SECRET]

Connect from desktop:
  Run sagco-phonelink.ps1 on Windows
  OR: python3 server.py --client 192.168.1.89

Protocol: line-delimited UTF-8, null-terminated responses.
Commands:
  !shell <cmd>   — run shell command on phone, stream output
  !sagco <cmd>   — run sagco organism command
  !ls            — list home directory
  !disk          — disk usage summary
  !ping          — heartbeat
  !clip <text>   — not yet (needs termux-api)
  quit           — disconnect
"""
import socket, threading, subprocess, os, sys, shlex, hashlib, time

PORT    = 9944
SECRET  = os.environ.get("SAGCO_LINK_SECRET", "")
TERM    = b"\x00\n"
BANNER  = "SAGCO-PHONE-LINK v1.0 — Strategickhaos DAO LLC"


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def _run_shell(cmd: str, timeout: int = 30) -> str:
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=timeout,
            env={**os.environ, "TERM": "xterm-256color"}
        )
        out = r.stdout + (("\n[stderr] " + r.stderr) if r.stderr.strip() else "")
        return out.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT after {timeout}s"
    except Exception as e:
        return f"ERROR: {e}"


def _dispatch(line: str) -> str:
    line = line.strip()
    if not line:
        return ""

    if line == "!ping":
        return f"PONG {time.strftime('%H:%M:%S')} — Z Fold alive"

    if line == "!disk":
        return _run_shell("df -h /data/data/com.termux/files 2>/dev/null || df -h ~")

    if line == "!ls":
        return _run_shell("ls --color=never ~")

    if line.startswith("!shell "):
        cmd = line[7:].strip()
        if not cmd:
            return "Usage: !shell <command>"
        return _run_shell(cmd)

    if line.startswith("!sagco "):
        sagco_cmd = line[7:].strip()
        return _run_shell(f"sagco {sagco_cmd}")

    if line.startswith("!nmap "):
        target = line[6:].strip()
        return _run_shell(f"nmap -p 22,80,443,8080,8443 {target}", timeout=60)

    if line == "!recon":
        return _run_shell("nmap -sn 192.168.1.0/24", timeout=120)

    if line.startswith("!cd "):
        return "(cd not persistent across commands — use !shell cd <dir> && <cmd>)"

    # raw shell fallback (any unrecognized command runs as shell)
    return _run_shell(line)


def _handle(conn, addr):
    print(f"[link] +++ {addr[0]}:{addr[1]}")
    try:
        # banner
        conn.sendall((BANNER + "\n").encode() + TERM)

        # optional auth
        if SECRET:
            challenge = _sha(str(time.time()))
            conn.sendall(f"AUTH_CHALLENGE:{challenge}\n".encode() + TERM)
            resp = conn.recv(256).decode().strip()
            expected = _sha(challenge + SECRET)
            if resp != expected:
                conn.sendall(b"AUTH_FAIL\n" + TERM)
                return
            conn.sendall(b"AUTH_OK\n" + TERM)

        buf = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line_b, buf = buf.split(b"\n", 1)
                line = line_b.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                if line.lower() in ("quit", "exit", "q"):
                    conn.sendall(b"BYE\n" + TERM)
                    return
                print(f"[link] ← {line[:80]}")
                response = _dispatch(line)
                conn.sendall((response + "\n").encode("utf-8") + TERM)
    except Exception as e:
        print(f"[link] error: {e}")
    finally:
        conn.close()
        print(f"[link] --- {addr[0]} disconnected")


def run_server(port: int = PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(5)
    ip = _run_shell("ip route get 1 | awk '{print $7; exit}' 2>/dev/null || echo unknown")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  SAGCO PHONE LINK SERVER")
    print(f"  phone IP  : {ip.strip()}")
    print(f"  port      : {port}")
    print(f"  auth      : {'ON' if SECRET else 'OFF (set SAGCO_LINK_SECRET to enable)'}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    try:
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=_handle, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[link] shutdown")
    finally:
        sock.close()


def run_client(host: str, port: int = PORT):
    """Minimal Python client (desktop fallback if PS1 not available)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print(f"Cannot connect to {host}:{port} — is server running?")
        return

    def _recv():
        buf = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    os._exit(0)
                buf += chunk
                while TERM in buf:
                    msg, buf = buf.split(TERM, 1)
                    text = msg.decode("utf-8", errors="replace").strip()
                    if text:
                        print(text)
            except Exception:
                break

    threading.Thread(target=_recv, daemon=True).start()
    print(f"Connected to SAGCO Z Fold @ {host}:{port}")
    print("Commands: !shell <cmd>  !sagco <cmd>  !disk  !ls  !recon  quit\n")
    try:
        while True:
            cmd = input("sagco-link › ")
            if not cmd.strip():
                continue
            sock.sendall((cmd + "\n").encode())
            time.sleep(0.1)
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    port = PORT
    if "--port" in args:
        port = int(args[args.index("--port") + 1])
    if "--secret" in args:
        os.environ["SAGCO_LINK_SECRET"] = args[args.index("--secret") + 1]

    if "--client" in args:
        host = args[args.index("--client") + 1]
        run_client(host, port)
    else:
        run_server(port)
