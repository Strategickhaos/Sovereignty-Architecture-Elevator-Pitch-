#!/bin/bash
# SAGCO-MENU v1.1 - Demo Script
# Demonstrates the menu system without requiring TTY

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                        SAGCO-MENU v1.1 Demo                                ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Demo 1: Show menu structure
echo "📋 Menu Structure"
echo "─────────────────"
python3 -c "
import yaml
with open('tools.yaml', 'r') as f:
    data = yaml.safe_load(f)
for cat in data.get('categories', []):
    print(f\"{cat['icon']} {cat['name']} ({len(cat['tools'])} tools)\")
"
echo ""

# Demo 2: Per-user state
echo "👥 Per-User State Management"
echo "─────────────────────────────"
export USER="alice"
./sagco-menu.py clear 2>/dev/null
./sagco-menu.py add "Network Mapper" "python3 network_sovereignty_monitor.py"
./sagco-menu.py add "Traffic Monitor" "python3 network_sovereignty_monitor.py --monitor"
echo "Alice's recents:"
./sagco-menu.py get | sed 's/^/  /'

export USER="bob"
./sagco-menu.py clear 2>/dev/null
./sagco-menu.py add "Vulnerability Scanner" "python3 eval_redteam.py"
./sagco-menu.py add "Quick Deploy" "bash quick-deploy.sh"
echo ""
echo "Bob's recents:"
./sagco-menu.py get | sed 's/^/  /'
echo ""

# Demo 3: Cap at 5
echo "📊 Recents Cap (5 items max)"
echo "─────────────────────────────"
export USER="charlie"
./sagco-menu.py clear 2>/dev/null
for i in {1..7}; do
    ./sagco-menu.py add "Tool $i" "echo $i" 2>/dev/null
done
echo "Added 7 tools, showing last 5:"
./sagco-menu.py get | sed 's/^/  /'
echo ""

# Demo 4: Deduplication
echo "🔄 Automatic Deduplication"
echo "──────────────────────────"
export USER="diana"
./sagco-menu.py clear 2>/dev/null
./sagco-menu.py add "Port Scanner" "bash ps5_neural_commands.sh scan" 2>/dev/null
./sagco-menu.py add "Web Crawler" "python3 crawler/crawl.py" 2>/dev/null
./sagco-menu.py add "Legion Orchestrator" "python3 legion_orchestrator.py" 2>/dev/null
echo "Initial recents:"
./sagco-menu.py get | sed 's/^/  /'
echo ""
./sagco-menu.py add "Port Scanner" "bash ps5_neural_commands.sh scan --verbose" 2>/dev/null
echo "After re-adding Port Scanner (moved to end, no duplicate):"
./sagco-menu.py get | sed 's/^/  /'
echo ""

# Demo 5: Main menu options
echo "🎯 Main Menu Options"
echo "────────────────────"
echo "  1. 🔍 Search Tools (Fuzzy)      - Search across all tools"
echo "  2. 📋 Browse Categories         - Browse by category"
echo "  3. ⏱️  Recent Tools              - Quick access to recents"
echo "  4. 🗑️  Clear Recents             - Clear history"
echo "  5. ❌ Exit                       - Exit menu"
echo ""

# Cleanup
echo "🧹 Cleanup"
echo "──────────"
for user in alice bob charlie diana; do
    export USER="$user"
    ./sagco-menu.py clear 2>/dev/null
done
echo "✅ Demo data cleaned up"
echo ""

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                       All Features Demonstrated!                           ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "To launch the interactive menu, run:"
echo "  ./sagco-menu.sh"
echo ""
echo "Features:"
echo "  ✅ Per-user state (Micro-hardening #1)"
echo "  ✅ Empty search guard (Micro-hardening #2)"
echo "  ✅ Recents capped at 5 (Micro-hardening #3)"
echo "  ✅ YAML-driven configuration"
echo "  ✅ Fuzzy search"
echo "  ✅ TTY-gated"
