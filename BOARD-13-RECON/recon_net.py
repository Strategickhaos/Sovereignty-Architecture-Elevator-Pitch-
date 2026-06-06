"""
SAGCO Net Scan Wing — BOARD-13-RECON brick 9

Maps the network fabric: who's online, what type, how connected.
Feeds RAT_NETWORK_BEACONING, RAT_PI_SSH_ANOMALY, and the full fleet.

Usage:
  python recon_net.py                    # ARP scan + subnet sweep
  python recon_net.py --deep             # ping-sweep all /24 hosts
  python recon_net.py --emit-citizens    # register all hosts as citizens
"""

import argparse, json, re, socket, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
REPORTS     = Path(__file__).resolve().parent / "reports"
REGISTRY    = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

PI_MAC_PREFIXES    = ("b8:27:eb", "dc:a6:32", "e4:5f:01", "d8:3a:dd", "28:cd:c1")
DOCKER_MAC_PREFIXES= ("02:42:",)
KNOWN_VENDORS      = {
    "b8:27:eb": "Raspberry Pi Foundation",
    "dc:a6:32": "Raspberry Pi Trading",
    "e4:5f:01": "Raspberry Pi Trading",
    "02:42:":   "Docker virtual",
}

GENESIS_INCREMENT  = 3449
PID_START          = 9100

# ── helpers ──────────────────────────────────────────────────────────────────

def _local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def _subnet_base(ip: str) -> str:
    parts = ip.split(".")
    return ".".join(parts[:3])

def _ping(ip: str) -> bool:
    param = "-n" if sys.platform.startswith("win") else "-c"
    try:
        r = subprocess.run(
            ["ping", param, "1", "-W", "1", ip],
            capture_output=True, timeout=3
        )
        return r.returncode == 0
    except Exception:
        return False

def _arp_table() -> list[dict]:
    entries = []
    try:
        raw = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL, timeout=10).decode()
        for line in raw.splitlines():
            # Match: host (ip) at mac [ether] on iface
            m = re.search(r"[\(\s](\d+\.\d+\.\d+\.\d+)[\)\s].*?([0-9a-f]{2}[:\-][0-9a-f]{2}[:\-][0-9a-f]{2}[:\-][0-9a-f]{2}[:\-][0-9a-f]{2}[:\-][0-9a-f]{2})", line, re.IGNORECASE)
            if m:
                ip  = m.group(1)
                mac = m.group(2).lower().replace("-", ":")
                entries.append({"ip": ip, "mac": mac})
    except Exception:
        pass
    return entries

def _resolve_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""

def _classify_host(ip: str, mac: str, hostname: str) -> dict:
    mac_lower = mac.lower()
    node_type = "network_host"
    vendor    = "unknown"
    tags      = []

    for prefix, vname in KNOWN_VENDORS.items():
        if mac_lower.startswith(prefix):
            vendor = vname
            break

    if any(mac_lower.startswith(p) for p in PI_MAC_PREFIXES):
        node_type = "raspberry_pi"
        tags.append("pi")
        tags.append("hardware")
    elif any(mac_lower.startswith(p) for p in DOCKER_MAC_PREFIXES):
        node_type = "docker_bridge"
        tags.append("docker")
        tags.append("virtual")
    elif "raspberry" in hostname.lower():
        node_type = "raspberry_pi"
        tags.append("pi")

    # local machine
    if ip == _local_ip():
        node_type = "local_host"
        tags.append("self")

    return {"node_type": node_type, "vendor": vendor, "tags": tags}

def _open_ports_quick(ip: str, ports: list[int] = [22, 80, 443, 8080, 3000, 6443]) -> list[int]:
    open_ports = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except Exception:
            pass
    return open_ports

