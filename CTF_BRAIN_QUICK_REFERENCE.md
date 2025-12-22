# CTF Brain Quick Reference

## Node Reference Table

| Node ID | Phase | PLL Algorithm | Key Tools | Primary Trigger |
|---------|-------|---------------|-----------|-----------------|
| 01-Ua-Recon | Reconnaissance | Ua Perm | nmap, masscan, shodan | scan, recon |
| 02-Ub-Enum | Enumeration | Ub Perm | gobuster, ffuf, enum4linux | enum, directory |
| 03-H-WebApp | Web Application | H Perm | burpsuite, sqlmap, nikto | web, sql, xss |
| 04-Z-Exploit | Exploitation | Z Perm | metasploit, nc, msfvenom | exploit, shell, rce |
| 05-Aa-Creds | Credential Attacks | Aa Perm | hydra, hashcat, john | password, hash |
| 06-Ab-PrivEsc | Privilege Escalation | Ab Perm | linpeas, winpeas, pspy | privesc, root, sudo |
| 07-E-Persist | Persistence | E Perm | cron, ssh keys, implants | persist, backdoor |
| 08-T-Exfil | Exfiltration | T Perm | nc, curl, scp | exfil, extract, data |
| 09-F-Pivot | Pivoting | F Perm | chisel, proxychains, socat | pivot, tunnel, lateral |
| 10-V-Cleanup | Cleanup | V Perm | shred, wevtutil, timestomp | cleanup, clear, logs |

## Common Workflows

### Full Penetration Test
```
01-Ua-Recon → 02-Ub-Enum → 04-Z-Exploit → 06-Ab-PrivEsc → 
07-E-Persist → 08-T-Exfil → 10-V-Cleanup
```

### Web Application Assessment
```
01-Ua-Recon → 03-H-WebApp → 04-Z-Exploit → 06-Ab-PrivEsc → 08-T-Exfil
```

### Network Lateral Movement
```
04-Z-Exploit → 09-F-Pivot → 01-Ua-Recon (internal) → 02-Ub-Enum → 04-Z-Exploit
```

### Credential-Based Assessment
```
01-Ua-Recon → 02-Ub-Enum → 05-Aa-Creds → 04-Z-Exploit → 06-Ab-PrivEsc
```

## CLI Commands

### Basic Queries
```bash
# Search for methodology by keywords
npm run ctf-brain query <keywords>

# Find methodology by tool
npm run ctf-brain tool <toolname>

# Get node details
npm run ctf-brain node <node-id>

# Show next steps
npm run ctf-brain next <node-id>

# Find path between nodes
npm run ctf-brain path <start> <end>

# List all nodes
npm run ctf-brain list

# Show workflow graph
npm run ctf-brain graph

# Show help
npm run ctf-brain help
```

### Example Commands
```bash
npm run ctf-brain query web sql injection
npm run ctf-brain tool nmap
npm run ctf-brain node 01-Ua-Recon
npm run ctf-brain next 04-Z-Exploit
npm run ctf-brain path 01-Ua-Recon 08-T-Exfil
```

## Discord Commands

### Available Slash Commands

- `/ctf-query keywords:<text>` - Search methodology by keywords
- `/ctf-tool toolname:<text>` - Find nodes using specific tool
- `/ctf-node node-id:<text>` - Get detailed node information
- `/ctf-next node-id:<text>` - Get recommended next steps
- `/ctf-path start:<text> end:<text>` - Find workflow path
- `/ctf-list` - List all methodology nodes
- `/ctf-info` - Show CTF Brain metadata

### Example Discord Usage
```
/ctf-query keywords: web application sql injection
/ctf-tool toolname: metasploit
/ctf-node node-id: 04-Z-Exploit
/ctf-next node-id: 06-Ab-PrivEsc
/ctf-path start: 01-Ua-Recon end: 10-V-Cleanup
```

## PLL Algorithm Notation

### Basic Moves
- **R** = Right face clockwise
- **R'** = Right face counter-clockwise
- **U** = Up face clockwise
- **U'** = Up face counter-clockwise
- **M** = Middle layer (left face direction)
- **M'** = Middle layer reverse
- **M2** = Middle layer 180°
- **x** = Rotate entire cube on R
- **y** = Rotate entire cube on U
- **D** = Down face clockwise
- **F** = Front face clockwise

### All PLL Algorithms

