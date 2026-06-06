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
    entries = []
    try:
        raw = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL, timeout=10).decode()
        for line in raw.splitlines():
            parts = line.split()
            if len(parts) >= 3:
                ip  = parts[0].strip("()")
                mac = parts[2].lower() if len(parts) > 2 else ""
                is_pi = any(mac.startswith(p) for p in PI_MAC_PREFIXES)
                entries.append({"ip": ip, "mac": mac, "likely_pi": is_pi})
    except Exception:
        pass
    return entries

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
