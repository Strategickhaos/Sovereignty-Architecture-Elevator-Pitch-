#!/bin/bash
# Setup script for TRIG6 Omni Calculator environment

set -e  # Exit on error

echo "=================================================="
echo "TRIG6 Omni Calculator - Environment Setup"
echo "=================================================="
echo ""

# Set repository path
REPO=$(pwd)
export REPO

echo "Repository path: $REPO"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Please install Python 3."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "$REPO/venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv "$REPO/venv"
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source "$REPO/venv/bin/activate"
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
if [ -f "$REPO/requirements.txt" ]; then
    pip install -r "$REPO/requirements.txt"
    echo "✓ Dependencies installed"
else
    echo "Warning: requirements.txt not found"
fi

# Test installation
echo ""
echo "Testing TRIG6 installation..."
python3 -c "import numpy, scipy, matplotlib; print('✓ All dependencies imported successfully')"

echo ""
echo "=================================================="
echo "Setup complete!"
echo "=================================================="
echo ""
echo "To activate the environment in future sessions:"
echo "  source $REPO/venv/bin/activate"
echo ""
echo "To run the calculator:"
echo "  python cli.py --theta 'math.pi/4'"
echo ""
echo "To run benchmarks:"
echo "  python bench.py"
echo ""
echo "To run all phases:"
echo "  ./phases.sh"
echo ""
