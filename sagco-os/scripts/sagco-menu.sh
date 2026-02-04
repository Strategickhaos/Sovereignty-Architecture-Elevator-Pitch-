#!/bin/bash
#
# SAGCO Tools Menu - TUI Launcher
# Reads tool groups from /opt/sagco/spm.yml and launches them via whiptail
# Kali/Parrot-style interactive menu system
#

set -e

SPM="/opt/sagco/spm.yml"
YQ="/usr/bin/yq"

# Check if spm.yml exists
if [ ! -f "$SPM" ]; then
    echo "Error: $SPM not found. Please run sagco-spm.py first."
    exit 1
fi

# Function to extract YAML values using Python (since yq might not be installed)
get_yaml_value() {
    local key="$1"
    python3 -c "
import yaml
with open('$SPM', 'r') as f:
    config = yaml.safe_load(f)
    
keys = '$key'.split('.')
value = config
for k in keys:
    value = value.get(k, {})
    
if isinstance(value, dict):
    print(' '.join(value.keys()))
elif isinstance(value, list):
    for item in value:
        if isinstance(item, dict):
            print(item.get('name', ''), item.get('description', ''), item.get('command', ''))
        else:
            print(item)
else:
    print(value)
"
}

# Get list of tool groups
get_tool_groups() {
    python3 -c "
import yaml
with open('$SPM', 'r') as f:
    config = yaml.safe_load(f)
    tools = config.get('tools', {})
    for name, data in tools.items():
        desc = data.get('description', name)
        print(f'{name}|{desc}')
"
}

# Get tools from a specific group
get_tools_in_group() {
    local group="$1"
    python3 -c "
import yaml
with open('$SPM', 'r') as f:
    config = yaml.safe_load(f)
    tools = config.get('tools', {})
    group_data = tools.get('$group', {})
    items = group_data.get('items', [])
    for item in items:
        name = item.get('name', '')
        desc = item.get('description', '')
        cmd = item.get('command', '')
        print(f'{name}|{desc}|{cmd}')
"
}

# Main menu - show tool categories
show_main_menu() {
    # Build menu options from YAML
    menu_options=()
    while IFS='|' read -r name desc; do
        menu_options+=("$name" "$desc")
    done < <(get_tool_groups)
    
    # Add exit option
    menu_options+=("Exit" "Exit to shell")
    
    CHOICE=$(whiptail --title "SAGCO Tools Menu - Ratio Ex Nihilo" \
                      --menu "Select a tool category:" \
                      20 70 10 \
                      "${menu_options[@]}" \
                      3>&1 1>&2 2>&3)
    
    exitstatus=$?
    if [ $exitstatus != 0 ]; then
        exit 0
    fi
    
    if [ "$CHOICE" = "Exit" ]; then
        exit 0
    fi
    
    show_tools_menu "$CHOICE"
}

# Tools menu - show tools in selected category
show_tools_menu() {
    local category="$1"
    
    # Build menu options for tools
    menu_options=()
    declare -A commands
    
    while IFS='|' read -r name desc cmd; do
        menu_options+=("$name" "$desc")
        commands["$name"]="$cmd"
    done < <(get_tools_in_group "$category")
    
    # Add back option
    menu_options+=("Back" "Return to main menu")
    
    TOOL_CHOICE=$(whiptail --title "SAGCO - $category" \
                           --menu "Select a tool to launch:" \
                           20 70 10 \
                           "${menu_options[@]}" \
                           3>&1 1>&2 2>&3)
    
    exitstatus=$?
    if [ $exitstatus != 0 ] || [ "$TOOL_CHOICE" = "Back" ]; then
        show_main_menu
        return
    fi
    
    # Launch the selected tool
    launch_tool "${commands[$TOOL_CHOICE]}"
    
    # Return to tools menu after command completes
    show_tools_menu "$category"
}

# Launch a tool command
launch_tool() {
    local cmd="$1"
    
    clear
    echo "=========================================="
    echo "SAGCO OS - Launching Tool"
    echo "=========================================="
    echo "Command: $cmd"
    echo ""
    
    # Execute the command
    eval "$cmd"
    
    echo ""
    echo "=========================================="
    echo "Press Enter to continue..."
    read -r
}

# Main entry point
main() {
    # Check if whiptail is installed
    if ! command -v whiptail &> /dev/null; then
        echo "Error: whiptail is not installed. Please install it first:"
        echo "  apt-get install whiptail"
        exit 1
    fi
    
    # Check if Python3 is installed
    if ! command -v python3 &> /dev/null; then
        echo "Error: python3 is not installed."
        exit 1
    fi
    
    # Start the main menu loop
    show_main_menu
}

# Run main function
main
