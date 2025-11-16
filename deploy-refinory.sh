#!/usr/bin/env bash
# deploy-refinory.sh - Idempotent deployment script
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "🔍 Checking prerequisites..."
    
    local missing=()
    
    command -v docker >/dev/null 2>&1 || missing+=("docker")
    command -v docker-compose >/dev/null 2>&1 || missing+=("docker-compose")
    command -v node >/dev/null 2>&1 || missing+=("node")
    command -v npm >/dev/null 2>&1 || missing+=("npm")
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing required tools: ${missing[*]}"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Validate configuration
validate_config() {
    log "📋 Validating configuration..."
    
    if [[ ! -f "discovery.yml" ]]; then
        error "discovery.yml not found"
        exit 1
    fi
    
    if [[ ! -f ".env" ]]; then
        warn ".env file not found, using defaults"
        cp .env.example .env
    fi
    
    # Check required environment variables
    source .env
    local required_vars=(
        "DISCORD_TOKEN"
        "CH_CLUSTER_STATUS_ID"
        "CH_ALERTS_ID"
        "CH_DEPLOYMENTS_ID"
        "CH_PRS_ID"
    )
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    # Run config validation script
    if [[ -x "./validate-config.sh" ]]; then
        ./validate-config.sh
    fi
    
    success "Configuration validation passed"
}

# Install dependencies
install_dependencies() {
    log "📦 Installing dependencies..."
    
    if [[ ! -d "node_modules" ]] || [[ "package.json" -nt "node_modules" ]]; then
        npm ci
        success "Node.js dependencies installed"
    else
        log "Node.js dependencies up to date"
    fi
}

# Build containers
build_containers() {
    log "🏗️  Building containers..."
    
    docker-compose build --pull
    success "Containers built successfully"
}

# Create required directories
setup_directories() {
    log "📁 Setting up directories..."
    
    local dirs=(
        "/var/refinory/artifacts"
        "/var/refinory/outputs" 
        "/var/refinory/models"
        "./monitoring/grafana/dashboards"
        "./monitoring/grafana/provisioning/dashboards"
        "./monitoring/grafana/provisioning/datasources"
        "./ssl"
    )
    
    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            sudo mkdir -p "$dir"
            if [[ "$dir" == /var/refinory/* ]]; then
                sudo chown -R 1001:1001 "$dir"
            fi
        fi
    done
    
    success "Directories created"
}

# Setup monitoring configuration
setup_monitoring() {
    log "📊 Setting up monitoring..."
    
    # Prometheus config
    mkdir -p monitoring
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'discord-bot'
    static_configs:
      - targets: ['discord-bot:3000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'event-gateway'
    static_configs:
      - targets: ['event-gateway:8080']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'refinory-api'
    static_configs:
      - targets: ['refinory-api:8085']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF

    # Grafana datasource
    mkdir -p monitoring/grafana/provisioning/datasources
    cat > monitoring/grafana/provisioning/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

    success "Monitoring configuration created"
}

# Setup nginx configuration
setup_nginx() {
    log "🌐 Setting up nginx..."
    
    cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream event_gateway {
        server event-gateway:8080;
    }
    
    upstream refinory_api {
        server refinory-api:8085;
    }
    
    upstream grafana {
        server grafana:3000;
    }

    server {
        listen 80;
        server_name events.strategickhaos.com;
        
        location / {
            proxy_pass http://event_gateway;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

    server {
        listen 80;
        server_name refinory.strategickhaos.local;
        
        location / {
            proxy_pass http://refinory_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

    server {
        listen 80;
        server_name monitor.strategickhaos.local;
        
        location / {
            proxy_pass http://grafana;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
EOF

    success "Nginx configuration created"
}

# Initialize database
init_database() {
    log "🗄️  Initializing database..."
    
    cat > init-db.sql << EOF
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS refinory;
CREATE SCHEMA IF NOT EXISTS discord;

-- Refinory tables
CREATE TABLE IF NOT EXISTS refinory.requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requester VARCHAR(255) NOT NULL,
    experts JSONB,
    status VARCHAR(50) DEFAULT 'created',
    progress INTEGER DEFAULT 0,
    artifacts JSONB DEFAULT '[]',
    active_experts JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Discord tables
CREATE TABLE IF NOT EXISTS discord.messages (
    id SERIAL PRIMARY KEY,
    channel_id VARCHAR(255),
    message_id VARCHAR(255),
    content TEXT,
    embeds JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_requests_status ON refinory.requests(status);
CREATE INDEX IF NOT EXISTS idx_requests_requester ON refinory.requests(requester);
CREATE INDEX IF NOT EXISTS idx_messages_channel ON discord.messages(channel_id);
EOF

    success "Database initialization script created"
}

# Deploy services
deploy_services() {
    log "🚀 Deploying services..."
    
    # Stop existing services
    docker-compose down
    
    # Start infrastructure services first
    log "Starting infrastructure services..."
    docker-compose up -d postgres redis qdrant
    
    # Wait for infrastructure to be healthy
    log "Waiting for infrastructure to be ready..."
    sleep 10
    
    # Start application services
    log "Starting application services..."
    docker-compose up -d
    
    success "Services deployed"
}

# Health check
health_check() {
    log "🏥 Performing health check..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        local healthy=0
        local total=0
        
        # Check each service
        for service in postgres redis qdrant event-gateway refinory-api grafana; do
            total=$((total + 1))
            if docker-compose ps "$service" | grep -q "Up (healthy)\|Up [0-9]"; then
                healthy=$((healthy + 1))
            fi
        done
        
        log "Health check attempt $attempt: $healthy/$total services healthy"
        
        if [[ $healthy -eq $total ]]; then
            success "All services are healthy!"
            return 0
        fi
        
        if [[ $attempt -eq $max_attempts ]]; then
            error "Health check failed after $max_attempts attempts"
            docker-compose logs --tail=50
            return 1
        fi
        
        sleep 10
        attempt=$((attempt + 1))
    done
}

# Show status
show_status() {
    log "📊 Service Status:"
    docker-compose ps
    
    log "🔗 Service URLs:"
    echo "  Event Gateway:  http://localhost:8080/health"
    echo "  Refinory API:   http://localhost:8085/health" 
    echo "  Grafana:        http://localhost:3000 (admin/admin)"
    echo "  Prometheus:     http://localhost:9090"
    echo "  Qdrant:         http://localhost:6333"
    
    log "📝 Logs:"
    echo "  View logs:      docker-compose logs -f"
    echo "  Bot logs:       docker-compose logs -f discord-bot"
    echo "  Gateway logs:   docker-compose logs -f event-gateway"
}

# Main deployment flow
main() {
    log "🎯 Starting Strategickhaos Sovereignty Architecture deployment..."
    
    check_prerequisites
    validate_config
    install_dependencies
    setup_directories
    setup_monitoring
    setup_nginx
    init_database
    build_containers
    deploy_services
    health_check
    show_status
    
    success "🎉 Deployment completed successfully!"
    log "Discord bot should now be online and responding to commands"
    log "Event gateway is ready to receive webhooks"
    log "Refinory AI orchestrator is ready for architecture requests"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "restart")
        log "🔄 Restarting services..."
        docker-compose restart
        health_check
        show_status
        ;;
    "stop")
        log "🛑 Stopping services..."
        docker-compose down
        ;;
    "logs")
        docker-compose logs -f "${2:-}"
        ;;
    "status")
        show_status
        ;;
    *)
        echo "Usage: $0 [deploy|restart|stop|logs|status]"
        exit 1
        ;;
esac