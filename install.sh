#!/bin/bash
#
# SAGCO Boot Identity Pipeline (SBIP) v1.0 - Installation Script
# 
# Entity: Strategickhaos DAO LLC
# EIN: 39-2923503
# Wyoming: 2025-001708194
#
# Usage: sudo ./install.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PREFIX="/usr/local"
SAGCO_ROOT="/opt/sagco"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${PURPLE}========================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}========================================${NC}"
}

# Check for root privileges
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root (use sudo)"
        exit 1
    fi
    log_info "Running with root privileges ✓"
}

# Check dependencies
check_dependencies() {
    log_section "Checking Dependencies"
    
    local missing_deps=()
    
    # Check for build tools
    if ! command -v make &> /dev/null; then
        missing_deps+=("build-essential")
    fi
    
    # Check for kernel headers
    if [ ! -d "/lib/modules/$(uname -r)/build" ]; then
        missing_deps+=("linux-headers-$(uname -r)")
    fi
    
    # Check for Plymouth (optional)
    if ! command -v plymouth &> /dev/null; then
        log_warn "Plymouth not found (optional for boot splash)"
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Install with: apt install ${missing_deps[*]}"
        exit 1
    fi
    
    log_info "All required dependencies installed ✓"
}

# Build and install kernel module
install_kernel_module() {
    log_section "Installing SAGCO CPU Kernel Module"
    
    cd "$SCRIPT_DIR/kernel"
    
    log_info "Building kernel module..."
    make clean
    make
    
    log_info "Installing kernel module..."
    make install
    
    log_info "Loading kernel module..."
    if ! modprobe sagco_cpu_mod; then
        log_error "Failed to load kernel module"
        return 1
    fi
    
    # Verify module loaded
    if lsmod | grep -q sagco_cpu_mod; then
        log_info "Kernel module loaded successfully ✓"
        dmesg | tail -10 | grep SAGCO_CPU || true
    else
        log_error "Kernel module not loaded"
        return 1
    fi
    
    # Add to modules to load at boot
    echo "sagco_cpu_mod" > /etc/modules-load.d/sagco.conf
    log_info "Module configured to load at boot ✓"
    
    cd "$SCRIPT_DIR"
}

# Install systemd services
install_systemd_services() {
    log_section "Installing systemd Services"
    
    # Install service binaries
    log_info "Installing service binaries..."
    install -m 755 "$SCRIPT_DIR/scripts/bin/sagco-banner" "$INSTALL_PREFIX/bin/"
    install -m 755 "$SCRIPT_DIR/scripts/bin/sagco-runtime" "$INSTALL_PREFIX/bin/"
    install -m 755 "$SCRIPT_DIR/scripts/bin/sagco-compiler" "$INSTALL_PREFIX/bin/"
    install -m 755 "$SCRIPT_DIR/scripts/bin/sagco-cpu-init" "$INSTALL_PREFIX/bin/"
    
    # Install systemd unit files
    log_info "Installing systemd unit files..."
    cp "$SCRIPT_DIR/systemd/"*.service /etc/systemd/system/
    cp "$SCRIPT_DIR/systemd/"*.target /etc/systemd/system/
    
    # Reload systemd
    systemctl daemon-reload
    
    # Enable services
    log_info "Enabling SAGCO services..."
    systemctl enable sagco-banner.service
    systemctl enable sagco-cpu.service
    systemctl enable sagco-runtime.service
    systemctl enable sagco-compiler.service
    systemctl enable sagco.target
    
    log_info "systemd services installed and enabled ✓"
}

# Install GRUB theme
install_grub_theme() {
    log_section "Installing GRUB Theme"
    
    # Create theme directory
    mkdir -p /boot/grub/themes/sagco
    
    # Copy theme files
    cp "$SCRIPT_DIR/boot/grub-theme/"* /boot/grub/themes/sagco/
    
    log_info "GRUB theme files copied ✓"
    log_warn "MANUAL STEP REQUIRED:"
    log_warn "  1. Edit /etc/default/grub"
    log_warn "  2. Add: GRUB_THEME=\"/boot/grub/themes/sagco/theme.txt\""
    log_warn "  3. Add: GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash sagco=1\""
    log_warn "  4. Run: update-grub"
    log_warn "  See: boot/grub-theme/grub.cfg.template for reference"
}

