#!/bin/bash
# SAGCO-MENU v1.1 - Interactive TUI Menu
# YAML-driven, state-aware menu with fuzzy search and recents

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_YAML="${SCRIPT_DIR}/tools.yaml"
MENU_PY="${SCRIPT_DIR}/sagco-menu.py"

# TTY-gated integration - only run if we have an interactive terminal
if [ ! -t 0 ]; then
    echo "Error: This script requires an interactive terminal (TTY)"
    exit 1
fi

# Check dependencies
if ! command -v whiptail &> /dev/null; then
    echo "Error: whiptail is required but not installed"
    echo "Install with: sudo apt-get install whiptail"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not installed"
    exit 1
fi

# Function to parse YAML and build menu
parse_tools() {
    python3 -c '
import yaml
import sys

try:
    with open("'"$TOOLS_YAML"'", "r") as f:
        data = yaml.safe_load(f)
except ImportError:
    # Fallback if PyYAML not installed - use basic parsing
    import re
    tools = []
    with open("'"$TOOLS_YAML"'", "r") as f:
        content = f.read()
        # Simple regex-based parsing
        in_tool = False
        current_tool = {}
        for line in content.split("\n"):
            if "- name:" in line and "tools:" not in line:
                if current_tool:
                    tools.append(current_tool)
                current_tool = {"name": line.split("name:")[1].strip().strip("\"")}
            elif "description:" in line and current_tool:
                current_tool["description"] = line.split("description:")[1].strip().strip("\"")
            elif "command:" in line and current_tool:
                current_tool["command"] = line.split("command:")[1].strip().strip("\"")
            elif "icon:" in line and current_tool:
                current_tool["icon"] = line.split("icon:")[1].strip().strip("\"")
        if current_tool:
            tools.append(current_tool)
    
    for tool in tools:
        name = tool.get("name", "Unknown")
        desc = tool.get("description", "")
        icon = tool.get("icon", "▶")
        cmd = tool.get("command", "")
        print(f"{icon} {name}|{desc}|{cmd}")
    sys.exit(0)

categories = data.get("categories", [])
for category in categories:
    cat_icon = category.get("icon", "📁")
    cat_name = category.get("name", "Unknown")
    tools = category.get("tools", [])
    
    for tool in tools:
        name = tool.get("name", "Unknown")
        desc = tool.get("description", "")
        icon = tool.get("icon", "▶")
        cmd = tool.get("command", "")
        
        print(f"{icon} {name}|{desc}|{cmd}|{cat_name}")
'
}

# Function to search tools
search_tools() {
    local query="$1"
    parse_tools | grep -i "$query" || true
}

# Function to show main menu
show_main_menu() {
    local choice
    choice=$(whiptail --title "SAGCO-MENU v1.1" \
        --menu "Choose an option:" 20 78 12 \
        "1" "🔍 Search Tools (Fuzzy)" \
        "2" "📋 Browse Categories" \
        "3" "⏱️  Recent Tools" \
        "4" "🗑️  Clear Recents" \
        "5" "❌ Exit" \
        3>&1 1>&2 2>&3)
    
    echo "$choice"
}

