# SAGCO Menu v1.2 - Workflow Demo

## Interactive Menu Flow

### 1. Launch Menu
```bash
/opt/sagco/bin/sagco-menu.sh
```

### 2. Category Selection Screen
```
┌─────────────────── SAGCO Tools Menu ────────────────────┐
│ Select category:                                         │
│                                                           │
│    recent      🕒 Recently Used                          │
│    security-tools  🔒 Security and penetration testing   │
│    networking     🌐 Network tools and utilities         │
│    development    💻 Development tools and environments  │
│    system-admin   ⚙️ System administration tools        │
│                                                           │
│                  <OK>        <Cancel>                     │
└───────────────────────────────────────────────────────────┘
```

### 3. Search Prompt (Optional)
```
┌─────────────────── Search networking ───────────────────┐
│ Enter search term (optional):                            │
│                                                           │
│ _______________________________________________________  │
│                                                           │
│                  <OK>        <Cancel>                     │
└───────────────────────────────────────────────────────────┘
```

### 4. Tool Selection Screen
```
┌─────────────────── SAGCO: networking ───────────────────┐
│ Select tool:                                              │
│                                                           │
│    networking::Ping       📡 Ping — Test network conn   │
│    networking::Traceroute 🗺️ Traceroute — Trace netwo  │
│    networking::Netstat    📊 Netstat — Network statist  │
│    networking::ss         🔌 ss — Socket statistics      │
│                                                           │
│                  <OK>        <Cancel>                     │
└───────────────────────────────────────────────────────────┘
```

Note: Keys are internal (networking::Ping) but display is clean.

### 5. Tool Execution
```bash
SAGCO ▶ Ping
CMD  ▶ ping -c 4 8.8.8.8

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=10.2 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=116 time=9.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=116 time=10.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=116 time=9.9 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 9.799/10.000/10.196/0.150 ms

Press Enter to return to menu...
```

## CLI Usage Examples

### List all categories
```bash
$ SPM_PATH=./opt/sagco/spm.yml ./opt/sagco/bin/sagco-menu.py categories
security-tools	🔒	Security and penetration testing tools
networking	🌐	Network tools and utilities
development	💻	Development tools and environments
system-admin	⚙️	System administration tools
```

### List tools in a category
```bash
$ SPM_PATH=./opt/sagco/spm.yml ./opt/sagco/bin/sagco-menu.py items networking
Ping	📡	Test network connectivity	ping -c 4 8.8.8.8	networking
Traceroute	🗺️	Trace network path	traceroute 8.8.8.8	networking
Netstat	📊	Network statistics	netstat -tuln	networking
ss	🔌	Socket statistics	ss -tuln	networking
```

### Global search across all tools
```bash
$ SPM_PATH=./opt/sagco/spm.yml ./opt/sagco/bin/sagco-menu.py items all "python"
Python Shell	🐍	Interactive Python interpreter	python3 -c '...'	development
```

### View recent tools
```bash
$ SPM_PATH=./opt/sagco/spm.yml ./opt/sagco/bin/sagco-menu.py recent
Ping	📡	Test network connectivity	ping -c 4 8.8.8.8	networking
```

### Add to recent
```bash
$ SPM_PATH=./opt/sagco/spm.yml ./opt/sagco/bin/sagco-menu.py add_recent networking Ping
```

## State File Location

### Default (XDG_STATE_HOME unset)
```bash
~/.local/state/sagco/menu_state.json
```

### With XDG_STATE_HOME set
```bash
$XDG_STATE_HOME/sagco/menu_state.json
```

### State File Format
```json
{
  "recent": [
    "networking:Ping",
    "development:Python Shell",
    "system-admin:Disk Usage"
  ]
}
```

**Note**: The state file uses single colon (`:`) format (`category:name`) for internal storage, while the shell script uses double colon (`::`) format (`category::name`) for whiptail menu keys to prevent collisions. The Python script handles the conversion between these formats.

## Key Features Demonstrated

### ✅ Bug Fix 1: Per-user State
- Non-root users can run the menu
- State stored in user's home directory
- Respects XDG Base Directory specification

### ✅ Bug Fix 2: Collision Prevention
- Tools with same name in different categories don't collide
- Internal keys use `category::name` format
- Display shows clean names without internal keys

### ✅ Bug Fix 3: Clean Categories
- "order" key never appears in category list
- Only actual categories are shown

### 🎯 Capstone Features
- YAML-driven (single source of truth)
- Ordered categories
- Full emoji/icon support
- Global fuzzy search
- Per-user recency tracking
- No hardcoded menu structure
