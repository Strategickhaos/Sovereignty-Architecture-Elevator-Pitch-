#!/bin/bash
# SAGCO-MENU v1.2 Architecture Visualization

cat << 'EOF'
╔════════════════════════════════════════════════════════════════════════════╗
║                      SAGCO-MENU v1.2 ARCHITECTURE                          ║
╚════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────┐
│                         USER LOGIN (Interactive TTY)                      │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                     /etc/profile.d/sagco-menu.sh                         │
│  • Detects interactive shell with TTY                                    │
│  • Checks for recursion (SAGCO_MENU_ACTIVE)                              │
│  • Launches main menu                                                    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    /opt/sagco/bin/sagco-menu.sh                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 1. Load Recent Tools (if any)                                   │    │
│  │    → Python: sagco-menu.py recent                               │    │
│  │                                                                  │    │
│  │ 2. Build Category Menu                                          │    │
│  │    → Python: sagco-menu.py categories                           │    │
│  │    → Display with icons: 🛠️ 🔒 ⚙️ 🌐                            │    │
│  │                                                                  │    │
│  │ 3. Show whiptail Menu                                           │    │
│  │    ┌────────────────────────────────┐                           │    │
│  │    │ 🕒 Recently Used               │                           │    │
│  │    │ 🛠️  Core System Utilities     │ ← User selects            │    │
│  │    │ 🔒 Security & Pen Testing     │                           │    │
│  │    │ ⚙️  DevOps & Operations       │                           │    │
│  │    └────────────────────────────────┘                           │    │
│  │                                                                  │    │
│  │ 4. Search Prompt (Optional)                                     │    │
│  │    → User can filter tools across ALL categories               │    │
│  │                                                                  │    │
│  │ 5. Build Tool Menu                                              │    │
│  │    → Python: sagco-menu.py items <category> [search]           │    │
│  │    → Cross-tool search if search term provided                 │    │
│  │    → Display with icons: 📂 🐳 ☸️                               │    │
│  │                                                                  │    │
│  │ 6. Execute Selected Tool                                        │    │
│  │    → Run command via bash -lc                                   │    │
│  │    → Display output                                             │    │
│  │                                                                  │    │
│  │ 7. Add to Recent                                                │    │
│  │    → Python: sagco-menu.py add_recent <category> <tool>        │    │
│  │                                                                  │    │
│  │ 8. Loop back to main menu                                       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              ▼                                           ▼
┌──────────────────────────────┐         ┌──────────────────────────────┐
│  /opt/sagco/bin/sagco-menu.py│         │     /opt/sagco/spm.yml      │
│                              │         │                              │
│  Python Backend Functions:   │         │  YAML Configuration:         │
│  • load_spm()                │ ◄───────│  • tools.order[]             │
│  • categories()              │         │  • Category definitions      │
│  • items()                   │         │    - icon                    │
│  • all_items()               │         │    - description             │
│  • recent()                  │         │    - items[]                 │
│  • add_recent()              │         │      - name                  │
│  • get_close_matches()       │         │      - icon                  │
│    (fuzzy search via difflib)│         │      - command               │
│                              │         │      - description            │
└──────────────────────────────┘         └──────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│           /var/lib/sagco/menu_state.json (Recently Used)                 │
│  {                                                                       │
│    "alice": {                                                            │
│      "recent": ["core-tools:Git", "security-tools:Nmap", ...]           │
│    },                                                                    │
│    "bob": {                                                              │
│      "recent": ["network-tools:Curl", "ops-tools:Terraform", ...]       │
│    }                                                                     │
│  }                                                                       │
└──────────────────────────────────────────────────────────────────────────┘


╔════════════════════════════════════════════════════════════════════════════╗
║                         DATA FLOW DIAGRAM                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

User Input (Search)
        │
        ▼
┌───────────────┐
│ sagco-menu.py │
│   items()     │
└───────────────┘
        │
        ├─► Load all tools from YAML
        │   └─► Iterate categories
        │       └─► Extract items
        │
        ├─► Apply search filter
        │   └─► get_close_matches() - Fuzzy matching
        │       • Cutoff: 0.6 (60% similarity)
        │       • Searches: name + description
        │
        └─► Return filtered results
            └─► Format: name\ticon\tdesc\tcmd\tcat


Recent Tool Usage
        │
        ▼
┌───────────────┐
│ sagco-menu.py │
│ add_recent()  │
└───────────────┘
        │
        ├─► Load state from JSON
        │   └─► Get user-specific data ($USER)
        │
        ├─► Create entry: "category:name"
        │   └─► Remove if already exists
        │   └─► Append to end (most recent)
        │
        ├─► Trim to last 5 entries
        │
        └─► Save state to JSON
            └─► Per-user keys in JSON


Category Ordering
        │
        ▼
┌───────────────┐
│ sagco-menu.py │
│ categories()  │
└───────────────┘
        │
        ├─► Load YAML
        │   └─► Read tools.order array
        │
        ├─► Iterate in order
        │   └─► For each key in order:
        │       └─► Get icon, description
        │
        └─► Return ordered list
            └─► Format: key\ticon\tdesc


╔════════════════════════════════════════════════════════════════════════════╗
║                         EXECUTION FLOW                                     ║
╚════════════════════════════════════════════════════════════════════════════╝

┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Login   │────>│ Category │────>│  Search  │────>│   Tool   │
│          │     │ Selection│     │ (Optional│     │ Selection│
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                           │
                                                           ▼
                                                    ┌──────────┐
                                                    │ Execute  │
                                                    │ Command  │
                                                    └──────────┘
                                                           │
                                                           ▼
                                                    ┌──────────┐
                                                    │   Add    │
                                                    │  Recent  │
                                                    └──────────┘
                                                           │
                                                           ▼
                                                    ┌──────────┐
                                                    │  Return  │
                                                    │ to Menu  │
                                                    └──────────┘


╔════════════════════════════════════════════════════════════════════════════╗
║                      KEY FEATURES SUMMARY                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

✨ CROSS-TOOL SEARCH
   • Searches across ALL categories simultaneously
   • Fuzzy matching via Python's difflib.get_close_matches()
   • 60% similarity threshold
   • Searches: tool name, description, and command

🎨 CATEGORY ORDERING
   • YAML "order" array controls display sequence
   • Deterministic menu structure
   • No hardcoding

🎭 ICONS
   • Category icons (emoji/ASCII): 🛠️ 🔒 ⚙️ 🌐
   • Tool icons: 📂 🐳 ☸️ 🔍 🦈
   • Visual identification

🕒 RECENTLY USED
   • Last 5 tools tracked
   • Per-user state (JSON)
   • Automatically added after execution
   • Deduplication (re-use moves to end)

👤 PER-USER STATE
   • Each user has independent recent list
   • $USER environment variable for key
   • Fallback to "global" if no $USER

📦 ZERO NEW DEPENDENCIES
   • Python difflib (built-in)
   • whiptail (existing from v1)
   • PyYAML (standard)


╔════════════════════════════════════════════════════════════════════════════╗
║                              VERSION INFO                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

Version: 1.2
Owner: Strategickhaos DAO LLC
Developer: Dom (Me10101)
Architecture: YAML-driven deterministic menu system

Enhancements from v1.1:
  • Cross-tool search with fuzzy matching
  • Per-user recently used tracking
  • No changes to YAML structure (backward compatible)

DOM. 😭🔥💜

EOF
