# StrategicKhaos CTF Brain

**Version:** 1.0.0  
**Author:** Dom (Me10101) - Strategickhaos DAO LLC

## Overview

The StrategicKhaos CTF Brain is a revolutionary framework that maps **Rubik's Cube PLL (Permutation of Last Layer) algorithms** to **penetration testing methodology**. This unique approach provides an intuitive, pattern-based system for navigating complex security assessments.

### Philosophy

> "See state → Recognize pattern → Execute algorithm → Objective achieved"

Just as a speedcuber recognizes a cube state and executes the perfect algorithm, a penetration tester recognizes system states and executes the appropriate methodology.

## Architecture

The CTF Brain consists of 10 methodology nodes, each mapped to a specific PLL algorithm:

### Node Structure

Each node represents a phase in the penetration testing lifecycle:

1. **01-Ua-Recon** - Reconnaissance (Ua Perm)
2. **02-Ub-Enum** - Enumeration (Ub Perm)
3. **03-H-WebApp** - Web Application Testing (H Perm)
4. **04-Z-Exploit** - Exploitation (Z Perm)
5. **05-Aa-Creds** - Credential Attacks (Aa Perm)
6. **06-Ab-PrivEsc** - Privilege Escalation (Ab Perm)
7. **07-E-Persist** - Persistence (E Perm)
8. **08-T-Exfil** - Exfiltration (T Perm)
9. **09-F-Pivot** - Pivoting (F Perm)
10. **10-V-Cleanup** - Cleanup (V Perm)

### Workflow Graph

The nodes are connected via edges that represent logical workflow transitions:

```
Recon → Enum → Exploit → PrivEsc → Persist → Exfil → Cleanup
  ↓      ↓        ↓         ↓         ↓        
WebApp → Creds → Pivot ←────┘─────────┘
  ↓              ↓
  └──────────────┴─→ Back to Recon (lateral movement)
```

## Features

### 1. Trigger-Based Recognition

Each node has associated trigger keywords that help identify the appropriate methodology phase:

```typescript
// Example: Reconnaissance node
triggers: ["scan", "recon", "discover", "find hosts", "port scan", "network map"]
```

The CTF Brain automatically scores and ranks nodes based on keyword matching.

### 2. Tool Association

Every node includes recommended tools for that phase:

```typescript
// Example: Web Application node
tools: ["burpsuite", "sqlmap", "nikto", "wpscan", "nuclei", "httpx"]
```

### 3. Expected Outputs

Clear definitions of what to expect from each phase:

```typescript
// Example: Exploitation node
expected_output: ["shell access", "reverse connection", "command execution"]
```

### 4. Quadrant Weighting System

The CTF Brain uses weighted scoring across four dimensions:

- **tool_ready** (30%): Tool availability and readiness
- **context_match** (30%): Contextual relevance to current state
- **success_rate** (25%): Historical success rate of the approach
- **efficiency** (15%): Time and resource efficiency

## Installation & Setup

### Prerequisites

- Node.js 18+ or TypeScript runtime (tsx)
- npm or yarn

### Install Dependencies

```bash
npm install
```

### Build

```bash
npm run build
```

## Usage

### CLI Interface

#### Interactive Mode

Launch the interactive CLI:

```bash
npm run ctf-brain
```

or with tsx directly:

```bash
tsx src/ctf-brain/cli.ts
```

#### Available Commands

**Query by keywords:**
```bash
ctf-brain> query web application sql injection
```

**Find tools:**
```bash
ctf-brain> tool nmap
```

**Get node details:**
```bash
ctf-brain> node 01-Ua-Recon
```

**Get next steps:**
```bash
ctf-brain> next 04-Z-Exploit
```

**Find workflow path:**
```bash
ctf-brain> path 01-Ua-Recon 08-T-Exfil
```

**List all nodes:**
```bash
ctf-brain> list
```

**Show graph:**
```bash
ctf-brain> graph
```

#### Non-Interactive Mode

