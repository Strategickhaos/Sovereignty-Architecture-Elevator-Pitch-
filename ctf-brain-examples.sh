#!/bin/bash
# CTF Brain Example Usage Script
# Demonstrates the various capabilities of the CTF Brain

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         CTF Brain Example Usage Demonstration            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Function to run a command with header
run_example() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Example $1: $2"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Command: $3"
    echo ""
    eval "$3"
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

# Example 1: Query by keywords
run_example "1" \
    "Search for methodology nodes related to web SQL injection" \
    "npm run ctf-brain query web sql injection"

# Example 2: Find tools
run_example "2" \
    "Find which methodology phase uses nmap" \
    "npm run ctf-brain tool nmap"

# Example 3: Get node details
run_example "3" \
    "Get detailed information about the Reconnaissance phase" \
    "npm run ctf-brain node 01-Ua-Recon"

# Example 4: Get next steps
run_example "4" \
    "Show recommended next steps after gaining shell access (Exploitation)" \
    "npm run ctf-brain next 04-Z-Exploit"

# Example 5: Find workflow path
run_example "5" \
    "Find the workflow path from Reconnaissance to Exfiltration" \
    "npm run ctf-brain path 01-Ua-Recon 08-T-Exfil"

# Example 6: List all nodes
run_example "6" \
    "List all methodology nodes" \
    "npm run ctf-brain list"

# Example 7: Query for privilege escalation
run_example "7" \
    "Search for privilege escalation methodology" \
    "npm run ctf-brain query privilege escalation root access"

# Example 8: Find metasploit usage
run_example "8" \
    "Find which phase uses metasploit framework" \
    "npm run ctf-brain tool metasploit"

# Example 9: Path from exploit to cleanup
run_example "9" \
    "Find workflow from Exploitation to Cleanup" \
    "npm run ctf-brain path 04-Z-Exploit 10-V-Cleanup"

# Example 10: Query credential attacks
run_example "10" \
    "Search for password cracking methodology" \
    "npm run ctf-brain query password hash crack"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         All Examples Complete!                           ║"
echo "║                                                          ║"
echo "║  Try the interactive mode:                               ║"
echo "║  $ npm run ctf-brain                                     ║"
echo "║                                                          ║"
echo "║  Or run individual commands:                             ║"
echo "║  $ npm run ctf-brain <command> <args>                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