# Install Plymouth theme
install_plymouth_theme() {
    log_section "Installing Plymouth Theme (Optional)"
    
    if ! command -v plymouth &> /dev/null; then
        log_warn "Plymouth not installed, skipping theme installation"
        return 0
    fi
    
    # Create theme directory
    mkdir -p /usr/share/plymouth/themes/sagco
    
    # Copy theme files
    cp "$SCRIPT_DIR/plymouth/"* /usr/share/plymouth/themes/sagco/
    
    log_info "Plymouth theme files copied ✓"
    log_warn "To activate Plymouth theme:"
    log_warn "  1. Run: plymouth-set-default-theme sagco"
    log_warn "  2. Run: update-initramfs -u"
}

# Install initramfs scripts
install_initramfs_scripts() {
    log_section "Installing initramfs Scripts"
    
    # Create SAGCO scripts directory
    mkdir -p /usr/local/share/sagco/scripts
    
    # Install verification script
    install -m 755 "$SCRIPT_DIR/scripts/initramfs/sagco-verify" \
                   /usr/local/share/sagco/scripts/
    
    # Install initramfs hook
    install -m 755 "$SCRIPT_DIR/scripts/initramfs/sagco-hook" \
                   /etc/initramfs-tools/hooks/sagco
    
    log_info "initramfs scripts installed ✓"
    log_info "Updating initramfs..."
    update-initramfs -u
    
    log_info "initramfs updated with SAGCO scripts ✓"
}

# Create SAGCO runtime directories
setup_runtime() {
    log_section "Setting up SAGCO Runtime"
    
    mkdir -p "$SAGCO_ROOT"/{bin,lib,share,etc,var}
    mkdir -p "$SAGCO_ROOT/var"/{log,run,cache}
    
    chmod 755 "$SAGCO_ROOT"
    
    log_info "SAGCO runtime directories created at $SAGCO_ROOT ✓"
}

# Display completion message
show_completion() {
    log_section "Installation Complete!"
    
    cat << 'EOF'

████████╗ ███████╗  ██████╗   ██████╗  ██████╗ 
██╔════██║██╔═══██║██╔════╝  ██╔════╝ ██╔═══██╗
████████║ ███████║ ██║  ███╗██║      ██║   ██║
╚════██║ ██╔═══██║██║   ██║██║      ██║   ██║
████████║██║   ██║╚██████╔╝╚██████╗╚██████╔╝
╚═══════╝╚═╝   ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ 

SAGCO Boot Identity Pipeline v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entity:     Strategickhaos DAO LLC
EIN:        39-2923503
Wyoming:    2025-001708194

Installation Status: SUCCESS ✓

EOF
    
    log_info "Installation summary:"
    log_info "  ✓ Kernel module installed and loaded"
    log_info "  ✓ systemd services installed and enabled"
    log_info "  ✓ initramfs scripts installed"
    log_info "  ✓ GRUB theme files installed"
    log_info "  ✓ Runtime directories created"
    
    echo ""
    log_warn "Manual steps required:"
    log_warn "  1. Update /etc/default/grub (see boot/grub-theme/grub.cfg.template)"
    log_warn "  2. Run: update-grub"
    log_warn "  3. Reboot to see SAGCO boot identity"
    
    echo ""
    log_info "Verification commands:"
    log_info "  lsmod | grep sagco_cpu_mod          # Check kernel module"
    log_info "  systemctl status sagco.target       # Check services"
    log_info "  cat /dev/sagco_cpu                  # Read CPU state"
    log_info "  dmesg | grep SAGCO                  # View kernel messages"
    
    echo ""
    echo -e "${PURPLE}🔥💜 STRATEGICKHAOS DAO LLC 💜🔥${NC}"
    echo -e "${PURPLE}Ratio Ex Nihilo - From Nothing, Through Reason, Everything${NC}"
    echo ""
}

# Main installation flow
main() {
    log_section "SAGCO Boot Identity Pipeline (SBIP) v1.0 Installation"
    log_info "Entity: Strategickhaos DAO LLC"
    log_info "EIN: 39-2923503 | Wyoming: 2025-001708194"
    
    check_root
    check_dependencies
    
    install_kernel_module || {
        log_error "Kernel module installation failed"
        exit 1
    }
    
    install_systemd_services
    install_grub_theme
    install_plymouth_theme
    install_initramfs_scripts
    setup_runtime
    
    show_completion
}

# Run installation
main "$@"
