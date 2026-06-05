#!/bin/bash
# TRIG6 Installer Script
# Installs TRIG6 Sovereign Compute Engine

set -e

echo "=========================================="
echo "TRIG6 Installer"
echo "Sovereign Compute Engine"
echo "=========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "Detected OS: $OS"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python 3 found: $PYTHON_VERSION"
echo ""

# Installation directory
INSTALL_DIR="${HOME}/.local/trig6"
BIN_DIR="${HOME}/.local/bin"

echo "Installation directory: $INSTALL_DIR"
echo "Binary directory: $BIN_DIR"
echo ""

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Download or copy TRIG6
echo "Installing TRIG6..."

# Check if we're running from source
if [ -f "trig6.py" ]; then
    echo "Installing from local source..."
    cp -r ./* "$INSTALL_DIR/"
else
    echo "Downloading TRIG6..."
    # In production, this would download from GitHub
    curl -fsSL -o /tmp/trig6.tar.gz https://github.com/Strategickhaos/trig6/archive/main.tar.gz
    tar -xzf /tmp/trig6.tar.gz -C "$INSTALL_DIR" --strip-components=1
    rm /tmp/trig6.tar.gz
fi

# Make executable
chmod +x "$INSTALL_DIR/trig6.py"

# Create wrapper script
cat > "$BIN_DIR/trig6" << 'EOF'
#!/bin/bash
python3 "${HOME}/.local/trig6/trig6.py" "$@"
EOF

chmod +x "$BIN_DIR/trig6"

# Create khaos alias for debate engine
cat > "$BIN_DIR/khaos" << 'EOF'
#!/bin/bash
if [ "$1" == "debate" ]; then
    python3 -c "
import sys
sys.path.insert(0, '${HOME}/.local/trig6')
from games.chess_debate import ChessDebate, list_fallacies

debate = ChessDebate()
print('Chess Debate Engine')
print('=' * 70)
print('Commands:')
print('  start <topic> | <position> - Start new debate')
print('  claim <text>               - Make a claim')
print('  evidence <text>            - Present evidence')
print('  logic <text>               - Make logical argument')
print('  status                     - Show debate status')
print('  fallacies                  - List all fallacies')
print('  quit                       - Exit')
print()

# Interactive loop
while True:
    try:
        cmd = input('> ').strip()
        if not cmd:
            continue
        
        if cmd == 'quit':
            break
        elif cmd == 'fallacies':
            print('\\nDetected fallacies:')
            for f in list_fallacies():
                print(f'  - {f.replace(\"_\", \" \")}')
        elif cmd.startswith('start '):
            parts = cmd[6:].split('|')
            if len(parts) == 2:
                topic = parts[0].strip()
                position = parts[1].strip()
                print(debate.start(topic, position))
            else:
                print('Usage: start <topic> | <position>')
        elif cmd.startswith('claim '):
            text = cmd[6:]
            print(debate.make_move('claim', text))
        elif cmd.startswith('evidence '):
            text = cmd[9:]
            print(debate.make_move('evidence', text))
        elif cmd.startswith('logic '):
            text = cmd[6:]
            print(debate.make_move('logic', text))
        elif cmd == 'status':
            print(debate.get_status())
        else:
            print('Unknown command. Type fallacies, start, claim, evidence, logic, status, or quit')
    except KeyboardInterrupt:
        print('\\n\\nExiting...')
        break
    except Exception as e:
        print(f'Error: {e}')
"
else
    python3 "${HOME}/.local/trig6/trig6.py" "$@"
fi
EOF

chmod +x "$BIN_DIR/khaos"

echo "✓ TRIG6 installed successfully!"
echo ""

# Add to PATH instructions
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️  Add $BIN_DIR to your PATH:"
    echo ""
    if [ "$OS" == "macos" ] || [ "$OS" == "linux" ]; then
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
    fi
    echo ""
fi

# Run doctor
echo "Running doctor validation..."
echo ""
"$BIN_DIR/trig6" doctor

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "Try these commands:"
echo "  trig6 doctor"
echo "  trig6 vector --theta 45"
echo "  trig6 bridle --load 300 --theta 30"
echo "  khaos debate"
echo ""
echo "For more info:"
echo "  trig6 --help"
echo "  trig6 list models"
echo ""
