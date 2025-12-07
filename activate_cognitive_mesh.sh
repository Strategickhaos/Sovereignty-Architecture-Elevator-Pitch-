#!/bin/bash
# Activate Sovereign Cognitive Architecture
# Version: 1.0.0

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "════════════════════════════════════════════════════════════════"
echo "   🧠 SOVEREIGN COGNITIVE ARCHITECTURE ACTIVATION"
echo "   Zero Vendor Lock-In | Multi-LLM Consciousness Layer"
echo "════════════════════════════════════════════════════════════════"
echo -e "${NC}"

# ============================================================================
# STEP 1: Pre-flight Checks
# ============================================================================

echo -e "${YELLOW}[1/8] Running pre-flight checks...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found: $(docker --version)${NC}"

# Check Docker Compose
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose v2.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose found: $(docker compose version)${NC}"

# Check environment variables
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  No API keys found in environment.${NC}"
    if [ -f .env ]; then
        echo -e "${BLUE}📄 Loading from .env file...${NC}"
        export $(grep -v '^#' .env | xargs)
    else
        echo -e "${RED}❌ No .env file found. Please create one with your API keys.${NC}"
        echo -e "${BLUE}Example .env file:${NC}"
        echo "ANTHROPIC_API_KEY=sk-ant-..."
        echo "OPENAI_API_KEY=sk-..."
        exit 1
    fi
fi

if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo -e "${GREEN}✅ Anthropic API key configured${NC}"
fi

if [ -n "$OPENAI_API_KEY" ]; then
    echo -e "${GREEN}✅ OpenAI API key configured${NC}"
fi

# ============================================================================
# STEP 2: Create Required Directories
# ============================================================================

echo -e "\n${YELLOW}[2/8] Creating required directories...${NC}"

mkdir -p data/qdrant
mkdir -p data/redis
mkdir -p data/ollama
mkdir -p data/exports
mkdir -p logs/memory-mesh
mkdir -p logs/claude
mkdir -p logs/gpt
mkdir -p logs/qwen
mkdir -p logs/custom
mkdir -p config/qdrant
mkdir -p config/redis
mkdir -p config/prometheus
mkdir -p config/grafana/dashboards

echo -e "${GREEN}✅ Directories created${NC}"

# ============================================================================
# STEP 3: Create Configuration Files
# ============================================================================

echo -e "\n${YELLOW}[3/8] Creating configuration files...${NC}"

# Redis configuration
cat > config/redis/redis.conf << 'EOF'
# Redis configuration for Sovereign Cognitive Architecture
bind 0.0.0.0
protected-mode no
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
loglevel notice
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data
EOF

echo -e "${GREEN}✅ Redis configuration created${NC}"

# Prometheus configuration
cat > config/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'memory-mesh'
    static_configs:
      - targets: ['memory-mesh:7000']
  
  - job_name: 'claude-api'
    static_configs:
      - targets: ['claude-api:8001']
  
  - job_name: 'gpt-api'
    static_configs:
      - targets: ['gpt-api:8002']
  
  - job_name: 'ollama'
    static_configs:
      - targets: ['ollama:11434']
EOF

echo -e "${GREEN}✅ Prometheus configuration created${NC}"

# ============================================================================
# STEP 4: Start Infrastructure Services
# ============================================================================

echo -e "\n${YELLOW}[4/8] Starting infrastructure services...${NC}"

docker compose -f docker-compose-cognitive-mesh.yml up -d qdrant redis

echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"
sleep 10

# ============================================================================
# STEP 5: Initialize Qdrant Collections
# ============================================================================

echo -e "\n${YELLOW}[5/8] Initializing Qdrant collections...${NC}"

# Create conversations collection
curl -s -X PUT http://localhost:6333/collections/conversations \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
  }' > /dev/null

echo -e "${GREEN}✅ Created 'conversations' collection${NC}"

# Create knowledge_base collection
curl -s -X PUT http://localhost:6333/collections/knowledge_base \
  -H 'Content-Type: application/json' \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
  }' > /dev/null