# Function to browse tools by category
browse_categories() {
    # Build category list
    local cat_list
    cat_list=$(python3 -c '
import yaml
with open("'"$TOOLS_YAML"'", "r") as f:
    data = yaml.safe_load(f)
    for i, cat in enumerate(data.get("categories", [])):
        icon = cat.get("icon", "📁")
        name = cat.get("name", "Unknown")
        print(f"{i}|{icon} {name}")
' 2>/dev/null || echo "0|📁 All Tools")
    
    local -a MENU_ARGS=()
    while IFS='|' read -r idx display; do
        MENU_ARGS+=("$idx" "$display")
    done <<< "$cat_list"
    
    if [[ ${#MENU_ARGS[@]} -eq 0 ]]; then
        whiptail --title "No Categories" --msgbox "No categories found." 8 50
        return
    fi
    
    local choice
    choice=$(whiptail --title "Browse Categories" \
        --menu "Select a category:" 20 78 12 \
        "${MENU_ARGS[@]}" \
        3>&1 1>&2 2>&3) || return
    
    # Show tools in selected category
    local cat_tools
    cat_tools=$(parse_tools | awk -F'|' -v cat="$choice" 'NR-1 == cat || cat == "0" {print}')
    show_tools_menu "$cat_tools" "Category Tools"
}

# Function to show tools menu
show_tools_menu() {
    local tools="$1"
    local title="${2:-Tool Selection}"
    
    local -a TOOL_ARGS=()
    local idx=0
    
    while IFS='|' read -r name desc _cmd _cat; do
        if [[ -n "$name" ]]; then
            TOOL_ARGS+=("$idx" "$name - $desc")
            idx=$((idx + 1))
        fi
    done <<< "$tools"
    
    # Micro-hardening #2: Guard empty search results
    if [[ ${#TOOL_ARGS[@]} -eq 0 ]]; then
        whiptail --title "No Results" --msgbox "No tools matched your search." 8 50
        return
    fi
    
    local choice
    choice=$(whiptail --title "$title" \
        --menu "Select a tool to run:" 20 78 12 \
        "${TOOL_ARGS[@]}" \
        3>&1 1>&2 2>&3) || return
    
    # Get the selected tool command
    local selected_tool
    selected_tool=$(echo "$tools" | sed -n "$((choice + 1))p")
    local tool_name
    tool_name=$(echo "$selected_tool" | cut -d'|' -f1)
    local tool_cmd
    tool_cmd=$(echo "$selected_tool" | cut -d'|' -f3)
    
    # Add to recent
    python3 "$MENU_PY" add "$tool_name" "$tool_cmd" 2>/dev/null || true
    
    # Confirm execution
    if whiptail --title "Confirm Execution" \
        --yesno "Run: $tool_name\n\nCommand: $tool_cmd\n\nContinue?" 12 78; then
        clear
        echo "=========================================="
        echo "Executing: $tool_name"
        echo "Command: $tool_cmd"
        echo "=========================================="
        echo ""
        
        # Execute the command
        # Security: Commands come from tools.yaml which should be system-controlled
        # This follows the pattern of system config files (sudoers, systemd units)
        eval "$tool_cmd" || true
        
        echo ""
        echo "=========================================="
        echo "Execution complete. Press Enter to continue..."
        read -r
    fi
}

# Function to show search interface
search_interface() {
    local query
    query=$(whiptail --title "🔍 Fuzzy Search" \
        --inputbox "Enter search term (name or description):" 10 78 \
        3>&1 1>&2 2>&3) || return
    
    if [[ -z "$query" ]]; then
        return
    fi
    
    local results
    results=$(search_tools "$query")
    show_tools_menu "$results" "Search Results: $query"
}

# Function to show recent tools
show_recent() {
    local recent
    recent=$(python3 "$MENU_PY" get 2>/dev/null || echo "")
    
    if [[ -z "$recent" ]] || [[ "$recent" == "No recent tools" ]]; then
        whiptail --title "Recent Tools" --msgbox "No recent tools found." 8 50
        return
    fi
    
    local -a TOOL_ARGS=()
    local idx=0
    
    while IFS=$'\t' read -r name _cmd; do
        if [[ -n "$name" ]]; then
            TOOL_ARGS+=("$idx" "$name")
            idx=$((idx + 1))
        fi
    done <<< "$recent"
    
    if [[ ${#TOOL_ARGS[@]} -eq 0 ]]; then
        whiptail --title "Recent Tools" --msgbox "No recent tools found." 8 50
        return
    fi
    
    local choice
    choice=$(whiptail --title "⏱️  Recent Tools" \
        --menu "Select a recent tool:" 20 78 12 \
        "${TOOL_ARGS[@]}" \
        3>&1 1>&2 2>&3) || return
    
    # Get the selected tool
    local selected
    selected=$(echo "$recent" | sed -n "$((choice + 1))p")
    local tool_name
    tool_name=$(echo "$selected" | cut -f1)
    local tool_cmd
    tool_cmd=$(echo "$selected" | cut -f2)
    
    # Confirm execution
    if whiptail --title "Confirm Execution" \
        --yesno "Run: $tool_name\n\nCommand: $tool_cmd\n\nContinue?" 12 78; then
        clear
        echo "=========================================="
        echo "Executing: $tool_name"
        echo "Command: $tool_cmd"
        echo "=========================================="
        echo ""
        
        # Execute the command
        # Security: Commands come from tools.yaml which should be system-controlled
        # This follows the pattern of system config files (sudoers, systemd units)
        eval "$tool_cmd" || true
        
        echo ""
        echo "=========================================="
        echo "Execution complete. Press Enter to continue..."
        read -r
    fi
}

# Function to clear recent tools
clear_recents() {
    if whiptail --title "Clear Recents" \
        --yesno "Are you sure you want to clear all recent tools?" 8 78; then
        python3 "$MENU_PY" clear 2>/dev/null || true
        whiptail --title "Success" --msgbox "Recent tools cleared." 8 50
    fi
}

# Main loop
main() {
    while true; do
        choice=$(show_main_menu)
        
        case $choice in
            1)
                search_interface
                ;;
            2)
                browse_categories
                ;;
            3)
                show_recent
                ;;
            4)
                clear_recents
                ;;
            5|"")
                clear
                echo "Exiting SAGCO-MENU. Goodbye!"
                exit 0
                ;;
            *)
                whiptail --title "Error" --msgbox "Invalid selection." 8 50
                ;;
        esac
    done
}

# Run main
main
