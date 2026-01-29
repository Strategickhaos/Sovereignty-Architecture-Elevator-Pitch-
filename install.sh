#!/bin/sh
# ============================================================
# KHAOS SOVEREIGN OS - Universal Installer/Updater
# ============================================================
# 
# Usage (install/update):
#   curl -sL https://raw.githubusercontent.com/Strategickhaos/trig6/main/install.sh | sh
#
# Or shorter (once DNS is set up):
#   curl -sL khaos.run | sh
#
# Works on: Linux, macOS, Termux (Android), iSH (iOS), WSL, Git Bash
#
# Owner: Strategickhaos DAO LLC
# Author: Domenic G. Garza
# ============================================================

set -e

# Colors (if terminal supports it)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Banner
banner() {
    echo ""
    echo "${PURPLE}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo "${PURPLE}║${NC}  ${RED}🔥${NC} ${YELLOW}KHAOS SOVEREIGN OS${NC}                                    ${PURPLE}║${NC}"
    echo "${PURPLE}║${NC}     ${BLUE}TRIG6 Physics Compiler + KHAOS Symbolic System${NC}        ${PURPLE}║${NC}"
    echo "${PURPLE}║${NC}     ${GREEN}Strategickhaos DAO LLC${NC}                                ${PURPLE}║${NC}"
    echo "${PURPLE}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Detect OS/Environment
detect_os() {
    OS="unknown"
    INSTALL_DIR="$HOME/.khaos"
    BIN_DIR="$HOME/.local/bin"
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    elif [ "$(uname)" = "Darwin" ]; then
        OS="macos"
    elif [ -d /data/data/com.termux ]; then
        OS="termux"
        INSTALL_DIR="$HOME/.khaos"
        BIN_DIR="$PREFIX/bin"
    elif [ -f /etc/alpine-release ]; then
        OS="alpine"  # iSH uses Alpine
    elif grep -q Microsoft /proc/version 2>/dev/null; then
        OS="wsl"
    fi
    
    echo "${BLUE}Detected OS:${NC} $OS"
}

# Check for Python
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON="python3"
        echo "${GREEN}✓${NC} Python3 found: $(python3 --version)"
    elif command -v python >/dev/null 2>&1; then
        PYTHON="python"
        echo "${GREEN}✓${NC} Python found: $(python --version)"
    else
        echo "${RED}✗${NC} Python not found!"
        echo ""
        echo "Install Python first:"
        case $OS in
            termux) echo "  pkg install python" ;;
            alpine) echo "  apk add python3" ;;
            ubuntu|debian) echo "  sudo apt install python3" ;;
            fedora) echo "  sudo dnf install python3" ;;
            macos) echo "  brew install python3" ;;
            *) echo "  Install Python 3.x for your system" ;;
        esac
        exit 1
    fi
}

# Check for Git (optional but recommended)
check_git() {
    if command -v git >/dev/null 2>&1; then
        GIT_AVAILABLE=1
        echo "${GREEN}✓${NC} Git found"
    else
        GIT_AVAILABLE=0
        echo "${YELLOW}!${NC} Git not found (will use curl/wget instead)"
    fi
}

# Create directories
setup_dirs() {
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    echo "${GREEN}✓${NC} Created $INSTALL_DIR"
}

# Download TRIG6
download_trig6() {
    echo ""
    echo "${BLUE}Downloading TRIG6...${NC}"
    
    REPO_URL="https://github.com/Strategickhaos/trig6"
    RAW_URL="https://raw.githubusercontent.com/Strategickhaos/trig6/main"
    
    if [ "$GIT_AVAILABLE" = "1" ]; then
        # Git clone/pull
        if [ -d "$INSTALL_DIR/trig6/.git" ]; then
            echo "Updating existing installation..."
            cd "$INSTALL_DIR/trig6"
            git pull --quiet
        else
            echo "Cloning repository..."
            rm -rf "$INSTALL_DIR/trig6"
            git clone --quiet "$REPO_URL.git" "$INSTALL_DIR/trig6"
        fi
    else
        # Fallback: download individual files
        echo "Downloading core files..."
        mkdir -p "$INSTALL_DIR/trig6/core"
        mkdir -p "$INSTALL_DIR/trig6/domains/rope"
        mkdir -p "$INSTALL_DIR/trig6/domains/pipe"
        mkdir -p "$INSTALL_DIR/trig6/domains/rigging"
        mkdir -p "$INSTALL_DIR/trig6/domains/khaos"
        mkdir -p "$INSTALL_DIR/trig6/packs"
        mkdir -p "$INSTALL_DIR/trig6/games"
        
        # Use curl or wget
        if command -v curl >/dev/null 2>&1; then
            DL="curl -sL"
        else
            DL="wget -qO-"
        fi
        
        $DL "$RAW_URL/trig6.py" > "$INSTALL_DIR/trig6/trig6.py"
        $DL "$RAW_URL/core/units.py" > "$INSTALL_DIR/trig6/core/units.py"
        $DL "$RAW_URL/core/doctor.py" > "$INSTALL_DIR/trig6/core/doctor.py"
        $DL "$RAW_URL/core/citations.py" > "$INSTALL_DIR/trig6/core/citations.py"
        $DL "$RAW_URL/core/model_registry.py" > "$INSTALL_DIR/trig6/core/model_registry.py"
        $DL "$RAW_URL/domains/rope/constants.json" > "$INSTALL_DIR/trig6/domains/rope/constants.json"
        $DL "$RAW_URL/domains/pipe/constants.json" > "$INSTALL_DIR/trig6/domains/pipe/constants.json"
        $DL "$RAW_URL/domains/rigging/constants.json" > "$INSTALL_DIR/trig6/domains/rigging/constants.json"
        $DL "$RAW_URL/domains/khaos/constants.json" > "$INSTALL_DIR/trig6/domains/khaos/constants.json"
        $DL "$RAW_URL/packs/default_pack.json" > "$INSTALL_DIR/trig6/packs/default_pack.json"
        $DL "$RAW_URL/games/chess_debate.py" > "$INSTALL_DIR/trig6/games/chess_debate.py"
    fi
    
    echo "${GREEN}✓${NC} TRIG6 downloaded to $INSTALL_DIR/trig6"
}

