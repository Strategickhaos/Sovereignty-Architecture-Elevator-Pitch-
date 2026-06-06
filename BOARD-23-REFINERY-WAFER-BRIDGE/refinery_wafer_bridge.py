#!/usr/bin/env python3
"""
SAGCO Refinery Wafer Bridge — BOARD-23

Converts ARP table + ResmonCfg telemetry into:
  M1 wafer  (ARP/network layer)
  M2 wafer  (process/memory layer)
  M3 wafer  (network send/receive layer)
  YAML nodes + citizen registry entries

ResmonCfg XML files are Windows Resource Monitor saved views.
We parse their tab/column schema to understand what telemetry is being tracked.

Usage:
  python refinery_wafer_bridge.py --all
  python refinery_wafer_bridge.py --layer m1
  python refinery_wafer_bridge.py --resmon sagco_overview.ResmonCfg
  python refinery_wafer_bridge.py --emit-citizens
"""

import argparse, csv, json, re, socket, subprocess, sys, time
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
BOARD     = Path(__file__).resolve().parent
WAFERS    = BOARD / "excel-wafers"
NODES     = BOARD / "network-nodes"
REPORTS   = BOARD / "reports"
REGISTRY  = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

GENESIS_INCREMENT = 3449
PID_BASE = 9300

# ── ResmonCfg parser ──────────────────────────────────────────────────────────

def parse_resmon_cfg(path: Path) -> dict:
    """Extract tab/column schema from a Windows ResmonCfg XML file."""
    result = {"tabs": {}, "focused_tab": None, "source": path.name}
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        for tab in root.findall("tab"):
            tab_id = tab.get("id", "unknown")
            focused = tab.get("focused") == "true"
            if focused:
                result["focused_tab"] = tab_id
            tables = {}
            for table in tab.findall("table"):
                table_id = table.get("id", "unknown")
                hidden   = table.get("hidden") == "true"
                cols = [
                    {
                        "id":     col.get("id"),
                        "width":  col.get("width"),
                        "hidden": col.get("hidden") == "true",
                    }
                    for col in table.findall("column")
                    if col.get("hidden") != "true"
                ]
                tables[table_id] = {"hidden": hidden, "visible_columns": cols}
            result["tabs"][tab_id] = tables
    except Exception as e:
        result["error"] = str(e)
    return result

# ── ARP → M1 wafer ───────────────────────────────────────────────────────────

def _arp_entries() -> list[dict]:
    entries = []
    try:
        raw = subprocess.check_output(["arp", "-a"], stderr=subprocess.DEVNULL, timeout=10).decode()
        for line in raw.splitlines():
            m = re.search(
                r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:]{17}|[0-9a-fA-F\-]{17})\s+(\w+)",
                line
            )
            if m:
                ip   = m.group(1)
                mac  = m.group(2).lower().replace("-", ":")
                kind = m.group(3)
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except Exception:
                    hostname = ""
                entries.append({"ip": ip, "mac": mac, "arp_type": kind, "hostname": hostname})
    except Exception:
        pass
    return entries

def build_m1_wafer(emit_citizens: bool = False) -> list[dict]:
    WAFERS.mkdir(parents=True, exist_ok=True)
    NODES.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    entries = _arp_entries()
    rows = []
    pid = PID_BASE

    for entry in entries:
        pid += 1
        safe = entry["ip"].replace(".", "_")
        canonical = f"REFINERY.WAFER.NET.{safe}"
        tick = int(time.time() * 1000) + pid
        cid  = f"sgc-artifact-{tick}-{tick % GENESIS_INCREMENT}"

        row = {
            "PID": pid, "CID": cid, "Canonical": canonical,
            "Layer": "M1_ARP",
            "IP": entry["ip"], "MAC": entry["mac"],
            "ARPType": entry["arp_type"], "Hostname": entry.get("hostname", ""),
            "Wafer": "M1", "Board": "BOARD-23-REFINERY-WAFER-BRIDGE",
        }
        rows.append(row)

        # Node YAML
        node_yaml = (
            f"pid: {pid}\n"
            f"cid: {cid}\n"
            f"canonical: {canonical}\n"
            f"type: refinery_network_node\n"
            f"layer: M1_ARP\n"
            f"ip: {entry['ip']}\n"
            f"mac: {entry['mac']}\n"
            f"arp_type: {entry['arp_type']}\n"
            f"hostname: {entry.get('hostname','')}\n"
            f"wafer: M1\n"
            f"role: pad_trace_bridge\n"
            f"status: observed\n"
            f"source: arp-a\n"
            f"strand: purple\n"
            f"created_at: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n"
        )
        (NODES / f"{canonical}.yaml").write_text(node_yaml)

    # CSV wafer
    csv_out = WAFERS / "m1_arp_wafer.csv"
    if rows:
        with open(csv_out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    print(f"  M1 wafer  → {len(rows)} ARP entr(ies)  [{csv_out}]")

    if emit_citizens and rows:
        _register_wafer_citizens(rows)

    return rows

# ── Citizen registration ──────────────────────────────────────────────────────

def _register_wafer_citizens(rows: list[dict]):
    if not REGISTRY.exists():
        print("  citizen registry not found")
        return
    raw = json.loads(REGISTRY.read_text())
    if isinstance(raw, list):
        doc, citizens = None, raw
    else:
        doc, citizens = raw, raw.get("citizens", [])

    existing = {c["cid"] for c in citizens}
    added = 0
    for row in rows:
        if row["CID"] in existing:
            continue
        citizens.append({
            "cid":        row["CID"],
            "name":       row["Canonical"],
            "kind":       "artifact",
            "born_in":    "genesis",
            "district":   "industrial",
            "status":     "active",
            "travel_log": [],
            "payload":    {k: row[k] for k in ("IP","MAC","ARPType","Hostname","Layer","Wafer")},
            "proofs":     [],
            "tags":       ["refinery", "wafer", "m1", "net", "recon"],
            "links":      [],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        added += 1

    if doc is not None:
        doc["citizens"] = citizens
        REGISTRY.write_text(json.dumps(doc, indent=2))
    else:
        REGISTRY.write_text(json.dumps(citizens, indent=2))
    print(f"  registered {added} wafer citizens in 08-CITIZENS")

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SAGCO Refinery Wafer Bridge")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all",    action="store_true", help="Build all wafer layers")
    group.add_argument("--layer",  choices=["m1","m2","m3"], help="Build specific layer")
    group.add_argument("--resmon", help="Parse a ResmonCfg XML file and print schema")
    parser.add_argument("--emit-citizens", action="store_true")
    args = parser.parse_args()

    if args.resmon:
        path = Path(args.resmon)
        if not path.exists():
            print(f"ERROR: {path} not found")
            sys.exit(1)
        schema = parse_resmon_cfg(path)
        print(f"\n  ResmonCfg: {path.name}")
        print(f"  Focused tab: {schema.get('focused_tab')}")
        for tab_id, tables in schema.get("tabs", {}).items():
            for table_id, info in tables.items():
                if not info["hidden"]:
                    cols = [c["id"] for c in info["visible_columns"]]
                    print(f"  [{tab_id}.{table_id}] visible columns: {cols}")
        return

    if args.all or args.layer == "m1":
        build_m1_wafer(emit_citizens=args.emit_citizens)

    print("\n  Refinery Wafer Bridge — done.")

if __name__ == "__main__":
    main()