Run single commands:

```bash
npm run ctf-brain query web sql injection
npm run ctf-brain tool metasploit
npm run ctf-brain node 03-H-WebApp
```

### Discord Bot Integration

The CTF Brain is fully integrated with the Discord bot. Available slash commands:

#### `/ctf-query <keywords>`
Search for methodology nodes based on keywords.

**Example:**
```
/ctf-query keywords: web sql injection
```

#### `/ctf-tool <toolname>`
Find nodes that use a specific tool.

**Example:**
```
/ctf-tool toolname: nmap
```

#### `/ctf-node <node-id>`
Get detailed information about a methodology node.

**Example:**
```
/ctf-node node-id: 01-Ua-Recon
```

#### `/ctf-next <node-id>`
Get recommended next steps from a specific node.

**Example:**
```
/ctf-next node-id: 04-Z-Exploit
```

#### `/ctf-path <start> <end>`
Find the workflow path between two nodes.

**Example:**
```
/ctf-path start: 01-Ua-Recon end: 08-T-Exfil
```

#### `/ctf-list`
List all methodology nodes.

#### `/ctf-info`
Display CTF Brain metadata and philosophy.

### Programmatic API

#### Import and Initialize

```typescript
import { CTFBrain } from './ctf-brain/index.js';

const brain = new CTFBrain();
```

#### Query Nodes

```typescript
// Find nodes by trigger keywords
const results = brain.findNodesByTrigger('web sql injection');
results.forEach(result => {
  console.log(`${result.nodeId}: ${result.node.name}`);
  console.log(`Score: ${result.score}`);
  console.log(`Matched: ${result.matchedTriggers.join(', ')}`);
});
```

#### Get Node Details

```typescript
const node = brain.getNode('01-Ua-Recon');
console.log(node.name);
console.log(node.description);
console.log(node.tools);
```

#### Navigate Workflow

```typescript
// Get next steps
const nextNodes = brain.getNextNodes('04-Z-Exploit');

// Get recommended workflows
const workflows = brain.getRecommendedWorkflow('04-Z-Exploit');

// Find path between nodes
const path = brain.findPath('01-Ua-Recon', '08-T-Exfil');
```

#### Tool Lookup

```typescript
// Find nodes by tool
const nodes = brain.findNodesByTool('nmap');

// Get tools for a phase
const tools = brain.getToolsForPhase('01-Ua-Recon');
```

## Methodology Deep Dive

### 01-Ua-Recon: Reconnaissance

**PLL Analog:** Ua Perm - M'2 U M U2 M' U M'2

Initial target discovery and mapping phase. Identify attack surface, open ports, and services.

**Tools:** nmap, masscan, shodan, whois, dig, theHarvester  
**Triggers:** scan, recon, discover, find hosts, port scan, network map  
**Output:** IP addresses, open ports, service versions, hostnames

### 02-Ub-Enum: Enumeration

**PLL Analog:** Ub Perm - M'2 U' M U2 M' U' M'2

Deep enumeration of discovered services. Extract detailed information about running services.

**Tools:** gobuster, ffuf, enum4linux, smbclient, ldapsearch, snmpwalk  
**Triggers:** enum, directory, users, shares, ldap, smb  
**Output:** directories, usernames, shares, domain info

### 03-H-WebApp: Web Application

**PLL Analog:** H Perm - M'2 U M'2 U2 M'2 U M'2

Web application vulnerability assessment. Test for common web vulnerabilities.

**Tools:** burpsuite, sqlmap, nikto, wpscan, nuclei, httpx  
**Triggers:** web, sql, injection, xss, http, api, form  
**Output:** vulnerabilities, injection points, auth bypasses

### 04-Z-Exploit: Exploitation

**PLL Analog:** Z Perm - M' U M'2 U M'2 U M' U2 M'2

Gaining initial access via exploitation of discovered vulnerabilities.

