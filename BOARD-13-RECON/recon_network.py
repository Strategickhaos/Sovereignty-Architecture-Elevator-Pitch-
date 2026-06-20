import json, socket, subprocess, platform
from pathlib import Path

PI_MAC_PREFIXES = ("b8:27:eb", "dc:a6:32", "e4:5f:01", "d8:3a:dd", "28:cd:c1")

def _local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def _arp_table() -> list[dict]:
    """ARP table with Termux/Android fallback: arp -a → ip neigh show → /proc/net/arp."""
    def _make(ip, mac):
        return {"ip": ip, "mac": mac.lower(), "likely_pi": any(mac.lower().startswith(p) for p in PI_MAC_PREFIXES)}

    # 1. arp -a
    try:
        raw = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL, timeout=10).decode()
        entries = []
        for line in raw.splitlines():
            parts = line.split()
            if len(parts) >= 3:
                entries.append(_make(parts[0].strip("()"), parts[2] if len(parts) > 2 else ""))
        if entries:
            return entries
    except Exception:
        pass

    # 2. ip neigh show (Termux — no root needed)
    try:
        raw = subprocess.check_output(["ip", "neigh", "show"], stderr=subprocess.DEVNULL, timeout=10).decode()
        entries = []
        for line in raw.splitlines():
            m = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+dev\s+\S+\s+lladdr\s+([0-9a-f:]{17})", line, re.IGNORECASE)
            if m:
                entries.append(_make(m.group(1), m.group(2)))
        if entries:
            return entries
    except Exception:
        pass

    # 3. /proc/net/arp (needs root on Android)
    try:
        with open("/proc/net/arp") as f:
            return [_make(p[0], p[3]) for p in (l.split() for l in f.readlines()[1:])
                    if len(p) >= 4 and p[3] != "00:00:00:00:00:00"]
    except Exception:
        pass

    return []

def _hostname() -> str:
    return socket.gethostname()

def scan(output_dir: Path) -> dict:
    local_ip = _local_ip()
    arp = _arp_table()
    pi_candidates = [e for e in arp if e["likely_pi"]]

    result = {
        "hostname": _hostname(),
        "local_ip": local_ip,
        "platform": platform.system(),
        "arp_entries": arp,
        "pi_candidates": pi_candidates,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "network.json"
    out.write_text(json.dumps(result, indent=2))
    print(f"  network   → host={local_ip}  pi_candidates={len(pi_candidates)}  [{out}]")
    return result
