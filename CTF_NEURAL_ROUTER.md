# CTF Neural Router

**Distributed Cognitive Orchestration Engine for CTF/Pentest Methodology**

> "See state → Recognize pattern → Execute algorithm → Objective achieved"

## 🎲 Philosophy

The CTF Neural Router uses a Rubik's Cube PLL (Permutation of Last Layer) algorithm pattern analogy to map CTF/pentest queries to methodology nodes. Like recognizing a PLL case on a cube and executing the right algorithm, the router recognizes the current phase and suggests optimal next moves.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the interactive CLI
python3 ctf_neural_router.py
```

## 📊 Methodology Graph

The router uses a 10-node methodology graph representing the CTF attack lifecycle:

1. **01-Ua-Recon** - Reconnaissance (Network scanning, port discovery)
2. **02-Ub-Enum** - Enumeration (Service enumeration, directory busting)
3. **03-H-WebApp** - Web Application Testing (SQL injection, XSS, vulnerabilities)
4. **04-Z-Exploit** - Exploitation (Gaining initial access, shells)
5. **05-Aa-Creds** - Credential Access (Password cracking, hash attacks)
6. **06-Ab-PrivEsc** - Privilege Escalation (Root/admin escalation)
7. **07-E-Persist** - Persistence (Backdoors, maintaining access)
8. **08-T-Exfil** - Exfiltration (Data extraction, file transfer)
9. **09-F-Pivot** - Lateral Movement (Network pivoting, tunneling)
10. **10-V-Cleanup** - Cleanup (Log clearing, covering tracks)

## 🎯 Features

### Query Classification

The router classifies natural language queries into methodology phases:

```python
from ctf_neural_router import CTFBrain
import asyncio

async def classify():
    brain = CTFBrain()
    result = await brain.classify_query("scan network for open ports")
    print(f"Phase: {result['name']}")  # Reconnaissance
    print(f"Tools: {result['tools']}")  # ['nmap', 'masscan', ...]

asyncio.run(classify())
```

### Next Move Prediction

Using a 4-quadrant scoring system:
- **Tool Readiness** (30%) - Are required tools available?
- **Context Match** (30%) - Does it fit current findings?
- **Success Rate** (25%) - Historical success probability
- **Efficiency** (15%) - Time/effort considerations

```python
brain = CTFBrain()
context = {
    "available_tools": ["nmap", "gobuster"],
    "findings": ["web server", "port 80 open"],
    "time_constraints": 20
}
moves = brain.suggest_next_moves("01-Ua-Recon", context)
for move in moves:
    print(f"{move.node_id}: {move.total_score:.2f}")
```

### Interactive CLI

```bash
$ python3 ctf_neural_router.py

ctf> scan the target network
📍 Node: 01-Ua-Recon
📛 Name: Reconnaissance
🛠️  Tools: nmap, masscan, rustscan
🎯 Confidence: 85% (keyword)

ctf> graph
📊 Graph: 10 nodes, 19 edges

ctf> nodes
📍 Methodology Nodes:
  01-Ua-Recon: Reconnaissance - 5 tools
  02-Ub-Enum: Enumeration - 6 tools
  ...

ctf> path 01-Ua-Recon 10-V-Cleanup
🛤️  Path: Reconnaissance → Enumeration → ... → Cleanup

ctf> next
➡️  Next moves from 01-Ua-Recon:
  02-Ub-Enum: 0.75 (tools:0.80 ctx:0.70)

ctf> tools nmap,gobuster,burpsuite
[SET] Available tools: ['nmap', 'gobuster', 'burpsuite']

ctf> help
Commands:
  <query>       - Classify query and get methodology
  graph         - Show graph statistics
  nodes         - List all methodology nodes
  path A B      - Show path from node A to node B
  next          - Suggest next moves from current node
  tools <list>  - Set available tools (comma-separated)
  help          - Show this help
  exit/quit     - Exit
```

## 🧪 Optional Features

### LLM Classification

Install Ollama for semantic query classification:

```bash
pip install ollama
```

The router will automatically use LLM-based classification when Ollama is available, falling back to keyword matching otherwise.

### Kubernetes Execution

Install Kubernetes client for cluster execution:

```bash
pip install kubernetes
```

Execute methodology nodes on GKE pods:

```python
result = await brain.execute_on_cluster(
    node_id="01-Ua-Recon",
    target="10.10.10.5",
    namespace="ctf-tools"
)
```

## 🎨 PLL Analogies

Each methodology node maps to a Rubik's Cube PLL case:

- **Ua Perm** (Recon) - Corner swap while edges stay → Initial probe
- **Ub Perm** (Enum) - Parallel corner swap → Deep enumeration
- **H Perm** (WebApp) - Edge swap pattern → Web-specific attacks
- **Z Perm** (Exploit) - Diagonal corner swap → Gaining access
- **Aa Perm** (Creds) - Clockwise corner cycle → Credential rotation
- **Ab Perm** (PrivEsc) - Counter-clockwise cycle → Privilege elevation
- **E Perm** (Persist) - Edge 3-cycle → Maintaining presence
- **T Perm** (Exfil) - Parallel edge swap → Data transfer
- **F Perm** (Pivot) - Adjacent edge swap → Network movement
- **V Perm** (Cleanup) - Corner + edge swap → Covering tracks

## 📝 Configuration

Customize the router behavior:

```python
brain = CTFBrain(
    graph_path="custom_methodology.json",  # Custom graph
    ollama_host="http://localhost:11434",  # LLM endpoint
    llm_model="mistral:7b"                 # Custom model
)
```

Edit `methodology_graph.json` to customize:
- Node triggers (keywords for classification)
- Tool lists
- Edge connections (valid transitions)
- Quadrant weights (scoring preferences)

## 🔒 Security

- No secrets in code
- Optional K8s RBAC integration
- Audit logging ready
- Sovereign architecture (no vendor lock-in)

## 📄 License

Sovereign - No vendor lock-in

## 👤 Author

Dom (Me10101) - Strategickhaos DAO LLC

## 🤝 Contributing

This is part of the Strategickhaos Sovereignty Architecture ecosystem. Contributions welcome!