1. **Ua Perm**: M'2 U M U2 M' U M'2
2. **Ub Perm**: M'2 U' M U2 M' U' M'2
3. **H Perm**: M'2 U M'2 U2 M'2 U M'2
4. **Z Perm**: M' U M'2 U M'2 U M' U2 M'2
5. **Aa Perm**: x' R2 D2 R U R' D2 R U' R
6. **Ab Perm**: x' R U' R D2 R' U R D2 R2
7. **E Perm**: x' R U' R' D R U R' D' R U R' D R U' R' D'
8. **T Perm**: R U R' U' R' F R2 U' R' U' R U R' F'
9. **F Perm**: R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R
10. **V Perm**: R' U R' U' y R' F' R2 U' R' U R' F R F

## Trigger Keywords by Phase

### 01-Ua-Recon
`scan`, `recon`, `discover`, `find hosts`, `port scan`, `network map`

### 02-Ub-Enum
`enum`, `directory`, `users`, `shares`, `ldap`, `smb`

### 03-H-WebApp
`web`, `sql`, `injection`, `xss`, `http`, `api`, `form`

### 04-Z-Exploit
`exploit`, `shell`, `reverse`, `payload`, `foothold`, `rce`

### 05-Aa-Creds
`password`, `crack`, `brute`, `hash`, `credential`, `ntlm`

### 06-Ab-PrivEsc
`privesc`, `root`, `admin`, `escalate`, `sudo`, `suid`

### 07-E-Persist
`persist`, `backdoor`, `maintain`, `cron`, `startup`

### 08-T-Exfil
`exfil`, `extract`, `data`, `transfer`, `steal`, `download`

### 09-F-Pivot
`pivot`, `tunnel`, `lateral`, `internal`, `proxy`

### 10-V-Cleanup
`cleanup`, `clear`, `logs`, `evidence`, `tracks`

## Tool Categories

### Reconnaissance
nmap, masscan, shodan, whois, dig, theHarvester

### Enumeration
gobuster, ffuf, enum4linux, smbclient, ldapsearch, snmpwalk

### Web Application
burpsuite, sqlmap, nikto, wpscan, nuclei, httpx

### Exploitation
metasploit, nc, searchsploit, pwntools, msfvenom

### Credential Attacks
hydra, hashcat, john, crackmapexec, responder, mimikatz

### Privilege Escalation
linpeas, winpeas, pspy, sudo -l, suid3num, powerup

### Persistence
cron, registry, scheduled tasks, ssh keys, implants

### Exfiltration
nc, curl, dns, base64, steghide, scp

### Pivoting
chisel, ligolo, sshuttle, proxychains, socat

### Cleanup
history -c, shred, wevtutil, timestomp

## Expected Outputs by Phase

| Phase | Expected Output |
|-------|-----------------|
| Reconnaissance | IP addresses, open ports, service versions, hostnames |
| Enumeration | directories, usernames, shares, domain info |
| Web Application | vulnerabilities, injection points, auth bypasses |
| Exploitation | shell access, reverse connection, command execution |
| Credential Attacks | cracked passwords, hashes, tokens, tickets |
| Privilege Escalation | root/admin access, elevated shell, system control |
| Persistence | persistent access, backdoor, callback mechanism |
| Exfiltration | extracted files, dumped databases, credentials |
| Pivoting | internal access, new subnets, additional hosts |
| Cleanup | cleared logs, removed artifacts, stealth maintained |

## Interactive Mode

Start interactive mode:
```bash
npm run ctf-brain
```

Available commands in interactive mode:
```
ctf-brain> query web application sql injection
ctf-brain> tool nmap
ctf-brain> node 01-Ua-Recon
ctf-brain> next 04-Z-Exploit
ctf-brain> path 01-Ua-Recon 08-T-Exfil
ctf-brain> list
ctf-brain> graph
ctf-brain> help
ctf-brain> exit
```

## Scoring System

The CTF Brain uses intelligent scoring for trigger matching:

- **Exact keyword match**: +10 points
- **Word match**: +3 points per word
- **Tool match**: +5 points

Results are automatically sorted by score, with highest matches first.

## Philosophy

**"See state → Recognize pattern → Execute algorithm → Objective achieved"**

The CTF Brain brings the precision and pattern recognition of Rubik's Cube speedcubing
to penetration testing methodology. Just as a cuber recognizes a specific permutation
and executes the perfect algorithm, security professionals can recognize assessment
states and execute the appropriate methodology.

---

*Created by Dom (Me10101) - Strategickhaos DAO LLC*
