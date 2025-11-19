#!/usr/bin/env bash
set -euo pipefail

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Strategickhaos Local Development Starter${NC}"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓${NC} Created .env file"
        echo -e "${YELLOW}⚠️  Please edit .env with your credentials before continuing${NC}"
        exit 1
    else
        echo -e "${RED}✗${NC} .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗${NC} Docker is not running. Please start Docker and try again."
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker is running"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${YELLOW}⚠️  ngrok is not installed${NC}"
    echo ""
    echo "Please install ngrok:"
    echo "  - macOS: brew install ngrok/ngrok/ngrok"
    echo "  - Linux: See https://ngrok.com/download"
    echo "  - Windows: Download from https://ngrok.com/download"
    echo ""
    echo "Then run: ngrok config add-authtoken YOUR_AUTH_TOKEN"
    echo ""
    echo "For now, continuing without ngrok..."
    NGROK_AVAILABLE=false
else
    echo -e "${GREEN}✓${NC} ngrok is installed"
    NGROK_AVAILABLE=true
fi

# Check if node_modules exists
if [ ! -d node_modules ]; then
    echo -e "${YELLOW}⚠️  node_modules not found. Running npm install...${NC}"
    npm install
    echo -e "${GREEN}✓${NC} Dependencies installed"
fi

echo ""
echo -e "${BLUE}Starting services...${NC}"
echo ""

# Start Docker Compose services
echo "Starting Docker Compose stack..."
docker-compose up -d

echo ""
echo -e "${GREEN}✓${NC} Services started successfully!"
echo ""
echo "Available services:"
echo "  • Event Gateway:  http://localhost:8080"
echo "  • Grafana:        http://localhost:3000 (admin/admin)"
echo "  • Prometheus:     http://localhost:9090"
echo "  • PostgreSQL:     localhost:5432"
echo "  • Redis:          localhost:6379"
echo "  • Qdrant:         http://localhost:6333"
echo ""

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 5

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓${NC} Services are healthy"
else
    echo -e "${YELLOW}⚠️  Some services may still be starting up${NC}"
fi

echo ""

# Start ngrok if available
if [ "$NGROK_AVAILABLE" = true ]; then
    echo -e "${BLUE}Starting ngrok tunnel...${NC}"
    echo ""
    echo "Choose an option:"
    echo "  1) Start ngrok for event-gateway (port 8080) - Recommended"
    echo "  2) Skip ngrok (webhooks won't work locally)"
    echo ""
    read -p "Enter choice (1-2): " choice
    
    case $choice in
        1)
            echo ""
            echo -e "${GREEN}Starting ngrok tunnel to localhost:8080...${NC}"
            echo ""
            echo "ngrok will run in the background."
            echo "Access the ngrok web interface at: ${BLUE}http://127.0.0.1:4040${NC}"
            echo ""
            
            # Check if ngrok is already running
            if pgrep -x "ngrok" > /dev/null; then
                echo -e "${YELLOW}⚠️  ngrok is already running${NC}"
                echo "To restart ngrok:"
                echo "  1. Stop: pkill ngrok"
                echo "  2. Start: ngrok http 8080"
            else
                # Start ngrok in background
                nohup ngrok http 8080 > /tmp/ngrok.log 2>&1 &
                sleep 3
                
                # Try to get the ngrok URL
                if command -v curl &> /dev/null; then
                    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*\.ngrok[^"]*' | head -1)
                    if [ ! -z "$NGROK_URL" ]; then
                        echo -e "${GREEN}✓${NC} ngrok tunnel started!"
                        echo ""
                        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
                        echo -e "${GREEN}Your webhook URL:${NC}"
                        echo -e "${YELLOW}${NGROK_URL}${NC}"
                        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
                        echo ""
                        echo "Use this URL in GitHub webhook settings:"
                        echo "  ${NGROK_URL}/webhooks/github"
                        echo ""
                    else
                        echo -e "${YELLOW}⚠️  Could not retrieve ngrok URL${NC}"
                        echo "Check ngrok status at: http://127.0.0.1:4040"
                    fi
                fi
            fi
            ;;
        2)
            echo ""
            echo -e "${YELLOW}Skipping ngrok setup${NC}"
            echo "To start ngrok later, run: ngrok http 8080"
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Development environment is ready!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Next steps:"
echo "  1. Configure GitHub webhook with your ngrok URL"
echo "  2. Test webhook: Create a PR in your repository"
echo "  3. View logs: docker-compose logs -f event-gateway"
echo "  4. ngrok inspector: http://127.0.0.1:4040"
echo ""
echo "For detailed instructions, see: LOCAL_DEVELOPMENT.md"
echo ""
echo "To stop services:"
echo "  • Docker: docker-compose down"
echo "  • ngrok: pkill ngrok"
echo ""
