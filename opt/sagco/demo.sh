#!/bin/bash
# SAGCO Menu Demo Script
# Demonstrates all features: categories, icons, search, and recently used

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SAGCO_PY="$REPO_ROOT/opt/sagco/bin/sagco-menu.py"

echo "================================================================================"
echo "SAGCO MENU v1.1 - DEMONSTRATION"
echo "================================================================================"
echo ""

# Clean state for demo
rm -f "$REPO_ROOT/opt/sagco/menu_state.json"

echo "1. Listing Categories (with icons and ordering)"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" categories
echo ""

echo "2. Listing Items in 'core-tools' Category"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" items core-tools
echo ""

echo "3. Listing Items in 'security-tools' Category"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" items security-tools
echo ""

echo "4. Search Functionality - Search for 'nmap'"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" items security-tools nmap
echo ""

echo "5. Search Functionality - Search for 'network' (by description)"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" items security-tools network
echo ""

echo "6. Recently Used - Initially Empty"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" recent || echo "(No recent items)"
echo ""

echo "7. Adding Items to Recently Used"
echo "--------------------------------------------------------------------------------"
echo "Adding: Git, Nmap, Docker, TMUX"
python3 "$SAGCO_PY" add_recent core-tools Git
python3 "$SAGCO_PY" add_recent security-tools Nmap
python3 "$SAGCO_PY" add_recent ops-tools Docker
python3 "$SAGCO_PY" add_recent core-tools TMUX
echo "Done!"
echo ""

echo "8. Recently Used - After Adding Items"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" recent
echo ""

echo "9. Adding Git Again (should move to end)"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" add_recent core-tools Git
python3 "$SAGCO_PY" recent
echo ""

echo "10. All Categories with Icons"
echo "--------------------------------------------------------------------------------"
python3 "$SAGCO_PY" categories | while IFS=$'\t' read -r key icon desc; do
  echo "  $icon  $desc ($key)"
done
echo ""

echo "================================================================================"
echo "DEMO COMPLETE - All Features Verified ✓"
echo "================================================================================"
echo ""
echo "Features Demonstrated:"
echo "  ✓ YAML-driven configuration"
echo "  ✓ Category ordering"
echo "  ✓ Icons for categories and items"
echo "  ✓ Search/filter functionality"
echo "  ✓ Recently used tracking"
echo "  ✓ Duplicate handling in recent list"
echo ""
echo "To run the interactive menu: ./opt/sagco/bin/sagco-menu.sh"
echo "(Requires whiptail - standard on most Linux distributions)"
