#!/bin/bash
# SAGCO-MENU v1.2 - Interactive Demo
# This script demonstrates the features without requiring full installation

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    SAGCO-MENU v1.2 DEMONSTRATION                           ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "This demo shows SAGCO-MENU v1.2 features without full system installation."
echo ""

# Setup test environment
DEMO_DIR="/tmp/sagco-demo-$$"
mkdir -p "$DEMO_DIR/opt/sagco/bin"
mkdir -p "$DEMO_DIR/var/lib/sagco"

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy files
cp "$SCRIPT_DIR/opt/sagco/spm.yml" "$DEMO_DIR/opt/sagco/"
cp "$SCRIPT_DIR/opt/sagco/bin/sagco-menu.py" "$DEMO_DIR/opt/sagco/bin/"

# Patch paths
sed -i 's|SPM_PATH = "/opt/sagco/spm.yml"|SPM_PATH = "'$DEMO_DIR'/opt/sagco/spm.yml"|' \
    "$DEMO_DIR/opt/sagco/bin/sagco-menu.py"
sed -i 's|STATE_PATH = "/var/lib/sagco/menu_state.json"|STATE_PATH = "'$DEMO_DIR'/var/lib/sagco/menu_state.json"|' \
    "$DEMO_DIR/opt/sagco/bin/sagco-menu.py"

chmod +x "$DEMO_DIR/opt/sagco/bin/sagco-menu.py"

MENU="$DEMO_DIR/opt/sagco/bin/sagco-menu.py"

# Feature 1: Category Display
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ Feature 1: Ordered Categories with Icons                              │"
echo "└────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Categories are displayed in YAML-defined order with icons:"
echo ""
$MENU categories | while IFS=$'\t' read -r key icon desc; do
    printf "  %s %s - %s\n" "$icon" "$key" "$desc"
done
echo ""
read -p "Press Enter to continue..."
echo ""

# Feature 2: Tools with Icons
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ Feature 2: Tools with Icons (Core Utilities)                          │"
echo "└────────────────────────────────────────────────────────────────────────┘"
echo ""
$MENU items core-tools | while IFS=$'\t' read -r name icon desc cmd cat; do
    printf "  %s %s - %s\n" "$icon" "$name" "$desc"
done
echo ""
read -p "Press Enter to continue..."
echo ""

# Feature 3: Cross-Tool Search
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ Feature 3: Cross-Tool Fuzzy Search                                    │"
echo "└────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Search 1: Looking for 'docker'"
$MENU items all docker | while IFS=$'\t' read -r name icon desc cmd cat; do
    printf "  %s %s - %s (in %s)\n" "$icon" "$name" "$desc" "$cat"
done
echo ""

echo "Search 2: Looking for 'network' (matches multiple tools)"
$MENU items all network | while IFS=$'\t' read -r name icon desc cmd cat; do
    printf "  %s %s - %s (in %s)\n" "$icon" "$name" "$desc" "$cat"
done
echo ""

echo "Search 3: Case-insensitive search for 'NMAP'"
$MENU items all NMAP | while IFS=$'\t' read -r name icon desc cmd cat; do
    printf "  %s %s - %s (in %s)\n" "$icon" "$name" "$desc" "$cat"
done
echo ""
read -p "Press Enter to continue..."
echo ""

# Feature 4: Recently Used
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ Feature 4: Recently Used Tracking                                     │"
echo "└────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Adding tools to recently used list..."
$MENU add_recent core-tools Git
echo "  ✓ Added Git"
$MENU add_recent security-tools Nmap
echo "  ✓ Added Nmap"
$MENU add_recent core-tools Docker
echo "  ✓ Added Docker"
$MENU add_recent network-tools Curl
echo "  ✓ Added Curl"
echo ""

echo "Recently used list:"
$MENU recent | while IFS=$'\t' read -r name icon desc cmd cat; do
    printf "  %s %s - %s\n" "$icon" "$name" "$desc"
done
echo ""
read -p "Press Enter to continue..."
echo ""

# Feature 5: Recent List Limit
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ Feature 5: Recent List Limit (5 items max)                            │"
echo "└────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Adding 3 more tools (total 7 tools added)..."
$MENU add_recent ops-tools Terraform
echo "  ✓ Added Terraform"
$MENU add_recent core-tools Python
echo "  ✓ Added Python"
$MENU add_recent network-tools SSH
echo "  ✓ Added SSH"
echo ""

echo "Recently used list (only last 5 shown):"
$MENU recent | while IFS=$'\t' read -r name icon desc cmd cat; do
    printf "  %s %s - %s\n" "$icon" "$name" "$desc"
done
echo ""
echo "Note: Git (first item) was removed automatically."
echo ""
read -p "Press Enter to continue..."
echo ""

# Feature 6: Move to End
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ Feature 6: Re-using Tool Moves to End                                 │"
echo "└────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "Re-using Docker (currently in middle of list)..."
$MENU add_recent core-tools Docker
echo ""

echo "Updated recently used list:"
$MENU recent | while IFS=$'\t' read -r name icon desc cmd cat; do
    printf "  %s %s - %s\n" "$icon" "$name" "$desc"
done
echo ""
echo "Note: Docker moved to the end (most recent)."
echo ""
read -p "Press Enter to continue..."
echo ""

# Feature 7: State Persistence
echo "┌────────────────────────────────────────────────────────────────────────┐"
echo "│ Feature 7: State Persistence (JSON)                                   │"
echo "└────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "State file location: $DEMO_DIR/var/lib/sagco/menu_state.json"
echo ""
echo "State file contents:"
cat "$DEMO_DIR/var/lib/sagco/menu_state.json" | python3 -m json.tool
echo ""
read -p "Press Enter to continue..."
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                              DEMO COMPLETE                                 ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "SAGCO-MENU v1.2 Features Demonstrated:"
echo ""
echo "  ✅ Ordered categories with emoji icons"
echo "  ✅ Tools with individual icons"
echo "  ✅ Cross-tool fuzzy search (searches ALL categories)"
echo "  ✅ Case-insensitive search"
echo "  ✅ Recently used tracking (per-user)"
echo "  ✅ Automatic limit to 5 recent items"
echo "  ✅ Re-using tool moves to end (most recent)"
echo "  ✅ JSON state persistence"
echo ""
echo "To install on your system:"
echo "  1. cd sagco/"
echo "  2. sudo ./install.sh"
echo "  3. Login to new shell or run: /opt/sagco/bin/sagco-menu.sh"
echo ""
echo "DOM. 😭🔥💜"
echo ""

# Cleanup
rm -rf "$DEMO_DIR"
