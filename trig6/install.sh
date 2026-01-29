#!/usr/bin/env bash
# TRIG6 Installer
# MIT License - Copyright (c) 2025 Strategickhaos

set -e

# Detect Python interpreter
detect_python() {
    if command -v python3 &>/dev/null; then
        echo "python3"
    elif command -v python &>/dev/null; then
        echo "python"
    else
        echo "ERROR: No Python interpreter found" >&2
        exit 1
    fi
}

# Install TRIG6 to user directory
install_trig6() {
    PYTHON=$(detect_python)
    echo "Using Python interpreter: $PYTHON"
    
    # Create installation directory
    INSTALL_DIR="$HOME/.khaos/trig6"
    mkdir -p "$INSTALL_DIR"
    
    # Copy files
    echo "Installing TRIG6 to $INSTALL_DIR..."
    cp -r trig6.py proof.py core/ domains/ packs/ games/ sagco/ "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/trig6.py" "$INSTALL_DIR/proof.py"
    
    # Create wrapper script with detected interpreter
    cat > "$INSTALL_DIR/trig6" <<EOF
#!/usr/bin/env bash
# TRIG6 Wrapper - Auto-generated
exec "\${PYTHON:-$PYTHON}" "\$HOME/.khaos/trig6/trig6.py" "\$@"
EOF
    chmod +x "$INSTALL_DIR/trig6"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.khaos/trig6:"* ]]; then
        echo ""
        echo "Add to your PATH by adding this line to your ~/.bashrc or ~/.zshrc:"
        echo "  export PATH=\"\$HOME/.khaos/trig6:\$PATH\""
    fi
    
    echo ""
    echo "Installation complete!"
    echo "Run: $INSTALL_DIR/trig6 doctor"
}

# Main
if [ "$1" = "install" ]; then
    install_trig6
else
    echo "TRIG6 Installer"
    echo "Usage: $0 install"
fi
