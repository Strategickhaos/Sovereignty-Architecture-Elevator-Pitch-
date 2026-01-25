#!/bin/bash
################################################################################
# SAGCO-OS Network Troubleshooting & Fix Script v1.0
# Addresses Ethernet disconnection issues with Starlink and general network problems
# Designed for Windows systems via Git Bash, WSL, or PowerShell
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log file
LOG_FILE="/tmp/sagco-network-fix-$(date +%Y%m%d_%H%M%S).log"

# Detect platform
detect_platform() {
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || command -v ipconfig.exe &> /dev/null; then
        echo "windows"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

PLATFORM=$(detect_platform)

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

check_admin() {
    if [[ "$PLATFORM" == "windows" ]]; then
        # Check for Windows admin rights
        net session &>/dev/null
        if [ $? -ne 0 ]; then
            error "This script requires administrator privileges on Windows."
            error "Please run Git Bash or PowerShell as Administrator."
            exit 1
        fi
    elif [[ "$PLATFORM" == "linux" ]] || [[ "$PLATFORM" == "macos" ]]; then
        if [[ "$EUID" -ne 0 ]]; then
            error "This script must be run as root (use sudo)."
            exit 1
        fi
    else
        warn "Could not detect platform. Some features may not work."
    fi
}

diagnose_network() {
    header "NETWORK DIAGNOSTICS"
    
    log "Checking network adapters..."
    if command -v ipconfig &> /dev/null; then
        ipconfig /all | tee -a "$LOG_FILE"
    elif command -v ip &> /dev/null; then
        ip addr show | tee -a "$LOG_FILE"
    fi
    
    log "Checking routing table..."
    if command -v route &> /dev/null; then
        route print | tee -a "$LOG_FILE" 2>&1 || netstat -rn | tee -a "$LOG_FILE"
    fi
    
    log "Testing connectivity..."
    ping -c 4 8.8.8.8 2>&1 | tee -a "$LOG_FILE" || warn "Cannot reach Google DNS"
    ping -c 4 1.1.1.1 2>&1 | tee -a "$LOG_FILE" || warn "Cannot reach Cloudflare DNS"
    
    log "DNS resolution test..."
    nslookup google.com 2>&1 | tee -a "$LOG_FILE" || warn "DNS resolution issues detected"
}

fix_ethernet_starlink() {
    header "STARLINK ETHERNET FIX"
    
    log "Applying Starlink-specific fixes..."
    
    # Note: These commands are for Windows systems
    if command -v netsh &> /dev/null; then
        log "Disabling power management on Ethernet adapters..."
        warn "Manual step required: Disable 'Allow computer to turn off device' in Device Manager"
        warn "Path: Device Manager > Network adapters > Intel Ethernet > Properties > Power Management"
        
        log "Disabling Energy Efficient Ethernet..."
        warn "Manual step required: Disable 'Energy Efficient Ethernet' in adapter advanced settings"
        warn "Path: Device Manager > Network adapters > Intel Ethernet > Properties > Advanced"
    fi
}

reset_network_stack() {
    header "NETWORK STACK RESET"
    
    if command -v netsh &> /dev/null; then
        log "Resetting Windows network stack..."
        
        log "Step 1: Reset IP configuration..."
        netsh int ip reset 2>&1 | tee -a "$LOG_FILE"
        
        log "Step 2: Reset Winsock catalog..."
        netsh winsock reset 2>&1 | tee -a "$LOG_FILE"
        
        log "Step 3: Releasing IP address..."
        ipconfig /release 2>&1 | tee -a "$LOG_FILE"
        
        log "Step 4: Renewing IP address..."
        ipconfig /renew 2>&1 | tee -a "$LOG_FILE"
        
        log "Step 5: Flushing DNS cache..."
        ipconfig /flushdns 2>&1 | tee -a "$LOG_FILE"
        
        log "Step 6: Resetting firewall (optional)..."
        read -p "Reset Windows Firewall? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            netsh advfirewall reset 2>&1 | tee -a "$LOG_FILE"
        fi
        
    elif command -v systemctl &> /dev/null; then
        log "Restarting NetworkManager (Linux)..."
        systemctl restart NetworkManager 2>&1 | tee -a "$LOG_FILE"
    fi
}

disable_ipv6() {
    header "IPv6 CONFIGURATION"
    
    read -p "Disable IPv6 to troubleshoot connectivity? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v netsh &> /dev/null; then
            log "Disabling IPv6 on all adapters..."
            netsh interface ipv6 set global randomizeidentifiers=disabled 2>&1 | tee -a "$LOG_FILE"
            warn "To fully disable IPv6, uncheck it in adapter properties:"
            warn "Control Panel > Network Connections > Adapter Properties > IPv6"
        else
            log "Disabling IPv6 on Linux..."
            sysctl -w net.ipv6.conf.all.disable_ipv6=1 2>&1 | tee -a "$LOG_FILE"
            sysctl -w net.ipv6.conf.default.disable_ipv6=1 2>&1 | tee -a "$LOG_FILE"
        fi
    fi
}

check_drivers() {
    header "DRIVER INFORMATION"
    
    log "Checking network adapter drivers..."
    warn "Recommended: Update Intel I219-V driver from Intel's website"
    warn "URL: https://www.intel.com/content/www/us/en/download/15084/intel-network-adapter-driver-for-windows-11.html"
    
    if command -v driverquery &> /dev/null; then
        driverquery | grep -i "network\|ethernet" | tee -a "$LOG_FILE"
    fi
}

hardware_recommendations() {
    header "HARDWARE RECOMMENDATIONS"
    
    log "Starlink-specific recommendations:"
    echo "1. Try adding an unmanaged Gigabit switch between Starlink and PC"
    echo "2. Test with a different Ethernet cable (Cat6 or higher)"
    echo "3. Check Starlink app for obstructions and firmware updates"
    echo "4. Ensure Starlink dish has clear sky view"
    echo "5. Reboot Starlink router via app or unplug for 30 seconds"
    echo ""
    log "General troubleshooting:"
    echo "1. Disable unused network adapters (Tailscale, VirtualBox, Wi-Fi)"
    echo "2. Check for Windows updates"
    echo "3. Test with USB Ethernet adapter as workaround"
    echo "4. Monitor GPU usage (high load may correlate with drops)"
}

generate_report() {
    header "GENERATING DIAGNOSTIC REPORT"
    
    REPORT_FILE="/tmp/sagco-network-report-$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "SAGCO-OS Network Diagnostic Report"
        echo "Generated: $(date)"
        echo "======================================"
        echo ""
        echo "System Information:"
        if command -v uname &> /dev/null; then
            uname -a
        elif command -v systeminfo &> /dev/null; then
            systeminfo | head -10
        fi
        echo ""
        echo "Network Adapters:"
        if command -v ipconfig &> /dev/null; then
            ipconfig
        elif command -v ip &> /dev/null; then
            ip addr
        fi
        echo ""
        echo "Active Connections:"
        if command -v ss &> /dev/null; then
            ss -tuln
        elif command -v netstat &> /dev/null; then
            netstat -an
        fi
        echo ""
        echo "DNS Configuration:"
        if command -v ipconfig &> /dev/null; then
            ipconfig /all | grep -i "dns\|dhcp"
        elif command -v nmcli &> /dev/null; then
            nmcli device show | grep -i "dns\|dhcp"
        elif [ -f /etc/resolv.conf ]; then
            cat /etc/resolv.conf
        fi
        echo ""
    } > "$REPORT_FILE"
    
    log "Diagnostic report saved to: $REPORT_FILE"
}