# Create CLI wrapper
create_cli() {
    echo ""
    echo "${BLUE}Creating CLI commands...${NC}"
    
    # trig6 command
    cat > "$BIN_DIR/trig6" << 'WRAPPER'
#!/bin/sh
exec python3 "$HOME/.khaos/trig6/trig6.py" "$@"
WRAPPER
    chmod +x "$BIN_DIR/trig6"
    echo "${GREEN}✓${NC} Created: trig6"
    
    # khaos command (alias/superset)
    cat > "$BIN_DIR/khaos" << 'WRAPPER'
#!/bin/sh
KHAOS_HOME="$HOME/.khaos/trig6"

case "$1" in
    update)
        echo "Updating KHAOS..."
        curl -sL https://raw.githubusercontent.com/Strategickhaos/trig6/main/install.sh | sh
        ;;
    doctor)
        exec python3 "$KHAOS_HOME/trig6.py" doctor "$@"
        ;;
    debate)
        shift
        exec python3 "$KHAOS_HOME/games/chess_debate.py" "$@"
        ;;
    version)
        echo "KHAOS Sovereign OS"
        echo "TRIG6 Physics Compiler v1.0.0"
        echo "Owner: Strategickhaos DAO LLC"
        python3 "$KHAOS_HOME/trig6.py" doctor 2>/dev/null | grep -q "PASS" && echo "Status: OPERATIONAL" || echo "Status: CHECK FAILED"
        ;;
    help|--help|-h)
        echo "KHAOS Sovereign OS"
        echo ""
        echo "Commands:"
        echo "  khaos update     - Update to latest version"
        echo "  khaos doctor     - Run self-tests"
        echo "  khaos version    - Show version info"
        echo "  khaos debate     - Launch Chess Debate engine"
        echo ""
        echo "TRIG6 Physics Commands:"
        echo "  trig6 vector --theta 45"
        echo "  trig6 bridle --load 300 --theta 120"
        echo "  trig6 highline --load 200 --sag 10"
        echo "  trig6 impact --weight 200 --ff 1"
        echo "  trig6 cite rope.knot.figure_8_on_bight"
        echo "  trig6 list --prefix rope"
        echo ""
        echo "More: https://github.com/Strategickhaos/trig6"
        ;;
    *)
        exec python3 "$KHAOS_HOME/trig6.py" "$@"
        ;;
esac
WRAPPER
    chmod +x "$BIN_DIR/khaos"
    echo "${GREEN}✓${NC} Created: khaos"
}

# Update PATH if needed
update_path() {
    echo ""
    
    # Check if BIN_DIR is in PATH
    case ":$PATH:" in
        *":$BIN_DIR:"*) 
            echo "${GREEN}✓${NC} $BIN_DIR already in PATH"
            ;;
        *)
            echo "${YELLOW}!${NC} Add this to your shell config (.bashrc, .zshrc, etc.):"
            echo ""
            echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            
            # Try to add automatically
            for RC in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
                if [ -f "$RC" ]; then
                    if ! grep -q ".local/bin" "$RC" 2>/dev/null; then
                        echo "" >> "$RC"
                        echo "# KHAOS Sovereign OS" >> "$RC"
                        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$RC"
                        echo "${GREEN}✓${NC} Added to $RC"
                    fi
                fi
            done
            ;;
    esac
}

# Run doctor
verify_install() {
    echo ""
    echo "${BLUE}Verifying installation...${NC}"
    
    # Source the updated PATH
    export PATH="$BIN_DIR:$PATH"
    
    if "$BIN_DIR/trig6" doctor 2>/dev/null | grep -q "PASS"; then
        echo "${GREEN}✓${NC} Doctor: ALL TESTS PASSED"
    else
        echo "${YELLOW}!${NC} Doctor: Some tests may have issues"
        "$BIN_DIR/trig6" doctor
    fi
}

# Final message
finish() {
    echo ""
    echo "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo "${GREEN}  KHAOS Sovereign OS installed successfully!${NC}"
    echo "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  ${YELLOW}Start a new terminal${NC} or run: ${BLUE}source ~/.bashrc${NC}"
    echo ""
    echo "  Quick commands:"
    echo "    ${PURPLE}khaos version${NC}     - Check status"
    echo "    ${PURPLE}khaos update${NC}      - Update to latest"
    echo "    ${PURPLE}khaos doctor${NC}      - Run self-tests"
    echo "    ${PURPLE}khaos debate${NC}      - Start Chess Debate"
    echo "    ${PURPLE}trig6 --help${NC}      - Physics commands"
    echo ""
    echo "  ${BLUE}Strategickhaos DAO LLC${NC} | ${RED}🔥${NC} It boots or it doesn't."
    echo ""
}

# Main
main() {
    banner
    detect_os
    check_python
    check_git
    setup_dirs
    download_trig6
    create_cli
    update_path
    verify_install
    finish
}

main "$@"
