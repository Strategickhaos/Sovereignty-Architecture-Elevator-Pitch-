# SAGCO Agents

Unified command center and specialized agent fleet for the SAGCO sovereign OS.

## Main Dispatcher

```bash
python sagco-agents/sagco.py <command> [args...]
```

## Commands

| Command    | Routes To                                      | Description                              |
|------------|------------------------------------------------|------------------------------------------|
| `recon`    | BOARD-13-RECON/sagco_recon.py                  | System recon (net, browser, cloud, pi)   |
| `catpush`  | 08-CITIZENS/catpush.py                         | Register any file/node as a citizen      |
| `physics`  | BOARD-21-PHYSICS-FLEET/src/eru_analyzer.py     | ERU physics case studies                 |
| `gke`      | BOARD-24-GCP-MASTERY/recon/gke_mapper.py       | Discover and map GKE clusters            |
| `refinery` | BOARD-23-REFINERY-WAFER-BRIDGE/refinery_wafer_bridge.py | ARP/ResmonCfg wafer builder  |
| `exam`     | BOARD-10-UNIVERSITY/src/exam_runner.py         | Grade the whole SAGCO organism           |
| `compile`  | SAGCO-LANG/target/release/flamec               | Compile .flame FlameLang files           |
| `citizen`  | built-in                                       | List, search, stats on citizen registry  |
| `antibody` | built-in                                       | List and fire BOARD-11 antibodies        |
| `agent`    | built-in                                       | Run specialized agents below             |

## Specialized Agents

| Agent         | File              | Description                                         |
|---------------|-------------------|-----------------------------------------------------|
| `eru`         | agent_eru.py      | Scan boards for ERU cases, log new variances        |
| `kube`        | agent_kube.py     | K8s node/pod/event navigator, district map          |
| `gcp`         | agent_gcp.py      | IAM drift scan, cost pulse, GCP badge check         |

## Examples

```bash
# Full recon pass
python sagco-agents/sagco.py recon --all

# List all citizens
python sagco-agents/sagco.py citizen --stats

# Fire a security antibody
python sagco-agents/sagco.py antibody --fire RAT_NETWORK_BEACONING 192.168.1.100

# Scan all boards for ERU case studies
python sagco-agents/sagco.py agent eru --scan-board BOARD-24-GCP-MASTERY

# Check K8s district alignment
python sagco-agents/sagco.py agent kube --district-map

# GCP IAM drift scan
python sagco-agents/sagco.py agent gcp --iam-drift --project my-project

# GCP badge readiness check
python sagco-agents/sagco.py agent gcp --badge-check

# Map live GKE clusters
python sagco-agents/sagco.py gke --auto --emit-citizens

# Run university exam
python sagco-agents/sagco.py exam --all
```