def _make_net_node(ip: str, mac: str, alive: bool, index: int) -> dict:
    hostname  = _resolve_hostname(ip) if alive else ""
    classify  = _classify_host(ip, mac, hostname)
    tick      = int(time.time() * 1000) + index
    cid       = f"sgc-artifact-{tick}-{tick % GENESIS_INCREMENT}"

    slug = re.sub(r"[^a-zA-Z0-9]+", "_", hostname or ip).upper()
    canonical = f"NET.HOST.{slug}"

    node = {
        "cid":       cid,
        "pid":       PID_START + index,
        "canonical": canonical,
        "name":      hostname or ip,
        "kind":      "artifact",
        "district":  "industrial",
        "status":    "online" if alive else "offline",
        "node_type": classify["node_type"],
        "vendor":    classify["vendor"],
        "ip":        ip,
        "mac":       mac,
        "hostname":  hostname,
        "tags":      classify["tags"] + ["net", "recon"],
        "open_ports": [],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return node

def _ping_sweep(subnet: str) -> list[str]:
    """Ping all 254 hosts in a /24 subnet in parallel."""
    targets = [f"{subnet}.{i}" for i in range(1, 255)]
    alive = []
    with ThreadPoolExecutor(max_workers=64) as ex:
        futures = {ex.submit(_ping, ip): ip for ip in targets}
        for f in as_completed(futures):
            ip = futures[f]
            try:
                if f.result():
                    alive.append(ip)
            except Exception:
                pass
    return sorted(alive, key=lambda ip: int(ip.split(".")[-1]))

def _register_citizens(nodes: list[dict]):
    if not REGISTRY.exists():
        print("  citizen registry not found — skipping")
        return
    raw = json.loads(REGISTRY.read_text())
    if isinstance(raw, list):
        doc, citizens = None, raw
    else:
        doc, citizens = raw, raw.get("citizens", [])

    existing = {c["cid"] for c in citizens}
    added = 0
    for node in nodes:
        if node["cid"] in existing:
            continue
        citizens.append({
            "cid":        node["cid"],
            "name":       node["name"],
            "kind":       node["kind"],
            "born_in":    "genesis",
            "district":   node["district"],
            "status":     node["status"],
            "travel_log": [],
            "payload":    {k: node[k] for k in ("ip","mac","hostname","node_type","vendor","open_ports")},
            "proofs":     [],
            "tags":       node["tags"],
            "links":      [],
            "created_at": node["created_at"],
        })
        added += 1

    if doc is not None:
        doc["citizens"] = citizens
        REGISTRY.write_text(json.dumps(doc, indent=2))
    else:
        REGISTRY.write_text(json.dumps(citizens, indent=2))
    print(f"  registered {added} net citizens in 08-CITIZENS")

# ── main scanner ─────────────────────────────────────────────────────────────

def scan(deep: bool = False, port_check: bool = False, emit_citizens: bool = False) -> list[dict]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    local_ip = _local_ip()
    subnet   = _subnet_base(local_ip)

    print(f"\n  net scan  → local={local_ip}  subnet={subnet}.0/24")

    # Always start with ARP table (instant, no network noise)
    arp_entries = _arp_table()
    known_ips   = {e["ip"] for e in arp_entries}
    print(f"    ARP table → {len(arp_entries)} entr(ies)")

    alive_ips = list(known_ips)

    if deep:
        print(f"    deep sweep → pinging {subnet}.1-254 (64 threads)...")
        swept = _ping_sweep(subnet)
        new   = [ip for ip in swept if ip not in known_ips]
        alive_ips = list(set(alive_ips) | set(swept))
        print(f"    sweep found {len(swept)} alive  ({len(new)} new beyond ARP)")

    # Build MAC map from ARP
    mac_map = {e["ip"]: e["mac"] for e in arp_entries}

    nodes = []
    for i, ip in enumerate(sorted(alive_ips, key=lambda x: int(x.split(".")[-1]))):
        mac   = mac_map.get(ip, "unknown")
        alive = _ping(ip)
        node  = _make_net_node(ip, mac, alive, i)

        if port_check and alive:
            node["open_ports"] = _open_ports_quick(ip)

        nodes.append(node)

        status_sym = "✓" if alive else "✗"
        pi_sym = " ← PI" if node["node_type"] == "raspberry_pi" else ""
        ports_str = f"  ports={node['open_ports']}" if node["open_ports"] else ""
        print(f"    {status_sym} {ip:<18} {mac:<20} {node['node_type']}{pi_sym}{ports_str}")

    # RAT fleet integration: flag unknown hosts
    pi_candidates    = [n for n in nodes if n["node_type"] == "raspberry_pi"]
    unknown_hosts    = [n for n in nodes if n["vendor"] == "unknown" and n["status"] == "online"]

    if pi_candidates:
        print(f"\n  ⚡ Pi candidate(s): {[n['ip'] for n in pi_candidates]}")
        print("     → Run: python sagco_recon.py pi --auto  to claim + register")

    if unknown_hosts:
        print(f"\n  ⚠  Unknown hosts online ({len(unknown_hosts)}) — check RAT_NETWORK_BEACONING:")
        for h in unknown_hosts[:5]:
            print(f"     {h['ip']}  {h['mac']}")

    # Write report
    out = REPORTS / "net_nodes.json"
    out.write_text(json.dumps(nodes, indent=2))
    print(f"\n  report    → {out}  ({len(nodes)} node(s))")

    if emit_citizens:
        _register_citizens(nodes)

    return nodes


def main():
    parser = argparse.ArgumentParser(description="SAGCO Net Scan Wing")
    parser.add_argument("--deep",          action="store_true", help="Ping-sweep full /24 subnet")
    parser.add_argument("--ports",         action="store_true", help="Quick port scan per live host")
    parser.add_argument("--emit-citizens", action="store_true")
    args = parser.parse_args()
    scan(deep=args.deep, port_check=args.ports, emit_citizens=args.emit_citizens)
    print("\nDone.")


if __name__ == "__main__":
    main()