**Tools:** metasploit, nc, searchsploit, pwntools, msfvenom  
**Triggers:** exploit, shell, reverse, payload, foothold, rce  
**Output:** shell access, reverse connection, command execution

### 05-Aa-Creds: Credential Attacks

**PLL Analog:** Aa Perm - x' R2 D2 R U R' D2 R U' R

Password attacks and credential harvesting through various techniques.

**Tools:** hydra, hashcat, john, crackmapexec, responder, mimikatz  
**Triggers:** password, crack, brute, hash, credential, ntlm  
**Output:** cracked passwords, hashes, tokens, tickets

### 06-Ab-PrivEsc: Privilege Escalation

**PLL Analog:** Ab Perm - x' R U' R D2 R' U R D2 R2

Escalating privileges on a compromised host to gain higher-level access.

**Tools:** linpeas, winpeas, pspy, sudo -l, suid3num, powerup  
**Triggers:** privesc, root, admin, escalate, sudo, suid  
**Output:** root/admin access, elevated shell, system control

### 07-E-Persist: Persistence

**PLL Analog:** E Perm - x' R U' R' D R U R' D' R U R' D R U' R' D'

Maintaining access after initial compromise through backdoors and persistence mechanisms.

**Tools:** cron, registry, scheduled tasks, ssh keys, implants  
**Triggers:** persist, backdoor, maintain, cron, startup  
**Output:** persistent access, backdoor, callback mechanism

### 08-T-Exfil: Exfiltration

**PLL Analog:** T Perm - R U R' U' R' F R2 U' R' U' R U R' F'

Extracting data from compromised systems to attacker-controlled infrastructure.

**Tools:** nc, curl, dns, base64, steghide, scp  
**Triggers:** exfil, extract, data, transfer, steal, download  
**Output:** extracted files, dumped databases, credentials

### 09-F-Pivot: Pivoting

**PLL Analog:** F Perm - R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R

Moving laterally through the network to access additional systems.

**Tools:** chisel, ligolo, sshuttle, proxychains, socat  
**Triggers:** pivot, tunnel, lateral, internal, proxy  
**Output:** internal access, new subnets, additional hosts

### 10-V-Cleanup: Cleanup

**PLL Analog:** V Perm - R' U R' U' y R' F' R2 U' R' U R' F R F

Removing traces of compromise to maintain stealth.

**Tools:** history -c, shred, wevtutil, timestomp  
**Triggers:** cleanup, clear, logs, evidence, tracks  
**Output:** cleared logs, removed artifacts, stealth maintained

## Configuration

The CTF Brain configuration is stored in `src/ctf-brain/config.json`. You can customize:

- Node definitions
- Tool associations
- Trigger keywords
- Edge connections (workflow paths)
- Quadrant weights

### Example Configuration Modification

```json
{
  "nodes": {
    "01-Ua-Recon": {
      "name": "Reconnaissance",
      "pll_analog": "Ua Perm - M'2 U M U2 M' U M'2",
      "tools": ["nmap", "masscan", "your-custom-tool"],
      "triggers": ["scan", "recon", "your-trigger"],
      "description": "Initial target discovery and mapping",
      "expected_output": ["IP addresses", "open ports"]
    }
  }
}
```

## Use Cases

### 1. Training & Education

Use the CTF Brain to teach penetration testing methodology:

```bash
# Start at reconnaissance
ctf-brain> node 01-Ua-Recon

# Show next steps
ctf-brain> next 01-Ua-Recon

# Navigate the workflow
ctf-brain> path 01-Ua-Recon 06-Ab-PrivEsc
```

### 2. Real-World Assessments

During live penetration tests, use CTF Brain to:

- Determine current phase
- Identify appropriate tools
- Plan workflow transitions
- Document methodology

```bash
# Gained initial shell, what's next?
ctf-brain> query shell foothold
# Result: 04-Z-Exploit

ctf-brain> next 04-Z-Exploit
# Options: PrivEsc or Pivot
```

### 3. CTF Competitions

In CTF environments, quickly identify the right approach:

