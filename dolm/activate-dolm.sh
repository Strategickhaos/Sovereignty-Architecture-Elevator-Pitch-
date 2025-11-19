#!/bin/bash
###############################################################################
# Department of Living Memory (DoLM) - Activation Script
# "Nothing is ever lost. Every error is a lesson. Every TODO is a prophecy."
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
VAULT_PATH="${DOLM_VAULT_PATH:-$HOME/strategic-khaos-private/dolm-vault}"
WATCH_PATH="${DOLM_WATCH_PATH:-$(pwd)}"
CONTAINER_NAME="dolm-daemon"
IMAGE_NAME="ghcr.io/strategickhaos/dolm-daemon:latest"
LOCAL_IMAGE_NAME="dolm-daemon:local"

echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   DEPARTMENT OF LIVING MEMORY (DoLM)                          ║
║                                                               ║
║   "Nothing is ever lost. Every error is a lesson.             ║
║    Every TODO is a prophecy."                                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Error: Docker daemon is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

echo -e "${CYAN}[1/5] Initializing DoLM vault...${NC}"
mkdir -p "$VAULT_PATH"
echo -e "${GREEN}✓ Vault directory created: $VAULT_PATH${NC}"

echo -e "${CYAN}[2/5] Building DoLM daemon container...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/Dockerfile" ]; then
    docker build -t "$LOCAL_IMAGE_NAME" "$SCRIPT_DIR"
    IMAGE_TO_USE="$LOCAL_IMAGE_NAME"
    echo -e "${GREEN}✓ Built local DoLM image${NC}"
else
    echo -e "${YELLOW}! Dockerfile not found, will try to pull from registry${NC}"
    IMAGE_TO_USE="$IMAGE_NAME"
fi

echo -e "${CYAN}[3/5] Stopping existing DoLM daemon (if any)...${NC}"
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    echo -e "${GREEN}✓ Cleaned up existing container${NC}"
else
    echo -e "${YELLOW}! No existing container found${NC}"
fi

echo -e "${CYAN}[4/5] Starting DoLM daemon...${NC}"
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -v "$WATCH_PATH:/swarm:ro" \
    -v "$VAULT_PATH:/vault" \
    -e DOLM_WATCH_PATH=/swarm \
    -e DOLM_VAULT_PATH=/vault \
    "$IMAGE_TO_USE"

echo -e "${GREEN}✓ DoLM daemon started${NC}"

echo -e "${CYAN}[5/5] Verifying installation...${NC}"
sleep 2

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${GREEN}✓ DoLM daemon is running${NC}"
    
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Department of Living Memory is now ONLINE${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}Vault location:${NC} $VAULT_PATH"
    echo -e "${CYAN}Watching:${NC} $WATCH_PATH"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Open the vault in Obsidian: File → Open vault → $VAULT_PATH"
    echo "  2. Watch as DoLM discovers TODOs and errors in your code"
    echo "  3. Explore the GraphView to see connections"
    echo ""
    echo -e "${CYAN}Useful commands:${NC}"
    echo "  • View logs:    docker logs -f $CONTAINER_NAME"
    echo "  • Stop daemon:  docker stop $CONTAINER_NAME"
    echo "  • Restart:      docker restart $CONTAINER_NAME"
    echo ""
    echo -e "${PURPLE}Every error, every TODO, every breath you take in the terminal${NC}"
    echo -e "${PURPLE}is now eternal, beautiful, and linked in Obsidian GraphView.${NC}"
    echo ""
    echo -e "${GREEN}The department is live. The vault is breathing.${NC}"
    echo -e "${GREEN}Your legacy is now unkillable.${NC}"
    echo ""
else
    echo -e "${RED}✗ DoLM daemon failed to start${NC}"
    echo "Check logs with: docker logs $CONTAINER_NAME"
    exit 1
fi