echo -e "${GREEN}✅ Created 'knowledge_base' collection${NC}"

# ============================================================================
# STEP 6: Start Core Services
# ============================================================================

echo -e "\n${YELLOW}[6/8] Starting core services (Memory Mesh, Claude, GPT, Ollama)...${NC}"

docker compose -f docker-compose-cognitive-mesh.yml up -d

echo -e "${BLUE}⏳ Waiting for services to initialize...${NC}"
sleep 15

# ============================================================================
# STEP 7: Pull Ollama Models
# ============================================================================

echo -e "\n${YELLOW}[7/8] Pulling Ollama models...${NC}"
echo -e "${BLUE}This may take several minutes on first run...${NC}"

docker exec sovereign-ollama ollama pull llama3 &
LLAMA_PID=$!

docker exec sovereign-ollama ollama pull mistral &
MISTRAL_PID=$!

wait $LLAMA_PID
echo -e "${GREEN}✅ Pulled llama3${NC}"

wait $MISTRAL_PID
echo -e "${GREEN}✅ Pulled mistral${NC}"

# Optional: Pull more models
# docker exec sovereign-ollama ollama pull codellama
# docker exec sovereign-ollama ollama pull phi3

# ============================================================================
# STEP 8: Verify All Services
# ============================================================================

echo -e "\n${YELLOW}[8/8] Verifying service health...${NC}"

check_service() {
    local name=$1
    local url=$2
    if curl -sf "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $name${NC} - $url"
        return 0
    else
        echo -e "${RED}❌ $name${NC} - $url (not responding)"
        return 1
    fi
}

ALL_HEALTHY=true

check_service "Qdrant" "http://localhost:6333/health" || ALL_HEALTHY=false

if redis-cli -h localhost -p 6379 PING > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis${NC} - redis://localhost:6379"
else
    echo -e "${RED}❌ Redis${NC} - redis://localhost:6379 (not responding)"
    ALL_HEALTHY=false
fi

check_service "Memory Mesh" "http://localhost:7000/health" || ALL_HEALTHY=false
check_service "Claude API" "http://localhost:8001/health" || ALL_HEALTHY=false
check_service "GPT API" "http://localhost:8002/health" || ALL_HEALTHY=false
check_service "Ollama" "http://localhost:11434/api/tags" || ALL_HEALTHY=false

# ============================================================================
# FINAL STATUS
# ============================================================================

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

if [ "$ALL_HEALTHY" = true ]; then
    echo -e "${GREEN}"
    echo "  🎉 SOVEREIGN COGNITIVE ARCHITECTURE IS LIVE!"
    echo ""
    echo "  Available LLM endpoints:"
    echo "    Claude:      http://localhost:8001"
    echo "    GPT:         http://localhost:8002"
    echo "    Ollama:      http://localhost:11434"
    echo ""
    echo "  Infrastructure:"
    echo "    Memory Mesh: http://localhost:7000"
    echo "    Qdrant:      http://localhost:6333"
    echo "    Redis:       redis://localhost:6379"
    echo ""
    echo "  Next steps:"
    echo "    1. Test an LLM: curl http://localhost:8001/health"
    echo "    2. Store conversation: curl -X POST http://localhost:7000/conversations"
    echo "    3. Export data: curl -X POST http://localhost:7000/export"
    echo ""
    echo "  Documentation: ./SOVEREIGN_COGNITIVE_ARCHITECTURE.md"
    echo -e "${NC}"
else
    echo -e "${YELLOW}"
    echo "  ⚠️  Some services are not responding"
    echo ""
    echo "  Check logs:"
    echo "    docker compose -f docker-compose-cognitive-mesh.yml logs"
    echo ""
    echo "  Restart services:"
    echo "    docker compose -f docker-compose-cognitive-mesh.yml restart"
    echo -e "${NC}"
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Built with 🔥 by Strategickhaos DAO LLC${NC}"
echo -e "${BLUE}Node 137 - DOM_010101${NC}"
echo -e "${BLUE}Trust nothing until it survives 100-angle crossfire.${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
