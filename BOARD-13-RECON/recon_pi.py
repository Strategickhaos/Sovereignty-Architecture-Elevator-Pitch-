"""
Fingerprint a Raspberry Pi by IP, register it as a SAGCO node manifest,
and optionally create a citizen entry in the registry.

Usage:
  python recon_pi.py --ip 192.168.1.42
  python recon_pi.py --auto          # discover from ARP table
"""
import argparse, json, socket, subprocess, sys, time
from pathlib import Path

PI_MAC_PREFIXES = ("b8:27:eb", "dc:a6:32", "e4:5f:01", "d8:3a:dd", "28:cd:c1")
REPO_ROOT = Path(__file__).resolve().parent.parent
PI_NODES_DIR = Path(__file__).resolve().parent / "pi-nodes"
REGISTRY = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

def _ping(ip: str) -> bool:
    param = "-n" if sys.platform.startswith("win") else "-c"
    try:
        r = subprocess.run(["ping", param, "1", ip], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False

def _arp_mac(ip: str) -> str:
    try:
        raw = subprocess.check_output(["arp", "-n", ip], stderr=subprocess.DEVNULL, timeout=5).decode()
        for line in raw.splitlines():
            parts = line.split()
            for part in parts:
                if ":" in part and len(part) == 17:
                    return part.lower()
    except Exception:
        pass
    return "unknown"

def _auto_discover() -> str | None:
    try:
        raw = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL, timeout=10).decode()
        for line in raw.splitlines():
            parts = line.split()
            if len(parts) >= 3:
                ip  = parts[0].strip("()")
                mac = parts[2].lower()
                if any(mac.startswith(p) for p in PI_MAC_PREFIXES):
                    return ip
    except Exception:
        pass
    return None

def fingerprint(ip: str) -> dict:
    alive = _ping(ip)
    mac   = _arp_mac(ip) if alive else "unknown"
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except Exception:
        hostname = "raspberrypi"

    return {
        "ip": ip,
        "mac": mac,
        "hostname": hostname,
        "alive": alive,
        "likely_pi": any(mac.startswith(p) for p in PI_MAC_PREFIXES) or "raspberry" in hostname.lower(),
        "fingerprinted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

def write_node_manifest(fp: dict, pid: int = 5001) -> Path:
    PI_NODES_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = fp["hostname"].replace(".", "_").replace("-", "_").upper()
    manifest = {
        "pid": pid,
        "canonical": f"PI.{safe_name}",
        "aliases": ["sagco-pi", "pi-master", fp["hostname"]],
        "node_type": "raspberry_pi",
        "ip": fp["ip"],
        "mac": fp["mac"],
        "hostname": fp["hostname"],
        "status": "active" if fp["alive"] else "unreachable",
        "fingerprinted_at": fp["fingerprinted_at"],
        "gpio_map": {
            "J8.PIN_01": {"gpio": 1,  "mode": "power_3v3"},
            "J8.PIN_02": {"gpio": 2,  "mode": "power_5v"},
            "J8.PIN_03": {"gpio": 3,  "mode": "SDA1_I2C"},
            "J8.PIN_05": {"gpio": 5,  "mode": "SCL1_I2C"},
            "J8.PIN_07": {"gpio": 7,  "mode": "GPIO4"},
            "J8.PIN_08": {"gpio": 8,  "mode": "TXD0_UART"},
            "J8.PIN_11": {"gpio": 11, "mode": "GPIO17"},
            "J8.PIN_13": {"gpio": 13, "mode": "GPIO27"},
        },
    }
    out = PI_NODES_DIR / f"{safe_name}.yaml"
    import yaml as _yaml
    out.write_text(_yaml.dump(manifest, sort_keys=False, allow_unicode=True))
    print(f"  node manifest → {out}")
    return out

def register_citizen(fp: dict) -> None:
    if not REGISTRY.exists():
        print("  citizen registry not found — skipping citizen registration")
        return
    import json as _json
    registry = _json.loads(REGISTRY.read_text())
    cid = f"sgc-artifact-{int(time.time() * 1000)}-{3449 % 3449 or 1}"
    citizen = {
        "cid": cid,
        "name": f"Pi Node — {fp['hostname']}",
        "kind": "artifact",
        "born_in": "genesis",
        "district": "industrial",
        "status": "active" if fp["alive"] else "embryo",
        "travel_log": [],
        "payload": {"ip": fp["ip"], "mac": fp["mac"], "hostname": fp["hostname"]},
        "proofs": [],
        "tags": ["pi", "hardware", "node"],
        "links": [],
        "created_at": fp["fingerprinted_at"],
    }
    registry.append(citizen)
    REGISTRY.write_text(_json.dumps(registry, indent=2))
    print(f"  citizen registered → {cid}")

def main():
    parser = argparse.ArgumentParser(description="SAGCO Pi recon + node registration")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ip",   help="Pi IP address")
    group.add_argument("--auto", action="store_true", help="Auto-discover from ARP table")
    parser.add_argument("--pid", type=int, default=5001, help="PID to assign (default 5001)")
    parser.add_argument("--no-citizen", action="store_true", help="Skip citizen registration")
    args = parser.parse_args()

    ip = args.ip
    if args.auto:
        ip = _auto_discover()
        if not ip:
            print("ERROR: no Raspberry Pi found in ARP table")
            print("  Tip: make sure the Pi is powered on and on the same network")
            sys.exit(1)
        print(f"  auto-discovered Pi at {ip}")

    print(f"\nSAGCO Pi Recon — {ip}")
    print("---")
    fp = fingerprint(ip)
    print(f"  hostname  : {fp['hostname']}")
    print(f"  mac       : {fp['mac']}")
    print(f"  alive     : {fp['alive']}")
    print(f"  likely_pi : {fp['likely_pi']}")

    write_node_manifest(fp, pid=args.pid)

    if not args.no_citizen:
        try:
            import yaml  # noqa: F401
            register_citizen(fp)
        except ImportError:
            print("  (install pyyaml to enable citizen registration)")

    print("\nDone. Pi is registered as a SAGCO node.")

if __name__ == "__main__":
    main()