```bash
ctf-brain> query web form sql
# Identifies 03-H-WebApp node with sqlmap, burpsuite

ctf-brain> tool sqlmap
# Shows which phase and expected outputs
```

### 4. Discord Team Collaboration

Use Discord bot commands for team coordination:

```
Team Member 1: /ctf-query keywords: found SMB shares
Team Member 2: /ctf-next node-id: 02-Ub-Enum
Bot: Recommended: Enumerate → Exploit or Enumerate → Creds
```

## Advanced Features

### Graph Visualization

Generate a full workflow graph:

```bash
ctf-brain> graph
```

Output shows all nodes and their connections.

### Scoring System

The trigger matching system uses intelligent scoring:

- **Exact match:** +10 points
- **Word match:** +3 points per word
- **Tool match:** +5 points

Results are sorted by score for best matches.

### Path Finding

The CTF Brain uses depth-first search (DFS) to find paths between nodes:

```bash
ctf-brain> path 01-Ua-Recon 10-V-Cleanup
```

Returns the complete workflow from reconnaissance to cleanup.

## Integration Examples

### Custom Tool Integration

```typescript
import { CTFBrain } from './ctf-brain/index.js';

const brain = new CTFBrain();

// Build a custom workflow advisor
function getWorkflowAdvice(currentPhase: string, findings: string[]) {
  const nextSteps = brain.getRecommendedWorkflow(currentPhase);
  
  // Match findings to next best step
  const scored = nextSteps.map(workflow => {
    const targetNode = brain.getNode(workflow.path[1]);
    const findingMatches = findings.filter(f => 
      targetNode?.triggers.some(t => f.toLowerCase().includes(t))
    );
    return { workflow, matches: findingMatches.length };
  });
  
  return scored.sort((a, b) => b.matches - a.matches)[0].workflow;
}
```

### Automation Scripts

```bash
#!/bin/bash
# Auto-suggest tools based on phase

PHASE="$1"
TOOLS=$(npm run ctf-brain node "$PHASE" | grep "Tools:" | cut -d: -f2)

echo "Recommended tools for $PHASE:"
echo "$TOOLS"
```

## Testing

The CTF Brain can be tested with various queries:

```bash
# Test trigger matching
npm run ctf-brain query scan network
npm run ctf-brain query sql injection
npm run ctf-brain query privilege escalation

# Test tool lookup
npm run ctf-brain tool nmap
npm run ctf-brain tool metasploit
npm run ctf-brain tool burpsuite

# Test workflow navigation
npm run ctf-brain node 01-Ua-Recon
npm run ctf-brain next 04-Z-Exploit
npm run ctf-brain path 01-Ua-Recon 08-T-Exfil
```

## Contributing

To extend the CTF Brain:

1. Add new nodes to `config.json`
2. Define PLL algorithm mappings
3. Specify tools and triggers
4. Update edges for workflow connections
5. Test with CLI and Discord bot

## Troubleshooting

### CLI Not Starting

```bash
# Ensure dependencies are installed
npm install

# Try running with tsx directly
npx tsx src/ctf-brain/cli.ts
```

### Discord Commands Not Registering

```bash
# Check bot token and app ID
export DISCORD_TOKEN="your-token"
export APP_ID="your-app-id"

# Restart the bot
npm run bot
```

### Import Errors

Ensure you're using ES modules (type: "module" in package.json) and `.js` extensions in imports.

## License

MIT License - see LICENSE file

## Credits

- **Author:** Dom (Me10101) - Strategickhaos DAO LLC
- **Organization:** Strategickhaos DAO LLC
- **Framework:** Inspired by Rubik's Cube PLL algorithms and speedcubing methodology

## Support

For issues, questions, or contributions:
- Discord: [StrategicKhaos Discord Server]
- GitHub Issues: [Repository Issues]

---

**"See state → Recognize pattern → Execute algorithm → Objective achieved"**

*The CTF Brain brings the precision of speedcubing to the art of penetration testing.*
