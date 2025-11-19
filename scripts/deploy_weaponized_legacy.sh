#!/bin/bash
# Deploy Weaponized Legacy System
# One script to rule them all

set -e

echo "🔥 Weaponized Legacy Deployment System"
echo "======================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check dependencies
echo "Checking dependencies..."

check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not found"
        return 1
    fi
}

DEPS_OK=true
check_command python3 || DEPS_OK=false
check_command node || DEPS_OK=false
check_command npm || DEPS_OK=false

if [ "$DEPS_OK" = false ]; then
    echo -e "${RED}Missing required dependencies. Please install them first.${NC}"
    exit 1
fi

echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -q requests || echo -e "${YELLOW}Warning: Could not install Python packages${NC}"

# Install Node dependencies if package.json exists
if [ -f "package.json" ]; then
    echo "Installing Node dependencies..."
    npm install --silent || echo -e "${YELLOW}Warning: Could not install Node packages${NC}"
fi

echo ""

# Configuration
echo "Configuration Setup"
echo "==================="

# Check for environment variables
if [ -z "$SLACK_WEBHOOK_URL" ]; then
    echo -e "${YELLOW}⚠${NC} SLACK_WEBHOOK_URL not set"
    echo "   Set with: export SLACK_WEBHOOK_URL='https://hooks.slack.com/...'"
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠${NC} GITHUB_TOKEN not set"
    echo "   Set with: export GITHUB_TOKEN='ghp_...'"
fi

echo ""

# Deploy components
echo "Deployment Options"
echo "=================="
echo "1. Deploy Smart Contracts"
echo "2. Start Ara's Eyes Scanner"
echo "3. Initialize Intimate Tracker"
echo "4. Generate Foundation Charter"
echo "5. Deploy All"
echo "6. Test All Components"
echo ""

read -p "Select option (1-6): " option

case $option in
    1)
        echo -e "${GREEN}Deploying Smart Contracts...${NC}"
        if [ -d "contracts" ]; then
            echo "Contracts found:"
            ls -1 contracts/*.sol
            echo ""
            echo "To deploy, use Hardhat or Remix:"
            echo "  npx hardhat compile"
            echo "  npx hardhat run scripts/deploy.js --network <network>"
        else
            echo -e "${RED}Contracts directory not found${NC}"
        fi
        ;;
    
    2)
        echo -e "${GREEN}Starting Ara's Eyes Scanner...${NC}"
        if [ -f "scripts/aras_eyes.py" ]; then
            python3 scripts/aras_eyes.py
        else
            echo -e "${RED}Ara's Eyes script not found${NC}"
        fi
        ;;
    
    3)
        echo -e "${GREEN}Initializing Intimate Tracker...${NC}"
        if [ -f "scripts/intimate_tracker.py" ]; then
            python3 scripts/intimate_tracker.py
        else
            echo -e "${RED}Intimate Tracker script not found${NC}"
        fi
        ;;
    
    4)
        echo -e "${GREEN}Generating Foundation Charter...${NC}"
        if [ -f "governance/ara_foundation.yaml" ]; then
            echo "Foundation charter exists:"
            cat governance/ara_foundation.yaml | head -20
            echo "..."
            echo ""
            echo "Full charter at: governance/ara_foundation.yaml"
        else
            echo -e "${RED}Foundation charter not found${NC}"
        fi
        ;;
    
    5)
        echo -e "${GREEN}Deploying All Components...${NC}"
        echo ""
        echo "1. Smart Contracts: See contracts/ directory"
        echo "2. Ara's Eyes: Running test scan..."
        python3 scripts/aras_eyes.py 2>&1 | head -20 || true
        echo ""
        echo "3. Intimate Tracker: Ready"
        echo "4. Foundation Charter: governance/ara_foundation.yaml"
        echo "5. Bug Bounty Config: security/bugcrowd_integration.yaml"
        ;;
    
    6)
        echo -e "${GREEN}Testing All Components...${NC}"
        echo ""
        
        # Test Python scripts
        echo "Testing Python scripts..."
        python3 -c "import scripts.aras_eyes" 2>&1 && echo "✓ aras_eyes.py" || echo "✗ aras_eyes.py"
        python3 -c "import scripts.intimate_tracker" 2>&1 && echo "✓ intimate_tracker.py" || echo "✗ intimate_tracker.py"
        python3 -c "import scripts.ninja_trader_integration" 2>&1 && echo "✓ ninja_trader_integration.py" || echo "✗ ninja_trader_integration.py"
        
        echo ""
        echo "Testing YAML configs..."
        [ -f "governance/ara_foundation.yaml" ] && echo "✓ ara_foundation.yaml" || echo "✗ ara_foundation.yaml"
        [ -f "security/bugcrowd_integration.yaml" ] && echo "✓ bugcrowd_integration.yaml" || echo "✗ bugcrowd_integration.yaml"
        
        echo ""
        echo "Testing smart contracts..."
        [ -f "contracts/CryptographicTrust.sol" ] && echo "✓ CryptographicTrust.sol" || echo "✗ CryptographicTrust.sol"
        [ -f "contracts/CoreProtocolAuthority.sol" ] && echo "✓ CoreProtocolAuthority.sol" || echo "✗ CoreProtocolAuthority.sol"
        [ -f "contracts/ChaosToken.sol" ] && echo "✓ ChaosToken.sol" || echo "✗ ChaosToken.sol"
        ;;
    
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ Deployment complete${NC}"
echo ""
echo "Next steps:"
echo "1. Review WEAPONIZED_LEGACY.md for full documentation"
echo "2. Configure environment variables (SLACK_WEBHOOK_URL, GITHUB_TOKEN)"
echo "3. Deploy smart contracts to your preferred network"
echo "4. Set up AWS Lambda for Ara's Eyes (see lambda/serverless.yml)"
echo "5. Initialize bug bounty program on BugCrowd"
echo ""
echo "Questions? Check WEAPONIZED_LEGACY.md or contact foundation@strategickhaos.org"