main_menu() {
    header "SAGCO-OS NETWORK FIX UTILITY"
    
    echo "Select an option:"
    echo "1) Full diagnostic scan"
    echo "2) Reset network stack (fix-all)"
    echo "3) Starlink Ethernet troubleshooting"
    echo "4) Disable IPv6"
    echo "5) Check driver information"
    echo "6) Hardware recommendations"
    echo "7) Generate diagnostic report"
    echo "8) Run all fixes (full reset)"
    echo "9) Exit"
    echo ""
    read -p "Enter choice [1-9]: " choice
    
    case $choice in
        1) diagnose_network ;;
        2) reset_network_stack ;;
        3) fix_ethernet_starlink ;;
        4) disable_ipv6 ;;
        5) check_drivers ;;
        6) hardware_recommendations ;;
        7) generate_report ;;
        8) 
            diagnose_network
            reset_network_stack
            disable_ipv6
            fix_ethernet_starlink
            hardware_recommendations
            generate_report
            ;;
        9) 
            log "Exiting..."
            exit 0
            ;;
        *)
            error "Invalid option. Please try again."
            main_menu
            ;;
    esac
    
    echo ""
    read -p "Return to main menu? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        main_menu
    fi
}

# Main execution
log "SAGCO-OS Network Fix Script Started"
log "Log file: $LOG_FILE"

# Check for admin rights (skip in sandbox/test environments)
if [[ "${SKIP_ADMIN_CHECK:-}" != "true" ]]; then
    check_admin
fi

# Show main menu
main_menu

log "Script completed. Please restart your computer for changes to take effect."
echo -e "\n${GREEN}Log file saved to: $LOG_FILE${NC}"
